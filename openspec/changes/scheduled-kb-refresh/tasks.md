## 1. KB provenance

- [ ] 1.1 Add a last-reviewed date field to `providers.json` and expose it (e.g. via the KB / `--version`)

## 2. Coverage check

- [ ] 2.1 Add `scripts/kb_drift.py`: fetch a maintained upstream provider list, diff against the bundled providers, and emit the uncovered providers — assigning no jurisdiction or endpoint
- [ ] 2.2 Add a weekly scheduled GitHub Action (`.github/workflows/kb-refresh.yml`, cron) that runs the script and opens a PR/issue listing the gaps for human curation

## 3. Tests & docs

- [ ] 3.1 Test the drift diff against a fixture upstream list (no network): the uncovered set is correct, and no jurisdiction/endpoint is auto-assigned
- [ ] 3.2 CONTRIBUTING / README note on the KB-freshness loop
