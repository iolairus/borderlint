# Tasks: kb-drift-resolution-7

## 1. Providers and sovereignty

- [x] 1.1 Add `coralbricks` to `borderlint/data/providers.json`: endpoint
  `inference.coralbricks.ai`, jurisdiction `us`, note recording the SF operator and the
  SCC-based outside-US processing caveat (design D1)
- [x] 1.2 Add `inferenceapis` to `providers.json`: endpoint `api.inferenceapis.com`,
  jurisdiction `us`, category `aggregator`, note recording the gateway shape (Together
  AI + DeepInfra upstream) and the unestablished legal entity (designs D1, D2)
- [x] 1.3 Add `nace` to `providers.json`: endpoints `console.nace.ai` and
  `drex.nace.ai`, jurisdiction `us`, note recording both hostnames serve the same
  decision-model API (design D1)
- [x] 1.4 Add `openinfer` to `providers.json`: endpoint `api.openinfer.ai`,
  jurisdiction `us`, note recording the `@oi/` third-party serving and the
  open-infer.org disambiguation (design D1)
- [x] 1.5 Add all four providers → `us` in `borderlint/data/sovereignty.json`
- [x] 1.6 Bump `updated` in `providers.json` and `sovereignty.json` to 2026-10-20

## 2. Provenance

- [x] 2.1 Add `semantic-ranker` and `vertex_ai/semantic-ranker` → Google, bloc `us`
- [x] 2.2 Add qualified `meta/sam` → Meta, bloc `us`; NO bare `sam` stem (design D4)
- [x] 2.3 Add `happyhorse` → Alibaba, bloc `cn`; add `wan2.` and `wan3.` →
  `Alibaba (Wan-AI)`, bloc `cn`; NO bare `wan` stem (design D4)
- [x] 2.4 Add `beam`, `reflection/beam`, `baseten/reflection/beam`,
  `together_ai/reflection/beam`, `nebius/reflection/beam` → Reflection AI, bloc `us`
  (design D6)
- [x] 2.5 Add `drex-v1.5`, `drex-v2.0`, `drex-latest` plus qualified `nace/` and HF-org
  `nace-ai/` forms → `Alibaba (Nace Drex post-train)`, bloc `cn` (design D5)
- [x] 2.6 Record `nace/drex-v1.0` as accept-unknown residue in
  `scripts/kb_drift_aliases.json` — base lineage undisclosed in primary sources
  (design D5)
- [x] 2.7 Confirm no tier-2 defaults for the four new providers (design D3); bump
  `updated` in `provenance.json` to 2026-10-20

## 3. Tests

- [x] 3.1 Provider tests: the four endpoint hosts resolve with jurisdiction `us`;
  `inferenceapis` carries category `aggregator`; both Nace hostnames resolve
- [x] 3.2 Provenance tests: semantic-ranker both forms → us; `meta/sam-3.1` → us;
  happyhorse and wan2./wan3. → cn; all five Beam forms → us; Drex v1.5/v2.0/-latest
  (bare, `nace/`, `nace-ai/`) → cn with the base-and-tuner org label
- [x] 3.3 Honest-unknown tests: `nace/drex-v1.0` stays unknown; no tier-2 defaults for
  the four providers
- [x] 3.4 Near-miss tests: hypothetical `sam-3.1` (bare), `wandb/some-org/some-model`,
  and `wander-7b` match no new pattern
- [x] 3.5 Drift-coverage test: `kb_drift.model_coverage_gap` returns no actionable ids
  for the wave-7 upstream keys (suffix walk covers the namespaced forms)

## 4. Verify

- [x] 4.1 Run the full test suite
- [x] 4.2 Run `scripts/kb_drift.py` and confirm the provider and model-family sections
  report zero actionable items (data-practice gaps grow to 98 as the four new providers
  join the standing backlog; residue grows by the v1.0 entry)
- [x] 4.3 `openspec validate kb-drift-resolution-7 --strict`
