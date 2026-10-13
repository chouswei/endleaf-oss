---
diagramKind: full document
whenToUse: One PDF: sections, prose, lists, tables, citations and sysml-tikz, TikZ or circuitikz figures; English and zh-TW.
minimalTemplate: fixtures/fulldoc.tex
allowedPackages: XeLaTeX, xeCJK, Noto CJK TC, TikZ, PIDcircuitTikZ, circuitikz, siunitx, TikZ shapes, TikZ arrows.meta, TikZ positioning, TikZ calc, pgfplots, chemfig, mhchem, pgfgantt, tikz-dimline, tikzscale, tikz-cd, forest, tikz-timing, bytefield, TikZ automata, TikZ mindmap, sysml-tikz.sty
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Send a LaTeX document body, not Markdown and not a preamble. Cite with \cite and one thebibliography; no .bib. Keep each figure with its caption. Prefer [htbp]. A float may move. A sysmlfigure header must stay with its canvas. A sysml canvas wider than the portrait line at the declared body size is landscape A4 at that size. Do not send \pdfpagewidth. 7 pt is a floor, not a fit target. If it still will not fit, the render is an error. Plain TikZ and circuitikz pictures are not auto-fitted. Use \sysmlconnection, \sysmlflow and \sysmlbinding, and end each line on the port outer edge.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/fulldoc
mcpPromptName: playbook-fulldoc
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Composition applies before page-size choice. Each embedded figure is one intent. Size and position are first-class: 7 pt absolute floor on every figure; no text intersecting boxes, lines, symbols, or other labels. A float-only page of cramped figures is FAIL. If a sysml canvas is too wide for portrait at the declared type size, the template makes that page landscape A4 and type stays declared. Do not send `\pdfpagewidth`, `\usepackage{geometry}` or a preamble. Compile success with crushed or colliding text is still FAIL.

Prefer proven picture bodies. Prove each figure individually on its picture-kind templateId: render that sheet alone against live Endleaf, pass the Composition proof bar, then assemble those proven bodies here. Do not invent many unproven figures in one first shot. Still budget re-renders. Soft-pass “TeX compiled = ship” is forbidden.

## When to use

One keyed `renderDocument` call that returns one PDF: title, optional author, sections and subsections, prose, lists, tables, captions and cross-references, with sysml-tikz, plain TikZ and circuitikz or PIDcircuitTikZ figures in the same body. English and zh-TW (Traditional Chinese) may be mixed in the caller's source. This kind renders now. The listing label is `renders now; performance bar not yet measured`. It is not labelled supported.

## templateId and body syntax

templateId is `fulldoc`. bodySyntax is a LaTeX document body, no preamble. Do not send Markdown, `\documentclass`, `\usepackage`, `\RequirePackage` or `\begin{document}`. The worker owns the class, the preamble and `\begin{document}`.

`outputFormat` is `pdf` only. HTML and DOCX are refused and are not wrapped as a tikz fence. One call returns one PDF. zh-TW in the body is set with xeCJK and Noto Sans CJK TC; CJK in the body does not need the fence font workaround.

A call is keyed. This key's quotas stay the Limits line. The worker refuses a fulldoc PDF of more than 16 pages. That page cap is `maxPages` on the Limits line, for this kind only. HTML and DOCX are refused before the worker and do not consume a quota job.

## Figures

Write each picture in a `figure` with `\caption` and `\label`, and point at it with `\ref`. Recommend the placement `[htbp]`. A float may move to a later page. A page that holds only floats is top-aligned. The gap between those floats is a fixed 12 pt. A PIDcircuitTikZ picture is a `tikzpicture` with `circuit pid ISO14617`, same wrapper as plain TikZ. A circuitikz picture uses `circuitikz`. A SysML picture uses `sysmlfigure` and `sysmlcanvas`. Every drawing kind's environment works in a figure: `tikzcd`, `forest`, `tikztimingtable`, `bytefield`, automata and mindmap `tikzpicture`s, `axis`, `ganttchart`, and bare `\chemfig` or `\ce`. checkDocument reports CHK-PACKAGE for an environment fulldoc does not load (tikz-feynman, tikz-3dplot, tabularx, ...) before you spend a render.

The worker, not the caller, wraps each figure so the picture and its caption stay together. For `sysmlfigure`, the header and the canvas stay in one box. The box is a kernel `minipage` of width `\linewidth`. Do not load `needspace`. The same wrap is applied to templateId `sysml`.

Lines use the v2 macros. `\sysmlconnection` is a solid line with no arrowhead unless `directed` is set. `\sysmlflow` draws the filled triangle. `\sysmlbinding` draws a solid line with `=` at the midpoint. End every line on the port outer edge, 1.6 mm out from the port centre. The example east port is centred at x = 26, so the connector starts at x = 27.6. The west port is centred at x = 58, so the connector ends at x = 56.4.

## Citations

Cite with the LaTeX kernel only. Write `\cite{key}` (or `\cite{a,b}`) in the text and end the body with one bibliography:

```
\begin{thebibliography}{9}
\bibitem{iec60034} IEC 60034-1, Rotating electrical machines: rating and performance, 2022.
\end{thebibliography}
```

- Keys: unique; letters, digits and `:` `-` `.` only; no spaces, commas or braces in a key.
- Entries are typeset text: escape `&` `%` `$` `#` `_` `{` `}` as `\&` `\%` `\$` `\#` `\_` `\{` `\}`. Write the entry in the order and style you want; nothing reformats it.
- `{9}` sizes the label column for up to 9 entries; use `{99}` for 10 to 99.

There is no `.bib` file, BibTeX, biber, natbib or biblatex, and `\citep`, `\citet` and `\printbibliography` are undefined. Entries print in `\bibitem` order as [1], [2], and the heading is References. The worker runs a second XeLaTeX pass when the body uses `\cite`, so citations resolve. `[?]` in the PDF, or `undefinedCite` above 0 on the summary warn line, means a `\cite` key has no `\bibitem`.

## Page and width

The worker class is `article` with `a4paper`. Send pageSize letter or a3 for those sizes; orientation landscape turns every page. It does not load `geometry`. The template owns page geometry. Do not send `\pdfpagewidth`, `\pdfpageheight` or a preamble. The portrait line width stays about 12 cm (about 345 pt, about 12.2 cm). If a sysml canvas is wider than that line at the declared body size, that figure goes on a landscape A4 page of its own (297 mm by 210 mm) and type stays at the declared size. Text after the figure keeps flowing on the portrait page before it; there is no forced page break. A picture that still runs past its line is returned with a `layout_overhang` warning. 7 pt is an absolute floor, not a fit target. The worker does not scale type down to 7 pt to force portrait, and it does not shrink the millimetre unit. If the canvas still will not fit on landscape A4 at the declared size, the render is an error. Split the sheet. Portrait sheets that already fit at the declared size stay portrait. Still one intent per figure, no text on geometry. Do not use `\resizebox`. The caption header reports the declared type size.

Plain TikZ and circuitikz pictures are not auto-fitted. A plain picture wider than the line is logged as `ENDLEAF_WIDE_PICTURE` and is not scaled, so keep those pictures within 12 cm on portrait.

A sysml canvas about 132 mm wide is wider than the portrait line, so that page is landscape A4 and the header stays at the declared type (10 pt in the worked example).

Tables and equations: a wide table uses fixed `p{3cm}`-style column widths that wrap, fewer columns, or two tables. Do not `\resizebox` or scale a table; `tabularx` and `longtable` are not loaded. A long display equation uses `multline`, or `split` inside `equation`, breaking before `=` or `+`; amsmath is loaded. Never shrink math. `overfull` above 0 on the summary warn line means a line or table ran past the margin.

## Kind notes

The preamble loads only packages already approved for the served kinds: XeLaTeX, xeCJK, Noto CJK TC, and the drawing set (TikZ, PIDcircuitTikZ, circuitikz, siunitx, the listed TikZ libraries, pgfplots, chemfig, mhchem, pgfgantt, tikz-dimline, tikzscale, sysml-tikz, endleaf-floorplan). It does not add a package. `packageSetHash` stays `73d55216488d240edccd26168576fcb402ce10794e04a3ef5ee8aec2bb166b98`. In that preamble the worker sets `\belowcaptionskip` to 4 pt, so a caption above a tabular does not sit on the top rule. Float pages are top-aligned, with a fixed 12 pt gap between floats. Cross-references and citations resolve when the body uses `\ref`, `\pageref`, `\eqref`, `\cite` or `\tableofcontents` (the worker runs a second XeLaTeX pass).

Every PDF carries the Endleaf document-info credit: Creator, Producer and Keywords. The credit is not page text.

The worked example has a title, an author line for the operator InkMirage / 衍跡 InkMirage, two sections, one subsection, a list, a table, and three figures (sysml-tikz, TikZ, circuitikz) with captions and `\ref`.

## Common failures and fixes

A preamble is refused. Markdown sent to this templateId is a TeX error. HTML or DOCX is refused and does not consume a quota job. A `sysmlfigure` header must not sit on the page before its canvas. A sysml canvas wider than the portrait line at the declared size is landscape A4 at that size; 7 pt is a floor, not a target. Do not send `\pdfpagewidth`. Crushed or colliding text is still FAIL. If it still will not fit on landscape, the render is an error. A plain TikZ or circuitikz picture wider than 12 cm is not auto-fitted. A fulldoc PDF of more than 16 pages is refused. A float may move. A float-only page of cramped figures is FAIL. Use `[htbp]`. A connection does not grow an arrowhead from the port directions. Stop each line on the outer edge.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. A failure is a tool result: fix it and resend, and budget re-renders.
