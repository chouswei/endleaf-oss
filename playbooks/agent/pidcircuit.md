---
topic: pidcircuit
titleEn: PIDcircuitTikZ
resourceUri: endleaf://guide/pidcircuit
promptName: render-pid
promptTitleEn: Render a P&ID
order: 4
---

# en

Render a P&ID with `templateId` `pidcircuit` and `outputFormat` `pdf`. The body is the picture below. Do not send a preamble or `\documentclass`. The picture uses TikZ `circuit pid ISO14617`.

Keep labels at `\small`. Place instruments off the line and use a dashed link.

# example

```latex example
\begin{tikzpicture}[circuit pid ISO14617, every info/.style={font=\small}]
  \draw (0,0) to[valve={info=V-101}] (2.5,0)
              to[pump={info=P-101}] (5,0)
              to[valve={info=V-102}] (7.5,0);
  \draw[flow path, pos=0.2] (0,0) -- (2.5,0);
  \draw[flow path, pos=0.8] (5,0) -- (7.5,0);
  \node[measurement device={info=FI}] (fi) at (5,1.5) {};
  \draw[dashed] (fi.south) -- (5,0.35);
\end{tikzpicture}
```
