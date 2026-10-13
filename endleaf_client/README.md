# Endleaf local MCP client

Thin stdio MCP client for [Endleaf by InkMirage](https://endleaf.inkmirage.xyz). It proxies the live keyed gate and writes PDF and source bytes to disk so agents never load them into context.

The remote gate returns a compact summary plus an embedded PDF blob. Clients that load that blob spend about 10k tokens per render. This process writes the file, checks `sha256`, and returns only the summary line with `file=` set to the local path.

## Install

Python >= 3.12. From an MCP config the simplest command is:

```bash
uvx --from git+https://github.com/chouswei/endleaf-oss#subdirectory=endleaf_client endleaf-mcp
```

Or from a clone:

```bash
pip install -e ".[dev]"
endleaf-mcp
```

Set `ENDLEAF_API_KEY`. Optional `ENDLEAF_MCP_URL` defaults to `https://endleaf.inkmirage.xyz/mcp`. The key is never logged.

## Cursor MCP config

```json
{
  "mcpServers": {
    "endleaf": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/chouswei/endleaf-oss#subdirectory=endleaf_client",
        "endleaf-mcp"
      ],
      "env": {
        "ENDLEAF_API_KEY": "<your key>"
      }
    }
  }
}
```

Other stdio clients use the same command and env. Do not point the agent at the remote HTTP endpoint if you want bytes kept off-context.

## Tools

The client fetches `tools/list` from the gate at start and on every list, so the public surface does not go stale (`tools.listChanged` is true). `uploadSource` is hidden. Local extras:

- `renderDocument.writeTo` — path or directory; default `./endleaf-out/`.
- `renderDocument.sourcePath` — read the source from disk, upload on the transport, render by `source_id`.
- `uploadFromPath(path)` — returns `source_id=... bytes=... sha256=... expires=...`.

`delivery` `inline` is passed through unchanged, including the blob.

Relative paths resolve against the client working directory. A relative write outside that directory is refused unless you pass an absolute path. An existing file is overwritten only when the sha matches; different content gets a suffix.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

Live smoke (skips when the key is unset):

```bash
ENDLEAF_API_KEY=... ENDLEAF_MCP_URL=https://endleaf.inkmirage.xyz/mcp python -m endleaf_client.smoke
```

Operator: InkMirage. Support: support@inkmirage.xyz.
