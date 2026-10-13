---
diagramKind: P&ID
whenToUse: A piping and instrumentation diagram. Use the circuit pid ISO14617 key and put tags in the template.
minimalTemplate: fixtures/pidcircuit.tex
allowedPackages: PIDcircuitTikZ, TikZ
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Put circuit pid ISO14617 on the tikzpicture; do not load the library again. Tag every symbol with info=. Place a flow marker with pos=0.2 or pos=0.8 on flow path.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/pidcircuit
mcpPromptName: playbook-pidcircuit
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Size and position are first-class: 7 pt absolute floor (`every info/.style={font=\small}` or larger). Tags must not collide with each other, with symbols, or with flow arrows. Reserved gutter for `info=` tags. Flow arrows stay clear of tags. At most 12 tagged symbols on one sheet; more than that is a mandatory split. If the sheet is too wide for portrait, prefer a landscape page when this kind supports it. Do not shrink tags. Compile success with crushed or colliding tags is still FAIL.

## When to use

A piping and instrumentation diagram: valves, pumps, flow paths and instruments, with tags a reader can see.

## templateId and body syntax

templateId is `pidcircuit`. bodySyntax is a LaTeX picture body, no preamble. Do not send Markdown, `\documentclass` or `\usepackage`. Sending Markdown to this templateId is a TeX error.

## Fence usage

For a figure inside a document, send templateId `document-shell` and put this same picture in a tikz fence with caption and alt. The fence class is `tikz`. Do not `\usetikzlibrary` the P&ID library; it is preloaded. The key on the picture is `circuit pid ISO14617`.

## Output formats

This templateId is PDF. HTML and DOCX are not sent as bare TeX: the gate wraps the body as a tikz fence under document-shell and the tool result includes a wrap line. Inline siunitx and mhchem stay PDF only.

## Kind notes

Tag every symbol with `info=` (for example `valve={info=V-101}`). A flow marker is `flow path` with `pos=`. `pos=0.2` and `pos=0.8` place the arrow at that fraction of the path. The worker keeps TikZ `pos` shared with the PID flow position. Set `every info/.style={font=\small}`. Tags stay at or above 7 pt, in a reserved gutter, clear of flow arrows and of other tags. If tags collide, re-layout or split; do not shrink.

## Common failures and fixes

A missing `circuit pid ISO14617` key draws ordinary lines. Loading the library again is unnecessary. To move a flow arrow, set `pos=0.2` or `pos=0.8` on that `flow path`.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. A failure is a tool result: fix it and resend, and budget re-renders.
