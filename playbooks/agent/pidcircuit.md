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

Keep labels at `\small`. Use ISO 14617 keys only. Lines run port to port: process solid, instrument dashed, mechanical dash-dot. Drains leave the vessel's `south` through a valve tagged NC; vents leave `north`. The check valve is `valve={non return}`. Off-sheet lines end in a `reference` arrow labelled with the id and the partner sheet. Open values go in a dashed box. About 12 tags per sheet is a guide; split when the fit warning says so.

# example

```latex example
\begin{tikzpicture}[circuit pid ISO14617, every info/.style={font=\small},
    pid process/.style={line width=0.8pt},
    pid signal/.style={dashed},
    pid mechanical/.style={dash dot},
    pid off sheet/.style={reference={info=above:#1}, anchor=west},
    pid open/.style={draw, dashed, font=\small, inner sep=1.5pt}]
  \node[tank={info=below right:T-101, circuit symbol unit=12pt}] (t1) at (5,0) {};
  \draw[pid process] (0,0) to[valve={non return, info=V-101}] (2.5,0) -- (t1.west);
  \draw[pid process] (t1.east) to[pump={name=p1, info=below:P-101}] (9.5,0);
  \node[pid off sheet={L-1 to sheet 2}] at (9.5,0) {};
  \draw[pid process] (t1.south) -- ++(0,-0.9)
        to[valve={info=V-102 NC}] ++(0,-1.4) -- ++(4.5,0);
  \node[pid off sheet={D-1 to sheet 2}] at (9.5,-2.85) {};
  \draw[pid process] (t1.north) -- ++(0,0.9) node[right, font=\small] {vent};
  \node[measurement device={info=LT}] (lt) at (2.5,1.6) {};
  \draw[pid signal] (lt.east) -| ([xshift=-6pt]t1.north);
  \draw[pid mechanical] (p1.north) -- ++(0,1.1) node[pid open, above] {drive TBD};
  \draw[flow path, pos=0.2] (0,0) -- (2.5,0);
\end{tikzpicture}
```
