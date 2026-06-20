## 1. Escape Mermaid labels

- [x] 1.1 Add a label helper in `report.py` that double-quotes a string after replacing `#` → `#35;` then `"` → `#quot;` (in that order — the quote escape introduces a `#`)
- [x] 1.2 Apply it to every Mermaid node and subgraph label in `report.mermaid()` — the `app` node, subgraph titles, and provider nodes; leave node/subgraph ids unquoted (already identifier-safe)

## 2. Tests

- [x] 2.1 Tests: the `unknown` jurisdiction (`Unknown (region-dependent)`) and a `Custom / OpenAI-compatible endpoint` provider name appear as double-quoted labels with the parens/slash inside the quotes; a label containing `#` → `#35;` and `"` → `#quot;`; node/subgraph ids remain bare identifiers
