from __future__ import annotations

from pathlib import Path

from mcp.server.lowlevel import NotificationOptions

from endleaf_client.server import _LOCAL_NOTE, build_server
from fake_gate import FakeGate


def test_list_changed_is_true(tmp_path: Path) -> None:
    gate = FakeGate()
    gate.instructions = "Call renderDocument."
    server = build_server(gate, tmp_path)
    caps = server.get_capabilities(notification_options=NotificationOptions(tools_changed=True))
    assert caps.tools is not None
    assert caps.tools.list_changed is True
    assert _LOCAL_NOTE.split()[0] in (server.instructions or "")
