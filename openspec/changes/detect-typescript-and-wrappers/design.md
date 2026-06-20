## Context

borderlint detects Python SDK imports + literal endpoints. Dogfooding showed it misses TS/JS
entirely and misses AI calls routed through aggregators/wrappers. This change extends detection
coverage to close those two gaps.

## Goals / Non-Goals

**Goals:** detect AI SDK imports in TS/JS; flag aggregator/router usage as `unknown`-jurisdiction.

**Non-Goals:** inferring runtime-routed jurisdictions; full TS AST; languages beyond TS/JS.

## Decisions

- **Regex-based JS/TS import detection, not tree-sitter.** Alternative: tree-sitter grammars.
  Rejected — it adds native build dependencies and breaks the zero-dependency guarantee, and
  `import` / `require` / dynamic-`import()` statements are regular enough for reliable package
  extraction. Revisit only if commented/stringified imports cause real false positives.
- **Aggregators resolve to `unknown`, never a guessed provider.** Alternative: infer the configured
  provider/model. Rejected — the destination is chosen at runtime; static analysis cannot know, and
  guessing would fabricate a jurisdiction. `unknown` + `on_unknown: fail` is the honest, safe result.
- **KB gains a parallel JS/TS package field; endpoint detection in TS reuses the existing text scan.**
  Only import detection is new for TS.
- **Scanner overlap on `.ts/.js` is intentional, not double-counting.** The text scan already
  flags endpoint literals in those files; the new import scan adds imports. A file with both yields
  two detections (distinct evidence — an import *and* an endpoint), which de-duplication keeps
  because it keys on file + line + evidence.

## Risks / Trade-offs

- Regex import detection may match imports inside comments/strings → over-report. Mitigation: anchor
  on leading `import`/`require` forms; accept rare over-reports (a residency over-report is safer
  than a miss).
- Aggregator-list staleness → extend the KB; community PRs.
