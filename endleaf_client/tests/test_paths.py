from __future__ import annotations

from pathlib import Path

import pytest

from endleaf_client.errors import ClientError
from endleaf_client.paths import destination_for, read_source, resolve_path, sha256_hex, write_artifact


def test_relative_stays_under_cwd(tmp_path: Path) -> None:
    target = resolve_path("out/a.pdf", tmp_path, for_write=True)
    assert target == (tmp_path / "out/a.pdf").resolve()


def test_relative_escape_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ClientError, match="outside the client working directory"):
        resolve_path("../outside.pdf", tmp_path, for_write=True)


def test_absolute_path_is_allowed(tmp_path: Path) -> None:
    outside = tmp_path.parent / "abs-out.pdf"
    resolved = resolve_path(str(outside), tmp_path, for_write=True)
    assert resolved == outside.resolve()


def test_same_sha_reuses_file(tmp_path: Path) -> None:
    data = b"same-bytes"
    digest = sha256_hex(data)
    path = tmp_path / "kept.pdf"
    path.write_bytes(data)
    written = write_artifact(path, data, digest)
    assert written == path
    assert path.read_bytes() == data


def test_different_sha_adds_suffix(tmp_path: Path) -> None:
    path = tmp_path / "doc.pdf"
    path.write_bytes(b"old")
    data = b"new-bytes"
    digest = sha256_hex(data)
    written = write_artifact(path, data, digest)
    assert written == tmp_path / "doc-1.pdf"
    assert written.read_bytes() == data
    assert path.read_bytes() == b"old"


def test_directory_write_to(tmp_path: Path) -> None:
    digest = sha256_hex(b"x")
    dest = destination_for("./endleaf-out/", tmp_path, "endleaf-x.pdf", digest)
    assert dest == tmp_path / "endleaf-out" / "endleaf-x.pdf"


def test_source_missing(tmp_path: Path) -> None:
    with pytest.raises(ClientError, match="sourcePath not found"):
        read_source("missing.md", tmp_path)
