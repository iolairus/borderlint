## ADDED Requirements

### Requirement: Optional provenance policy block
The system SHALL accept an optional `provenance` block in the policy. When the block is absent,
no provenance evaluation SHALL occur and no `provenance` or `provenance_unknown` finding reason
SHALL be produced, so that existing policies behave identically to before. When present, the
block MAY declare per-classification provenance allow-lists and an `on_unknown` setting (`warn`
or `fail`, default `warn`). Provenance bloc tokens in the block SHALL be validated against the
provenance vocabulary at policy load time.

#### Scenario: Absent provenance block leaves behaviour unchanged
- **WHEN** a policy has no `provenance` block
- **THEN** no flow is ever evaluated for provenance and no provenance reason is produced

#### Scenario: Invalid provenance token in the policy is rejected
- **WHEN** a policy's `provenance` block lists the bloc `mars` for a classification
- **THEN** policy loading fails with an error naming the invalid token and the accepted vocabulary

### Requirement: Provenance deny-by-default evaluation
The system SHALL report a `provenance` reason for a flow whose provenance is not on the
allow-list for the active classification's provenance block; a flow whose provenance is on the
allow-list SHALL pass the provenance check. A flow with provenance `unknown` SHALL be reported
with a `provenance_unknown` reason, treated according to the `on_unknown` setting.

#### Scenario: Provenance outside the allow-list
- **WHEN** the `customer-pii` provenance allow-list is `us`, `eu` and a flow resolves to provenance `cn`
- **THEN** the flow is reported with a `provenance` reason

#### Scenario: Provenance within the allow-list
- **WHEN** the `customer-pii` provenance allow-list is `us`, `eu` and a flow resolves to provenance `eu`
- **THEN** the flow passes the provenance check

#### Scenario: Unknown provenance configured to warn
- **WHEN** `on_unknown` is `warn` and a flow resolves to provenance `unknown`
- **THEN** the flow is reported as a warning and does not fail the run on account of provenance

### Requirement: Provenance failure set with a symmetric unknown gate
The `fail_on` set SHALL accept `provenance`. When `provenance` is in `fail_on` and a flow's
reason is a `provenance` mismatch, the finding SHALL fail the run. A `provenance_unknown` reason
SHALL fail the run when the provenance block's `on_unknown` is `fail`, on its own, without also
requiring `provenance` in `fail_on`. The default `fail_on` SHALL NOT include `provenance`.

#### Scenario: Provenance failure when fail_on includes provenance
- **WHEN** `fail_on` includes `provenance` and a flow's provenance is outside the allow-list
- **THEN** the finding fails the run

#### Scenario: Provenance warns by default
- **WHEN** `fail_on` does not include `provenance` and a flow's provenance is outside the allow-list
- **THEN** the finding is a warning and does not fail the run

#### Scenario: Unknown provenance fails on its own gate
- **WHEN** the provenance block sets `on_unknown` to `fail`, `fail_on` does not include `provenance`, and a flow resolves to provenance `unknown`
- **THEN** the finding fails the run

### Requirement: Waiver applies to provenance findings
A waiver with a non-empty justification SHALL downgrade a provenance failure to the `waived`
state, consistent with residency and sovereignty waiver behaviour. A waiver SHALL NOT override
an explicit provider deny-list entry.

#### Scenario: Justified waiver on a provenance failure
- **WHEN** a flow that would fail the provenance allow-list carries a waiver with a justification
- **THEN** the finding is `waived` and does not contribute to the exit code
