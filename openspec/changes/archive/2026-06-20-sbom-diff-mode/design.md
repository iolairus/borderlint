## Context

D5 ships a deterministic, policy-independent SBOM. Two of them (base branch vs PR) can now be compared
byte-for-byte. D6 is that comparison surfaced as a CI gate: "did this PR add a new place data goes?"

## Goals / Non-Goals

**Goals:** a `diff` command over two SBOM documents; report added/removed flows; gate on new egress.

**Non-Goals:** producing the baseline (CI/git's job); policy-aware diffing; site-level churn reporting.

## Decisions

- **Separate `diff` subcommand over two SBOM files, not `scan --baseline`.** Single responsibility; the
  deterministic SBOM is the interchange format (this is what D5's determinism was for). CI already
  checks out the base branch and runs `scan --format sbom` twice, then diffs the two files.
- **Flow granularity = (provider id, jurisdiction).** A flow is extracted as `(component.id, j)` for
  each `j` in the component's **`jurisdictions`** list — the component-level set, not per-site
  jurisdiction (per-site disagreement could surface the same logical flow as both added and removed).
  Identity is the component id, never the display name. Alternative: site-level (file:line). Rejected —
  moving a call between files is not a new flow; *a new place data goes* is the signal.
- **`diff` owns its exit codes**, independent of the `scan` policy gate: exit 1 = new non-`local`
  egress, exit 0 = no new egress, exit 2 = invalid input. The two non-zero codes are distinct so a CI
  consumer can tell "review this flow" (1) from "fix your SBOM pipeline" (2).
- **Gate on added non-`local` flows.** `local` additions are on-device inference, not egress → never
  gate. `unknown` additions DO gate (egress to an undetermined place is exactly the risk). Removed flows
  are reported but never gate (a PR that stops sending data abroad must not fail).
- **Input validation at the trust boundary.** Both files MUST be `borderlint.ai-dataflow-sbom/1`
  documents; a parse error or wrong/missing schema → exit 2. `# ponytail: input validation is not lazy`.
- **KB/policy-independent.** Provider display names come from the SBOM documents themselves, so `diff`
  needs neither the KB nor a policy.

## Risks / Trade-offs

- Provider-jurisdiction granularity misses a same-flow region change (e.g. Bedrock `us` → `eu` is caught,
  but two `us` regions collapse) → acceptable; jurisdiction is the residency-relevant unit.
- Gating on any new non-local flow may be noisy for repos that add providers often → the signal is the
  point; a future `--fail-on` scope is additive if needed.
