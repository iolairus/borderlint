## Why

Dogfooding borderlint on real repos exposed two false-negative gaps: TypeScript/JavaScript code is
invisible (the scanner reads Python + config only), and AI calls routed through multi-provider
aggregators (litellm, langchain) or wrapper libraries slip past SDK-import detection. Dogfooding on
internal repos — a TypeScript app, and a Python service using an httpx wrapper — surfaced both gaps.
This change closes them.

## What Changes

- Detect AI SDK imports in **TypeScript/JavaScript** (`import`, `require`, dynamic `import()`) across
  `.ts/.tsx/.js/.jsx/.mjs/.cjs`. Endpoint references in those files already match via the text scan;
  this adds import detection.
- Recognize **multi-provider aggregator/router libraries** (litellm, langchain, llama-index,
  aisuite) in Python and JS as flows whose destination is chosen at runtime → resolved as `unknown`,
  so a policy with `on_unknown: fail` blocks them for sensitive classes.
- Extend the knowledge base with **JS/TS package names** per provider and aggregator entries.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `flow-detection`: add TypeScript/JavaScript import detection and aggregator-library detection.
- `jurisdiction-classification`: the KB gains JS/TS package names per provider and aggregator entries
  resolving to `unknown`.

## Impact

- `borderlint/detect.py` (a regex-based JS/TS import scanner), `borderlint/kb.py` (JS package lookup),
  `borderlint/data/providers.json` (npm names + aggregator entries). No new runtime dependencies —
  regex, not tree-sitter.

## Non-goals

- Inferring a jurisdiction for an aggregator or a dynamic / `base_url` / env-supplied endpoint —
  runtime-determined values stay `unknown` by design.
- Full TypeScript type analysis or an AST parser; a regex over import/require statements suffices.
- Languages beyond TS/JS (Go, Java, …) — later.
