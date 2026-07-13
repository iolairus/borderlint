# add-html-report-format — tasks

## 1. Renderer

- [x] 1.1 Add `report.html(findings, kb, policy=None, envelope=None)`: document skeleton with single `<style>` block, metadata header from the envelope (path, git commit, KB review dates; policy digest + classification when present; absent fields render "unavailable") — spec: HTML report content
- [x] 1.2 Render findings grouped by residency jurisdiction, each row with residency/sovereignty/provenance, severity chips as text+class; inventory mode renders flows without verdicts — spec: HTML report content
- [x] 1.3 Render the waiver register section when any finding is waived, with justification; surface regime tags and arrangement references (as `<a href>` reference links) like other formats — spec: HTML report content
- [x] 1.4 `html.escape(..., quote=True)` on every repo/KB-derived string (paths, evidence, model IDs, waiver reasons, provider names) — spec: HTML report format (injection scenario)

## 2. CLI wiring

- [x] 2.1 Add `html` to `--format` choices (`cli.py:52`), build the envelope when `a.format in ("evidence","html")` (`cli.py:91`), add the renderer lambda, extend the export exit-0 tuple (`cli.py:97`) — spec: HTML report format, CI exit code (MODIFIED)

## 3. Tests

- [x] 3.1 Renderer tests: grouped output with all three axes, header fields (policy digest/classification), waiver register presence/absence, inventory mode without verdicts, arrangement reference rendered as a hyperlink for a flagged cross-border flow — substring asserts per house style
- [x] 3.2 Injection test: evidence string containing `<script>` renders escaped
- [x] 3.3 Self-containment test: output contains no fetched-resource markup (`<script src`, `<link `, `<img `, `@import`, `url(`) — `<a href>` reference links are allowed
- [x] 3.4 CLI test: `--format html` with a violating scan exits 0 and emits the document

## 4. Docs

- [x] 4.1 README: add `html` to the `--format` line with one sentence on the audience (share with your privacy/compliance reviewer); CAPABILITIES.md: mark the capability shipped
