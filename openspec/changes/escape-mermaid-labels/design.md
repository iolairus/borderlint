## Context

`report.mermaid()` interpolates `juris(j)` and `kb.name(pid)` straight into `[...]` label brackets.
Mermaid treats `()`, `/`, `[]` as metacharacters outside quotes, so common labels (`Unknown
(region-dependent)`, `Custom / OpenAI-compatible endpoint`) produce a parse error.

## Goals / Non-Goals

**Goals:** valid Mermaid for any label. **Non-Goals:** id sanitising; other output formats.

## Decisions

- **Quote labels; escape `#` → `#35;` then `"` → `#quot;`.** Mermaid carries metacharacters by wrapping
  a label in double quotes, with `#` as its *entity-escape prefix* (`#35;` = `#`, `#quot;` = `"`). So a
  literal `#` must be escaped too, or it is read as an entity — and the `#` pass must run *before* the
  quote pass, since `"`→`#quot;` itself introduces a `#`. Quoting then carries parentheses, slashes, and
  brackets unchanged. `# ponytail: one helper, three call sites`.
- **Testable guarantee is mechanical, not "parser-valid".** A zero-dep project has no Mermaid parser, so
  the requirement promises the mechanical output (double-quoted; `#`→`#35;`; `"`→`#quot;`), not a parse.
  Provider and jurisdiction names are single-line display strings, so newlines are not a concern.
- **Ids untouched.** `pid` (bundled-KB provider ids) and `jid = "j_" + j.replace("-", "_")` are
  `[A-Za-z0-9_]` — valid Mermaid node ids. Only the human-readable labels are the bug. (A `--providers`
  id with unsafe characters is out of scope per non-goals.)

## Risks / Trade-offs

- The escape covers the metacharacters that actually occur in provider/jurisdiction names (parens,
  slashes, and the `#`/`"` escape chars). A name with an embedded newline is not handled → none exist,
  and it would be a KB-data problem, not a rendering one.
