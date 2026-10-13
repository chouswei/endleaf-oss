"""Live smoke: URL and key from env. Skips when unset."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import tempfile
from pathlib import Path

from endleaf_client.errors import ClientError
from endleaf_client.gate import DEFAULT_MCP_URL, GateClient
from endleaf_client.proxy import dispatch
from endleaf_client.server import load_settings

_SOURCE = "Hello from the Endleaf local client.\n"


async def run_smoke(url: str, key: str, cwd: Path) -> str:
    gate = GateClient(url, key)
    try:
        await gate.initialize()
        source = cwd / "smoke-source.md"
        source.write_text(_SOURCE, encoding="utf-8")
        result = await dispatch(
            gate,
            "renderDocument",
            {
                "outputFormat": "pdf",
                "templateId": "document-shell",
                "sourcePath": str(source.name),
            },
            cwd,
        )
        text = ""
        content = result.get("content")
        if isinstance(content, list) and content and isinstance(content[0], dict):
            raw = content[0].get("text")
            if isinstance(raw, str):
                text = raw
        if result.get("isError"):
            raise ClientError(text.splitlines()[0] if text else "smoke render failed", "see Fix.")
        return text
    finally:
        await gate.aclose()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Live Endleaf local-client smoke.")
    parser.add_argument("--require", action="store_true", help="fail when URL or key is unset")
    args = parser.parse_args(argv)
    if not os.environ.get("ENDLEAF_API_KEY", "").strip():
        message = "skip live smoke: ENDLEAF_API_KEY is unset"
        print(message, file=sys.stderr)
        return 2 if args.require else 0
    try:
        url, key = load_settings(os.environ, default_url=os.environ.get("ENDLEAF_MCP_URL") or DEFAULT_MCP_URL)
    except ClientError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="endleaf-smoke-") as tmp:
        try:
            text = asyncio.run(run_smoke(url, key, Path(tmp)))
        except ClientError as exc:
            print(str(exc), file=sys.stderr)
            return 1
    print(text)
    print(f"chars={len(text)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
