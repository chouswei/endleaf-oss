---
topic: circuits
titleEn: Circuits
resourceUri: endleaf://guide/circuits
promptName: render-circuit
promptTitleEn: Render a circuit
order: 5
---

# en

Render a circuit with `templateId` `circuits` and `outputFormat` `pdf`. The body is the picture below. Do not send a preamble or `\documentclass`. The picture uses circuitikz.

# example

```latex example
\begin{circuitikz}
  \draw (0,0) to[V, v=$V$] (0,2)
        to[R, l=$R$] (3,2)
        to[C, l=$C$] (3,0) -- (0,0);
\end{circuitikz}
```
