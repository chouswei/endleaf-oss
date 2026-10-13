---
topic: tikz
titleEn: TikZ
resourceUri: endleaf://guide/tikz
promptName: render-tikz
promptTitleEn: Render a TikZ diagram
order: 3
---

# en

Render a TikZ diagram with `templateId` `document-shell` and `outputFormat` `pdf`. The body is Markdown. Put the picture in one tikz fence whose info string is `{.tikz caption="Box" alt="A box and an arrow"}`. Do not send a preamble or `\documentclass`.

Use `\small` for labels. Do not put `scale=` on text. The picture below is the fence body.

# example

```latex example
\begin{tikzpicture}
  \draw[->] (0,0) -- (2,0);
  \node[draw] (box) at (1,1) {box};
  \draw[->] (box) -- (1,0);
\end{tikzpicture}
```
