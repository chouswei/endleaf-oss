---
diagramKind: plots
whenToUse: pgfplots charts in 2D, and in 3D with at most 25 samples per axis and one surf or mesh.
minimalTemplate: fixtures/pgfplots.tex
allowedPackages: pgfplots
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Use one axis at 0.9 linewidth. Data inline only. Do not call gnuplot. 3D samples stay at most 25 per axis, with one surf or mesh.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/plots
mcpPromptName: playbook-plots
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Size and position are first-class: 7 pt absolute floor. Do not ship a path that shrinks type under 7 pt. Split the series or the page, or use a landscape page when this kind supports it. Labels stay clear of the plot, legend and axes. Compile success with crushed or colliding text is still FAIL. One intent per figure.

## When to use

A pgfplots chart: one 2D axis with labels, grid, legend and title, or a single 3D surf or mesh.

## templateId and body syntax

templateId is `plots`. bodySyntax is a LaTeX picture body, no preamble. The reference file is `pgfplots.tex`; the templateId is still `plots`. Do not send Markdown.

## Fence usage

For HTML or DOCX, put this axis in a tikz fence under document-shell, or let the gate wrap it. The fence class is `tikz`, with caption and alt. Do not ship a picture that shrinks type under 7 pt. Split the series or the page, or use a landscape page when this kind supports it.

## Output formats

This templateId is PDF. HTML and DOCX are wrapped by the gate as a document-shell tikz fence; the tool result says so. Inline siunitx in a caption is PDF only.

## Kind notes

Use one axis, `width=0.9\linewidth`, with xlabel, ylabel, grid, legend and title. A 2D curve can use samples=50. 3D: samples at most 25 per axis, and one surf or mesh. Data inline only (`coordinates` or an inline `table`). No external files. No gnuplot. There is no separate sample-budget setting to read; use this rule.

## Common failures and fixes

Two default-width axes side by side overflow the line. Missing labels leave a bare curve. gnuplot is refused. A huge samples value hits the wall clock: lower it and resend.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. A failure is a tool result: fix it and resend, and budget re-renders.
