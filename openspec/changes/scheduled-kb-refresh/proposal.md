## Why

borderlint's value is its provider knowledge base, which drifts as the ecosystem adds providers,
endpoints, and regions. Without a maintenance loop the bundled KB silently goes stale and starts
missing flows. This adds a scheduled coverage check that surfaces gaps for human curation, keeping
the KB fresh while preserving deterministic, offline scans.

## What Changes

- A **weekly scheduled GitHub Action** compares borderlint's bundled providers against a maintained
  upstream provider list (e.g. litellm's registry) and opens a PR/issue listing providers not yet
  covered.
- Discovered gaps are surfaced for **human review** — jurisdictions and endpoint hosts are never
  auto-assigned (that mapping is judgment).
- The bundled KB gains a **provenance stamp** (a last-reviewed date) and remains the pinned, offline
  source for scans (no runtime fetch).

## Capabilities

### New Capabilities
- `kb-freshness`: a scheduled coverage check that reports provider gaps versus an upstream registry,
  for human curation, plus a KB provenance stamp — without changing runtime scan behaviour.

## Impact

- New `scripts/kb_drift.py` (fetch upstream, diff coverage, emit gaps), a scheduled
  `.github/workflows/kb-refresh.yml`, and a last-reviewed date field in `providers.json`. No change
  to the scanner, classifier, or policy; no new runtime dependency (the script is dev/CI-only).

## Non-goals

- Auto-assigning jurisdictions or endpoint hosts — that is human judgment.
- Fetching the registry at scan time — scans stay deterministic and offline.
- Locking to one upstream — the script targets a maintained source, which may change over time.
