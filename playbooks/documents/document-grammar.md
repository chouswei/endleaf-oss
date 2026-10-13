# Document grammar playbook

Worked recipes for editing an Endleaf Document with the document grammar. Every call below is copy-pasteable and every reply is what Endleaf returns, trimmed: `…` stands for an id, a token or text you get back. The calls run on one example document, a short pump test note that recipe loop imports; after that the recipes run in order, so revisions count up from rev-1.

Read the short card first: guide(topic:"grammar"). One recipe: guide(topic:"grammar", section:"<id>"). Everything: section "all".

Escaping: ops are grammar statements inside JSON strings. Grammar strings use single quotes; a backslash escapes the next character. So a LaTeX `\cite` is `\\cite` in the grammar and `\\\\cite` in JSON, and an apostrophe is `\\'` in JSON. There are no escape sequences such as `\n`: a backslash before n is just n.

## loop: The edit loop

Every change is the same four steps. Reads, checks, diffs and dry runs never count against the edit rate; only a committed apply does.

1. Read what you need: the where-am-I summary, then the partId, parentId and orderKey of the parts around your edit, then the full text of only the parts you will rewrite.
2. Dry run: checkDocument with ops. Nothing changes. You get the checks as they would be, the diff and a dryRunId.
3. Ask the human, showing the diff and your one-line reason.
4. applyChange with the dryRunId, a fresh idempotencyKey and the reason (one line, at most 200 characters). You get the new revision.

Start the example document: an import is a dry run, then an apply.

```call
importDocument {"kind":"fulldoc","format":"latex","source":"\\title{Pump Test Note}\n\\author{Example Lab}\n\\section{Introduction}\\label{sec:intro}\nThis note reports a bench test of a small centrifugal pump. The rig follows the rating method in \\cite{iec60034}.\n\nThe test ran for two hours at three flow rates. Section~\\ref{sec:method} gives the set-up.\n\\section{Method}\\label{sec:method}\nFlow was measured with a turbine meter upstream of the valve. Pressure was logged at one sample a second.\n\nPower was taken from the drive input, as in Equation~\\ref{eq:power}.\n\\begin{equation}\\label{eq:power}\nP = \\rho g Q H\n\\end{equation}\n\\section{Results}\\label{sec:results}\nEfficiency peaked near the middle flow rate. The curve is flat within two percent across the range.\n\\begin{thebibliography}{9}\n\\bibitem{iec60034} IEC 60034-1, Rotating electrical machines, 2022.\n\\end{thebibliography}\n","dryRun":true}
```

```reply
{
 "byRule": {},
 "countsByKind": {"BibItem": 1, "Equation": 1, "Paragraph": 5, "Section": 3, "TitleBlock": 1},
 "dryRunId": "dr_…",
 "failed": 0,
 "leftoverLatexParts": 0,
 "passed": 11,
 "references": {"cite": {"found": 1, "resolved": 1, "unresolved": 0}, "ref": {"found": 2, "resolved": 2, "unresolved": 0}},
 "results": [],
 "total": 0
}
```

```call
importDocument {"kind":"fulldoc","dryRun":false,"dryRunId":"dr_…","idempotencyKey":"pump-import-1","reason":"import the pump test note"}
```

```reply
{
 "byRule": {},
 "countsByKind": {"BibItem": 1, "Equation": 1, "Paragraph": 5, "Section": 3, "TitleBlock": 1},
 "documentId": "doc_7f3a9c1e2b4d",
 "failed": 0,
 "leftoverLatexParts": 0,
 "passed": 11,
 "references": {"cite": {"found": 1, "resolved": 1, "unresolved": 0}, "ref": {"found": 2, "resolved": 2, "unresolved": 0}},
 "results": [],
 "revision": "rev-1",
 "total": 0
}
```

Where am I: readDocument with only the documentId gives the latest revision, the sections, part counts and recent changes. An agent with no memory starts here.

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d"}
```

```reply
{
 "checks": {"byRule": {}, "failed": 0},
 "documentId": "doc_7f3a9c1e2b4d",
 "kind": "fulldoc",
 "labels": {},
 "partCounts": {"BibItem": 1, "Equation": 1, "Paragraph": 5, "Section": 3, "TitleBlock": 1},
 "recent": [
  {"reason": "import the pump test note", "rev": "rev-1"}
 ],
 "rev": "rev-1",
 "sections": [
  {"level": 1, "partId": "s1", "title": "Introduction"},
  {"level": 1, "partId": "s2", "title": "Method"},
  {"level": 1, "partId": "s3", "title": "Results"}
 ],
 "title": "Pump Test Note"
}
```

## find: Find a part

A pattern read names the fields it returns. `RETURN p` is refused. Name only what you need (partId, parentId, orderKey) to stay small; name p.text only for the part you will rewrite.

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","pattern":"MATCH (p:Paragraph {parentId:'s2'}) RETURN p.partId, p.orderKey"}
```

```reply
{
 "rows": [
  {"orderKey": "FV", "partId": "p3"},
  {"orderKey": "V0", "partId": "p4"}
 ]
}
```

Text search: CONTAINS is a case-insensitive substring of at least 3 characters. It returns the count and a snippet of about 60 characters per part. Past 150 rows or 16 KiB the reply carries a continuation: send the same call with "continuation" set to it until none comes back.

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","pattern":"MATCH (p:Paragraph) WHERE p.text CONTAINS 'flow' RETURN p.partId, snippet(p.text)"}
```

```reply
{
 "count": 3,
 "rows": [
  {"partId": "p2", "snippet": " ran for two hours at three flow rates. Section~\\ref{sec:met"},
  {"partId": "p3", "snippet": "Flow was measured with a turbine meter upstream of the valve"},
  {"partId": "p5", "snippet": "ency peaked near the middle flow rate. The curve is flat wit"}
 ]
}
```

Paragraphs that cite one BibItem, by its key (one fixed hop):

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","pattern":"MATCH (p:Paragraph)-[:cites]->(b:BibItem {key:'iec60034'}) RETURN p.partId, p.parentId"}
```

```reply
{
 "rows": [
  {"parentId": "s1", "partId": "p1"}
 ]
}
```

## rewrite: Rewrite a paragraph

Read the full text of the one part you change, by partId.

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","pattern":"MATCH (p {partId:'p3'}) RETURN p.partId, p.text"}
```

```reply
{
 "rows": [
  {"partId": "p3", "text": "Flow was measured with a turbine meter upstream of the valve. Pressure was logged at one sample a second."}
 ]
}
```

Dry run the new text.

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'p3'}) SET p.text = 'Flow was measured with a turbine meter two metres upstream of the valve. Pressure was logged once a second.'"]}
```

```reply
{
 "base": "rev-1",
 "diff": [
  {"after": {"text": "Flow was measured with a turbine meter two metres upstream of the valve. Pressure was logged once a second."}, "before": {"text": "Flow was measured with a turbine meter upstream of the valve. Pressure was logged at one sample a second."}, "op": "set", "partId": "p3"}
 ],
 "dryRunId": "dr_…",
 "failed": 0,
 "passed": 11
}
```

After the human says yes:

```call
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pump-rewrite-p3","reason":"say where the flow meter sits"}
```

```reply
{
 "changeId": "chg_…",
 "diff": ["…"],
 "failed": 0,
 "passed": 11,
 "revision": "rev-2"
}
```

## insert: Insert between two parts

Order comes from orderKey, never from a next edge. Keys sort as text over 0-9, then A-Z, then a-z, and are unique within a parent. To go between two siblings, take a key strictly between theirs: appending a middle digit such as V to the left key always works while the result stays below the right key. Read the keys in s1 first: p1 is Kf and p2 is fK, so KfV goes between them.

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","pattern":"MATCH (p {parentId:'s1'}) RETURN p.partId, p.orderKey"}
```

```reply
{
 "rows": [
  {"orderKey": "Kf", "partId": "p1"},
  {"orderKey": "fK", "partId": "p2"}
 ]
}
```

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["INSERT (:Paragraph {partId:'p6', parentId:'s1', orderKey:'KfV', text:'The pump is a single-stage end-suction unit.'})"]}
```

```reply
{
 "base": "rev-2",
 "diff": [
  {"after": {"orderKey": "KfV", "parentId": "s1", "partId": "p6", "status": "live", "text": "The pump is a single-stage end-suction unit."}, "before": {}, "op": "insert", "partId": "p6"}
 ],
 "dryRunId": "dr_…",
 "failed": 0,
 "passed": 12
}
```

```call
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pump-insert-p6","reason":"describe the pump"}
```

```reply
{
 "changeId": "chg_…",
 "diff": ["…"],
 "failed": 0,
 "passed": 12,
 "revision": "rev-3"
}
```

A key already used by a sibling is reported by the CHK-TREE check in the dry run; pick another key. A new part is always live; do not set status on INSERT. partId is optional: without one Endleaf picks it.

## move: Move a part

A move is a SET of orderKey, and of parentId to change section. Here p6 moves to the start of Method (s2), before p3 at FV.

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'p6'}) SET p.parentId = 's2', p.orderKey = 'F'"]}
```

```reply
{
 "base": "rev-3",
 "diff": [
  {"after": {"orderKey": "F", "parentId": "s2"}, "before": {"orderKey": "KfV", "parentId": "s1"}, "op": "set", "partId": "p6"}
 ],
 "dryRunId": "dr_…",
 "failed": 0,
 "passed": 12
}
```

```call
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pump-move-p6","reason":"move the pump description into Method"}
```

```reply
{
 "changeId": "chg_…",
 "diff": ["…"],
 "failed": 0,
 "passed": 12,
 "revision": "rev-4"
}
```

## figure: Add a figure and refer to it

INSERT a Figure with body (the picture only: no figure environment, caption or label), caption and label, then point at it from a paragraph with an inline `\ref`. The refersTo edge comes from the token; never set it. Both ops go in one change. Without alt, the caption is the alt text. A Figure has no width field: it is as wide as its picture, and you size it inside the body.

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["INSERT (:Figure {partId:'f1', parentId:'s3', orderKey:'a', body:'\\\\begin{tikzpicture}\\\\draw[->] (0,0) -- (4,0) node[right] {flow}; \\\\draw[->] (0,0) -- (0,3) node[above] {efficiency}; \\\\draw (0.5,1) .. controls (2,2.8) .. (3.5,1.2);\\\\end{tikzpicture}', caption:'Efficiency against flow rate', label:'fig:eff'})","INSERT (:Paragraph {partId:'p7', parentId:'s3', orderKey:'b', text:'Figure~\\\\ref{fig:eff} shows the efficiency curve.'})"]}
```

```reply
{
 "base": "rev-4",
 "diff": [
  {"after": {"alt": "Efficiency against flow rate", "body": "\\begin{tikzpicture}\\draw[->] (0,0) -- (4,0) node[right] {flow}; \\draw[->] (0,0) -- (0,3) node[above] {efficiency}; \\draw (0.5,1) .. controls (2,2.8) .. (3.5,1.2);\\end{tikzpicture}", "caption": "Efficiency against flow rate", "label": "fig:eff", "orderKey": "a", "parentId": "s3", "partId": "f1", "status": "live"}, "before": {}, "op": "insert", "partId": "f1"},
  {"after": {"orderKey": "b", "parentId": "s3", "partId": "p7", "status": "live", "text": "Figure~\\ref{fig:eff} shows the efficiency curve."}, "before": {}, "op": "insert", "partId": "p7"}
 ],
 "dryRunId": "dr_…",
 "failed": 0,
 "passed": 14
}
```

```call
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pump-figure-f1","reason":"add the efficiency figure"}
```

```reply
{
 "changeId": "chg_…",
 "diff": ["…"],
 "failed": 0,
 "passed": 14,
 "revision": "rev-5"
}
```


If a render says a picture runs past the text line, the warning gives the fix. `scaleToFit` is the text line divided by the picture's width, and `minTextPt` is the smallest text in the picture at that scale:

- `layout_overhang: packages=tikz: f1 pg2: a picture runs 54.1 mm past the text line; scaleToFit 0.69, minTextPt 8.2. Fix: scale inside the source to 0.69`: SET the body once with the scale on the picture, for TikZ `\begin{tikzpicture}[scale=0.69, transform shape]`, then render once.
- `…; scaleToFit 0.49, minTextPt 4.9 (below 7 pt). Fix: redraw or split; scaling would put text at 4.9 pt`: do not scale. Redraw the picture narrower, or split it into two figures.

`widthFraction` on a Figure is deleted. Until 2026-11-08 a write that names it still goes through, the field is dropped, and the reply carries `"deprecations": ["deprecated: widthFraction is ignored; scale inside the figure source"]`. A Table column's widthFraction is unchanged. A change that stores nothing new (only that field, or a field set to the value it has) is marked `"noChange": true` on the dry run; applying it makes no revision and answers `no change` with the current revision, and it does not count against the edit rate.

## cite: Add a citation and its BibItem

INSERT the BibItem (key: letters, digits, : - . only) and edit the citing text in the same change. The cites edge comes from `\cite`; never set it.

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["INSERT (:BibItem {partId:'b2', key:'iso9906', text:'ISO 9906, Rotodynamic pumps, hydraulic performance acceptance tests, 2012.', orderKey:'z'})","MATCH (p {partId:'p5'}) SET p.text = 'Efficiency peaked near the middle flow rate, as expected from \\\\cite{iso9906}. The curve is flat within two percent across the range.'"]}
```

```reply
{
 "base": "rev-5",
 "diff": [
  {"after": {"key": "iso9906", "orderKey": "z", "partId": "b2", "status": "live", "text": "ISO 9906, Rotodynamic pumps, hydraulic performance acceptance tests, 2012."}, "before": {}, "op": "insert", "partId": "b2"},
  {"after": {"text": "Efficiency peaked near the middle flow rate, as expected from \\cite{iso9906}. The curve is flat within two percent across the range."}, "before": {"text": "Efficiency peaked near the middle flow rate. The curve is flat within two percent across the range."}, "op": "set", "partId": "p5"}
 ],
 "dryRunId": "dr_…",
 "failed": 0,
 "passed": 15
}
```

```call
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pump-cite-b2","reason":"cite the acceptance-test standard"}
```

```reply
{
 "changeId": "chg_…",
 "diff": ["…"],
 "failed": 0,
 "passed": 15,
 "revision": "rev-6"
}
```

## cancel: Cancel a part safely

Nothing is deleted; DELETE is refused. Cancel is SET status 'cancelled' with a one-line reason and a date. A part that live text still points at cannot be cancelled alone: the refusal names the referrers. Here Method (s2) is cancelled: first find its children and anything that points at it or into it.

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","pattern":"MATCH (p {parentId:'s2'}) RETURN p.partId, p.orderKey"}
```

```reply
{
 "rows": [
  {"orderKey": "kV", "partId": "e1"},
  {"orderKey": "FV", "partId": "p3"},
  {"orderKey": "V0", "partId": "p4"},
  {"orderKey": "F", "partId": "p6"}
 ]
}
```

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","pattern":"MATCH (p)-[:refersTo]->(s {partId:'s2'}) RETURN p.partId, p.text"}
```

```reply
{
 "rows": [
  {"partId": "p2", "text": "The test ran for two hours at three flow rates. Section~\\ref{sec:method} gives the set-up."}
 ]
}
```

Cancel the section and its children, and drop the `\ref` from p2, in one change. (p4's reference to e1 goes with p4.)

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'s2'}) SET p.status = 'cancelled', p.reason = 'method moves to a separate note', p.date = '2026-10-09'","MATCH (p {partId:'p6'}) SET p.status = 'cancelled', p.reason = 'method moves to a separate note', p.date = '2026-10-09'","MATCH (p {partId:'p3'}) SET p.status = 'cancelled', p.reason = 'method moves to a separate note', p.date = '2026-10-09'","MATCH (p {partId:'p4'}) SET p.status = 'cancelled', p.reason = 'method moves to a separate note', p.date = '2026-10-09'","MATCH (p {partId:'e1'}) SET p.status = 'cancelled', p.reason = 'method moves to a separate note', p.date = '2026-10-09'","MATCH (p {partId:'p2'}) SET p.text = 'The test ran for two hours at three flow rates.'"]}
```

```reply
{
 "base": "rev-6",
 "diff": [
  {"after": {"date": "2026-10-09", "reason": "method moves to a separate note", "status": "cancelled"}, "before": {"status": "live"}, "op": "cancel", "partId": "e1"},
  {"after": {"text": "The test ran for two hours at three flow rates."}, "before": {"text": "The test ran for two hours at three flow rates. Section~\\ref{sec:method} gives the set-up."}, "op": "set", "partId": "p2"},
  {"after": {"date": "2026-10-09", "reason": "method moves to a separate note", "status": "cancelled"}, "before": {"status": "live"}, "op": "cancel", "partId": "p3"},
  {"after": {"date": "2026-10-09", "reason": "method moves to a separate note", "status": "cancelled"}, "before": {"status": "live"}, "op": "cancel", "partId": "p4"},
  {"after": {"date": "2026-10-09", "reason": "method moves to a separate note", "status": "cancelled"}, "before": {"status": "live"}, "op": "cancel", "partId": "p6"},
  {"after": {"date": "2026-10-09", "reason": "method moves to a separate note", "status": "cancelled"}, "before": {"status": "live"}, "op": "cancel", "partId": "s2"}
 ],
 "dryRunId": "dr_…",
 "failed": 0,
 "passed": 10
}
```

```call
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pump-cancel-s2","reason":"move the method to a separate note"}
```

```reply
{
 "changeId": "chg_…",
 "diff": ["…"],
 "failed": 0,
 "passed": 10,
 "revision": "rev-7"
}
```

## batch: Batch several ops into one change

One change holds up to 50 ops, applied all together or not at all, and counts once against the edit rate. Group related edits into one dry run and one apply instead of many.

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'s3'}) SET p.title = 'Results and discussion'","MATCH (p {partId:'p7'}) SET p.text = 'Figure~\\\\ref{fig:eff} shows the efficiency curve against flow rate.'","INSERT (:Paragraph {partId:'p8', parentId:'s3', orderKey:'c', text:'A longer run at the top flow rate is planned.'})"]}
```

```reply
{
 "base": "rev-7",
 "diff": [
  {"after": {"text": "Figure~\\ref{fig:eff} shows the efficiency curve against flow rate."}, "before": {"text": "Figure~\\ref{fig:eff} shows the efficiency curve."}, "op": "set", "partId": "p7"},
  {"after": {"orderKey": "c", "parentId": "s3", "partId": "p8", "status": "live", "text": "A longer run at the top flow rate is planned."}, "before": {}, "op": "insert", "partId": "p8"},
  {"after": {"title": "Results and discussion"}, "before": {"title": "Results"}, "op": "set", "partId": "s3"}
 ],
 "dryRunId": "dr_…",
 "failed": 0,
 "passed": 11
}
```

```call
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pump-batch-1","reason":"retitle the results and add a next step"}
```

```reply
{
 "changeId": "chg_…",
 "diff": ["…"],
 "failed": 0,
 "passed": 11,
 "revision": "rev-8"
}
```

## errors: Recover from errors

Every refusal is one JSON object: error, msg, a fix you can follow, and fields that help. Nothing is written.

stale_base: the document moved on since your dry run. Dry-run the same ops again on the current revision (the reply names it and the parts that changed), ask again if the diff changed, then apply.

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","revision":"rev-1","ops":["MATCH (p {partId:'p8'}) SET p.text = 'A longer run at the top flow rate is planned for next month.'"]}
```

```reply
{
 "changedPartIds": ["b2", "e1", "f1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "s2", "s3"],
 "currentRevision": "rev-8",
 "error": "stale_base",
 "fix": "dry-run the same ops on the current revision",
 "msg": "base is behind rev-8"
}
```

dangling_reference: the part is still cited or referred to. Edit or cancel the referrers in the same change (recipe cancel).

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'b2'}) SET p.status = 'cancelled', p.reason = 'drop the standard', p.date = '2026-10-09'"]}
```

```reply
{
 "edge": "cites",
 "error": "dangling_reference",
 "fix": "edit those tokens or cancel those parts in the same change",
 "msg": "b2 is still referenced",
 "referrers": ["p5"],
 "target": "b2",
 "totalReferencing": 1,
 "truncated": false
}
```

rate_limited: too many applies in the last minute. Wait retryAfter seconds (or until retryAt), then send the same applyChange again with the same idempotencyKey; next time batch the ops. Reads, checks and dry runs still work.

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'p8'}) SET p.text = 'A longer run at the top flow rate is planned for next month.'"]}
```

```reply
{
 "base": "rev-8",
 "diff": [
  {"after": {"text": "A longer run at the top flow rate is planned for next month."}, "before": {"text": "A longer run at the top flow rate is planned."}, "op": "set", "partId": "p8"}
 ],
 "dryRunId": "dr_…",
 "failed": 0,
 "passed": 11
}
```

```call at-rate
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pump-next-month","reason":"say when the longer run is"}
```

```reply
{
 "error": "rate_limited",
 "fix": "retry in … s (at …); batch ops into one change",
 "limit": 20,
 "msg": "20 document edits per minute reached",
 "retryAfter": 60,
 "retryAt": "…",
 "scope": "key"
}
```

After retryAfter seconds, the same call goes through:

```call
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pump-next-month","reason":"say when the longer run is"}
```

```reply
{
 "changeId": "chg_…",
 "diff": ["…"],
 "failed": 0,
 "passed": 11,
 "revision": "rev-9"
}
```

gql_unsupported: the statement is outside the grammar. Follow the fix; here, name fields.

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","pattern":"MATCH (p:Paragraph) RETURN p"}
```

```reply
{
 "error": "gql_unsupported",
 "fix": "name fields, e.g. RETURN p.partId, p.text",
 "msg": "RETURN p returns a whole part"
}
```

batch_too_large: more than 50 ops in a change (or a change too large to store at once). Split it into smaller changes. The call below is 51 copies of one op.

```call repeat=51
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'p1'}) SET p.text = 'Scope.'"]}
```

```reply
{
 "error": "batch_too_large",
 "fix": "split the change into smaller ones",
 "limit": 50,
 "msg": "this change is too large",
 "used": 51
}
```

Size limits are invalid_field with the limit: a string field holds at most 16384 bytes, a reason one line of at most 200 characters, an orderKey 128 bytes. A cancel without reason and date is invalid_field too. The call below sends a 17000-character text.

```call fill=17000
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'p1'}) SET p.text = '{{fill}}'"]}
```

```reply
{
 "error": "invalid_field",
 "fix": "keep each string at 16384 bytes or less",
 "limit": 16384,
 "msg": "text is over 16384 bytes"
}
```

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'p7'}) SET p.status = 'cancelled'"]}
```

```reply
{
 "error": "invalid_field",
 "fix": "SET p.status = 'cancelled', p.reason = '…', p.date = 'YYYY-MM-DD'",
 "msg": "cancel needs reason and date"
}
```

## render: Render a revision and diff two revisions

Render any revision by documentId and revision; templateId is fulldoc. It spends one render job, so render when the human wants to see the page, not after every edit.

```call
renderDocument {"outputFormat":"pdf","templateId":"fulldoc","documentId":"doc_7f3a9c1e2b4d","revision":"rev-8"}
```

```reply
ok pages=… page=… bytes=… sha256=… format=pdf templateId=fulldoc kind=fulldoc file=endleaf-fulldoc-….pdf
document: doc_7f3a9c1e2b4d@rev-8 (compiled from 11 parts; not stored)
…
```

Diff two revisions (rev-N, a label, latest, or a dryRunId). Each op shows only the changed fields.

```call
diffDocument {"documentId":"doc_7f3a9c1e2b4d","revA":"rev-2","revB":"rev-3"}
```

```reply
{
 "ops": [
  {"after": {"orderKey": "KfV", "parentId": "s1", "partId": "p6", "status": "live", "text": "The pump is a single-stage end-suction unit."}, "before": {}, "op": "insert", "partId": "p6"}
 ],
 "revA": "rev-2",
 "revB": "rev-3"
}
```

## pages: Read the page layout

To fix how the pages fall (a figure that sticks out, a section that spills a few lines onto the next page), read the pages view, not the text. After a render, readDocument with view "pages" gives one line per rendered page in reading order: how full the page is and how far it runs over, each section with its first and last page, runs of paragraphs as an id range with a count and a height, and each figure and table with its number, width, size, placement and the page of its first reference. A figure past the text line adds `over Xmm fit S text Tpt`, and `<7pt` when scaling would put its text under 7 pt. An overfull line shows as `overfull p12 3.1pt` on its page; one the render could not place is counted in the stamp as location unknown. In the one-page view, references read as the reader sees them: `Figure~\ref{fig:eff}` shows as `Figure 1`. An arrow `→` marks a paragraph that runs across the page break. Then read the full text of only the parts you will rewrite.

The stamp names the revision the view was rendered from. A change after that render marks its page and every later page stale; earlier pages stay valid. Re-render before any layout decision on a stale page. Before the first render there are no page lines, only a stamp that says so.

```call
renderDocument {"outputFormat":"pdf","templateId":"fulldoc","documentId":"doc_7f3a9c1e2b4d","revision":"latest"}
```

```reply
ok pages=… page=… bytes=… sha256=… format=pdf templateId=fulldoc kind=fulldoc file=endleaf-fulldoc-….pdf
document: doc_7f3a9c1e2b4d@rev-9 (compiled from 11 parts; not stored)
```

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","view":"pages"}
```

```reply
{
 "pages": [
  "pg1 fill …% | §1 s1 Introduction pg1 | p1–p2 (2, …mm) | §2 s3 Results and discussion pg1–3",
  "pg2 fill …% | p5 (1, …mm) | f1 fig:eff Figure 1 …mm [htbp] ref pg2 | p7→ (1, …mm)",
  "pg3 fill …% | →p7–p8 (2, …mm) | References | b1–b2→ (2, …mm)",
  "pg4 fill …% | References | →b2 (1, …mm)"
 ],
 "stamp": "rendered at rev-9; 0 parts changed since"
}
```

One page with a line per part (id, height, first words), for that page only:

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","view":"pages","page":1}
```

```reply
{
 "pages": ["pg1 fill …% | §1 s1 Introduction pg1 | p1–p2 (2, …mm) | §2 s3 Results and discussion pg1–3"],
 "parts": [
  "s1 heading Introduction",
  "p1 …mm This note reports a bench test of a…",
  "p2 …mm The test ran for two hours at three…",
  "s3 heading Results and discussion"
 ],
 "stamp": "rendered at rev-9; 0 parts changed since"
}
```

After an edit the view is stale from the edited part's page on:

```call
checkDocument {"documentId":"doc_7f3a9c1e2b4d","ops":["MATCH (p {partId:'p5'}) SET p.text = 'Efficiency peaked near the middle flow rate. The curve is flat within two percent.'"]}
```

```reply
{"base": "rev-9", "dryRunId": "dr_…", "failed": 0, "diff": [{"op": "set", "partId": "p5", "after": {"text": "Efficiency peaked near the middle flow rate. The curve is flat within two percent."}, "before": {"text": "…"}}]}
```

```call
applyChange {"documentId":"doc_7f3a9c1e2b4d","dryRunId":"dr_…","idempotencyKey":"pages-1","reason":"shorten the results paragraph"}
```

```reply
{"revision": "rev-10", "failed": 0}
```

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d","view":"pages"}
```

```reply
{
 "pages": [
  "pg1 fill …% | §1 s1 Introduction pg1 | p1–p2 (2, …mm) | §2 s3 Results and discussion pg1–3",
  "pg2 … stale",
  "pg3 … stale",
  "pg4 … stale"
 ],
 "stamp": "rendered at rev-9; 1 parts changed since; pages from pg2 are stale: re-render before any layout decision on a stale page"
}
```

Here p5 changed on pg2, so pg1 still holds and pg2 to the end wait for a new render.

## delete: Delete a whole document

Only when the human asks to delete the document. Deleting is permanent: the document and every revision go, and it cannot be restored. To drop one part instead, cancel it (recipe cancel). deleteDocument takes the documentId and confirm, which must repeat the same documentId; anything else is refused and nothing changes. It does not count against the edit rate.

```call
deleteDocument {"documentId":"doc_7f3a9c1e2b4d","confirm":"yes"}
```

```reply
{"error": "confirm_mismatch", "fix": "ask the human first; then send confirm equal to the documentId", "msg": "confirm must repeat the documentId"}
```

```call
deleteDocument {"documentId":"doc_7f3a9c1e2b4d","confirm":"doc_7f3a9c1e2b4d"}
```

```reply
{"deleted": true, "documentId": "doc_7f3a9c1e2b4d", "revisions": 10}
```

After that the id is unknown, the same as an id that never existed:

```call
readDocument {"documentId":"doc_7f3a9c1e2b4d"}
```

```reply
{"error": "unknown_document", "fix": "check the documentId, or create one with importDocument (dryRun true, then apply)", "msg": "unknown document"}
```
