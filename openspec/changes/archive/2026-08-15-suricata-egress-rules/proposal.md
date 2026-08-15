## Why

The static scan sees the code; it cannot see runtime egress — an env-configured base URL, an agent's tool call, a laptop process outside the repo. The provider KB already knows every AI endpoint host, so the residency policy can be compiled into network detection rules that catch violating AI egress where it actually happens: on the wire.

## What Changes

- Add `--format suricata` to `borderlint scan`: emit a Suricata ruleset derived from the provider KB and the policy, not from scan findings.
- With a policy: one `alert` rule per KB endpoint host whose per-host jurisdiction is outside the expanded allow-list for the active classification; allowed hosts produce no rule; region-scheme providers' hosts always alert (marked region-dependent). Alert posture only — a comment header documents converting to `drop` for IPS deployments.
- Without a policy (inventory mode): one `alert` rule per KB endpoint host — full visibility of AI egress on the network.
- Rules match on TLS SNI, carry the provider, jurisdiction, and reason in `msg`/`metadata`, use `classtype:policy-violation`, and get deterministic sids (stable sort, fixed base) so two runs over the same KB and policy are byte-identical.
- The format is an artifact export, not a gate: exits 0 regardless of violations, like sbom/evidence/html/badge.

## Capabilities

### New Capabilities
- `suricata-egress-rules`: compiling the provider KB and residency policy into a Suricata TLS-SNI alert ruleset for network-level detection of disallowed AI egress.

### Modified Capabilities
- `cli-and-reporting`: `--format` gains `suricata`; the non-gating export list gains the new format.

## Impact

- `borderlint/report.py`: new `suricata(findings, kb, policy)` renderer (reads KB + policy; ignores findings by design).
- `borderlint/cli.py`: format choice + non-gating export list.
- No KB changes; no new dependencies; SARIF/evidence/other formats unchanged.

## Non-goals

- No enforcement semantics (default-deny allowlists are firewall/proxy artifacts, not Suricata rules) — a plain host-list export can follow as a separate change if wanted.
- No HTTP-host or QUIC rule variants in v1; TLS SNI only.
- No per-region rule splitting for region-scheme providers (see design ceiling).
