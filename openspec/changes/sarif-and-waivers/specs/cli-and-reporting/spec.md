## ADDED Requirements

### Requirement: SARIF output
The CLI SHALL emit findings as SARIF when SARIF output is requested, with one result per finding
carrying a rule identifier, a level, a file-and-line location, and a message.

#### Scenario: SARIF requested
- **WHEN** the user requests SARIF output
- **THEN** the CLI emits SARIF with one result per finding, each carrying a rule id, a level, a `file:line` location, and a message

### Requirement: Waived findings are reported
A waived finding SHALL appear in the output marked as waived with its justification, distinct from a
violation, and SHALL NOT contribute to the failure exit code.

#### Scenario: A waived flow in the report
- **WHEN** a flow has been waived
- **THEN** it appears marked as waived with its justification and does not cause a non-zero exit
