"""Resolve and write local paths. ENDLEAF-R53-PATHS."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

from endleaf_client.errors import fail

_FILE_EXTS = {".pdf", ".html", ".docx", ".bin"}
DEFAULT_WRITE_TO = "./endleaf-out/"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve_path(raw: str, cwd: Path, *, for_write: bool) -> Path:
    """Resolve relative to cwd. Relative paths must stay under cwd."""
    if not isinstance(raw, str) or raw.strip() == "":
        raise fail(
            "path is empty",
            "pass a path relative to the client working directory, or an absolute path.",
        )
    text = raw.strip()
    given_absolute = os.path.isabs(text)
    path = Path(text)
    if not given_absolute:
        path = (cwd / path).resolve()
        try:
            path.relative_to(cwd.resolve())
        except ValueError as exc:
            kind = "writeTo" if for_write else "sourcePath"
            raise fail(
                f"{kind} is outside the client working directory",
                "pass a relative path under that directory, or an absolute path if you intend to leave it.",
            ) from exc
    else:
        path = path.resolve()
    return path


def is_directory_target(raw: str, path: Path) -> bool:
    if raw.endswith(("/", "\\")):
        return True
    if path.exists() and path.is_dir():
        return True
    if path.suffix.lower() in _FILE_EXTS:
        return False
    return not path.exists()


def unique_destination(path: Path, digest: str) -> Path:
    """Reuse a file with the same sha. Otherwise add a numeric suffix."""
    if not path.exists():
        return path
    if path.is_file() and sha256_hex(path.read_bytes()) == digest:
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    index = 1
    while True:
        candidate = parent / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
        if candidate.is_file() and sha256_hex(candidate.read_bytes()) == digest:
            return candidate
        index += 1


def write_artifact(path: Path, data: bytes, digest: str) -> Path:
    destination = unique_destination(path, digest)
    if destination.exists() and sha256_hex(destination.read_bytes()) == digest:
        return destination
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    except OSError as exc:
        raise fail(
            f"writeTo not writable: {destination}",
            "pass a writable path under the client working directory, or an absolute path you can write.",
        ) from exc
    written = sha256_hex(destination.read_bytes())
    if written != digest:
        raise fail(
            f"sha256 mismatch expected={digest} got={written}",
            "delete the written file and call renderDocument again.",
        )
    return destination


def destination_for(write_to: str, cwd: Path, filename: str, digest: str) -> Path:
    raw = write_to if write_to.strip() else DEFAULT_WRITE_TO
    path = resolve_path(raw, cwd, for_write=True)
    if is_directory_target(raw, path):
        path = path / filename
    return unique_destination(path, digest)


def read_source(raw: str, cwd: Path) -> bytes:
    path = resolve_path(raw, cwd, for_write=False)
    if not path.is_file():
        raise fail(
            f"sourcePath not found: {path}",
            "pass a readable path relative to the client working directory, or an absolute path.",
        )
    try:
        return path.read_bytes()
    except OSError as exc:
        raise fail(
            f"sourcePath not readable: {path}",
            "pass a readable file and retry.",
        ) from exc
