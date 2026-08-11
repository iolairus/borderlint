# plain-language-explanations Specification

## Purpose
Per-finding plain-language explanation of why a flow violates residency/sovereignty/provenance and what to change. Explanations are advisory, deterministic template-driven, and never affect gating.
## Requirements
### Requirement: Plain-language explanation per finding
The system SHALL provide a plain-language explanation for each finding when `--explain` is set.

#### Scenario: Residency violation explanation
- **WHEN** a finding has reason `residency` and `--explain` is set
- **THEN** the output SHALL include an explanation stating the provider, jurisdiction, and that the jurisdiction is not in the policy allow-list for the classification

### Requirement: Remediation hint per finding
The system SHALL provide a remediation hint for each finding when `--explain` is set.

#### Scenario: Remediation for residency
- **WHEN** a finding has reason `residency`
- **THEN** the output SHALL include a hint to update the policy allow-list or change the provider/endpoint
