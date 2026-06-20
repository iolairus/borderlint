## Why

HK and GBA entities are wiring LLMs and agents into products but cannot answer, from their own
codebase, where AI data and traffic flow — and whether that honours their PDPO agreed-locations or
PIPL obligations. Existing tools are runtime gateways with an EU lens; none govern the east-west
boundary statically, in CI, before code ships. borderlint closes that gap.

## What Changes

- Introduce `borderlint`, a static CLI that scans a repo, detects AI provider usage, resolves each
  flow to a jurisdiction, and checks it against a classification-keyed residency policy — failing
  CI on violations.
- Detect AI provider **SDK imports** and **endpoint references** in Python and config/text files.
- Bundle a vendor-neutral, **east-west** provider knowledge base (Western providers plus Tencent,
  Alibaba, DeepSeek, …) mapping each to a jurisdiction, honouring region-specific endpoints
  (e.g. `dashscope-intl` → `sg`) and the `CN-GBA` / `GBA` tokens.
- Policy is a user-provided **JSON eval-set**: data classification
  (`non-pii` | `employee-pii` | `customer-pii`) → allow-list of jurisdiction codes; **deny-by-default**.
  A per-run `--classification` declares the data class on the scanned path.
- Support **provider allow/deny lists**, a configurable **failure set** (which findings fail the
  run), and a declared **home regime** (`pdpo` | `pipl`) that selects which arrangement references
  are surfaced.
- Output: human-readable CLI, JSON, and a Mermaid flow map; non-zero exit on violations; the
  relevant cross-border arrangement (e.g. GBA Standard Contract) surfaced as a reference link.

## Capabilities

### New Capabilities
- `flow-detection`: locate AI provider usage (SDK imports + endpoint references) in Python and
  config/text files, producing detections with `file:line` evidence.
- `jurisdiction-classification`: a bundled east-west provider knowledge base that resolves each
  detection to a jurisdiction (ccTLD/ISO codes plus `CN-GBA` / `GBA`), honouring region-specific
  endpoints and marking region-in-endpoint providers as unknown.
- `residency-policy`: the classification-keyed JSON eval-set, the per-run classification input, and
  deny-by-default evaluation of flows into pass/fail verdicts; plus provider allow/deny lists, a
  configurable failure set, and a declared home regime.
- `cli-and-reporting`: the `scan` CLI (`--policy`, `--classification`), text/JSON/Mermaid reporters,
  CI exit codes, and arrangement reference links.

### Modified Capabilities
- None — greenfield; `openspec/specs/` is empty.

## Impact

- New Python package with a console entry point (`borderlint`), a PyYAML dependency, and a pytest
  suite.
- New bundled data file (the provider knowledge base). No external services; deterministic and
  offline.
- Consumers integrate it as a CI step on the path to production.

## Non-goals

- Not a runtime gateway/proxy, DLP, or general SAST; the single concern is AI data residency.
- Not a global residency solver — v1 is for HK/GBA home bases (PDPO / PIPL / GBA).
- Does not adjudicate which legal arrangement applies (links only); no per-city `CN-GBA` resolution.
- TypeScript scanning, SARIF, GitHub Action, and LLM enrichment are later phases, out of this change.
