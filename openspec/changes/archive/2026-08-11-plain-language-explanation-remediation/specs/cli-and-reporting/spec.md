## ADDED Requirements

### Requirement: CLI explain flag
The CLI SHALL accept an `--explain` flag on the `scan` command.

#### Scenario: Flag parsing
- **WHEN** user runs `borderlint scan . --policy p.json --classification c --explain`
- **THEN** the system SHALL parse the flag and enable explanations in output

### Requirement: Explain field in JSON output
The JSON output SHALL include an `explanation` field per finding when `--explain` is set, and SHALL omit the field when it is not set.

#### Scenario: JSON with explain
- **WHEN** scan runs with `--format json --explain`
- **THEN** each finding object SHALL contain `explanation` string

#### Scenario: JSON without explain
- **WHEN** scan runs with `--format json` and no `--explain`
- **THEN** finding objects SHALL NOT contain an `explanation` key

### Requirement: Explain field in text output
The text output SHALL include explanation lines per finding when `--explain` is set.

#### Scenario: Text with explain
- **WHEN** scan runs with `--format text --explain`
- **THEN** each finding block SHALL include an explanation line
