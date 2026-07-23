## Why

The weekly `kb-refresh` run updates issue #39 in place — by design, so persistent conditions
don't spawn duplicates. But when the report is unchanged week over week (the common case now
that residue is acknowledged), the issue update is a content no-op: GitHub does not bump the
issue's `updated_at`, so the issue's last activity reads as weeks stale even though the check
ran on schedule. A reviewer cannot tell "the check ran and found nothing new" from "the check
never fired" without digging into Actions logs — which is exactly what happened on 2026-07-23.

## What Changes

- The freshness report states the **run's reference date** in its leading summary line
  (e.g. "… · checked 2026-07-20"). Two runs a week apart with identical findings now produce
  different bodies, so the in-place issue update is never a no-op and `updated_at` reflects
  the latest run.
- No new API calls, no comments, no title changes: the heartbeat rides on the existing
  update-in-place mechanism.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kb-freshness`: the report summary requirement gains the run-date statement, so the review
  item's last-updated timestamp always reflects the most recent scheduled run.

## Impact

- `scripts/kb_drift.py` (`render_report` gains the reference date; `main` passes it), tests.
- Issue #39's `updated_at` becomes a reliable "last checked" signal.

## Non-goals

- No change to what counts as actionable, covered, or residue.
- No comment-based heartbeat (weekly notification spam for watchers).
- No auto-close or escalation logic for long-quiet periods.
