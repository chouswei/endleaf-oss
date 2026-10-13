---
topic: getting-started
titleEn: Getting started
resourceUri: endleaf://guide/getting-started
order: 1
---

# en

Endleaf by InkMirage renders Markdown and LaTeX to PDF. Send a body; Endleaf owns the preamble; templateId picks the frame. 1. Call renderDocument with outputFormat pdf, templateId document-shell, and source. 2. Read the summary line (ok, pages, page, bytes, sha256, file). 3. Call getQuota for remaining jobs. This key: plan {{plan}} ({{planStatus}}). Limits: {{jobsPerDay}} jobs a day, {{perMinute}} a minute, {{maxInputKiB}} KiB.

Clients that load the blob into context spend tokens. Use the local stdio client `endleaf-mcp` (package `endleaf_client`), env `ENDLEAF_API_KEY` (optional `ENDLEAF_MCP_URL`). It writes to disk: `writeTo` saves the PDF, checks sha256, and returns one line (about 55 tokens, not about 10k). `sourcePath` sends a file, so TeX never passes through the model. `uploadFromPath` returns a source_id to reuse. The remote gate cannot write to your disk. Plain remote clients get the file as a resource blob. pageSize a4 (default), letter or a3; optional orientation portrait or landscape.

Pick a templateId by content: concept map → mindmap; states, steps or flow → automata (a plain flowchart is a TikZ fence in document-shell); architecture and interfaces → sysml; schedule → gantt; signals and timing → tikztiming; hierarchy or taxonomy → forest; data and measurements → plots; packet or register layout → bytefield; commutative diagram → tikzcd; circuit → circuits, P&ID → pidcircuit; molecule or reaction → chemistry; rooms → floorplan; prose with figures and citations → fulldoc; plain prose → document-shell.

fulldoc: send the body only, no `\documentclass`, no `\begin{document}`; pdf only. Other templateIds: pdf, html, or docx. Mermaid and D2 are refused. Empty `guide` lists topics and kinds. Page `endleaf://guide/getting-started`. Point the client at [https://endleaf.inkmirage.xyz/mcp](https://endleaf.inkmirage.xyz/mcp). Help: [support@inkmirage.xyz](mailto:support@inkmirage.xyz). The skill pack is `endleaf://guide/skill`.
