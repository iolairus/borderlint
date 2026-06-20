## ADDED Requirements

### Requirement: SBOM diff mode
The CLI SHALL provide a `diff` command that takes two AI data-flow SBOM documents — a baseline and a
current one — and reports, in human-readable and JSON form, the data flows added and removed between
them. A flow is the pair (provider id, jurisdiction) for each jurisdiction in a component's
`jurisdictions` list; provider identity is the component id, not its display name. The command defines
its own exit status, independent of the policy-violation gate of `scan`: it SHALL exit 1 when the
current SBOM introduces a flow to a non-`local` jurisdiction (including `unknown`) that is absent from
the baseline, SHALL exit 0 otherwise (removed-only or `local`-only changes do not gate), and SHALL exit
2 when an input is not a valid `borderlint.ai-dataflow-sbom/1` document. Removed flows SHALL be reported
but SHALL NOT affect the exit status.

#### Scenario: A new cross-border flow gates the build
- **WHEN** the current SBOM contains a (provider, jurisdiction) flow to a non-`local` jurisdiction absent from the baseline
- **THEN** the command reports it as added and exits 1

#### Scenario: A new unknown-jurisdiction flow gates the build
- **WHEN** the only added flow is to the `unknown` jurisdiction
- **THEN** the command reports it as added and exits 1

#### Scenario: A new local-only flow does not gate
- **WHEN** the only added flow is to the `local` jurisdiction
- **THEN** the command reports it as added and exits 0

#### Scenario: Removed flows do not gate
- **WHEN** a flow present in the baseline is absent from the current SBOM and no non-`local` flow was added
- **THEN** the command reports it as removed and exits 0

#### Scenario: Swapping the inputs inverts added and removed
- **WHEN** the baseline and current documents are exchanged
- **THEN** a flow previously reported as added is reported as removed

#### Scenario: Non-SBOM input is rejected
- **WHEN** an input file is not a `borderlint.ai-dataflow-sbom/1` document
- **THEN** the command exits 2
