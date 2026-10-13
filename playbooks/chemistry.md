---
diagramKind: chemistry
whenToUse: chemfig structures and mhchem formulae.
minimalTemplate: fixtures/chemistry.tex
allowedPackages: chemfig, mhchem
forbidden: shell-escape, \write18, Asymptote, outside programs, network, TikZ external library, file reads by path, runaway loops, cap evasion
commonErrorsAndFixes: Inline mhchem is PDF only. Put a formula in a tikz fence to keep it visible in HTML and DOCX.
capBudget: RenderWorker.sandbox.limits
resourceUri: endleaf://playbooks/chemistry
mcpPromptName: playbook-chemistry
---

## Kind packing

Shared Composition is served above this section and outranks the macros below. Size and position are first-class: 7 pt absolute floor. One structure family per figure. Names stay readable and clear of bonds. Do not shrink names. Compile success with crushed or colliding names is still FAIL.

## When to use

chemfig structures and mhchem reaction formulae, with names a reader can see.

## templateId and body syntax

templateId is `chemistry`. bodySyntax is a LaTeX picture body, no preamble. Do not send Markdown. Give structures room with `\setchemfig{atom sep=2em}` and name them with `\chemname`.

## Fence usage

To keep a `\ce` formula visible in HTML or DOCX, put it in a tikz fence (it becomes an image). The fence class is `tikz`, with caption and alt.

## Output formats

This templateId is PDF. HTML and DOCX are wrapped by the gate as a document-shell tikz fence; the tool result says so. Inline mhchem is PDF only. The worker `warnings` field (`notationPdfOnly`) is copied into the tool result when an inline formula falls back to source text.

## Kind notes

Leave space between a structure and a reaction (`\qquad`, `\par\medskip`). Mixed zh-TW names such as 苯酚 Phenol are fine on this TeX path.

In a fulldoc document, a `figure` whose body is only chemistry (`\chemfig`, `\ce`, `\schemestart`…`\schemestop`, with `\chemname`, `\setchemfig`, `\arrow`, `\+` and spacing) imports as a Figure: you can edit it and its `\ref` resolves. Any other command in that body leaves it a raw LatexPart.

## Common failures and fixes

A cramped one-line structure is hard to read: separate the pictures and the reaction. An inline `\ce` in HTML or DOCX becomes source text: move it into a tikz fence.

## Forbidden

No `\write18`, shell-escape, Asymptote, outside programs, network, or the TikZ external library. No file reads by path (`\input` or `\include` of `/…` or `../…`, `\openin`, `\read`). No runaway loops. No cap evasion. A failure is a tool result: fix it and resend, and budget re-renders.
