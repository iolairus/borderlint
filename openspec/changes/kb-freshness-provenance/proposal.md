## Why

The weekly kb-refresh job diffs upstream provider names against `providers.json` and nothing
else. The two newer governance dimensions have no scheduled freshness check: model provenance
(the fastest-churning data in the repo — new model families ship monthly) is never compared
against any upstream, and sovereignty is only indirectly prompted when a brand-new provider
appears — nothing verifies that existing provider entries carry a valid sovereignty bloc. The
`updated` last-reviewed dates on the bundled KBs are honor-system: no check ever reads them.
Both dimension designs promised to fold their data into the kb-freshness machinery; this change
delivers that.

## What Changes

- The weekly drift script produces a **three-section report** from the same single upstream
  fetch (litellm price list — its keys are model identifiers, currently discarded):
  1. **Providers** — the existing name diff, with the review prompt now explicitly asking for a
     sovereignty bloc alongside endpoint and jurisdiction.
  2. **Provenance** — upstream model identifiers matched by no provenance prefix (after
     passthrough-org stripping), aggregated by org/family prefix with a count and one example
     each, so the issue lists families to review rather than thousands of model IDs.
  3. **Sovereignty** — provider ids with no entry in the bundled sovereignty map, or an entry
     outside the bloc vocabulary (sovereignty lives in `sovereignty.json`, not on the provider
     entries).
- A **staleness warning** per bundled KB carrying an `updated` date (providers, provenance,
  sovereignty, regimes, arrangements) when that date is older than the review interval.
- The weekly GitHub issue renders the sections; empty sections are omitted; no issue when all
  sections are empty; an existing open freshness issue is updated rather than duplicated. All
  assignments remain human-curated — never auto-merged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kb-freshness`: the scheduled check extends from provider-name drift to provenance model
  coverage, sovereignty completeness, and KB staleness; the human-assignment rule extends to
  sovereignty and provenance blocs; the deterministic-diff rule covers the new computations.

## Impact

- `scripts/kb_drift.py` — new pure functions (model coverage gap, sovereignty completeness,
  staleness) plus sectioned output; existing functions unchanged.
- `.github/workflows/kb-refresh.yml` — issue body assembled from the sectioned report.
- `tests/` — offline unit tests for each new pure function.
- **Dependency**: requires `provenance.json` from `model-provenance-dimension` (PR #37); this
  change builds on that branch and ships after it.

## Non-goals

- No HF Hub top-N/trending sweep (different upstream, auth, and churn profile — separate change).
- No auto-assignment of jurisdictions, sovereignty, or provenance blocs.
- No scan-path changes: the check stays dev/CI-only; the scanner performs no network access.
