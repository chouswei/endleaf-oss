---
topic: teaching
titleEn: zh-TW teaching materials
resourceUri: endleaf://guide/teaching
promptName: render-teaching
promptTitleEn: Render zh-TW teaching materials
order: 8
---

# en

Use this for Traditional Chinese class materials: a worksheet, a handout, a lesson plan, or a short assessment. Send `templateId` `document-shell` and `outputFormat` `pdf`. The body is Markdown. Do not send a preamble or `\documentclass`. Fenced figures inherit shared Composition: 7 pt floor, no text on geometry, one intent per fence.

### Document types

A worksheet (學習單) has a student header, numbered questions with room to write, a data table, and a checkbox list.

```markdown
# 學習單

姓名＿＿＿　班級＿＿＿　座號＿＿

## 問題

1. 一質點由靜止出發。在下方留白作答。

## 紀錄

| 次數 | 時間 | 位移 |
| --- | --- | --- |
| 1 |  |  |

## 自查

- ☐ 單位已寫出
- ☐ 有效數字已核對
```

A handout (講義) has the key concepts, each formula with the condition under which it holds, and a worked-example outline.

```markdown
# 講義

## 概念

- 力會改變速度

## 公式

$$ \vec{F} = m\vec{a} $$

條件：質量不隨時間改變。

加速度可用 `\qty{9.8}{\metre\per\second\squared}`。

## 例題

1. 寫出已知。
2. 選用公式。
3. 代入數值與單位。
4. 寫出答案。
```

A lesson plan (教案) has a timed activity-flow table.

```markdown
# 教案

| 分鐘 | 活動 | 教具 |
| --- | --- | --- |
| 0–5 | 引起動機 | 圖 |
| 5–20 | 操作 | 尺 |
| 20–30 | 討論 | 學習單 |
```

A short assessment has questions and a rubric table.

```markdown
# 評量

1. 求合力的大小。

## 評分規準

| 項目 | 配分 |
| --- | --- |
| 公式 | 2 |
| 單位 | 1 |
| 答案 | 2 |
```

### Physics figures

circuitikz and siunitx are in the v1 package set and are loaded for every render. Put a mechanics or optics picture in a tikz fence inside the Markdown. The info string is `{.tikz caption="Free body" alt="A block with two force arrows"}`. A circuit picture may use that fence, or `templateId` `circuits` with the picture body alone. The fence class is `tikz`. Vectors use `\vec`. Inline math is `$...$` and a one-line display is `$$...$$`. amsmath is not loaded: do not send `align`, `gather`, or `\begin{equation}`.

### Printing

The print target is A4 portrait, margins of about 25 mm for photocopying, a 12 pt body, and Traditional Chinese. The service page is A4 `article` with xeCJK and Noto Sans CJK TC. It does not pass `12pt`, photocopy margins, or an answer-key switch. Do not send `\documentclass`, `geometry`, or `\usepackage` to add them. That is a template gap for 12 pt and margins. This guide does not change the render service.

Write full-width punctuation in Chinese prose. xeCJK breaks Chinese lines, and `PunctStyle=quanjiao` keeps that punctuation full width. Write Traditional characters only. The font is Noto Sans CJK TC, so the PDF does not switch to a Simplified Chinese font.

A teacher version and a student version come from one Markdown source. The student render omits the answer section. The teacher render keeps it. Send two `renderDocument` calls. The full documents in the example section use `\ifshowanswers` to show the print target. The service template has no such switch.

### From Markdown to Endleaf

- `#`, `##` and `###` become headings.
- `1.` becomes a numbered question. A blank line under the item is the answer space.
- A Markdown table becomes a table. Keep it short.
- A checkbox is the character ☐ in a list item. Do not add a package for it.
- A blank is a run of ＿.
- A formula is `$...$` or `$$...$$`. `\vec` is available. `\qty` is available because siunitx is loaded. amsmath is not loaded.
- Stay within {{maxInputKiB}} KiB. Split a long pack into several renders: one worksheet, one handout, one lesson plan, one assessment. Do not join them with `\input` or `\include`.

### Slides

Slides are out of scope. The document class is `article`. Beamer is not a v1 class. Do not send a slide deck.

# example

```latex document
% teaching: worksheet
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK TC}
\xeCJKsetup{PunctStyle=quanjiao}
\usepackage{booktabs}
\usepackage{siunitx}
\setlength{\textwidth}{160mm}
\setlength{\textheight}{247mm}
\setlength{\oddsidemargin}{0pt}
\setlength{\evensidemargin}{0pt}
\setlength{\topmargin}{0pt}
\setlength{\headheight}{0pt}
\setlength{\headsep}{0pt}
\newif\ifshowanswers
\showanswerstrue
\begin{document}
\begin{center}學習單\end{center}
姓名＿＿＿　班級＿＿＿　座號＿＿

\begin{enumerate}
\item 一質點由靜止出發。在下方留白作答。

\vspace{16mm}
\ifshowanswers 答案：寫出已知與單位。\fi
\end{enumerate}

\begin{tabular}{ccc}
\toprule
次數 & 時間 & 位移 \\
\midrule
1 & \qty{0.5}{\second} & \qty{1.2}{\metre} \\
\bottomrule
\end{tabular}

\begin{itemize}
\item ☐ 單位已寫出
\item ☐ 有效數字已核對
\end{itemize}
\end{document}
```

```latex document
% teaching: handout
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK TC}
\xeCJKsetup{PunctStyle=quanjiao}
\usepackage{siunitx}
\setlength{\textwidth}{160mm}
\setlength{\textheight}{247mm}
\setlength{\oddsidemargin}{0pt}
\setlength{\evensidemargin}{0pt}
\setlength{\topmargin}{0pt}
\setlength{\headheight}{0pt}
\setlength{\headsep}{0pt}
\begin{document}
\begin{center}講義\end{center}

力會改變速度。

\[ \vec{F} = m\vec{a} \]

條件：質量不隨時間改變。加速度 \qty{9.8}{\metre\per\second\squared}。

\begin{enumerate}
\item 寫出已知。
\item 選用公式。
\item 代入數值與單位。
\item 寫出答案。
\end{enumerate}
\end{document}
```

```latex document
% teaching: lesson-plan
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK TC}
\xeCJKsetup{PunctStyle=quanjiao}
\usepackage{booktabs}
\setlength{\textwidth}{160mm}
\setlength{\textheight}{247mm}
\setlength{\oddsidemargin}{0pt}
\setlength{\evensidemargin}{0pt}
\setlength{\topmargin}{0pt}
\setlength{\headheight}{0pt}
\setlength{\headsep}{0pt}
\begin{document}
\begin{center}教案\end{center}

\begin{tabular}{lll}
\toprule
分鐘 & 活動 & 教具 \\
\midrule
0--5 & 引起動機 & 圖 \\
5--20 & 操作 & 尺 \\
20--30 & 討論 & 學習單 \\
\bottomrule
\end{tabular}
\end{document}
```

```latex document
% teaching: quiz
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK TC}
\xeCJKsetup{PunctStyle=quanjiao}
\usepackage{booktabs}
\setlength{\textwidth}{160mm}
\setlength{\textheight}{247mm}
\setlength{\oddsidemargin}{0pt}
\setlength{\evensidemargin}{0pt}
\setlength{\topmargin}{0pt}
\setlength{\headheight}{0pt}
\setlength{\headsep}{0pt}
\newif\ifshowanswers
\showanswerstrue
\begin{document}
\begin{center}評量\end{center}

\begin{enumerate}
\item 求合力的大小。

\vspace{12mm}
\ifshowanswers 答案：寫出向量和與單位。\fi
\end{enumerate}

\begin{tabular}{lr}
\toprule
項目 & 配分 \\
\midrule
公式 & 2 \\
單位 & 1 \\
答案 & 2 \\
\bottomrule
\end{tabular}
\end{document}
```

```latex example
% teaching: free-body
\begin{tikzpicture}[>=stealth]
  \draw[fill=black!5] (0,0) rectangle (1.2,1.2);
  \draw[->, thick] (0.6,1.2) -- (0.6,2.4) node[above] {$\vec{N}$};
  \draw[->, thick] (0.6,0) -- (0.6,-1.2) node[below] {$\vec{W}$};
\end{tikzpicture}
```

```latex example
% teaching: projectile
\begin{tikzpicture}[>=stealth]
  \draw[->] (0,0) -- (4.4,0) node[right] {$x$};
  \draw[->] (0,0) -- (0,2.6) node[above] {$y$};
  \draw[thick] (0,0) parabola bend (2,2) (4,0);
\end{tikzpicture}
```

```latex example
% teaching: ray
\begin{tikzpicture}[>=stealth]
  \draw (2,-1.3) -- (2,1.3);
  \draw[->] (0,0.45) -- (2,0.45) -- (3.8,-0.7);
  \draw[->] (0,-0.45) -- (2,-0.45) -- (3.8,0.7);
  \node[left] at (0,0) {物};
  \node[right] at (3.8,0) {像};
\end{tikzpicture}
```

```latex example
% teaching: circuit
\begin{circuitikz}
  \draw (0,0) to[V, v=$V$] (0,2)
        to[R, l=$R$] (3,2)
        to[lamp] (3,0) -- (0,0);
\end{circuitikz}
```
