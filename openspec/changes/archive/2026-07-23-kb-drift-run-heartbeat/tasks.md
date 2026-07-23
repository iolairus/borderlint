## 1. Drift checker

- [x] 1.1 `render_report` in `scripts/kb_drift.py` takes the reference date as a required parameter (no default — the report stays a pure function of one reference date) and appends `· checked YYYY-MM-DD` to the leading summary line on **both** head variants (`**Actionable:**` and `**Nothing actionable.**`) (D1, D2)
- [x] 1.2 `main` passes its existing `dt.date.today()` to `render_report` (D1)

## 2. Tests

- [x] 2.1 Adapt the eight existing `render_report` call sites in `tests/test_borderlint.py` (lines ~386–448) to pass a fixed reference date; assertions must keep passing
- [x] 2.2 The rendered report states the supplied reference date in the summary line — exercised on both head variants (actionable findings present, and residue-only)
- [x] 2.3 Two renders with identical findings but different reference dates produce different report bodies (the weekly issue update is never a no-op)

## 3. Validation

- [x] 3.1 Full test suite passes and `openspec validate kb-drift-run-heartbeat --strict` is clean
- [x] 3.2 Live `python3 scripts/kb_drift.py` run shows the date in the summary line
