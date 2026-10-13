---
diagramKind: floor plans
whenToUse: Building, room and lab layouts drawn to scale with coordinate-form floorplan styles.
minimalTemplate: fixtures/floorplan.tex
allowedPackages: endleaf-floorplan.sty, tikz-dimline, tikzscale
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Place the scale bar and the north arrow with a scope shift, never as draw options. Set /floorplan/plan-scale once. A 3 m wall reads 3.00 m. Do not use tikzscale; it needs an external tikz file.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/floorplan
mcpPromptName: playbook-floorplan
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Size and position are first-class: 7 pt absolute floor; room labels stay clear of dimensions, walls, doors and the scale bar. One scale story only. A door must break the wall, not sit on a solid line. If the plan is too wide for portrait, prefer a landscape page when this kind supports it. Do not shrink labels. Compile success with crushed or colliding room labels is still FAIL.

## When to use

A building, room or lab plan drawn to scale, with a scale bar, a north arrow and dimension labels.

## templateId and body syntax

templateId is `floorplan`. bodySyntax is a LaTeX picture body, no preamble. Do not send Markdown. Styles, provided by the worker image: floorplan wall, floorplan door, floorplan window, floorplan room label, floorplan scale bar, floorplan north arrow, floorplan dimension.

## Fence usage

For HTML or DOCX, put this picture in a tikz fence under document-shell. The fence class is `tikz`, with caption and alt. Do not use tikzscale: it needs an external tikz file.

## Output formats

This templateId is PDF. HTML and DOCX are wrapped by the gate as a document-shell tikz fence; the tool result says so.

## Kind notes

Use the coordinate form. Set `/floorplan/plan-scale` once (1000 means 1 TikZ cm is 1 m). Room areas and dimension labels are computed from it. A 3 m wall reads 3.00 m. Place the scale bar and the north arrow with a scope shift, never as `\draw` options (those draw a second copy at the origin).

## Common failures and fixes

`\draw[floorplan scale bar]` and `\draw[floorplan north arrow]` add a second mark at the origin. A door must break the wall, not sit on a solid line. Room labels stay clear of dimensions. Do not pass a scale as a draw option. Do not shrink labels under 7 pt.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. A failure is a tool result: fix it and resend, and budget re-renders.
