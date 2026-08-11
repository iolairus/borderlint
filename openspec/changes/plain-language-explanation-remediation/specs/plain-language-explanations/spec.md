## ADDED Requirements

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

## ADDED Requirements

### Requirement: CLI explain flag
The CLI SHALL accept `--explain` flag for `scan` command.

#### Scenario: Flag parsing
- **WHEN** user runs `borderlint scan . --policy p.json --classification c --explain`
- **THEN** the system SHALL parse the flag and enable explanations in output
