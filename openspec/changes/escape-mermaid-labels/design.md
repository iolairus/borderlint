## Context

`report.mermaid()` interpolates `juris(j)` and `kb.name(pid)` straight into `[...]` label brackets.
Mermaid treats `()`, `/`, `[]` as metacharacters outside quotes, so common labels (`Unknown
(region-dependent)`, `Custom / OpenAI-compatible endpoint`) produce a parse error.

## Goals / Non-Goals

**Goals:** valid Mermaid for any label. **Non-Goals:** id sanitising; other output formats.

## Decisions

- **Quote labels, escape `"` → `#quot;`.** Mermaid's documented way to carry metacharacters in a label
  is to wrap it in double quotes; a literal quote inside becomes the HTML entity `#quot;`. Alternative:
  strip/replace metacharacters — rejected, it corrupts the label text. `# ponytail: one helper, three call sites`.
- **Ids untouched.** `pid` (KB provider ids) and `jid = "j_" + j.replace("-", "_")` are `[A-Za-z0-9_]`
  — valid Mermaid node ids. Only the human-readable labels are the bug.

## Risks / Trade-offs

- A label containing the literal text `#quot;` would round-trip oddly → negligible; provider/jurisdiction
  names don't contain it.
