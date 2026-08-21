# Tasks: xiaomi-mimo-coverage

## 1. Provider entry and provenance

- [x] 1.1 Add the `xiaomi_mimo` provider to `borderlint/data/providers.json`: endpoints `api.xiaomimimo.com` (jurisdiction `unknown`) and `token-plan-cn.xiaomimimo.com` (via `endpoint_jurisdictions`, `cn`), name "Xiaomi MiMo", category, no SDK keys per design D4 (D1, D2, D4)
- [x] 1.2 Add provenance patterns to `borderlint/data/provenance.json`: `mimo-` and `novita/xiaomimimo/` → bloc `cn`, org Xiaomi (the literal qualifier form is required — `match_model` anchors at the literal start) (D3)
- [x] 1.3 Retire the drift residue entry for `novita/xiaomimimo/mimo-v2-flash` in `scripts/kb_drift_aliases.json` once the patterns cover it (it can no longer fire) (D3)

## 2. Data practices

- [x] 2.1 Curate the `xiaomi_mimo` entry in `borderlint/data/data_practices.json`: training_default `no`, retention, storage-region note (EU + Singapore), Token Plan tier note; subprocessors null; citations to privacy.mi.com §3.1/§6 and the service agreement §4.4 (D5)

## 3. Tests

- [x] 3.1 Detection tests: endpoint references to both hosts resolve to `xiaomi_mimo` with jurisdictions `unknown` and `cn` respectively
- [x] 3.2 Provenance tests: bare `mimo-v2.5-pro`, qualified `xiaomi/mimo-…`, and `novita/xiaomimimo/mimo-v2-flash` all resolve bloc `cn`
- [x] 3.3 Data-practices tests: entry loads, every non-null fact cited, keys exist in providers.json

## 4. Validation

- [x] 4.1 Run full pytest suite and fix regressions
- [x] 4.2 Run `openspec validate xiaomi-mimo-coverage --strict`
