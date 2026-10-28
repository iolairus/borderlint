# Tasks: kb-drift-resolution-8

## 1. Providers and sovereignty

- [x] 1.1 Add `opencode_go` to `borderlint/data/providers.json`: endpoint `opencode.ai`,
  jurisdiction `us`, category `aggregator`, note recording the shared-site host with
  path-scoped API (`/inference/go/`), the EU+US default processing regions, and the
  per-model retention/training variance including the Muse Spark contributor tiers
  (design D1)
- [x] 1.2 Add `opencode_go` → `us` in `borderlint/data/sovereignty.json`
- [x] 1.3 Bump `updated` in `providers.json` and `sovereignty.json` to 2026-10-26

## 2. Provenance

- [x] 2.1 Add qualified patterns `azure/eu/o1`, `azure/eu/o3`, `azure/us/o1`, and
  `azure/us/o3` → OpenAI, bloc `us`; NO bare `o1`/`o3` stems, NO passthrough entry for
  the region segments (design D2)
- [x] 2.2 Add hub-qualified pattern `cloudflare/clairic` → Cloudflare, bloc `us`
  (design D3)
- [x] 2.3 Add `step-5` and `opencode_go/step-5` → StepFun, bloc `cn`; NO bare `step`
  stem (design D4)
- [x] 2.4 Add `baseten/decision-models/baseten-elephant`,
  `baseten/decision-models/baseten-mammoth`, `baselabs/elephant`, and
  `baselabs/mammoth` → `Alibaba (Base Labs post-train)`, bloc `cn`; NO bare
  `elephant`/`mammoth` stems and NO `baseten/decision-models/` wildcard (design D5)
- [x] 2.5 Bump `updated` in `borderlint/data/provenance.json` to 2026-10-27 (pattern
  extension; providers/sovereignty keep their 2026-10-26 review date)

## 3. Tests

- [x] 3.1 Provider test: `opencode.ai` resolves `opencode_go`/us with category
  `aggregator`; sovereignty `us`
- [x] 3.2 Provenance tests: `azure/eu/o1`, `azure/eu/o3`, `azure/us/o1`, `azure/us/o3` →
  us (OpenAI); `cloudflare/clairic` → us (Cloudflare); `step-5-preview` and
  `opencode_go/step-5-preview` → cn (StepFun)
- [x] 3.3 Inheritance test: both `baseten/decision-models/` forms and both `baselabs/`
  HF forms → cn with the base-and-tuner org label
- [x] 3.4 Near-miss tests: `step-up-7b`, `o3unknown`, `elephant-9b`, and `mammoth-27b`
  stay unknown; `o1-preview-clone` still resolves via the pre-existing `o1-` pattern
- [x] 3.5 Tier-2 test: unbound `opencode_go` flow stays provenance `unknown`
- [x] 3.6 Drift-coverage test: `kb_drift.model_coverage_gap` returns no actionable ids
  for the wave-8 upstream keys — the `azure/eu/o*` and `azure/us/o*` id sets, both
  `clairic` forms, both `baseten/decision-models/` ids, and the full `opencode_go/*`
  catalog (suffix walk)

## 4. Verify

- [x] 4.1 Run the full test suite
- [x] 4.2 Run `scripts/kb_drift.py` and confirm the provider and model-family sections
  report zero actionable items (data-practice gaps grow to 99 as `opencode_go` joins
  the standing backlog)
- [x] 4.3 `openspec validate kb-drift-resolution-8 --strict`
