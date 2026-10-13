"""Local tool behaviour on top of the remote gate. ENDLEAF-R53."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from endleaf_client.errors import ClientError, fail
from endleaf_client.gate import GateClient
from endleaf_client.paths import DEFAULT_WRITE_TO, read_source
from endleaf_client.render import (
    enforce_size,
    error_text,
    first_text,
    format_upload_line,
    parse_quota_kib,
    save_render,
)

HIDDEN_TOOLS = frozenset({"uploadSource"})
# ENDLEAF-R56-PASS. Every gate argument except these is forwarded as sent.
LOCAL_RENDER_FIELDS = frozenset({"writeTo", "sourcePath"})
INLINE = "inline"


def annotate_tools(remote: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Pass through gate tools, hide uploadSource, add local fields."""
    out: list[dict[str, Any]] = []
    for tool in remote:
        name = tool.get("name")
        if name in HIDDEN_TOOLS:
            continue
        item = copy.deepcopy(tool)
        if name == "renderDocument":
            schema = item.setdefault("inputSchema", {})
            if not isinstance(schema, dict):
                schema = {}
                item["inputSchema"] = schema
            props = schema.setdefault("properties", {})
            if not isinstance(props, dict):
                props = {}
                schema["properties"] = props
            # ENDLEAF-R56-PASS. A host may keep an older copy of this list.
            # Open the schema so a newer gate field still reaches the gate;
            # the gate stays strict and names an unknown field in one line.
            schema["additionalProperties"] = True
            props["writeTo"] = {
                "type": "string",
                "description": (
                    "Path or directory for the saved file. Default ./endleaf-out/. "
                    "The client writes the blob and returns only the summary line."
                ),
            }
            props["sourcePath"] = {
                "type": "string",
                "description": (
                    "Read source from this local path. The client uploads it; "
                    "do not send source, body, or source_id."
                ),
            }
            description = item.get("description")
            extra = (
                " Optional writeTo saves the file and returns the summary only. "
                "Optional sourcePath reads disk so the agent never sends source bytes."
            )
            if isinstance(description, str) and extra.strip() not in description:
                item["description"] = description.rstrip() + extra
        out.append(item)
    out.append(_upload_from_path_tool())
    return out


def _upload_from_path_tool() -> dict[str, Any]:
    return {
        "name": "uploadFromPath",
        "description": (
            "Read a local source file and store it on the gate. "
            "Returns source_id, bytes, sha256 and expires. "
            "Does not render. Then call renderDocument with source_id."
        ),
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "required": ["path"],
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Local source path, relative to the client working directory.",
                }
            },
        },
        "annotations": {
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
        },
    }


def tool_result(text: str, *, is_error: bool = False) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": text}],
        "isError": is_error,
    }


def _content(result: dict[str, Any]) -> list[dict[str, Any]]:
    raw = result.get("content")
    if not isinstance(raw, list):
        return []
    return [item for item in raw if isinstance(item, dict)]


async def quota_kib(gate: GateClient) -> int | None:
    result = await gate.call_tool("getQuota", {})
    if result.get("isError"):
        raise fail(
            first_text(_content(result)) or "getQuota failed",
            "check ENDLEAF_API_KEY and retry getQuota.",
        )
    return parse_quota_kib(first_text(_content(result)))


async def upload_bytes(gate: GateClient, data: bytes) -> dict[str, Any]:
    import base64

    encoded = base64.b64encode(data).decode("ascii")
    result = await gate.call_tool("uploadSource", {"blob_b64": encoded})
    text = first_text(_content(result))
    if result.get("isError"):
        raise fail(text.splitlines()[0] if text else "uploadSource failed", _fix_from(text))
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise fail(
            "uploadSource returned no JSON",
            "retry uploadFromPath.",
        ) from exc
    if not isinstance(payload, dict):
        raise fail("uploadSource returned no source_id", "retry uploadFromPath.")
    return payload


def _fix_from(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("Fix:"):
            return line[4:].strip()
    return "correct the source and retry."


async def handle_upload_from_path(gate: GateClient, arguments: dict[str, Any], cwd: Path) -> dict[str, Any]:
    path = arguments.get("path")
    if not isinstance(path, str) or not path.strip():
        raise fail(
            "uploadFromPath requires path",
            "pass path to a readable local source file.",
        )
    extra = sorted(key for key in arguments if key != "path")
    if extra:
        raise fail(
            f"unexpected argument: {extra[0]}",
            "uploadFromPath requires exactly {path}.",
        )
    data = read_source(path, cwd)
    enforce_size(data, await quota_kib(gate))
    payload = await upload_bytes(gate, data)
    return tool_result(format_upload_line(payload))


async def handle_render(gate: GateClient, arguments: dict[str, Any], cwd: Path) -> dict[str, Any]:
    args = dict(arguments)
    write_to = args.pop("writeTo", None)
    source_path = args.pop("sourcePath", None)
    if write_to is not None and not isinstance(write_to, str):
        raise fail("writeTo must be a string", "pass a path or directory.")
    if source_path is not None and not isinstance(source_path, str):
        raise fail("sourcePath must be a string", "pass a readable local path.")
    delivery = args.get("delivery")
    if source_path:
        if any(key in args and args[key] not in (None, "") for key in ("source", "body", "source_id", "documentId")):
            raise fail(
                "renderDocument sourcePath cannot be combined with source, body, source_id, or documentId",
                "send only sourcePath, or only source_id, or only source, or only documentId.",
            )
        data = read_source(source_path, cwd)
        enforce_size(data, await quota_kib(gate))
        stored = await upload_bytes(gate, data)
        args["source_id"] = stored["source_id"]
        args.pop("source", None)
        args.pop("body", None)
    result = await gate.call_tool("renderDocument", args)
    content = _content(result)
    if result.get("isError"):
        text = first_text(content) or "renderDocument failed"
        return tool_result(text, is_error=True)
    if delivery == INLINE:
        return result
    summary = save_render(content, write_to=write_to or DEFAULT_WRITE_TO, cwd=cwd)
    return tool_result(summary)


async def handle_passthrough(gate: GateClient, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name in HIDDEN_TOOLS:
        raise fail(
            "uploadSource is not a local tool",
            "call uploadFromPath or renderDocument with sourcePath.",
        )
    return await gate.call_tool(name, arguments)


async def dispatch(gate: GateClient, name: str, arguments: dict[str, Any] | None, cwd: Path) -> dict[str, Any]:
    args = dict(arguments or {})
    try:
        if name == "renderDocument":
            return await handle_render(gate, args, cwd)
        if name == "uploadFromPath":
            return await handle_upload_from_path(gate, args, cwd)
        return await handle_passthrough(gate, name, args)
    except ClientError as exc:
        return tool_result(str(exc), is_error=True)
    except Exception as exc:
        return tool_result(error_text(exc), is_error=True)
