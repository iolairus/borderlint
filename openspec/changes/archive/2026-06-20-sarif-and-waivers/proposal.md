## Why

Two things gate real-world CI adoption: findings should surface where engineers already look
(GitHub code-scanning consumes **SARIF**), and teams need a *reviewed* way to accept a known
cross-border flow without disabling the gate (a **waiver with justification**). This change adds both.

## What Changes

- **SARIF output** — emit findings as SARIF JSON, one result per finding (rule, level, `file:line`,
  message), so they appear in GitHub code-scanning.
- **Inline waivers** — a `borderlint: allow <reason>` comment on, or immediately above, a flagged
  flow marks it **waived** (not a violation). The justification is required and shown in the report;
  a waiver with no reason is ignored, so there is no silent blanket disable.

## Capabilities

### Modified Capabilities
- `cli-and-reporting`: a SARIF output format; waived findings rendered distinctly.
- `flow-detection`: recognise inline waiver annotations and capture their justification.
- `residency-policy`: a validly-waived flow is not a violation.

## Impact

- `borderlint/report.py` (SARIF renderer + waived rendering), `borderlint/detect.py` (waiver-comment
  scan), `borderlint/policy.py` (waived → not a violation), `borderlint/cli.py` (`sarif` format).
  No new dependencies — SARIF is JSON.

## Non-goals

- Policy-file / global waivers — this is the inline form; a centralised waiver list can come later.
- Waivers that *hide* a finding — waived flows are still reported, just not failed.
- Auto-expiring waivers or approval workflows.
