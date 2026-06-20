## Why

Rendering the `retire` flow map to PNG exposed that `report.mermaid()` emits **unescaped labels** —
invalid Mermaid whenever a label contains parentheses or a slash. The `unknown` jurisdiction renders as
`Unknown (region-dependent)` and the `custom_endpoint` provider as `Custom / OpenAI-compatible endpoint`;
both break the Mermaid parser. So `--format mermaid` is broken for any repo with a runtime / OpenAI-
compatible endpoint — which v0.9.0 just made common. This is a correctness bug in shipped output.

## What Changes

- Emit every Mermaid **node and subgraph label** as a quoted string, replacing any embedded double quote
  with `#quot;` (Mermaid's escape), so labels with parentheses, slashes, or other metacharacters render.
- Node and subgraph **ids stay unquoted** — provider ids and `j_<token>` are already identifier-safe.

## Capabilities

### Modified Capabilities
- `cli-and-reporting`: the Mermaid flow map now escapes labels.

## Impact

- A one-line label helper applied in `report.mermaid()`. No new dependency; no output change beyond
  producing valid Mermaid.

## Non-goals

- Sanitising node ids (provider ids / jurisdiction tokens are `[A-Za-z0-9_]`); if a future id had spaces
  that is a separate concern.
- Other formats — text / JSON / SARIF / SBOM are unaffected.
