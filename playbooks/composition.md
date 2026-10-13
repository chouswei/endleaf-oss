Composition law overrides macro tips.

Shared bar for every Endleaf kind. Kind macros never outrank this section. Sufficiency is an arm's-length human scan, not a TeX compile. Soft-pass “macros correct means sheet good” is false. Soft-pass “TeX compiled = ship” is forbidden.

**Size, position and typography are first-class Composition law, equal rank with one intent per sheet.** They are not optional polish. Compile success with crushed or colliding text is still FAIL. Frequent font or style changes are uncomfortable to read and are a layout failure.

### Size (first-class)

7 pt is an absolute floor for any human-facing label or body type on a figure. Never shrink-to-fit under that floor. If the picture will not fit at 7 pt, split the picture, the page, or the series, or turn that page landscape when the kind supports it. Refuse to ship. Tighter kerning, `\resizebox`, `scale=` on text, and fitting that drops type below 7 pt are layout failures.

#### Size estimation (pre-layout)

Agents shall pre-estimate label width and height before placing, not only know the 7 pt fail line. This is a heuristic, not a TeX measure and not a PDF metrics engine.

At figure label size S pt (S ≥ 7):

- Latin and mono ≈ 0.5·S pt per glyph width
- CJK / zh-TW ≈ 1.0·S pt per character
- Height ≈ S pt plus a small leading

Convert with 1 mm ≈ 2.845 pt, or stay in millimetres when the canvas uses mm (`sysmlcanvas`). Reserve gutters. Do not place if the estimated box intersects geometry or another label. If the box will not fit at ≥ 7 pt, split, use landscape, or refuse. Never shrink-to-fit.

**Proportional Heros:** 0.50–0.55·S per character is a **mean** only. Heros is proportional, so tokens such as `vWire`, `EiTungstenWirePowerDriver`, and `«part»` run wide while `i` / `l` run narrow. Size the box for the **widest token** on that line, or shorten canvas tokens and move long paths under the figure. Do not size from average character count alone.

**Three-line part compartment:** budget stereotype + name + type as **three** lines (≈ 3·S + leading), never one-line box height. A single label is still ≈ S pt plus leading.

Body prose on `fulldoc` and `document-shell` stays 10 pt Pagella. Figure labels use Heros. Mono uses Cursor. Estimation uses the face’s role; the 0.5 em / 1 em rule is a mean only.

### Position (first-class)

No text intersecting a box, a line, a symbol, or another label. Port and symbol tags get a reserved gutter. Labels stay clear of dimensions and arrows. Fail = re-layout. Do not kern tighter to hide a collision. Fail = do not ship.

**Port pitch:** never assume a fixed 10 mm. Pitch ≥ estimated label width + reserved gutter; else stagger sides or externalize labels. Five-letter names at tight pitch = FAIL.

**Elbow / connector routing:** reserve a **label rectangle** before routing; never route a line through glyph bounds. Orthogonal fork/join: name the midpoints and route with `|-` / `-|`. Do not freehand a path that cuts labels.

**Relative placement:** prefer the `positioning` library (`right=of`) over deprecated `right of=` or `\tikzstyle`. Sibling boxes in a row shall share equal minimum width and height, sized for the **widest** label in that row, so one fat node does not skew the chain.

**Place then connect:** place blocks first, then draw edges. Short signal labels sit on the connector (`node {$e$}`), not as caption paragraphs inside boxes.

### Tables and equations

fulldoc: a wide table gets fixed `p{3cm}` columns that wrap, fewer columns, or two tables; never `\resizebox` or a scaled table. A long display equation uses `multline`, or `split` inside `equation`; never shrink math. document-shell pipe tables wrap when the dash row is wider than the text.

### One intent (first-class)

One intent per figure or sheet. Split if crowded. Do not stuff several intents onto one canvas.

### Landscape (prefer over shrink)

The template owns page geometry. Do not send `\pdfpagewidth`, `\pdfpageheight`, `\usepackage{geometry}`, or a preamble.

If a sysml canvas is wider than the portrait A4 text line at the declared body size, that page is landscape A4 and type stays at the declared size. Do not scale type down to the 7 pt floor to force portrait. 7 pt is an absolute floor, not a fit target. If the canvas still will not fit on landscape A4 at the declared size, the render is an error. Split the sheet. Do not shrink the coordinate unit to cram names.

Portrait sheets that already fit at the declared size stay portrait. Do not landscape everything.

Prefer landscape over shrink-to-fit or overlapping labels. Prefer canvas `scale≈1` (or equivalent fixed geometry) over shrinking text to fit. Never `\resizebox{\textwidth}{!}{...}` a `tikzpicture` (or equivalent shrink-to-fit). Still one intent per sheet, 7 pt floor, and no text on geometry. If the kind cannot rotate that page, split the picture.

### Typography (first-class)

One type stack for every human-facing PDF. The worker owns it in the template preamble. Callers do not send `fontspec`, `\setmainfont`, or a preamble.

- Body and prose: TeX Gyre Pagella (`tgpagella`), serif. Not Computer Modern and not Latin Modern Roman. Body is 10 pt on `fulldoc` and `document-shell`.
- Headings: Pagella only, at the article size scale. Do not switch to an unrelated display face.
- Sans and diagram UI labels: TeX Gyre Heros (`tgheros`). Figure labels use Heros on every kind. Do not mix a random face per kind.
- Mono, canvas tokens, and code-like ids: TeX Gyre Cursor (`tgcursor`). One mono face. Not Inconsolata.
- Size floor on figures stays 7 pt absolute.
- zh-TW/CJK in the caller's source still goes through xeCJK, with one CJK companion: Noto Sans CJK TC (the bundled Traditional glyphs). Do not invent a bilingual playbook. Served prompts stay English only.

### KEEP

- Human readability first.
- One type stack: Pagella body, Heros figure labels, Cursor mono, Noto Sans CJK TC.
- 7 pt absolute floor; labels stay off geometry.
- Landscape page over shrink-to-fit when the kind supports it.
- No Mermaid or D2. This render path is TikZ only.
- No preamble from the caller. The worker owns the template.
- Honour the cap budget and the forbidden sandbox.
- zh-TW with xeCJK. Traditional characters only.
- Kind split: document-shell is Markdown; picture kinds are a LaTeX picture body; fulldoc is a LaTeX document body.
- Proof before assemble: prove each picture-kind sheet individually (render it alone), then assemble proven figures.
- Size for the **widest token**; Heros 0.50–0.55 em is a mean only. Part boxes are three lines.
- After each proved sheet, check the visual fail list, then **keep | simplify | split | reject**.
- Prefer canvas `scale≈1` (fixed geometry) over shrinking text to fit.
- Honest unsupported: if a package or glyph path is not on the Endleaf worker, refuse or simplify. Do not emit pseudo-TikZ that looks correct in preview and fails at render.
- Prefer `positioning` (`right=of`). Sibling boxes share equal minimum width/height, sized for the widest label. Place blocks first, then edges; short signal labels on the connector (`node {$e$}`).

### KILL (refuse as a layout failure)

- Ship when only the compile succeeds.
- Computer Modern or Latin Modern Roman as the default body.
- Switching headings to an unrelated display face, or mixing a random face per kind.
- Compile success with crushed or colliding text (still FAIL).
- Shrink-to-fit that takes type under 7 pt.
- Text on geometry: no text intersecting a box, line, symbol, or other label.
- Meta or debug chrome on the human face (view, overrides, depth, body size, worker diagnostics). Title and optional revision id stay.
- RFC decoration on the canvas (`CANDIDATE`, `MAY`, `SHOULD`, `TBD`).
- One figure stuffed with several intents.
- Table cells that dump usage, items, ends and binds as multi-line soup.
- Invent many unproven figures in one first `fulldoc` or document-shell shot.
- Size from average character count alone, a one-line part box, a fixed 10 mm port pitch, or an elbow through glyph bounds.
- Ship a sheet that hits the visual fail list (title-band collision, text overlap, near-edge / clipped labels, crowding, text-over-plot).
- Shrink text to fit a crowded canvas (prefer `scale≈1`).
- Fake an unavailable package or glyph path with pseudo-TikZ.
- `\resizebox{\textwidth}{!}{...}` wrapping a `tikzpicture` (or equivalent shrink-to-fit).
- Deprecated `right of=` or `\tikzstyle`. Freehand paths that cut labels instead of named midpoints with `|-` / `-|`.
- Caption paragraphs inside boxes, or one fat sibling that skews a row.

### CORRECT

1. One intent per figure or sheet. Split if crowded.
2. 7 pt absolute floor. Pre-estimate the box (Latin/mono ≈ 0.5·S is a **mean**; CJK ≈ 1.0·S) for the **widest token** on that line before placing. Part compartments are **three** lines (stereotype + name + type, ≈ 3·S + leading). Do not shrink labels to fit. Split the picture, the page, or the series, or use a landscape page when the kind supports it.
3. No text intersecting a box, line, symbol, or other label. Reserved gutters for tags. Port pitch ≥ estimated label width + gutter (never a fixed 10 mm). Reserve a **label rectangle** before routing elbows. Fail = re-layout, not tighter kerning.
4. Short tokens on the canvas. Detail goes under the figure (caption, legend, or a clean table).
5. Tables: one idea per cell. Connection maps are two columns at most and must be scannable.
6. Arm's-length proof: every label is legible, no text on geometry, one layer or intent only. Fail = do not ship.
7. The served payload must include these rules. Agents only get what the gate serves.
8. Soft-pass “TeX compiled = ship” is forbidden. Crushed or colliding text is FAIL even when TeX exits 0.
9. One type stack: Pagella body (10 pt on fulldoc and document-shell), Heros figure labels, Cursor mono, Noto Sans CJK TC. Headings stay on the Pagella scale.
10. **Proof before assemble.** Prove each picture-kind sheet individually: render that sheet alone against live Endleaf, remeter this proof bar, then assemble those proven figures into `fulldoc` or document-shell fences. Especially SysML Sheet A and Sheet B IBDs. This is the CORRECT workflow, not optional advice. Still budget re-renders.
11. **Visual fail list, then keep | simplify | split | reject.** After render and before assemble, check the list below. Then decide the design outcome.

### Proof before assemble

Prove each picture-kind sheet **individually**. Render that sheet **alone** against live Endleaf (especially SysML Sheet A / Sheet B IBDs). Pass this proof bar: arm's-length ≥ 7 pt, no text on geometry, one layer. Run the **visual fail list**. Decide **keep | simplify | split | reject**. **Then** assemble those proven figures into `fulldoc` or document-shell fences. Do not invent many unproven figures in one first shot. Soft-pass “TeX compiled = ship” stays forbidden. Still budget re-renders.

Summary suffix `warn overfull=N undefinedRef=N undefinedCite=N` (only when one is above 0): overfull is text past the margin; undefinedRef or undefinedCite is a key with no `\label` or `\bibitem`. Fix and re-render; never ship `??` or `[?]`.

Judge rendered pages from the `renderDocument` MCP result: the compact summary plus the saved file (`retentionMode=none`). Never by reading PDF bytes in context. Do not use local XeLaTeX or a host sty as the proof. Some clients load blobs into context. With the local client, pass `writeTo` so the PDF goes to disk and only the summary comes back. Plain remote clients get the embedded file; save it. A repo-saved `.pdf` is an editor copy of that file.

### Visual fail list

On each proved picture sheet (after render, before assemble), FAIL if any of these is true:

- **title-band collision** — title, header or band covers labels or geometry
- **text overlap** — two labels share glyph bounds
- **near-edge / clipped labels** — a label is cut by the canvas or page edge
- **crowding** — gutters collapse; the arm's-length scan cannot name each token
- **text-over-plot** — label glyphs sit on strokes, lines or connectors

### Design outcome

After that inspection, decide exactly one: **keep** (assemble this sheet), **simplify** (same intent, fewer or shorter tokens), **split** (new sheet; layer-split KILL stays), or **reject** (do not ship). Split is a new sheet, not a denser canvas.

