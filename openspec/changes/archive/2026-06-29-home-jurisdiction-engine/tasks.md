## 1. Data file

- [x] 1.1 Add `borderlint/data/regimes.json` as an envelope `{"updated": "<date>", "regimes": {"<jurisdiction>": {"regime": ..., "arrangements": []}}}` (matching `arrangements.json`), seeded with the current mappings only (`hk`→PDPO, `mo`→Macao PDPA, `cn`/`CN-GBA`→PIPL), each with an empty `arrangements` list.

## 2. Regime map loader + resolution (report.py)

- [x] 2.1 Load `regimes.json` at import alongside `arrangements.json`; add `regime_of(j)` reading the map (replaces the `_REGIME_OF` dict).
- [x] 2.2 Rewrite `_regimes()` to derive tags from `regime_of(home_location)` and `regime_of(dest)` for each flagged destination; preserve the legacy `home_regime` path unchanged. (Requirement: Regime tags)
- [x] 2.3 Rewrite `_arrangements()` to surface `regimes.json[home].arrangements` for any flagged cross-border flow, keeping the GBA-span, plain-`cn`→PIPL, and EU/EEA→GDPR selections as verbatim special-cases; preserve the legacy `home_regime` path. (Requirements: Arrangement reference links, Home location)
- [x] 2.4 Handle an unmapped `home_location`: no home regime tag, no home-derived arrangement, no error. (Requirement: Home location)

## 3. uk alias + home_location validation (policy.py / cli.py)

- [x] 3.1 Add `uk`→`gb` normalisation applied in `policy._allowed` and when reading `home_location`. (Requirement: United Kingdom token alias)
- [x] 3.2 Validate `home_location` format (recognised special token or two-letter lowercase code after normalisation); warn on stderr for a malformed value, never change the exit code. (Requirement: Home location declaration)

## 4. Tests

- [x] 4.1 Regression: hk/mo/cn/CN-GBA regime-tag and arrangement output is identical to pre-change (covers existing scenarios).
- [x] 4.2 `uk` in an allow-list permits a `gb` flow; `home_location: uk` behaves as `gb`. (jurisdiction-classification scenarios)
- [x] 4.3 An unmapped `home_location` degrades gracefully (no tag, no arrangement, no failure). (cli-and-reporting scenario)
- [x] 4.4 A malformed `home_location` warns but does not change the exit code. (residency-policy scenario)
- [x] 4.5 An unmapped destination contributes no regime tag. (cli-and-reporting scenario)

## 5. Validate

- [x] 5.1 `openspec validate home-jurisdiction-engine --strict` passes; full pytest suite green.
