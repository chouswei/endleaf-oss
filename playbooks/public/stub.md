# en

Endleaf renders Markdown or LaTeX (with TikZ, circuits, P&ID, plots, chemistry and zh-TW text) to PDF, HTML or DOCX through a keyed MCP endpoint, for AI agents and tools. It is a service of InkMirage. For help, email [support@inkmirage.xyz](mailto:support@inkmirage.xyz). Paid plans are not available yet.

## What it renders

- XeLaTeX, with xeCJK and Noto CJK TC for zh-TW
- Markdown prose with fenced figures, or a full LaTeX document
- TikZ, P&ID (PIDcircuitTikZ), circuits (circuitikz), plots (pgfplots, 2D and 3D), chemistry (chemfig, mhchem), Gantt (pgfgantt), floor plans (tikz-dimline, tikzscale) and SysML interconnection diagrams (sysml-tikz)
- tikz-cd, forest, automata, mind maps, tikz-timing and bytefield, on their own or inside a full document
- siunitx, and the TikZ libraries shapes, arrows.meta, positioning and calc
- PDF, HTML and DOCX (in HTML and DOCX, diagrams appear as images)
- A4, Letter or A3, portrait or landscape; a wide figure can go on its own landscape page
- `\cite` resolves to a number such as [1]
- TeX warning counts, and for a failed render the first error's cause with a Fix line
- A fit report for each picture: how far it overhangs, the scale that would fit, and its smallest text against the 7 pt floor
- A SysML diagram with overlapping parts is refused, with the reason
- Upload a source once with `uploadSource`, then render it by reference

Inline sources are not kept. Uploaded sources are deleted after 24 hours.

## Documents

A document is kept until you delete it. It uses two languages: the document grammar holds its structure and every change, and LaTeX holds the text, math and pictures inside each part (a figure body is a LaTeX picture, such as TikZ). Endleaf writes the headings, floats, captions and layout.

- Save a document from a LaTeX body or a starter template. Endleaf splits it into parts: title, sections, paragraphs, figures, tables, equations and references.
- Edit it with small changes. Each change is checked and shown as a diff first, and becomes a new revision when applied.
- Read a page-by-page view of the last render: what is on each page, how full it is, and what runs past the text width.
- Compare any two revisions.
- Render any revision to PDF.
- Delete a document with all its revisions.

## Playbooks

Fifteen playbooks, one per kind.

### documentShell
Markdown prose with fenced figures.

### pidcircuit
ISO 14617 P&ID drawings with PIDcircuitTikZ.

### circuits
circuitikz schematics and siunitx quantities.

### plots
2D and 3D plots with pgfplots.

### chemistry
chemfig structures and mhchem formulae.

### gantt
Gantt charts with pgfgantt.

### floorplan
Floor plans with tikz-dimline and tikzscale.

### sysml
SysML interconnection diagrams with sysml-tikz.

### fulldoc
One PDF with title, sections, prose and mixed figures.

### tikzcd
Commutative diagrams with tikz-cd.

### forest
Trees, including syntax trees and directory trees.

### automata
Finite automata and state machines.

### mindmap
Mind maps with the TikZ mindmap library.

### tikztiming
Digital timing diagrams with tikz-timing.

### bytefield
Protocol headers and bit or byte field diagrams.

A documentShell TikZ picture body can use tikz-cd, forest, automata, mindmap, tikz-timing and bytefield with no new worker package. Named playbooks and documentShell both remain valid. tikz-feynman and tikz-3dplot are not playbooks.

# zh-TW

蝶頁經由需金鑰的 MCP 端點，把 Markdown 或 LaTeX（含 TikZ、電路、P&ID、圖表、化學與繁體中文）編成 PDF、HTML 或 DOCX，供 AI 代理與工具使用。蝶頁為 衍跡 InkMirage 之服務。如需協助，請寫信至 [support@inkmirage.xyz](mailto:support@inkmirage.xyz)。付費方案尚未開放。

## 可編排內容

- XeLaTeX，繁體中文使用 xeCJK 與 Noto CJK TC
- Markdown 內文搭配程式碼區塊中的圖，或完整的 LaTeX 文件
- TikZ、P&ID（PIDcircuitTikZ）、電路（circuitikz）、圖表（pgfplots，含 2D 與 3D）、化學（chemfig、mhchem）、甘特圖（pgfgantt）、平面圖（tikz-dimline、tikzscale）與 SysML 互連圖（sysml-tikz）
- tikz-cd、forest、automata、心智圖、tikz-timing 與 bytefield，可單獨使用，也可放進完整文件
- siunitx，以及 TikZ 程式庫 shapes、arrows.meta、positioning、calc
- PDF、HTML 與 DOCX（在 HTML 與 DOCX 中，圖以影像呈現）
- A4、Letter 或 A3，直式或橫式；過寬的圖可單獨排在一張橫式頁面
- `\cite` 會編成 [1] 這樣的編號
- TeX 警告數；編譯失敗時，列出第一個錯誤的原因與一行修正建議（Fix）
- 每張圖的版面檢查：超出版心多少、可容納的縮放比例，以及最小字級與 7 pt 下限的比較
- SysML 圖若有元件重疊，會拒絕編譯並說明原因
- 先用 `uploadSource` 上傳原始檔，再以參照編譯

直接送出的原始檔不會保留。上傳的原始檔在 24 小時後刪除。

## 文件

文件會保存到你刪除為止。文件使用兩種語言：文件語法負責結構與每一次修改，LaTeX 負責各部分裡的文字、數學式與圖（圖的內容是 TikZ 等 LaTeX 圖）。標題、浮動圖表、圖說與版面由蝶頁產生。

- 從 LaTeX 內文或起始範本建立文件。蝶頁會把它拆成各個部分：標題、章節、段落、圖、表格、方程式與參考文獻。
- 以小幅修改編輯文件。每次修改都會先經過檢查並以差異呈現，套用後成為新的修訂版。
- 查看上次編排的逐頁版面：每頁放了哪些內容、版面多滿，以及哪些內容超出版心寬度。
- 比較任兩個修訂版。
- 將任一修訂版編成 PDF。
- 刪除文件及其所有修訂版。

## 教戰手冊

十五種教戰手冊，每種一本。

### documentShell
Markdown 內文，圖放在程式碼區塊中。

### pidcircuit
以 PIDcircuitTikZ 畫 ISO 14617 P&ID。

### circuits
circuitikz 電路圖與 siunitx 量值。

### plots
以 pgfplots 畫 2D 與 3D 圖表。

### chemistry
chemfig 結構與 mhchem 化學式。

### gantt
以 pgfgantt 畫甘特圖。

### floorplan
以 tikz-dimline 與 tikzscale 畫平面圖。

### sysml
以 sysml-tikz 畫 SysML 互連圖。

### fulldoc
一份含標題、章節、內文與混用圖的 PDF。

### tikzcd
以 tikz-cd 畫交換圖。

### forest
以 forest 畫樹，含句法樹與目錄樹。

### automata
有限自動機與狀態機。

### mindmap
以 TikZ mindmap 畫心智圖。

### tikztiming
以 tikz-timing 畫數位時序圖。

### bytefield
協定標頭與位元或位元組欄位圖。

已安裝的靜默套件可在 documentShell 的 TikZ 圖內使用，不必新增工作節點套件。具名教戰手冊與 documentShell 對 tikz-cd、forest、automata、mindmap、tikz-timing、bytefield 都有效。tikz-feynman 與 tikz-3dplot 不是教戰手冊。
