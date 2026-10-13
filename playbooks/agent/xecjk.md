---
topic: xecjk
titleEn: xeCJK (zh-TW)
resourceUri: endleaf://guide/xecjk
promptName: render-zh-tw
promptTitleEn: Render a zh-TW document
order: 6
---

# en

Render a zh-TW document with `templateId` `document-shell` and `outputFormat` `pdf`. The body is Markdown and may contain Traditional Chinese directly. The service sets XeLaTeX, xeCJK and Noto CJK TC. Do not send a preamble or `\documentclass`.

```markdown
# 幫浦

一臺幫浦（Pump）。
```

A Chinese label inside a TikZ picture uses the picture below as the fence body. Write Traditional Chinese only.

# example

```latex example
\begin{tikzpicture}
  \node[draw, font=\small] {幫浦};
\end{tikzpicture}
```
