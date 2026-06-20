## ADDED Requirements

### Requirement: Waived flows are not violations
A waiver with a non-empty justification SHALL change a finding that would otherwise be a residency
(allow-list) or unknown-jurisdiction failure into the `waived` state — a terminal state that is
reported but never contributes to the failure exit code, regardless of the `fail_on` set. A waiver
SHALL NOT override an explicit provider deny-list entry. A waiver with no justification SHALL be
ignored, and the flow SHALL be evaluated normally. Only a failing finding can be waived.

#### Scenario: Justified waiver on a residency failure
- **WHEN** a flow that would fail the allow-list carries a waiver with a justification
- **THEN** the finding is `waived` and does not contribute to the exit code

#### Scenario: Waiver does not override a provider deny-list
- **WHEN** a flow whose provider is on the policy deny-list carries a waiver
- **THEN** the finding remains a violation, because a waiver cannot clear an explicit deny

#### Scenario: Unjustified waiver is ignored
- **WHEN** a flow carries a waiver with no justification
- **THEN** the waiver is ignored and the flow is evaluated normally
