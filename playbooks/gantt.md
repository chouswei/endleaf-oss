---
diagramKind: Gantt
whenToUse: Gantt charts drawn with pgfgantt.
minimalTemplate: fixtures/gantt.tex
allowedPackages: pgfgantt
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: No \\ after the last row. Set x unit so units times x unit plus about 3 cm of labels fit the line. Name bars and link them with ganttlink.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/gantt
mcpPromptName: playbook-gantt
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Size and position are first-class: 7 pt absolute floor. Do not ship shrunk illegible bars. If the chart is too wide for portrait, prefer a landscape page when this kind supports it, or split the chart. Compile success with crushed bar labels is still FAIL.

## When to use

A Gantt chart of groups, bars and milestones that fits the page, with titles and links.

## templateId and body syntax

templateId is `gantt`. bodySyntax is a LaTeX picture body, no preamble. Do not send Markdown. The picture is one `ganttchart` environment.

## Fence usage

For HTML or DOCX, put the same `ganttchart` in a tikz fence under document-shell. The fence class is `tikz`, with caption and alt.

## Output formats

This templateId is PDF. HTML and DOCX are wrapped by the gate as a document-shell tikz fence; the tool result says so. A chart wider than the line must not shrink labels under 7 pt. Split the chart, or use a landscape page when this kind supports it.

## Kind notes

No `\\` after the last row (it adds an empty row). Set `x unit` so the chart fits the line: units times x unit, plus about 3 cm of labels, at most 12 cm. Name bars and link them with `\ganttlink`. Title, bar, group and milestone fonts are `\small`.

## Common failures and fixes

A trailing `\\` leaves a blank row. A default x unit overflows the page. Unnamed bars cannot be linked.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. A failure is a tool result: fix it and resend, and budget re-renders.
