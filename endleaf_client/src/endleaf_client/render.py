"""Strip the gate blob and rewrite the summary line. ENDLEAF-R53-WRITE."""

from __future__ import annotations

import base64
import binascii
import json
import re
from pathlib import Path
from typing import Any

from endleaf_client.errors import ClientError, fail
from endleaf_client.paths import DEFAULT_WRITE_TO, destination_for, sha256_hex, write_artifact

_SHA = re.compile(r"(?:^|\s)sha256=([0-9a-fA-F]{64})")
_FILE = re.compile(r"(?:^|\s)file=(\S+)")
_SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def first_text(content: list[dict[str, Any]]) -> str:
    for item in content:
        if item.get("type") == "text" and isinstance(item.get("text"), str):
            return item["text"]
    return ""


def extract_blob(content: list[dict[str, Any]]) -> tuple[bytes, str] | None:
    """Return (bytes, filename hint) from an embedded resource, or None."""
    for item in content:
        if item.get("type") != "resource":
            continue
        resource = item.get("resource")
        if not isinstance(resource, dict):
            continue
        blob = resource.get("blob")
        if not isinstance(blob, str) or blob == "":
            continue
        try:
            data = base64.b64decode(blob, validate=True)
        except (ValueError, binascii.Error) as exc:
            raise fail(
                "gate resource blob is not standard base64",
                "retry renderDocument; if it persists, call guide topic getting-started.",
            ) from exc
        name = _filename_hint(resource)
        return data, name
    return None


def _filename_hint(resource: dict[str, Any]) -> str:
    meta = resource.get("_meta")
    if isinstance(meta, dict) and isinstance(meta.get("filename"), str) and meta["filename"]:
        return Path(str(meta["filename"])).name
    for key in ("name", "uri"):
        value = resource.get(key)
        if isinstance(value, str) and value:
            name = Path(value).name
            if name and name not in {".", "/"}:
                return name
    return "endleaf-result.bin"


def summary_digest(text: str) -> str | None:
    match = _SHA.search(text.splitlines()[0] if text else "")
    if match is None:
        return None
    return match.group(1).lower()


def summary_filename(text: str, fallback: str) -> str:
    match = _FILE.search(text.splitlines()[0] if text else "")
    if match is None:
        return fallback
    return Path(match.group(1)).name or fallback


def rewrite_summary(text: str, local_path: Path) -> str:
    first = text.splitlines()[0] if text else "ok"
    shown = str(local_path)
    if _FILE.search(first):
        first = re.sub(r"file=\S+", f"file={shown}", first)
    else:
        first = f"{first} file={shown}".strip()
    return first


def contains_blob_payload(text: str, data: bytes | None) -> bool:
    if "blob" in text.lower():
        return True
    if data and base64.b64encode(data).decode("ascii") in text:
        return True
    return False


def save_render(
    content: list[dict[str, Any]],
    *,
    write_to: str,
    cwd: Path,
) -> str:
    text = first_text(content)
    extracted = extract_blob(content)
    if extracted is None:
        if text:
            return text.splitlines()[0]
        raise fail(
            "renderDocument returned no file resource",
            "retry the render, or send delivery inline only if you need the blob.",
        )
    data, hint = extracted
    digest = summary_digest(text) or sha256_hex(data)
    if sha256_hex(data) != digest:
        raise fail(
            f"sha256 mismatch expected={digest} got={sha256_hex(data)}",
            "delete any partial file and call renderDocument again.",
        )
    filename = summary_filename(text, hint)
    if _SAFE_NAME.sub("", filename) == "":
        filename = hint
    target = destination_for(write_to or DEFAULT_WRITE_TO, cwd, filename, digest)
    written = write_artifact(target, data, digest)
    summary = rewrite_summary(text, written)
    if contains_blob_payload(summary, data):
        raise fail(
            "refusing to return blob bytes to the agent",
            "use the local file path in the summary line.",
        )
    return summary


def parse_quota_kib(text: str) -> int | None:
    """Return max_doc_kib, or None when unlimited."""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise fail(
            "getQuota did not return JSON",
            "call getQuota and retry, or check ENDLEAF_API_KEY.",
        ) from exc
    if not isinstance(payload, dict):
        raise fail(
            "getQuota did not return max_doc_kib",
            "call getQuota and retry, or check ENDLEAF_API_KEY.",
        )
    limits = payload.get("limits")
    if not isinstance(limits, dict):
        raise fail(
            "getQuota did not return max_doc_kib",
            "call getQuota and retry, or check ENDLEAF_API_KEY.",
        )
    raw = limits.get("max_doc_kib")
    if raw == "unlimited":
        return None
    if isinstance(raw, int) and raw > 0:
        return raw
    if isinstance(raw, str) and raw.isdigit() and int(raw) > 0:
        return int(raw)
    raise fail(
        "getQuota did not return max_doc_kib",
        "call getQuota and retry, or check ENDLEAF_API_KEY.",
    )


def enforce_size(data: bytes, max_kib: int | None) -> None:
    if max_kib is None:
        return
    if len(data) > max_kib * 1024:
        got = (len(data) + 1023) // 1024
        raise fail(
            f"sourcePath exceeds max_doc_kib={max_kib} (got {got} KiB)",
            f"shrink the source below {max_kib} KiB, or use a plan with a larger document cap.",
        )


def format_upload_line(payload: dict[str, Any]) -> str:
    source_id = payload.get("source_id")
    size = payload.get("bytes")
    digest = payload.get("sha256")
    expires = payload.get("expires_at") or payload.get("expires")
    if not isinstance(source_id, str) or not source_id:
        raise fail(
            "uploadSource returned no source_id",
            "retry uploadFromPath; if it persists, call getQuota and check the key.",
        )
    return (
        f"source_id={source_id} bytes={size} sha256={digest} expires={expires}"
    )


def error_text(exc: BaseException) -> str:
    if isinstance(exc, ClientError):
        return str(exc)
    text = " ".join(str(exc).split())
    if not text:
        text = "local client failed"
    return f"{text}\nFix: correct the path or arguments and retry."
