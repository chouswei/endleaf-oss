"""ENDLEAF-R56-SESSION: re-open a lost gate session and retry once."""

from __future__ import annotations

import itertools

import httpx
import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from endleaf_client.errors import ClientError
from endleaf_client.gate import GateClient


class Gate:
    """Sessions in memory, like the live gate. restart() forgets them."""

    def __init__(self) -> None:
        self.sessions: set[str] = set()
        self.ids = itertools.count(1)
        self.log: list[tuple[str, int]] = []
        self.refuse_initialize = False
        self.calls_done = 0

    def restart(self) -> None:
        self.sessions.clear()

    async def mcp(self, request: Request) -> Response:
        body = await request.json()
        method = body.get("method")
        rpc_id = body.get("id")
        if method == "initialize":
            if self.refuse_initialize:
                self.log.append((method, 404))
                return _invalid(rpc_id)
            sid = f"s{next(self.ids)}"
            self.sessions.add(sid)
            self.log.append((method, 200))
            return JSONResponse(
                {"jsonrpc": "2.0", "id": rpc_id, "result": {"serverInfo": {"name": "Endleaf by InkMirage"}}},
                headers={"mcp-session-id": sid},
            )
        if request.headers.get("mcp-session-id") not in self.sessions:
            self.log.append((method, 404))
            return _invalid(rpc_id)
        self.log.append((method, 200 if method != "notifications/initialized" else 202))
        if method == "notifications/initialized":
            return Response(status_code=202)
        if method == "tools/call":
            self.calls_done += 1
            return JSONResponse(
                {"jsonrpc": "2.0", "id": rpc_id, "result": {"content": [{"type": "text", "text": "ok"}], "isError": False}}
            )
        return JSONResponse({"jsonrpc": "2.0", "id": rpc_id, "result": {"tools": []}})


def _invalid(rpc_id: object) -> JSONResponse:
    # Same body and status as endleaf_gate mcp._invalid_session.
    return JSONResponse(
        {"jsonrpc": "2.0", "id": rpc_id, "error": {"code": -32000, "message": "invalidSession", "data": {"reason": "invalidSession"}}},
        status_code=404,
    )


async def _client(gate: Gate) -> tuple[GateClient, httpx.AsyncClient]:
    app = Starlette(routes=[Route("/mcp", gate.mcp, methods=["POST"])])
    http = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://gate.test")
    client = GateClient("http://gate.test/mcp", "fixture-key", client=http)
    await client.initialize()
    return client, http


@pytest.mark.asyncio
async def test_gate_restart_reinitializes_and_retries_once() -> None:
    gate = Gate()
    client, http = await _client(gate)
    try:
        gate.restart()
        gate.log.clear()
        result = await client.call_tool("getQuota", {})
    finally:
        await http.aclose()
    assert result["isError"] is False
    assert gate.log == [
        ("tools/call", 404),
        ("initialize", 200),
        ("notifications/initialized", 202),
        ("tools/call", 200),
    ]
    assert gate.calls_done == 1
    assert client.generation == 1


@pytest.mark.asyncio
async def test_refused_new_session_is_one_honest_line() -> None:
    gate = Gate()
    client, http = await _client(gate)
    try:
        gate.restart()
        gate.refuse_initialize = True
        with pytest.raises(ClientError) as caught:
            await client.call_tool("renderDocument", {"outputFormat": "pdf"})
    finally:
        await http.aclose()
    assert gate.calls_done == 0
    assert caught.value.message == "gate session ended and a new one was refused"
    assert "correct the call" not in str(caught.value)
    assert len(str(caught.value).splitlines()) == 2


@pytest.mark.asyncio
async def test_other_errors_are_not_retried() -> None:
    gate = Gate()
    client, http = await _client(gate)

    async def boom(request: Request) -> Response:
        return JSONResponse({"jsonrpc": "2.0", "id": 9, "error": {"message": "method not found"}}, status_code=404)

    try:
        http._transport = httpx.ASGITransport(app=Starlette(routes=[Route("/mcp", boom, methods=["POST"])]))
        with pytest.raises(ClientError):
            await client.call_tool("guide", {})
    finally:
        await http.aclose()
    assert client.generation == 0
