## Why

The headline CI question for a sovereignty tool is "**what new cross-border flows did this PR
introduce?**" Today a reviewer has to eyeball two full reports. The D5 SBOM is byte-deterministic
precisely so two of them can be diffed mechanically. This adds a `diff` command that compares a
baseline SBOM against the current one and gates the build when the PR opens a new place data can go.

## What Changes

- **`borderlint diff <baseline-sbom> <current-sbom>`** — compare two AI data-flow SBOMs and report the
  flows **added** and **removed**, at provider-and-jurisdiction granularity.
- **Gates CI** — exits non-zero when the PR introduces a flow to a non-`local` jurisdiction absent from
  the baseline (a new provider, or an existing provider now reaching a new jurisdiction). Removed flows
  are reported but never gate.
- **text + JSON** output; operates purely on the two SBOM documents — no KB, no policy (names come from
  the SBOMs themselves). Relies on the SBOM determinism shipped in D5.

## Capabilities

### Modified Capabilities
- `cli-and-reporting`: a new `diff` subcommand alongside `scan`.

## Impact

- A `diff` subcommand + a pure `report.diff_flows(old, new)` helper. Scanner and policy engine
  unchanged. No new dependency.

## Non-goals

- Generating the baseline. CI does the git work (check out the base branch, `scan --format sbom`); the
  `diff` command consumes two finished documents.
- Policy-aware diffing (allow-list deltas). `diff` is structural — it reports *new egress*; pair it with
  `scan` for the policy verdict.
