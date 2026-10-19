---
diagramKind: P&ID
whenToUse: A piping and instrumentation diagram. Use the circuit pid ISO14617 key and put tags in the template.
minimalTemplate: fixtures/pidcircuit.tex
allowedPackages: PIDcircuitTikZ, TikZ
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Lines run port to port; drains leave the vessel's own outlet through a valve tagged NC. Check valve is valve={non return}. Put circuit pid ISO14617 on the tikzpicture; do not load the library again. Tag every symbol with info=. Place a flow marker with pos=0.2 or pos=0.8 on flow path.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/pidcircuit
mcpPromptName: playbook-pidcircuit
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Size and position are first-class: 7 pt absolute floor (`every info/.style={font=\small}` or larger). Tags must not collide with each other, with symbols, or with flow arrows. Reserved gutter for `info=` tags. Flow arrows stay clear of tags. About 12 tagged symbols on a portrait sheet is a guide, not a cap. The fit warning decides: split when tags would fall below 7 pt or collide. If the sheet is too wide for portrait, prefer a landscape page when this kind supports it. Do not shrink tags. Compile success with crushed or colliding tags is still FAIL.

## When to use

A piping and instrumentation diagram: valves, pumps, flow paths and instruments, with tags a reader can see.

## templateId and body syntax

templateId is `pidcircuit`. bodySyntax is a LaTeX picture body, no preamble. Do not send Markdown, `\documentclass` or `\usepackage`. Sending Markdown to this templateId is a TeX error.

## Fence usage

For a figure inside a document, send templateId `document-shell` and put this same picture in a tikz fence with caption and alt. The fence class is `tikz`. Do not `\usetikzlibrary` the P&ID library; it is preloaded. The key on the picture is `circuit pid ISO14617`.

## Output formats

This templateId is PDF. HTML and DOCX are not sent as bare TeX: the gate wraps the body as a tikz fence under document-shell and the tool result includes a wrap line. Inline siunitx and mhchem stay PDF only.

## Kind notes

Tag every symbol with `info=` (for example `valve={info=V-101}`). A flow marker is `flow path` with `pos=`. `pos=0.2` and `pos=0.8` place the arrow at that fraction of the path. The worker keeps TikZ `pos` shared with the PID flow position. Set `every info/.style={font=\small}`. Tags stay at or above 7 pt, in a reserved gutter, clear of flow arrows and of other tags. If tags collide, re-layout or split; do not shrink.

## P&ID rules

Use ISO 14617 keys only. Define the line styles once on the picture (the snippet in the worked example): `pid process` solid, `pid signal` dashed for instrument lines, `pid mechanical` dash-dot for a link to an item mounted on equipment. Never draw a signal or mechanical link as a process line.

- Check valve: `valve={non return}`. Do not hand-draw one.
- Ports: every process line starts and ends at a symbol or named anchor. A waste, overfill or drain line leaves the owning equipment's own outlet, never a tee off another process line and never from an actuator.
- Before you render, check that no line ends in mid-air. A line ends at an anchor, an off-sheet connector, or a labelled open end such as a vent.
- Valve state: put NO or NC in the tag (`info=V-102 NC`) when the normal position matters. Every drain has a valve tagged NC.
- Vessels: use `tank`, `tank atmospheric pressure` or `pressure vessel`. For each vessel ask: does it receive gas with the liquid? Then draw a vent from `north`. How is it emptied? Then draw a drain from `south`.
- Off-sheet: end the line in `pid off sheet={L-1 to sheet 2}`, a style on the `reference` arrow. Use the same id on the partner sheet, pointing back.
- Open values: write them in `pid open` (a dashed box, for example `drive TBD`) and list them again in the notes.
- If a key is missing, leave that item out. Never hand-draw a substitute.

## Worked example

```latex
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

## Common failures and fixes

A missing `circuit pid ISO14617` key draws ordinary lines. Loading the library again is unnecessary. To move a flow arrow, set `pos=0.2` or `pos=0.8` on that `flow path`.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. A failure is a tool result: fix it and resend, and budget re-renders.
