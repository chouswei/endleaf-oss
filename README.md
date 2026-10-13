# Endleaf by InkMirage — open-source client and playbooks

Endleaf renders Markdown and LaTeX (diagrams, plots, circuits, P&ID, chemistry, Gantt, floor plans, SysML, full documents) to PDF through a keyed MCP endpoint at `https://endleaf.inkmirage.xyz/mcp`.

This repository contains the public parts of Endleaf:

- `endleaf_client/` — a thin stdio MCP client that proxies the hosted endpoint and writes PDF and source files to disk. See `endleaf_client/README.md`.
- `playbooks/` — the LaTeX playbooks, templates and agent guides the service serves through `listPlaybooks`, `getPlaybook` and `guide`.

The hosted gate, billing, quota enforcement and account integration are not part of this repository. The render worker is [latex-on-http](https://github.com/chouswei/latex-on-http) (AGPL-3.0).

## Operator

Endleaf is operated by InkMirage. Contact: support@inkmirage.xyz.

## License

GNU Affero General Public License v3.0 (AGPL-3.0). See `LICENSE`. InkMirage may relicense future versions under MIT.
