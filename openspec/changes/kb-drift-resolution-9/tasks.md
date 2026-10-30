# Tasks: kb-drift-resolution-9

## 1. Providers and sovereignty

- [x] 1.1 Alias `bigmodel` → `zhipu` in `scripts/kb_drift_aliases.json` and enrich
  the `zhipu` entry's note in `borderlint/data/providers.json` (operator entity,
  domestic/international split, Vidu not-strictly-first-party nuance) — NO new
  provider entry: `open.bigmodel.cn` was already a `zhipu` endpoint (design D1)
- [x] 1.2 Add `streamlake`: endpoints `vanchin.streamlake.ai` and
  `wanqing.streamlakeapi.com`, jurisdiction `cn`, note recording the STREAMLAKE
  PTE. LTD. Singapore operating entity and the Kuaishou/Beijing parent (design D2)
- [x] 1.3 Add `kyma`: endpoint `kymaapi.com`, jurisdiction `us`, category
  `aggregator`, note recording the DeepSeek-direct PRC routing disclosure (design D3)
- [x] 1.4 Add `aiand`: endpoint `api.aiand.com`, jurisdiction `jp`, note recording
  the Japan data-residency commitment (design D5)
- [x] 1.5 Add `clf_ai_gateway`: endpoint `api.clfaigateway.dev`, jurisdiction `vn`,
  category `aggregator`, note recording not-affiliated-with-Cloudflare and the
  Workers AI upstream (design D3)
- [x] 1.6 Add `zerogpu`: endpoint `api.zerogpu.ai`, jurisdiction `us`, note recording
  the not-Hugging-Face-ZeroGPU distinction (design D3)
- [x] 1.7 Add `refuseless`: endpoint `api.refuseless.com`, jurisdiction `unknown`,
  note recording the undisclosed operator and the cn-base lineup (design D4)
- [x] 1.8 Add `eu_jev`: endpoint `eu-jev.com`, jurisdiction `eu`, note recording
  Bevelites GmbH and the Germany-hosted first-party model (design D6)
- [x] 1.9 Add the seven mappings to `borderlint/data/sovereignty.json` (cn, us,
  jp, vn, us, unknown, eu)
- [x] 1.10 Add `vn` to `_SOVEREIGNTY_BLOCS` in `borderlint/kb.py`, a `vn` source
  citation (Law on Cybersecurity 2018 + PDPL 2025) in `sovereignty.json`, and a
  `vn` display name in `borderlint/report.py` (design D6b)
- [x] 1.11 Bump `updated` in `providers.json` and `sovereignty.json` to 2026-10-30
- [x] 1.12 Record `abliteration` in `scripts/kb_drift_aliases.json` `ignore`
  (catalog org, no inference API, hosts zero models; judged 2026-10-30)

## 2. Provenance

- [x] 2.1 Add tier-2 provider defaults `soniox` → `us` and `eu_jev` → `eu`, plus the
  dash-anchored `eu-jeff` brand-stem pattern → Bevelites (eu/jev), bloc `eu`; NO bare
  `stt`/`stt-rt`/`stt-async` stems (design D6, D7)
- [x] 2.2 Add `lfm2.` → Liquid AI, bloc `us`; NO bare `lfm` stem (design D8)
- [x] 2.3 Add `baseten/decision-models/baseten-joey` → `Alibaba (Base Labs
  post-train)`, bloc `cn`; NO `baseten/decision-models/` wildcard (design D8)
- [x] 2.4 Add `motif-3` → Motif Technologies, bloc `kr`; NO bare `motif` stem
  (design D8)
- [x] 2.5 Record `abliteration/` and `kyma/sonar` in `scripts/kb_drift_aliases.json`
  `residue` with dated judgments (design D9)
- [x] 2.6 Bump `updated` in `borderlint/data/provenance.json` to 2026-10-30

## 3. Tests

- [x] 3.1 Provider tests: the new endpoints resolve to their providers and
  jurisdictions (`open.bigmodel.cn` → `zhipu`/cn via the pre-existing endpoint; then
  cn, us, jp, vn, us, unknown, eu for the seven new entries); `kyma` and
  `clf_ai_gateway` carry category `aggregator`; sovereignty mappings match
- [x] 3.2 Tier-2 default tests: `soniox/stt-rt-preview`, `soniox/stt-rt-v5`, and an
  unbound `soniox` flow resolve us; `eu_jev/eu-jeff-1.0.0` and `eu_jev/eu-jeff-latest`
  resolve eu via the `eu-jeff` pattern, and an unbound `eu_jev` flow resolves eu via
  the default
- [x] 3.3 Pattern tests: `zerogpu/LFM2.5-1.2B-Instruct` and bare `lfm2.5-7b-chat` →
  us (Liquid AI); `baseten/decision-models/baseten-joey-2b-latest` → cn with the
  base-and-tuner org label; `aiand/motif-technologies/motif-3` → kr (Motif
  Technologies)
- [x] 3.4 Near-miss tests: `stt-9-ultra`, `lfm-turbo-7b`, and `motif-blank-7b` stay
  unknown
- [x] 3.5 No-default tests: unbound flows on `streamlake`, `kyma`, `aiand`,
  `clf_ai_gateway`, `zerogpu`, and `refuseless` stay provenance `unknown`
- [x] 3.6 Residue tests: `abliteration/abliterated-model` and `kyma/sonar` stay
  provenance `unknown`
- [x] 3.7 Drift-coverage test: `kb_drift.model_coverage_gap` returns no actionable
  ids for the wave-9 upstream keys — the full `soniox/*` stt family, both `eu_jev/*`
  ids, both `zerogpu/LFM*` ids, the `baseten/decision-models/baseten-joey-*` id, the
  `aiand/motif-technologies/*` id, and the full `refuseless/*` catalog (suffix walk)

## 4. Verify

- [x] 4.1 Run the full test suite
- [x] 4.2 Run `scripts/kb_drift.py` and confirm the provider and model-family
  sections report zero actionable items (data-practice gaps grow to 106 as the seven
  new providers join the standing backlog)
- [x] 4.3 `openspec validate kb-drift-resolution-9 --strict`
