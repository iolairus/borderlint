## 1. Drift script — pure functions

- [x] 1.1 Add `model_coverage_gap(model_ids, kb)` to `scripts/kb_drift.py`: covered when the key or any of its `/`-suffixes resolves via `kb.match_model`; return uncovered keys (D1, "Model provenance coverage check")
- [x] 1.2 Add `family_stems(uncovered)`: group by leading-alpha stem of the basename, return `(stem, count, example)` sorted by count descending (D2)
- [x] 1.3 Add `sovereignty_gaps(provider_ids, sov_map)`: ids absent from the bundled sovereignty map (`sovereignty.json`) or mapped to a bloc outside the vocabulary (imported from `borderlint.kb`) (D3, "Sovereignty completeness check")
- [x] 1.4 Add `stale_kbs(kb_dates, today, interval_days=90)`: stale entries among all `borderlint/data/*.json` files carrying a top-level `updated` date, with age (D4, "Knowledge base staleness warning")

## 2. Drift script — report assembly

- [x] 2.1 Add `render_report(...)`: sectioned markdown (`### New providers` with jurisdiction+sovereignty prompt, `### Uncovered model families` capped at 50 with omitted-count line, `### Sovereignty gaps`, `### Stale knowledge bases`), empty sections omitted, empty report renders nothing (D5, "Scheduled coverage check")
- [x] 2.2 Rewire `main()`: single upstream fetch, run all checks, print the rendered report; existing provider functions untouched (D5)

## 3. Workflow

- [x] 3.1 Update `.github/workflows/kb-refresh.yml`: issue body is the script output verbatim (drop the code fence), title `KB freshness: items to review`; when output is non-empty, update an existing open issue with that title or create it, never duplicate (D5, "Scheduled coverage check")

## 4. Tests

- [x] 4.1 Offline unit tests for `model_coverage_gap` (qualified-prefix covered, uncovered reported) and `family_stems` (aggregation, ordering)
- [x] 4.2 Offline unit tests for `sovereignty_gaps` (missing, invalid, complete) and `stale_kbs` (stale vs fresh)
- [x] 4.3 Unit tests for `render_report`: section omission, cap disclosure, empty report renders nothing, no bloc/jurisdiction auto-assigned in any record ("Human-assigned jurisdictions", D5)

## 5. Validation

- [x] 5.1 Run the full test suite and `openspec validate kb-freshness-provenance --strict`; run `python3 scripts/kb_drift.py` once live to sanity-check the first-run report shape
