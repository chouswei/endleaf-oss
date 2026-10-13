"""ENDLEAF-R56-PASS and ENDLEAF-R56-LISTCHANGED."""

from __future__ import annotations

from pathlib import Path

import pytest

from endleaf_client.proxy import annotate_tools, dispatch
from endleaf_client.server import refresh_tool_list
from fake_gate import FakeGate


@pytest.mark.asyncio
async def test_unknown_gate_fields_reach_the_gate(tmp_path: Path) -> None:
    gate = FakeGate()
    await dispatch(
        gate,
        "renderDocument",
        {
            "outputFormat": "pdf",
            "templateId": "document-shell",
            "source": "hi",
            "pageSize": "a3",
            "orientation": "landscape",
            "futureField": 1,
            "writeTo": "out/",
        },
        tmp_path,
    )
    name, sent = gate.calls[-1]
    assert name == "renderDocument"
    assert sent == {
        "outputFormat": "pdf",
        "templateId": "document-shell",
        "source": "hi",
        "pageSize": "a3",
        "orientation": "landscape",
        "futureField": 1,
    }


def test_advertised_schema_keeps_gate_fields_and_is_open() -> None:
    gate = FakeGate()
    render = gate.tools[0]
    render["inputSchema"]["properties"]["pageSize"] = {"type": "string", "enum": ["a4", "letter", "a3"]}
    render["inputSchema"]["properties"]["orientation"] = {"type": "string", "enum": ["portrait", "landscape"]}
    local = next(t for t in annotate_tools(gate.tools) if t["name"] == "renderDocument")
    props = local["inputSchema"]["properties"]
    assert props["pageSize"]["enum"] == ["a4", "letter", "a3"]
    assert props["orientation"]["enum"] == ["portrait", "landscape"]
    assert {"writeTo", "sourcePath"} <= set(props)
    assert local["inputSchema"]["additionalProperties"] is True
    # The gate's own copy is not modified.
    assert render["inputSchema"]["additionalProperties"] is False


class _Session:
    def __init__(self) -> None:
        self.sent = 0

    async def send_tool_list_changed(self) -> None:
        self.sent += 1


@pytest.mark.asyncio
async def test_list_changed_when_host_calls_without_listing() -> None:
    gate = FakeGate()
    gate.generation = 0
    session = _Session()
    state = {"listed": None, "generation": 0}
    assert await refresh_tool_list(gate, state, session) is True
    assert await refresh_tool_list(gate, state, session) is False
    assert session.sent == 1


@pytest.mark.asyncio
async def test_list_changed_after_reinit_only_when_the_list_changed() -> None:
    from endleaf_client.gate import tools_digest

    gate = FakeGate()
    gate.generation = 0
    session = _Session()
    state = {"listed": tools_digest(annotate_tools(gate.tools)), "generation": 0}
    gate.generation = 1  # re-initialized, same list
    assert await refresh_tool_list(gate, state, session) is False
    gate.generation = 2  # re-initialized after a roll that added a field
    gate.tools[0]["inputSchema"]["properties"]["orientation"] = {"type": "string"}
    assert await refresh_tool_list(gate, state, session) is True
    assert session.sent == 1
