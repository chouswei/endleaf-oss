"""CLI entry for `endleaf-mcp`."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

from endleaf_client.errors import ClientError
from endleaf_client.gate import GateClient
from endleaf_client.server import load_settings, serve


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="endleaf-mcp: %(message)s")
    # Never attach a filter that could echo env values.
    try:
        url, key = load_settings(os.environ)
    except ClientError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    cwd = Path.cwd()

    async def _run() -> None:
        gate = GateClient(url, key)
        try:
            await gate.initialize()
            await serve(gate, cwd)
        finally:
            await gate.aclose()

    try:
        asyncio.run(_run())
    except ClientError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
