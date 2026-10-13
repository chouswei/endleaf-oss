---
diagramKind: document shell
whenToUse: Any Endleaf document: fenced diagrams, zh-TW text, math, and pdf, html or docx. A tikz fence may use tikz-cd, forest, automata, mindmap, tikz-timing and bytefield with no named playbook. Named playbooks for those kinds also remain valid.
minimalTemplate: fixtures/document-shell.md
allowedPackages: XeLaTeX, xeCJK, Noto CJK TC
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Close each fence. The fence class is tikz, with caption and alt. Mermaid and D2 are refused: use a tikz fence. Inline siunitx and mhchem are PDF only. CJK inside a fence needs the Noto font workaround. HTML math is a plain-text approximation.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/document-shell
mcpPromptName: playbook-document-shell
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Every fenced figure inherits shared Composition. The fence is not a dump zone. One intent per fence. 7 pt floor. No text on geometry. Compile success with crushed or colliding labels is still FAIL. Prefer proven fence bodies: prove each picture individually on its kind templateId (render that sheet alone), then assemble. Do not invent many unproven fences in one first shot.

## When to use

Any Endleaf document that mixes prose, Traditional Chinese, math and figures. This is the only templateId that is natively pdf, html and docx. A tikz fence may use tikz-cd, forest, automata, mindmap, tikz-timing and bytefield. Named playbooks for those kinds also remain valid.

## templateId and body syntax

templateId is `document-shell`. bodySyntax is Markdown. Do not send a preamble or `\documentclass`. The worker owns the template.

## Fence usage

The fence class is always `tikz`, for every kind. The fence body is the same picture code as that kind's TeX template (a `tikzpicture`, `circuitikz` or `ganttchart`). Set `caption=` and `alt=`. At most five fences. Mermaid and D2 fences are refused. Draw flowcharts with TikZ positioning.

## Output formats

HTML and DOCX keep fenced diagrams as images. Inline siunitx and mhchem are PDF only; the tool result carries the worker `warnings` field when they fall back to source text. HTML math is a plain-text approximation, with no MathJax. Kind templateIds are PDF; if you ask for HTML or DOCX the gate wraps them as a tikz fence under this template and says so.

## Kind notes

zh-TW prose in the Markdown is rendered with xeCJK. CJK inside a fence is a separate limit: see Readability.

## Common failures and fixes

An unclosed fence drops the rest of the document. A mermaid or d2 fence is refused: use a tikz fence. A kind templateId sent as Markdown fails as TeX; this templateId is the Markdown one.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. A failure is a tool result: fix it and resend, and budget re-renders.
