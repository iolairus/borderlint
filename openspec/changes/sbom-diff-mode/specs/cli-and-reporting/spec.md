## ADDED Requirements

### Requirement: SBOM diff mode
The CLI SHALL provide a `diff` command that takes two AI data-flow SBOM documents — a baseline and a
current one — and reports the data flows added and removed between them at provider-and-jurisdiction
granularity. The command SHALL exit non-zero when the current SBOM introduces a flow to a non-`local`
jurisdiction that is absent from the baseline, and zero otherwise; removed flows SHALL be reported but
SHALL NOT affect the exit status. The command SHALL reject an input that is not a
`borderlint.ai-dataflow-sbom/1` document with a non-zero error status.

#### Scenario: A new cross-border flow gates the build
- **WHEN** the current SBOM contains a (provider, jurisdiction) flow to a non-`local` jurisdiction that is absent from the baseline
- **THEN** the command reports it as added and exits with a non-zero status

#### Scenario: Removed flows do not gate
- **WHEN** a flow present in the baseline is absent from the current SBOM and no non-`local` flow was added
- **THEN** the command reports it as removed and exits with a zero status

#### Scenario: A new local-only flow does not gate
- **WHEN** the only added flow is to the `local` jurisdiction
- **THEN** the command reports it as added and exits with a zero status

#### Scenario: Non-SBOM input is rejected
- **WHEN** an input file is not a `borderlint.ai-dataflow-sbom/1` document
- **THEN** the command exits with a non-zero error status
