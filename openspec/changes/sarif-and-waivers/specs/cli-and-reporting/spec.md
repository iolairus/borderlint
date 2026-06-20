## ADDED Requirements

### Requirement: SARIF output
The CLI SHALL emit findings as SARIF 2.1.0 when SARIF output is requested: a top-level object with
`version` set to `2.1.0`, a `$schema`, and a `runs` array whose entry has `tool.driver.name` set to
`borderlint` and one `results` entry per finding, each carrying a `ruleId`, a `level`, a `message`,
and a physical `file:line` location.

#### Scenario: SARIF requested
- **WHEN** the user requests SARIF output
- **THEN** the CLI emits a SARIF 2.1.0 document whose run has `tool.driver.name` `borderlint` and one result per finding, each with a `ruleId`, a `level`, a `message`, and a `file:line` location

### Requirement: Waived findings are reported
A waived finding SHALL appear in the output marked as waived with its justification, distinct from a
violation, and SHALL NOT contribute to the failure exit code. In SARIF, a waived result SHALL carry
`level` `note` and a `suppressions` entry so that a code-scanning consumer does not treat it as failing.

#### Scenario: A waived flow in the report
- **WHEN** a flow has been waived
- **THEN** it appears marked as waived with its justification and does not cause a non-zero exit

#### Scenario: A waived flow is suppressed in SARIF
- **WHEN** SARIF output is requested and a finding is waived
- **THEN** its SARIF result has `level` `note` and a `suppressions` entry
