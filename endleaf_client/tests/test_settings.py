from __future__ import annotations

import pytest

from endleaf_client.errors import ClientError
from endleaf_client.gate import DEFAULT_MCP_URL
from endleaf_client.server import load_settings


def test_key_required() -> None:
    with pytest.raises(ClientError, match="ENDLEAF_API_KEY is missing"):
        load_settings({})


def test_url_default() -> None:
    url, key = load_settings({"ENDLEAF_API_KEY": "secret-test-key"})
    assert url == DEFAULT_MCP_URL
    assert key == "secret-test-key"


def test_url_override() -> None:
    url, key = load_settings(
        {"ENDLEAF_API_KEY": "secret-test-key", "ENDLEAF_MCP_URL": "http://127.0.0.1:9/mcp"}
    )
    assert url == "http://127.0.0.1:9/mcp"
    assert key == "secret-test-key"
