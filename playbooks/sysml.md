---
diagramKind: SysML
whenToUse: SysML v2 interconnection diagrams drawn with sysml-tikz: parts, ports and connectors.
minimalTemplate: fixtures/sysml.tex
allowedPackages: sysml-tikz.sty, TikZ
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Pass in, out or inout as the last argument of \sysmlport so the direction arrow stays inside the port square. conjugated or a leading tilde flips in and out and shows a tilde. End every line on the port outer edge, 1.6 mm out from the port centre on that side. Do not draw the line or the arrowhead into the square. A connection has no arrowhead unless directed is set. Use \sysmlflow for a filled triangle and \sysmlbinding for a solid line with =. Port direction does not choose the line arrowhead. A flow item that cannot sit clear of both ports is a render error; do not glue the word to one end. Overlapping text or a line into a port square is a render error (layout_overlap, line_into_port); re-layout, never shrink. Empty lx and ly put a port label outside the part. The worker keeps the sysmlfigure header with the canvas. A canvas wider than the portrait line at the declared body size is landscape A4 at that size. Do not send \pdfpagewidth. 7 pt is a floor, not a fit target. If it still will not fit, the render is an error.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/sysml
mcpPromptName: playbook-sysml
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Size, position and one layer are first-class. Compile success with crushed or colliding text is still FAIL.

Owner lock: **one layer per diagram**. No nested part internals on the same sheet as the parent face.

### KEEP

- templateId `sysml` + sysml-tikz (not Mermaid or D2 on this render path).
- Port square, outer-edge connector, `in` / `out` / `inout` inside the square.
- `\sysmlflow` / `\sysmlbinding` / `directed` semantics.
- 7 pt absolute floor. Port labels get a reserved gutter. No text on box, line, symbol, or other label.
- Size for the **widest token** (Heros 0.50–0.55 em is a mean). Part boxes are **three** lines (stereotype + name + type).
- Port pitch ≥ estimated label width + gutter (never a fixed 10 mm). Reserve a **label rectangle** before elbows.
- After render, before assemble: visual fail list, then **keep | simplify | split | reject**.
- Prefer canvas `scale≈1` over shrinking text. Honest unsupported: refuse or simplify; do not fake TikZ.
- Never `\resizebox{\textwidth}{!}{...}`. Orth elbows: named midpoints and `|-` / `-|`. Sibling parts share equal minima sized for the widest label. Place parts first, then connectors.
- PDF first. Fence path for HTML and DOCX.
- If the canvas is too wide for portrait at the declared type size, the template makes that page landscape A4 and type stays declared. Do not send `\pdfpagewidth`. Do not shrink-to-fit.

### KILL (refuse as a layout failure)

- Parent IBD and child internals on one canvas.
- Free-floating barrier essays drawn on top of boxes or lines.
- Visible meta chrome in the figure header (`view`, overrides, depth, body size) on human sheets.
- Port-name fog: stacked west labels, or signal text on both the wire and the port.
- Connection table cells that dump usage, item, ends and binds in one multi-line soup.
- On-canvas RFC noise (`CANDIDATE`, `MAY`, `SHOULD`, `TBD`) as decoration.
- One sheet that tries to be external context, isolation barrier and power islands together.
- Shrink-to-fit under 7 pt, or overlapping port labels. Fail = re-layout, not tighter kerning.
- A flow item box that cannot sit clear of both ports. Fail the render. Do not glue the word to one end.
- The stereotype line on the row of the top-edge port squares or their labels, a side port label over the name block, or a port label across the part outline. The render fails with `layout_overlap`.
- Item flows on one sheet drawn with both `directed` open sticks and `\sysmlflow` triangles. Every item flow is `\sysmlflow`.
- A part stretched far past its ports and labels, leaving a large empty area.
- One-line part box height, average-count sizing, a fixed 10 mm port pitch, or an elbow through glyph bounds.
- Five-letter port names at tight pitch. Title-band collision, text overlap, clipped labels, crowding, or text-over-plot.
- `\resizebox{\textwidth}{!}{...}`. Deprecated `right of=` / `\tikzstyle`. Caption paragraphs inside part boxes.

### Interconnection view (this kind only)

A SysML v2 Interconnection view shows the **encapsulated structural contents of one Usage**: nested parts, ports, and the connectors among those ports (and interfaces where we have macros). It is a structural interconnect of what is *inside* that usage. It is not a General, Action Flow, State Transition, Sequence, or Geometry view. templateId `sysml` stays this view on sysml-tikz. Do not invent those other kinds.

**Sheet A** is the interconnection of the parent face: the boundary, black-box child usages (name only), boundary ports, external peers, and connectors that attach at that boundary. Do not open child internals on Sheet A.

**Sheet B — inner interconnect** is the interconnection view of **one** child Usage alone:

1. Open that child's own sheet.
2. Place inner parts with `\sysmlpart` and the name/type labels (`\sysmllabel`). Budget **three** lines (stereotype + name + type). Size each line for the **widest token**.
3. Place their ports with `\sysmlport` (`in` / `out` / `inout`; `conjugated` or a leading `~` as needed). End every line on the port outer edge.
4. Connect those ports with `\sysmlconnection`, `\sysmlflow`, `\sysmlbinding`, or `directed`, as already documented below.
5. Render this sheet **alone** against live Endleaf (the `renderDocument` MCP PDF payload: summary plus the saved file; never read bytes in context). Remeter the Composition proof bar (arm's-length ≥ 7 pt, no text on geometry, one layer). Check the **visual fail list**. Decide **keep | simplify | split | reject**. Then **assemble** proven sheets into `fulldoc` or document-shell.

Sheet B shows only internals of that one child. Cross-level links that leave the child attach at the child's boundary on Sheet A; do not draw them through nested boxes on A. Never draw Sheet A and Sheet B on one canvas (layer-split KILL). Render this sheet alone, remeter, then assemble.

Same packing budget and Composition rules: 7 pt floor; pre-estimate from the **widest token** (Latin/mono ≈ 0.5·S is a mean, CJK ≈ 1.0·S); part boxes are **three** lines; reserved gutters; no text on geometry. Port pitch is not a fixed 10 mm. Reserve a **label rectangle** before routing elbows. Short tokens on the canvas; detail under the figure. Keywords and multiplicity stay readable at ≥ 7 pt. If the estimated box will not fit, split or landscape — never shrink-to-fit.

### NARROW / CORRECT

1. **Layer split:** Sheet A = parent-face interconnection (black-box children). Sheet B = interconnection of one child Usage. Never A and B together.
2. **Sheet B workflow:** open the child sheet; `\sysmlpart` / `\sysmllabel`; `\sysmlport`; then `\sysmlconnection` / `\sysmlflow` / `\sysmlbinding` / `directed` among those inner ports only.
3. **Intent split:** separate sheets for external IBD, digital/isolation, and power/islands. One intent family per sheet.
4. **Packing budget:** at most 8 parts on a canvas; at least 6 mm clear between boxes. Size each box for the **widest token**; part compartments are **three** lines. Port pitch ≥ estimated label width + reserved gutter — never a fixed 10 mm. If labels collide, stagger sides, split or externalize, or use a landscape page when this kind supports it. Do not shrink. Estimate first (Composition Size estimation).
5. **Barrier:** one dashed line + at most a 6-word title. Detail prose goes under the figure (caption or note), never on geometry. Title-band collision is FAIL.
6. **Canvas tokens:** short names on the figure; full path in a two-column table: token | from→to (one line). Binds = a separate mini-table. Kill irregular word-spacing and three-line cells.
7. **Header:** human sheets show title (optional revision id). Hide worker diagnostics from the printed face.
8. **Proof bar (agent must remeter):** arm's-length read — every label legible at or above 7 pt, no text on box, no text on line, one layer only. Reserve a **label rectangle** before elbows; never route through glyph bounds. Fail = re-layout, do not ship.
9. **Label band:** the stereotype line starts at least 1 mm below the top-edge port squares, or the top-edge port labels sit outside the part. Side port labels never share a row with the name block. Leave `lx` and `ly` empty (`{}{}`) to put a port label outside the part beside its square. A port label never sits on an end head.
10. **Heads:** every item flow is `\sysmlflow` (filled triangle). `directed` is only for a directed connection that carries no item. The tip touches the port outer face and the head stays outside.
11. **Pack:** size each part to its ports and labels; pull the next part up to the 6 mm gap instead of stretching a box.
12. **Proof before assemble:** render this sheet alone, remeter, run the **visual fail list** (title-band collision, text overlap, near-edge / clipped labels, crowding, text-over-plot), then **keep | simplify | split | reject**. Then assemble. Do not first-shot Sheet A and Sheet B into one unproven `fulldoc`. Soft-pass “TeX compiled = ship” stays forbidden. Still budget re-renders.

Soft-pass “macros correct means sheet good” is false. Sufficiency is a human scan, not a TeX compile.

## When to use

A SysML v2 interconnection diagram: parts, ports and the connectors between those ports. Draw it with the sysml-tikz macros. The worker preamble loads sysml-tikz. Do not send a preamble.

## templateId and body syntax

templateId is `sysml`. bodySyntax is a LaTeX picture body, no preamble. Do not send Markdown, `\documentclass` or `\usepackage`. Sending Markdown to this templateId is a TeX error.

The body is one `sysmlfigure` containing one `sysmlcanvas`. Coordinates are millimetres, and y grows downward. Macros, as defined by sysml-tikz:

- `\sysmlpart{name}{x}{y}{width}{height}` draws a rounded usage box.
- `\sysmllabel[keyword]{x}{y}{\sysmlguillemets{part}}`, `\sysmllabel[name]{x}{y}{...}` and `\sysmllabel[type]{x}{y}{...}` place the three label lines. Anchors are north.
- `\sysmlport{name}{cx}{cy}{SIDE}{lx}{ly}{label}{direction}` draws a 3.2 mm square centred on `(cx,cy)`. `SIDE` is `EAST`, `WEST`, `NORTH` or `SOUTH`. `direction` is `in`, `out` or `inout`. The direction arrow is drawn inside the square. `\sysmlport[conjugated]{...}` or a leading `~` in the label flips `in` and `out` on that inner arrow and shows `~` in the label. `inout` stays bidirectional. `(lx,ly)` is the north-west corner of the label. Empty `lx` and `ly` (`{}{}`) put the label outside the part beside the square: NORTH above-right, SOUTH below-right, EAST above-right, WEST above-left, clear of the line and of an end head.
- `\sysmlconnection[from=PdMon.pump.outlet, to=PdMon.motor.inlet]{name}{(x1,y1) -- (x2,y2)}` draws a solid connector with no arrowhead. Each end sits on a port's outer edge. `from` and `to` name the ports. Port direction does not choose an arrowhead. The two-argument form `\sysmlconnection{name}{path}` is the same plain line. The name argument is not drawn. `directed` (or `directed=true`) draws an open stick arrowhead at the `to` end, including when the path is written the other way. `flow=forward` or `flow=reverse`, with optional `item=`, draws a filled triangle at the arc-length midpoint of the whole path. The triangle follows the segment it lands on. The item text stays upright and is centred on the middle of the `from` half, clear of the triangle. On a horizontal run it sits on the line. On a vertical run it sits to the right of the line. A path written the other way keeps that text in the same place. An end arrowhead follows the final segment. If that item box cannot sit clear of both ports, the render is an error.
- `\sysmlflow[from=PdMon.motor.outlet, to=PdMon.ctrl.inlet, item=液位]{name}{(x1,y1) -- (x2,y2)}` draws a solid line with a filled triangle pointing from `from` to `to`. The triangle sits at the target. `at=mid` places the triangle at the arc-length midpoint of the whole path. The triangle follows that segment. Without `at=mid` the item text is centred on the arc-length midpoint. With `at=mid` the item text is centred on the middle of the `from` half, clear of the triangle. On a horizontal run the text sits on the line, and the white fill is only the label box. On a vertical run the text stays upright, to the right of the line. A path written the other way keeps the text in the same place. A reversed path still points the triangle toward the `to` port. The name argument is not drawn. If the item box cannot sit clear of both ports, the render is an error. Do not glue the word to one end.
- `\sysmlbinding[from=PdMon.pump.bind, to=PdMon.motor.bind]{name}{path}` draws a solid line with an upright `=` at the arc-length midpoint of the whole path and no arrowhead. The glyph is not rotated. The stroke is gapped around it. It is not dashed.
- `\sysmlinterface` is a solid line with an optional `\sysmlguillemets{interface}` label and no arrowhead. `\sysmlsuccessionflow` is dashed with a filled triangle at the target. `\sysmlmessage` is solid with a hollow closed triangle at the target. `\sysmlallocation` is solid with an open stick arrowhead at the target (the same two-stroke head as `directed`, not a closed triangle) and `\sysmlguillemets{allocate}`. Those labels are centred on the arc-length midpoint. On a horizontal run they sit on the line. On a vertical run they stay upright, to the right of the line. A label shifts along the path rather than cover a port label, a port square, a part box, or other text. Only the triangles and the open stick follow the segment.

## Fence usage

For HTML or DOCX, put this picture in a tikz fence under document-shell. The fence class is `tikz`, with caption and alt. zh-TW labels in that fence need the Noto font workaround until the fence preamble loads xeCJK: the first fence line is `\font\zh="Noto Sans CJK TC" at 9pt` and the label is `{\zh 幫浦}`. On templateId `sysml` (PDF) CJK renders directly.

## Output formats

This templateId is PDF. HTML and DOCX are wrapped by the gate as a document-shell tikz fence; the tool result says so.

## Kind notes

The port square runs from 1.6 mm left of the centre to 1.6 mm right of it (and the same on y). A connector stops on that outer face. In the example the east port is centred at x = 26, so the connector starts at x = 27.6. The west port is centred at x = 58, so the connector ends at x = 56.4. The connector does not enter either square.

Human sheets show a title (optional revision id). Hide `view`, `overrides`, `depth` and `body size` from the printed face. Text is not set below 7 pt. Port labels get a reserved gutter and must not intersect a box, a line, a symbol, or another label. A flow item that cannot sit clear of both ports is a render error, not a glued mark and not a shrink. The worker checks the finished picture: text on text (1 mm gutter on one row), text on a port square, text across a part outline, text on another line or an end head, and a line into a port square fail the render with one line, `layout_overlap: <a> on <b> (+N more)` or `line_into_port: line <name> into port <id>`.

The template owns A4 page geometry. Do not send `\pdfpagewidth`, `\pdfpageheight`, `\usepackage{geometry}` or a preamble. A `sysmlcanvas` wider than the portrait text line (about 12 cm, about 345 pt) at the declared body size is landscape A4 at that declared type size. The printed face stays title and optional revision id. 7 pt is an absolute floor, not a fit target: the worker does not scale type down to 7 pt to force portrait, and it does not shrink the millimetre unit (that leaves names outside their boxes). If the canvas still will not fit on landscape A4 at the declared size, the render is an error. Split the sheet. Portrait sheets that already fit at the declared size stay portrait. The worker wraps the `sysmlfigure` header with the canvas after that page-size decision. Do not load `needspace`. Compile success with crushed or colliding text is still FAIL.

A later path will generate this TikZ from a SysMLEdge model at a revision. That generator is separate work. This playbook does not build it. Send the picture body above.

## Common failures and fixes

An arrow drawn as a separate path across the square leaves the port. Put `in`, `out` or `inout` on `\sysmlport` instead. A line that uses the port centre runs through the square. Stop it on the outer edge, so the arrowhead tip touches that edge and the head stays outside. A connection does not grow an arrowhead from the port directions. Use `\sysmlflow` for a filled triangle and `directed` for an open stick at `to`. A flow item that cannot sit clear of both ports is a render error; lengthen the connector or shorten the item. A missing `sysmlcanvas` ignores the millimetre, y-down coordinates. `layout_overlap: keyword at x,y on label of P.port`: move the stereotype below the top-edge port row, or leave that port's `lx` and `ly` empty. `layout_overlap: type T on label of P.port`: move the side label outside or grow the part. `line_into_port`: stop the line on the outer face.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. No graphdrawing and no Lua. A failure is a tool result: fix it and resend, and budget re-renders.
