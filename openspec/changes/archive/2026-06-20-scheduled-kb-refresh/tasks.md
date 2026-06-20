## 1. KB provenance

- [x] 1.1 Add a last-reviewed ISO-8601 date to a top-level field in `providers.json`, expose it on load and via `--version`

## 2. Coverage check

- [x] 2.1 Add `scripts/kb_drift.py`: a pure diff of (bundled providers, supplied upstream list) → uncovered provider names with no jurisdiction/endpoint, plus a fetch of a maintained upstream (litellm)
- [x] 2.2 Add a weekly scheduled GitHub Action (`.github/workflows/kb-refresh.yml`, cron) that runs the script and opens an issue/PR listing the gaps for human curation

## 3. Tests & docs

- [x] 3.1 Tests (no network): the diff returns the correct uncovered set; gap records carry no jurisdiction/endpoint; the bundled KB exposes an ISO date; the scanner / KB-load path has no network imports
- [x] 3.2 CONTRIBUTING / README note on the KB-freshness loop
