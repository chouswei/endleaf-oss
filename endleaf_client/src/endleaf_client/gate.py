"""Streamable HTTP client for the live Endleaf gate. ENDLEAF-R53-PROXY."""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any
from collections.abc import Mapping

import httpx

from endleaf_client.errors import fail

log = logging.getLogger("endleaf_client")

DEFAULT_MCP_URL = "https://endleaf.inkmirage.xyz/mcp"
_PROTOCOL = "2025-06-18"
_ACCEPT = "application/json, text/event-stream"
# ENDLEAF-R56-SESSION. The gate keeps sessions in memory; a restart or
# eviction answers HTTP 404 with this JSON-RPC reason before any work.
_INVALID_SESSION = "invalidSession"


class SessionLost(Exception):
    """The gate refused the session id before doing any work."""


class GateClient:
    """POST-only Streamable HTTP. The gate answers GET with 405."""

    def __init__(
        self,
        url: str,
        api_key: str,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        if not api_key or any(ch.isspace() for ch in api_key):
            raise fail(
                "ENDLEAF_API_KEY is missing or invalid",
                "set ENDLEAF_API_KEY to the Bearer key; the value is never logged.",
            )
        self._url = url.rstrip("/")
        self._key = api_key
        self._session_id: str | None = None
        self._rpc = 0
        self._owned = client is None
        self._http = client or httpx.AsyncClient(timeout=120.0)
        self.instructions = ""
        self.server_name = "Endleaf by InkMirage"
        self.server_version = ""
        # Bumped on every re-initialize after a lost session. ENDLEAF-R56-LISTCHANGED.
        self.generation = 0

    async def aclose(self) -> None:
        if self._owned:
            await self._http.aclose()

    def _next_id(self) -> int:
        self._rpc += 1
        return self._rpc

    def _headers(self) -> dict[str, str]:
        headers = {
            "accept": _ACCEPT,
            "content-type": "application/json",
            "authorization": f"Bearer {self._key}",
            "mcp-protocol-version": _PROTOCOL,
        }
        if self._session_id:
            headers["mcp-session-id"] = self._session_id
        return headers

    async def rpc(self, method: str, params: Mapping[str, Any] | None = None, *, notify: bool = False) -> Any:
        """One JSON-RPC call. A lost session is re-opened and the call sent once more.

        Safe for tools/call: the gate checks the session id before it
        reserves a job or reads the body, so a refused call did no work.
        """
        try:
            return await self._rpc_once(method, params, notify=notify)
        except SessionLost:
            if method == "initialize":
                raise _session_error() from None
        log.info("gate session lost; re-initializing method=%s", method)
        self._session_id = None
        try:
            await self.initialize()
        except SessionLost:
            raise _session_error() from None
        self.generation += 1
        try:
            return await self._rpc_once(method, params, notify=notify)
        except SessionLost:
            raise _session_error() from None

    async def _rpc_once(self, method: str, params: Mapping[str, Any] | None = None, *, notify: bool = False) -> Any:
        body: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if not notify:
            body["id"] = self._next_id()
        if params is not None:
            body["params"] = dict(params)
        try:
            response = await self._http.post(self._url, headers=self._headers(), json=body)
        except httpx.HTTPError as exc:
            log.info("gate transport failed method=%s", method)
            raise fail(
                "gate is unreachable",
                "check ENDLEAF_MCP_URL and retry.",
            ) from exc
        session = response.headers.get("mcp-session-id")
        if session:
            self._session_id = session
        if response.status_code == 401:
            raise fail(
                "gate refused the key",
                "set a valid ENDLEAF_API_KEY; the value is never logged.",
            )
        payload = _decode_body(response)
        if response.status_code == 404 and _is_invalid_session(payload):
            raise SessionLost()
        if notify:
            return None
        if not isinstance(payload, dict):
            raise fail(
                "gate returned a non-object body",
                "retry; if it persists, call guide topic getting-started.",
            )
        if "error" in payload:
            raise _rpc_error(payload["error"])
        return payload.get("result")

    async def initialize(self) -> dict[str, Any]:
        result = await self._rpc_once(
            "initialize",
            {
                "protocolVersion": _PROTOCOL,
                "capabilities": {},
                "clientInfo": {"name": "endleaf-local", "version": "0.1.0"},
            },
        )
        if not isinstance(result, dict):
            raise fail(
                "gate initialize failed",
                "check ENDLEAF_MCP_URL and ENDLEAF_API_KEY.",
            )
        info = result.get("serverInfo")
        if isinstance(info, dict):
            if isinstance(info.get("name"), str):
                self.server_name = info["name"]
            if isinstance(info.get("version"), str):
                self.server_version = info["version"]
        if isinstance(result.get("instructions"), str):
            self.instructions = result["instructions"]
        await self._rpc_once("notifications/initialized", notify=True)
        return result

    async def list_tools(self) -> list[dict[str, Any]]:
        result = await self.rpc("tools/list", {})
        tools = result.get("tools") if isinstance(result, dict) else None
        if not isinstance(tools, list):
            raise fail(
                "gate tools/list returned no tools",
                "retry; if it persists, call guide topic getting-started.",
            )
        return [item for item in tools if isinstance(item, dict)]


    async def call_tool(self, name: str, arguments: Mapping[str, Any] | None = None) -> dict[str, Any]:
        result = await self.rpc(
            "tools/call",
            {"name": name, "arguments": dict(arguments or {})},
        )
        if not isinstance(result, dict):
            raise fail(
                f"{name} returned no tool result",
                "retry the call.",
            )
        return result

    async def list_resources(self) -> list[dict[str, Any]]:
        result = await self.rpc("resources/list", {})
        rows = result.get("resources") if isinstance(result, dict) else None
        return [item for item in rows if isinstance(item, dict)] if isinstance(rows, list) else []

    async def read_resource(self, uri: str) -> dict[str, Any]:
        result = await self.rpc("resources/read", {"uri": uri})
        if not isinstance(result, dict):
            raise fail("resources/read failed", "pass a listed endleaf:// URI.")
        return result

    async def list_prompts(self) -> list[dict[str, Any]]:
        result = await self.rpc("prompts/list", {})
        rows = result.get("prompts") if isinstance(result, dict) else None
        return [item for item in rows if isinstance(item, dict)] if isinstance(rows, list) else []

    async def get_prompt(self, name: str) -> dict[str, Any]:
        result = await self.rpc("prompts/get", {"name": name})
        if not isinstance(result, dict):
            raise fail("prompts/get failed", "pass a listed prompt name.")
        return result


def _decode_body(response: httpx.Response) -> Any:
    ctype = (response.headers.get("content-type") or "").split(";", 1)[0].strip().lower()
    text = response.text
    if ctype == "text/event-stream":
        chunks: list[str] = []
        for line in text.splitlines():
            if line.startswith("data:"):
                chunks.append(line[5:].lstrip())
        text = "\n".join(chunks)
    if not text.strip():
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise fail(
            "gate returned non-JSON",
            "retry; if it persists, check ENDLEAF_MCP_URL.",
        ) from exc


def _rpc_error(error: object) -> Exception:
    if isinstance(error, dict):
        message = error.get("message") or error.get("data") or "gate JSON-RPC error"
        data = error.get("data")
        reason = ""
        if isinstance(data, dict) and isinstance(data.get("reason"), str):
            reason = data["reason"]
        shown = reason or str(message)
        if shown == _INVALID_SESSION:
            return fail("gate session ended (gate restarted)", "retry the call; the client opens a new session.")
        return fail(shown, "correct the call or wait and retry.")
    return fail("gate JSON-RPC error", "correct the call or wait and retry.")


def tools_digest(tools: list[dict[str, Any]]) -> str:
    """Stable digest of a tool list. A change means the host should re-list."""
    return hashlib.sha256(json.dumps(tools, sort_keys=True).encode("utf-8")).hexdigest()


def _is_invalid_session(payload: Any) -> bool:
    if not isinstance(payload, dict):
        return False
    error = payload.get("error")
    if not isinstance(error, dict):
        return False
    data = error.get("data")
    reason = data.get("reason") if isinstance(data, dict) else None
    return reason == _INVALID_SESSION or error.get("message") == _INVALID_SESSION


def _session_error() -> Exception:
    return fail(
        "gate session ended and a new one was refused",
        "retry in a minute; restart the client if it repeats.",
    )
