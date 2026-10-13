from __future__ import annotations

import json

import httpx
import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from endleaf_client.gate import GateClient


class Recorder:
    def __init__(self) -> None:
        self.auths: list[str] = []
        self.methods: list[str] = []


def _app(rec: Recorder) -> Starlette:
    async def mcp(request: Request) -> JSONResponse:
        rec.auths.append(request.headers.get("authorization") or "")
        body = await request.json()
        rec.methods.append(str(body.get("method")))
        method = body.get("method")
        rpc_id = body.get("id")
        if method == "initialize":
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "result": {
                        "protocolVersion": "2025-06-18",
                        "capabilities": {"tools": {"listChanged": False}},
                        "serverInfo": {"name": "Endleaf by InkMirage", "version": "0.1.0"},
                        "instructions": "Call renderDocument.",
                    },
                },
                headers={"mcp-session-id": "sess-1"},
            )
        if method == "notifications/initialized":
            return JSONResponse({}, status_code=202)
        if method == "tools/list":
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "result": {
                        "tools": [
                            {"name": "renderDocument", "inputSchema": {"type": "object"}},
                            {"name": "uploadSource", "inputSchema": {"type": "object"}},
                        ]
                    },
                },
                headers={"mcp-session-id": "sess-1"},
            )
        return JSONResponse(
            {"jsonrpc": "2.0", "id": rpc_id, "error": {"message": "method not found"}},
            status_code=404,
        )

    return Starlette(routes=[Route("/mcp", mcp, methods=["POST"])])


@pytest.mark.asyncio
async def test_http_initialize_and_list_uses_bearer() -> None:
    rec = Recorder()
    transport = httpx.ASGITransport(app=_app(rec))
    http = httpx.AsyncClient(transport=transport, base_url="http://gate.test")
    gate = GateClient("http://gate.test/mcp", "fixture-key", client=http)
    try:
        await gate.initialize()
        tools = await gate.list_tools()
    finally:
        await http.aclose()
    assert [item["name"] for item in tools] == ["renderDocument", "uploadSource"]
    assert rec.auths
    assert all(item == "Bearer fixture-key" for item in rec.auths)
    assert "initialize" in rec.methods
    assert "tools/list" in rec.methods
    dumped = json.dumps(rec.auths)
    assert "ENDLEAF_API_KEY" not in dumped
