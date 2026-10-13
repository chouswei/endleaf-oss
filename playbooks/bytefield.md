---
diagramKind: byte fields
whenToUse: Protocol headers and bit or byte field diagrams drawn with bytefield.
minimalTemplate: fixtures/bytefield.tex
allowedPackages: bytefield
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Send a LaTeX picture body, not Markdown and not a preamble. One bytefield environment. HTML and DOCX wrap as a document-shell tikz fence.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/bytefield
mcpPromptName: playbook-bytefield
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Size and position are first-class: 7 pt absolute floor; no text intersecting boxes, lines, symbols, or other labels. One intent per figure. If the picture is too wide for portrait, prefer a landscape page when this kind supports it; otherwise split. Do not shrink-to-fit. Compile success with crushed or colliding text is still FAIL.

## When to use

A protocol header or a bit or byte field diagram drawn with bytefield, with field names a reader can see.

## templateId and body syntax

templateId is `bytefield`. bodySyntax is a LaTeX picture body, no preamble. Do not send Markdown, `\documentclass` or `\usepackage`. Sending Markdown to this templateId is a TeX error. The picture is one `bytefield` environment. Bit numbers are 7 pt sans and the bit width is measured from them, so a 32-bit row fits the portrait line; a fixed `bitwidth` above 1em for 32 bits runs past it.

A documentShell TikZ picture body may still use bytefield. Named playbooks and documentShell both remain valid.

## Fence usage

For HTML or DOCX, put the same `bytefield` in a tikz fence under document-shell. The fence class is `tikz`, with caption and alt.

## Output formats

This templateId is PDF. The worker owns a template for this kind, so a PDF render sends your body as is. HTML and DOCX wrap it as a document-shell tikz fence with alt text and no invented caption; the tool result says so. The same environment works in a fulldoc `figure`.

## Kind notes

This kind renders now. The listing label is `renders now; performance bar not yet measured`. It is not labelled supported. The worker preamble loads bytefield. Do not send a preamble.

## Common failures and fixes

A Markdown body here fails with a TeX error. A preamble is refused. Field widths that do not add up to the declared word width fail to compile: fix the widths and resend.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. No mermaid fence, no d2 fence, and no tikz-feynman auto-layout. A failure is a tool result: fix it and resend, and budget re-renders.
