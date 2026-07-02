## ADDED Requirements

### Requirement: Optional sovereignty policy block
The system SHALL accept an optional `sovereignty` block in the policy. When the block is absent,
no sovereignty evaluation SHALL occur and no `sovereignty` finding reason SHALL be produced, so
that existing policies behave identically to before. When present, the block MAY declare
per-classification sovereignty allow-lists, an `on_unknown` setting (`warn` or `fail`, default
`warn`), and inclusion of `sovereignty` in `fail_on`.

#### Scenario: Absent sovereignty block leaves behaviour unchanged
- **WHEN** a policy has no `sovereignty` block
- **THEN** no flow is ever evaluated for sovereignty and no `sovereignty` reason is produced

#### Scenario: A classification declares a sovereignty allow-list
- **WHEN** the `sovereignty` block maps `customer-pii` to the allow-list `eu`, `uk`, `local`
- **THEN** flows for the `customer-pii` classification are evaluated against that sovereignty allow-list

### Requirement: Sovereignty deny-by-default evaluation
A flow whose sovereignty is not on the allow-list for the active classification's sovereignty block SHALL be reported as a `sovereignty` reason; a flow whose sovereignty is on the allow-list SHALL pass the sovereignty check. A flow with sovereignty `unknown` SHALL be treated according to the `on_unknown` setting. A flow with sovereignty `local` SHALL NOT count as a sovereignty violation regardless of the allow-list, mirroring the residency `local` exemption, because self-hosted inference has no external sovereign. Every sovereignty evaluation MUST respect the active classification's declared allow-list.

#### Scenario: Sovereignty outside the allow-list
- **WHEN** the `customer-pii` sovereignty allow-list is `eu`, `uk`, `local` and a flow resolves to sovereignty `us`
- **THEN** the flow is reported with a `sovereignty` reason

#### Scenario: Sovereignty within the allow-list
- **WHEN** the `customer-pii` sovereignty allow-list is `eu`, `uk`, `local` and a flow resolves to sovereignty `eu`
- **THEN** the flow passes the sovereignty check

#### Scenario: Local sovereignty is exempt
- **WHEN** a flow resolves to sovereignty `local` and the active sovereignty allow-list does not list `local`
- **THEN** the flow passes the sovereignty check

#### Scenario: Unknown sovereignty configured to warn
- **WHEN** `on_unknown` is `warn` and a flow resolves to sovereignty `unknown`
- **THEN** the flow is reported as a warning and does not fail the run on account of sovereignty

### Requirement: Sovereignty failure set
The `fail_on` set SHALL accept `sovereignty`. When `sovereignty` is in `fail_on` and a flow's
sovereignty reason is a `sovereignty` mismatch (not `unknown`-as-warn), the finding SHALL fail
the run. The default `fail_on` SHALL NOT include `sovereignty`, so that opting into the
sovereignty block without explicitly failing on it produces warnings only.

#### Scenario: Sovereignty failure when fail_on includes sovereignty
- **WHEN** `fail_on` includes `sovereignty` and a flow's sovereignty is outside the allow-list
- **THEN** the finding fails the run

#### Scenario: Sovereignty warns by default
- **WHEN** `fail_on` does not include `sovereignty` and a flow's sovereignty is outside the allow-list
- **THEN** the finding is a warning and does not fail the run

### Requirement: Waiver applies to sovereignty findings
A waiver with a non-empty justification SHALL downgrade a sovereignty failure to the `waived`
state, consistent with the residency waiver behaviour. A waiver SHALL NOT override an explicit
provider deny-list entry.

#### Scenario: Justified waiver on a sovereignty failure
- **WHEN** a flow that would fail the sovereignty allow-list carries a waiver with a justification
- **THEN** the finding is `waived` and does not contribute to the exit code
