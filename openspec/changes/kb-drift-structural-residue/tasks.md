## 1. Suppression data

- [ ] 1.1 Add a `residue` block to `scripts/kb_drift_aliases.json`: prefixes for the timeless classes (`fireworks-ai-`, `together-ai-` pricing buckets; `fal_ai/` path ids) plus a bulk seed of every remaining currently-uncovered id as an exact key, generated from a live run at implementation time, reason "reviewed 2026-07-05: nothing actionable in the current list" (D1, D2)
- [ ] 1.2 Move the seven surfacing providers (darkbloom, pinstripes, llamagate, morph, reducto, text-completion-inception, tensormesh) to the ignore list with reasons recording the 2026-07-05 review (D2)

## 2. Drift checker

- [ ] 2.1 Validate residue reasons non-empty in `validate_suppression` (raise naming the entry) (D2, "Acknowledged structural residue is separated from actionable items")
- [ ] 2.2 Split `model_coverage_gap`'s output: uncovered ids matching a residue entry (lowercase full-key prefix; exact keys are their own prefix) grouped per entry; the rest actionable (D1)
- [ ] 2.3 `render_report`: leading summary line (actionable providers, actionable families, residue id count); residue section as a collapsed `<details>` block with reason + count per class (D3, "The report leads with an actionable summary")

## 3. Tests

- [ ] 3.1 Classification after matching: residue-prefixed uncovered id counted, covered id unaffected; unacknowledged id stays actionable
- [ ] 3.2 Empty-reason residue entry raises; shipped residue block validates
- [ ] 3.3 Summary line counts; residue section renders counts not id lists

## 4. Validation

- [ ] 4.1 Full suite + `openspec validate kb-drift-structural-residue --strict`; live run shows the actionable/residue split and the summary line
