## ADDED Requirements

### Requirement: Explain field in JSON output
The JSON output SHALL include an `explanation` field per finding when `--explain` is set.

#### Scenario: JSON with explain
- **WHEN** scan runs with `--format json --explain`
- **THEN** each finding object SHALL contain `explanation` string

### Requirement: Explain field in text output
The text output SHALL include explanation lines per finding when `--explain` is set.

#### Scenario: Text with explain
- **WHEN** scan runs with `--format text --explain`
- **THEN** each finding block SHALL include an explanation line
