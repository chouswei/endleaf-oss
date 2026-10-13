---
diagramKind: circuits
whenToUse: circuitikz schematics, siunitx quantities, and TikZ block diagrams.
minimalTemplate: fixtures/circuits.tex
allowedPackages: circuitikz, siunitx, TikZ shapes, TikZ arrows.meta, TikZ positioning, TikZ calc
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Inline siunitx is PDF only. Put a quantity in a tikz fence to keep it visible in HTML and DOCX. Other pgf libraries may be loaded except external.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/circuits
mcpPromptName: playbook-circuits
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Size and position are first-class: 7 pt absolute floor; no text intersecting a box, line, symbol, or other label. Compile success with crushed or colliding text is still FAIL.

Demand zones. A barrier is one dashed line plus a short title, not an essay on the canvas. Isolator labels must not overlap. Do not scale labels down; split the schematic, or use a landscape page when this kind supports it. One intent per figure.

## When to use

circuitikz schematics with siunitx quantities, and TikZ block diagrams that need shapes, arrows, positioning or calc.

## templateId and body syntax

templateId is `circuits`. bodySyntax is a LaTeX picture body, no preamble. Do not send Markdown. Write quantities with `\qty`, not `\SI`.

## Fence usage

To keep a quantity visible in HTML or DOCX, put the formula in a tikz fence (it becomes an image). The fence class is `tikz`, with caption and alt. The fence body is this same picture.

## Output formats

This templateId is PDF. HTML and DOCX are wrapped by the gate as a document-shell tikz fence; the tool result says so. Inline siunitx is PDF only. The worker `warnings` field (`notationPdfOnly`) is copied into the tool result when an inline quantity falls back to source text.

## Kind notes

Preloaded libraries are listed under Readability. `\usetikzlibrary{fit,backgrounds}` and other pgf libraries are allowed in the body. `external` is refused.

## Common failures and fixes

A Markdown body here fails with a TeX error. An inline `\qty` in HTML or DOCX becomes source text: move it into a tikz fence. Do not scale the labels down to fit. Split the schematic, or use a landscape page when this kind supports it. Labels stay at or above 7 pt and clear of symbols. Compile success with crushed or colliding text is still FAIL.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. A failure is a tool result: fix it and resend, and budget re-renders.
