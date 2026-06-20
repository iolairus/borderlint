## ADDED Requirements

### Requirement: Waived flows are not violations
A flow carrying a waiver with a non-empty justification SHALL NOT be a residency violation. A waiver
with no justification SHALL be ignored, and the flow SHALL be evaluated normally.

#### Scenario: Justified waiver passes
- **WHEN** a flow that would otherwise violate the policy carries a waiver with a justification
- **THEN** the flow is not a violation

#### Scenario: Unjustified waiver is ignored
- **WHEN** a flow carries a waiver with no justification
- **THEN** the waiver is ignored and the flow is evaluated normally
