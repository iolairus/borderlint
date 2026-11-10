# Tasks: kb-drift-resolution-10

## 1. Providers and sovereignty

- [x] 1.1 Add `empiriolabs` to `borderlint/data/providers.json`: endpoint
  `api.empiriolabs.ai`, jurisdiction `us`, category `aggregator`, note recording the
  New Mexico LLC / Seattle entity, the multi-source ToS disclosure, per-model author
  pages, and aplomb-1 as the only first-party model (design D1)
- [x] 1.2 Add `hostinger_router`: endpoint `router.hostinger.com`, jurisdiction `eu`,
  category `aggregator`, note recording the Cyprus/Luxembourg contracting entities,
  Kaunas group HQ, and undisclosed upstream inference locations (design D2)
- [x] 1.3 Add `wally`: endpoint `inference.runanywhere.ai`, jurisdiction `us`, note
  recording RunAnywhere, Inc. (Delaware, Redwood City), the fixed cn-origin open-weight
  catalog, and default ZDR (design D3)
- [x] 1.4 Add the three mappings to `borderlint/data/sovereignty.json` (us, eu, us)
- [x] 1.5 Bump `updated` in `providers.json` and `sovereignty.json` to 2026-11-10

## 2. Provenance

- [x] 2.1 Add `empiriolabs/perplexity-` → Perplexity, `us` (qualified; NO bare
  `perplexity-` stem) (design D5)
- [x] 2.2 Add `seed-2-` → ByteDance, `cn` and `step-3-` → StepFun, `cn`
  (dash anchors beside the existing dot anchors) (design D4)
- [x] 2.3 Add `stepaudio-` → StepFun, `cn`; `tongyi-embedding-vision` → Alibaba,
  `cn`; `skylark-embedding` → ByteDance, `cn` (NO bare `skylark`) (design D5)
- [x] 2.4 Add `fugu-` → Sakana AI, `jp` (design D5)
- [x] 2.5 Add `aplomb-1` → `Alibaba (EmpirioLabs post-train)`, `cn` (design D7)
- [x] 2.6 Add `jina-reranker-m0` and `jina-reranker-v3.5` → `Alibaba (Jina AI
  post-train)`, `cn` (exact version-anchored stems; `jina_ai` default unchanged)
  (design D6)
- [x] 2.7 Add `grok4.` → xAI, `us` (design D5)
- [x] 2.8 Add `ripple-65b` → Ricursive Intelligence, `us` and `rnj-1` → Essential AI,
  `us` (design D5)
- [x] 2.9 Record `together_ai/elorian-labs/glimpse-1.0` in
  `scripts/kb_drift_aliases.json` `residue` (base lineage undisclosed; judged
  2026-11-10) (design D8)
- [x] 2.10 Bump `updated` in `borderlint/data/provenance.json` to 2026-11-10

## 3. Tests

- [x] 3.1 Provider tests: the three endpoints resolve to their providers and
  jurisdictions (us, eu, us); `empiriolabs` and `hostinger_router` carry category
  `aggregator`; sovereignty mappings match
- [x] 3.2 Reseller-qualified test: `empiriolabs/perplexity-sonar-pro` and
  `empiriolabs/perplexity-advanced-deep-research` → us (Perplexity)
- [x] 3.3 Dash-anchor tests: `seed-2-0-pro`, `seed-2-1-turbo`, `step-3-5-flash`,
  `step-3-5-flash-2603`, `step-3-7-flash` resolve to cn (ByteDance/StepFun), and the
  dot-anchored `seed-2.0-pro` / `step-3.5-flash` still resolve as before
- [x] 3.4 cn-family tests: `stepaudio-2-5-chat` → StepFun, `tongyi-embedding-vision-
  flash` → Alibaba, `skylark-embedding-vision` → ByteDance; `fugu-max` and
  `fugu-ultra-v2-0` → jp (Sakana AI)
- [x] 3.5 Inheritance tests: `aplomb-1` → cn with `Alibaba (EmpirioLabs post-train)`;
  `jina-reranker-m0` and `jina-reranker-v3.5` → cn with `Alibaba (Jina AI
  post-train)`; `jina_ai` unbound flow stays eu
- [x] 3.6 us-lab tests: bare `grok4.6` → xAI/us; bare `ripple-65b-preview` → Ricursive
  Intelligence/us; bare `rnj-1-instruct` → Essential AI/us
- [x] 3.7 Near-miss tests: `seed-9`, `step-up-7b`, `skylark-7b`, `ripple-effect-3b`,
  `perplexity-clone` stay unknown
- [x] 3.8 No-default tests: unbound flows on `empiriolabs`, `hostinger_router`, and
  `wally` stay provenance `unknown`
- [x] 3.9 Residue test: `together_ai/elorian-labs/glimpse-1.0` splits to residue with
  zero actionable
- [x] 3.10 Drift-coverage test: `kb_drift.model_coverage_gap` returns no actionable
  ids for the wave-10 upstream keys — the full 23-id `empiriolabs/*` catalog, both
  jina rerankers, `gmi/xai/grok4.6`, `gmi/gmicloud/Ripple-65B-Preview`, and
  `together_ai/ricursive-ai/Ripple-65B-Preview`, `together_ai/essentialai/rnj-1-instruct`

## 4. Verify

- [x] 4.1 Run the full test suite
- [x] 4.2 Run `scripts/kb_drift.py` and confirm the provider and model-family
  sections report zero actionable items (data-practice gaps grow to 109 as the three
  new providers join the standing backlog)
- [x] 4.3 `openspec validate kb-drift-resolution-10 --strict`
