"""Stdio MCP server. Fetches the live tool list. ENDLEAF-R53-LIST."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    EmbeddedResource,
    ListPromptsResult,
    ListResourcesResult,
    ListToolsResult,
    Prompt,
    ReadResourceRequestParams,
    ReadResourceResult,
    Resource,
    TextContent,
    TextResourceContents,
    Tool,
    ToolAnnotations,
)

from endleaf_client import __version__
from endleaf_client.errors import ClientError
from endleaf_client.gate import DEFAULT_MCP_URL, GateClient, tools_digest
from endleaf_client.proxy import annotate_tools, dispatch

log = logging.getLogger("endleaf_client")

_LOCAL_NOTE = (
    "This local client writes PDFs to disk and never returns the blob. "
    "Use writeTo, sourcePath, or uploadFromPath."
)


def _as_tool(item: dict[str, Any]) -> Tool:
    schema = item.get("inputSchema")
    if not isinstance(schema, dict):
        schema = {"type": "object"}
    kwargs: dict[str, Any] = {
        "name": str(item.get("name") or ""),
        "description": str(item.get("description") or ""),
        "inputSchema": schema,
    }
    raw = item.get("annotations")
    if isinstance(raw, dict):
        allowed = {key: raw[key] for key in ("title", "readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint") if key in raw}
        if allowed:
            kwargs["annotations"] = ToolAnnotations.model_validate(allowed)
    return Tool.model_validate(kwargs)


def _content_blocks(result: dict[str, Any]) -> list[TextContent | EmbeddedResource]:
    blocks: list[TextContent | EmbeddedResource] = []
    for item in result.get("content") or []:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "text" and isinstance(item.get("text"), str):
            blocks.append(TextContent(type="text", text=item["text"]))
        elif item.get("type") == "resource" and isinstance(item.get("resource"), dict):
            blocks.append(EmbeddedResource.model_validate(item))
    if not blocks:
        blocks.append(TextContent(type="text", text=""))
    return blocks


async def refresh_tool_list(gate: GateClient, state: dict[str, Any], session: Any) -> bool:
    """ENDLEAF-R56-LISTCHANGED. Tell the host to re-list when its copy may be stale.

    Stale means: the host called a tool before it listed tools from this
    process (it is using a cached list), or the gate session was re-opened
    (a gate restart is usually a roll) and the gate list changed.
    """
    stale = state.get("listed") is None
    if gate.generation != state.get("generation", 0):
        state["generation"] = gate.generation
        try:
            digest = tools_digest(annotate_tools(await gate.list_tools()))
        except Exception:
            return False
        stale = stale or digest != state.get("listed")
    if not stale or state.get("notified") == (state.get("listed"), gate.generation):
        return False
    state["notified"] = (state.get("listed"), gate.generation)
    sender = getattr(session, "send_tool_list_changed", None)
    if sender is None:
        return False
    try:
        await sender()
    except Exception:
        log.info("tools/list_changed not sent")
        return False
    return True


def build_server(gate: GateClient, cwd: Path) -> Server[Any]:
    state: dict[str, Any] = {"listed": None, "generation": getattr(gate, "generation", 0)}

    async def on_list_tools(_ctx: Any, _params: Any) -> ListToolsResult:
        local = annotate_tools(await gate.list_tools())
        state["listed"] = tools_digest(local)
        state["generation"] = gate.generation
        return ListToolsResult(tools=[_as_tool(item) for item in local])

    async def on_call_tool(ctx: Any, params: CallToolRequestParams) -> CallToolResult:
        arguments = params.arguments if isinstance(params.arguments, dict) else {}
        result = await dispatch(gate, params.name, arguments, cwd)
        await refresh_tool_list(gate, state, getattr(ctx, "session", None))
        return CallToolResult(
            content=_content_blocks(result),
            isError=bool(result.get("isError")),
        )

    async def on_list_resources(_ctx: Any, _params: Any) -> ListResourcesResult:
        rows = await gate.list_resources()
        out: list[Resource] = []
        for item in rows:
            uri = item.get("uri")
            name = item.get("name") or uri
            if not isinstance(uri, str) or not isinstance(name, str):
                continue
            out.append(
                Resource(
                    uri=uri,
                    name=name,
                    description=item.get("description") if isinstance(item.get("description"), str) else None,
                    mimeType=item.get("mimeType") if isinstance(item.get("mimeType"), str) else None,
                )
            )
        return ListResourcesResult(resources=out)

    async def on_read_resource(_ctx: Any, params: ReadResourceRequestParams) -> ReadResourceResult:
        result = await gate.read_resource(str(params.uri))
        contents = result.get("contents")
        out: list[TextResourceContents] = []
        if isinstance(contents, list):
            for item in contents:
                if not isinstance(item, dict):
                    continue
                text = item.get("text")
                item_uri = item.get("uri") or str(params.uri)
                if isinstance(text, str):
                    out.append(
                        TextResourceContents(
                            uri=item_uri,
                            mimeType=item.get("mimeType") if isinstance(item.get("mimeType"), str) else "text/plain",
                            text=text,
                        )
                    )
        return ReadResourceResult(contents=out)

    async def on_list_prompts(_ctx: Any, _params: Any) -> ListPromptsResult:
        rows = await gate.list_prompts()
        out: list[Prompt] = []
        for item in rows:
            name = item.get("name")
            if not isinstance(name, str):
                continue
            out.append(
                Prompt(
                    name=name,
                    description=item.get("description") if isinstance(item.get("description"), str) else None,
                )
            )
        return ListPromptsResult(prompts=out)

    instructions = gate.instructions.strip()
    if _LOCAL_NOTE not in instructions:
        instructions = f"{instructions}\n{_LOCAL_NOTE}".strip()
    return Server(
        "endleaf-local",
        version=__version__,
        instructions=instructions,
        on_list_tools=on_list_tools,
        on_call_tool=on_call_tool,
        on_list_resources=on_list_resources,
        on_read_resource=on_read_resource,
        on_list_prompts=on_list_prompts,
    )


async def serve(gate: GateClient, cwd: Path) -> None:
    server = build_server(gate, cwd)
    options = server.create_initialization_options(
        notification_options=NotificationOptions(tools_changed=True),
    )
    async with stdio_server() as (read, write):
        await server.run(read, write, options)


def load_settings(
    env: dict[str, str],
    *,
    default_url: str = DEFAULT_MCP_URL,
) -> tuple[str, str]:
    key = (env.get("ENDLEAF_API_KEY") or "").strip()
    if not key:
        raise ClientError(
            "ENDLEAF_API_KEY is missing",
            "set ENDLEAF_API_KEY in the MCP config env; the value is never logged.",
        )
    url = (env.get("ENDLEAF_MCP_URL") or default_url).strip() or default_url
    return url, key
