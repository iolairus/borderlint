## 1. Escape Mermaid labels

- [ ] 1.1 Add a label helper in `report.py` that wraps a string in double quotes and replaces any embedded `"` with `#quot;`
- [ ] 1.2 Apply it to every Mermaid node and subgraph label in `report.mermaid()` — the `app` node, subgraph titles, and provider nodes; leave node/subgraph ids unquoted (already identifier-safe)

## 2. Tests

- [ ] 2.1 Tests: the `unknown` jurisdiction (`Unknown (region-dependent)`) and a `Custom / OpenAI-compatible endpoint` provider name appear as quoted labels (`["..."]`); a label containing `"` is emitted as `#quot;`; node/subgraph ids remain bare identifiers
