from __future__ import annotations

import base64
from pathlib import Path

import pytest

from endleaf_client.paths import sha256_hex
from endleaf_client.proxy import annotate_tools, dispatch, handle_render
from endleaf_client.render import first_text
from fake_gate import FakeGate


def _text(result: dict) -> str:
    return first_text(result.get("content") or [])


@pytest.mark.asyncio
async def test_render_writes_file_and_returns_summary_only(tmp_path: Path) -> None:
    gate = FakeGate()
    result = await dispatch(
        gate,
        "renderDocument",
        {"outputFormat": "pdf", "templateId": "document-shell", "source": "hi"},
        tmp_path,
    )
    text = _text(result)
    assert result["isError"] is False
    assert text.startswith("ok ")
    assert f"sha256={gate.digest}" in text
    assert f"file={tmp_path / 'endleaf-out' / gate.filename}" in text
    assert "blob" not in text.lower()
    assert base64.b64encode(gate.artifact).decode("ascii") not in text
    saved = tmp_path / "endleaf-out" / gate.filename
    assert saved.read_bytes() == gate.artifact
    assert sha256_hex(saved.read_bytes()) == gate.digest
    assert len(text) < 400
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"


@pytest.mark.asyncio
async def test_source_path_uploads_then_renders(tmp_path: Path) -> None:
    gate = FakeGate()
    source = tmp_path / "body.md"
    source.write_text("hello from disk", encoding="utf-8")
    result = await dispatch(
        gate,
        "renderDocument",
        {
            "outputFormat": "pdf",
            "templateId": "document-shell",
            "sourcePath": "body.md",
        },
        tmp_path,
    )
    text = _text(result)
    assert result["isError"] is False
    assert "blob" not in text.lower()
    names = [name for name, _ in gate.calls]
    assert names == ["getQuota", "uploadSource", "renderDocument"]
    uploaded = gate.calls[1][1]
    assert uploaded["blob_b64"] == base64.b64encode(b"hello from disk").decode("ascii")
    forwarded = gate.calls[2][1]
    assert forwarded["source_id"].startswith("src_")
    assert "source" not in forwarded
    assert "sourcePath" not in forwarded
    assert "writeTo" not in forwarded


@pytest.mark.asyncio
async def test_size_refusal_before_upload(tmp_path: Path) -> None:
    gate = FakeGate(max_doc_kib=1)
    source = tmp_path / "big.md"
    source.write_bytes(b"x" * 2048)
    result = await dispatch(
        gate,
        "renderDocument",
        {"outputFormat": "pdf", "templateId": "document-shell", "sourcePath": "big.md"},
        tmp_path,
    )
    text = _text(result)
    assert result["isError"] is True
    assert "max_doc_kib=1" in text
    assert "Fix:" in text
    assert "uploadSource" not in [name for name, _ in gate.calls]
    assert "renderDocument" not in [name for name, _ in gate.calls]


@pytest.mark.asyncio
async def test_upload_from_path_one_line(tmp_path: Path) -> None:
    gate = FakeGate()
    source = tmp_path / "note.md"
    source.write_text("reuse me", encoding="utf-8")
    result = await dispatch(gate, "uploadFromPath", {"path": "note.md"}, tmp_path)
    text = _text(result)
    assert result["isError"] is False
    assert text.startswith("source_id=src_")
    assert "bytes=8" in text
    assert "sha256=" in text
    assert "expires=" in text
    assert "blob" not in text


@pytest.mark.asyncio
async def test_inline_passthrough_keeps_blob(tmp_path: Path) -> None:
    gate = FakeGate()
    result = await handle_render(
        gate,
        {
            "outputFormat": "pdf",
            "templateId": "document-shell",
            "source": "hi",
            "delivery": "inline",
        },
        tmp_path,
    )
    types = [item.get("type") for item in result["content"]]
    assert "resource" in types
    blob = result["content"][1]["resource"]["blob"]
    assert blob == base64.b64encode(gate.artifact).decode("ascii")
    assert not (tmp_path / "endleaf-out").exists()


@pytest.mark.asyncio
async def test_sha_mismatch_is_one_line(tmp_path: Path) -> None:
    gate = FakeGate()
    gate.summary = gate.summary.replace(gate.digest, "0" * 64)
    result = await dispatch(
        gate,
        "renderDocument",
        {"outputFormat": "pdf", "templateId": "document-shell", "source": "hi"},
        tmp_path,
    )
    text = _text(result)
    assert result["isError"] is True
    assert "sha256 mismatch" in text
    assert "Fix:" in text
    assert "blob" not in text.lower()


@pytest.mark.asyncio
async def test_conflict_suffix_when_different_content(tmp_path: Path) -> None:
    gate = FakeGate()
    existing = tmp_path / "endleaf-out" / gate.filename
    existing.parent.mkdir()
    existing.write_bytes(b"other-content")
    result = await dispatch(
        gate,
        "renderDocument",
        {"outputFormat": "pdf", "templateId": "document-shell", "source": "hi"},
        tmp_path,
    )
    text = _text(result)
    assert result["isError"] is False
    assert "-1.pdf" in text
    assert existing.read_bytes() == b"other-content"


def test_tools_hide_upload_and_add_local_fields() -> None:
    gate = FakeGate()
    tools = annotate_tools(gate.tools)
    names = [item["name"] for item in tools]
    assert "uploadSource" not in names
    assert "uploadFromPath" in names
    render = next(item for item in tools if item["name"] == "renderDocument")
    props = render["inputSchema"]["properties"]
    assert "writeTo" in props
    assert "sourcePath" in props


@pytest.mark.asyncio
async def test_source_path_rejects_inline_source(tmp_path: Path) -> None:
    gate = FakeGate()
    (tmp_path / "a.md").write_text("x", encoding="utf-8")
    result = await dispatch(
        gate,
        "renderDocument",
        {"outputFormat": "pdf", "templateId": "document-shell", "sourcePath": "a.md", "source": "nope"},
        tmp_path,
    )
    assert result["isError"] is True
    assert "cannot be combined" in _text(result)


@pytest.mark.asyncio
async def test_source_path_rejects_document_id(tmp_path: Path) -> None:
    gate = FakeGate()
    (tmp_path / "a.tex").write_text("x", encoding="utf-8")
    result = await dispatch(
        gate,
        "renderDocument",
        {"outputFormat": "pdf", "templateId": "fulldoc", "sourcePath": "a.tex", "documentId": "doc_x"},
        tmp_path,
    )
    assert result["isError"] is True
    assert "cannot be combined" in _text(result)
    assert "documentId" in _text(result)
