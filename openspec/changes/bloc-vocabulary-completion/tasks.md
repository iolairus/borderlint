## 1. Vocabulary

- [x] 1.1 Add `jp`, `kr`, `sg`, `au`, `ae` to `_SOVEREIGNTY_BLOCS` and `_PROVENANCE_BLOCS` in `borderlint/kb.py` and their mirrors in `borderlint/policy.py` (D1, "Sovereignty bloc vocabulary", "Provenance bloc vocabulary")
- [x] 1.2 Add display names for the five blocs to `SOVEREIGNTY` in `borderlint/report.py` (D1)

## 2. Bundled data

- [x] 2.1 Add `sources` entries for `jp`, `kr`, `sg`, `au`, `ae` to `borderlint/data/sovereignty.json`; verify every vocabulary bloc has one (`local`/`unknown` keep their descriptive notes); bump `updated` (D3, "Sovereignty bloc vocabulary")
- [x] 2.2 Add provenance patterns to `borderlint/data/provenance.json`: pinned stems (`falcon-`, `falcon2`, `falcon3`, `solar-`) and distinctive stems (`exaone`, `plamo`, `sarashina`, `elyza`, `sea-lion`, `hyperclova`) with their blocs (D2, "Provenance bloc vocabulary")
- [x] 2.3 Add org-prefix entries: `tiiuae/`→ae; `upstage/`, `lgai-exaone/`, `naver-hyperclovax/`→kr; `sbintuitions/`, `pfnet/`, `tokyotech-llm/`, `rinna/`, `elyza/`→jp; `aisingapore/`→sg; rewrite the `passthrough_orgs_note` sentence that declares Falcon/EXAONE/Solar deliberately absent (now false); bump `updated` (D2)

## 3. Tests

- [x] 3.1 Vocabulary acceptance: policy sovereignty/provenance blocks and user-KB mappings with new tokens load; an invalid token still rejects ("Sovereignty bloc vocabulary", "Provenance bloc vocabulary")
- [x] 3.2 Resolution per new bloc: `tiiuae/falcon-180B` and `falcon-40b-instruct`→ae, `exaone-3.5-7.8b`→kr, `aisingapore/gemma-sea-lion-v4-27b-it`→sg, `pfnet/plamo-2-8b`→jp; `solarwinds-agent` and `falcon` (bare) do not match (D2)
- [x] 3.3 Sources completeness: every vocabulary bloc has a `sources` note (asserts scenario "Every vocabulary bloc carries a source note")
- [x] 3.4 Drift interaction: `model_coverage_gap` no longer reports the now-covered families (fixture with a falcon/exaone id)

## 4. Docs & validation

- [x] 4.1 Update README and CAPABILITIES bloc lists for both dimensions
- [x] 4.2 Run the full test suite and `openspec validate bloc-vocabulary-completion --strict`
