## Context

`kb-refresh.yml` runs `kb_drift.py` weekly and updates the open "KB freshness: items to
review" issue in place. Verified on 2026-07-23: the 2026-07-20 scheduled run fired and
PATCHed issue #39 successfully, but the body was byte-identical to the previous week's, so
GitHub left `updated_at` at 2026-07-13 — the issue looked untouched despite a healthy run.
The report already renders a leading summary line ("The report leads with an actionable
summary"), and the deterministic-diff requirement already names "a supplied reference date"
as an input, so a run date in the report is spec-consistent.

## Goals / Non-Goals

**Goals:** the issue's `updated_at` always reflects the latest run; a reader can see when the
check last ran without opening Actions logs.
**Non-Goals:** changing finding semantics; any new GitHub API interaction; notification
mechanisms.

## Decisions

### D1 — The heartbeat is a date in the report body, not a comment or title change
**Decision:** `render_report` takes the reference date and appends it to the leading summary
line as `· checked YYYY-MM-DD`. `main` passes the same `dt.date.today()` it already computes
for the staleness check, so the whole report stays a pure function of one reference date.
**Rationale:** A changed body makes the existing weekly PATCH a real edit, which bumps
`updated_at` — and issue body edits send no notifications, so watchers are not spammed. The
date also documents, inside the issue itself, which upstream snapshot the findings reflect.
**Alternatives rejected:**
- *Comment on no-change weeks.* Rejected: comments notify every watcher weekly; the heartbeat
  would become the noisiest part of the repo.
- *Force a non-no-op edit (e.g. trailing whitespace churn, dummy HTML comment).* Rejected: an
  invisible mutation is dishonest; the date line is both the heartbeat and useful content.
- *Encode the date in the issue title.* Rejected: retitling breaks the update-in-place lookup,
  which matches on the exact title (same reason the residue change rejected title churn).

### D2 — Date only, not a timestamp
**Decision:** `YYYY-MM-DD`, matching the KB `updated` field format and the staleness check's
granularity. A weekly job needs no finer resolution, and date-only keeps the rendered report
deterministic within a day (manual `workflow_dispatch` re-runs the same day stay no-ops,
which is correct — nothing new could have been checked).
**Alternatives rejected:**
- *Full UTC timestamp.* Rejected: makes same-day dispatch re-runs dirty the issue and adds
  noise (`checked 2026-07-20T09:20:01Z` answers no question the date doesn't).

## Risks / Trade-offs

- **[Summary line grows]** One more clause in a line whose job is scannability. → Accepted:
  `· checked YYYY-MM-DD` is 20 characters and reads as metadata, not a finding.
- **[Fully empty report stays silent]** If a run produces a completely empty report (no
  findings, no residue), the workflow skips the issue update entirely and `updated_at` still
  won't move. → Accepted: the report is currently never empty (residue counts always render),
  and the "no review item on zero findings" behaviour is intentional per the scheduled-check
  requirement.

## Migration Plan

1. `render_report` gains the reference-date parameter and renders it in the summary line.
2. `main` passes the existing `today`.
3. Tests: date renders; identical findings on different dates produce different reports.
4. Rollback: revert; the issue simply goes back to no-op updates on quiet weeks.

## Open Questions

None.
