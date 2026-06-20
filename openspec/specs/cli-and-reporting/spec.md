# cli-and-reporting Specification

## Purpose
TBD - created by archiving change mvp-residency-scanner. Update Purpose after archive.
## Requirements
### Requirement: Scan command
The CLI SHALL provide a `scan` command that takes a path to scan, an optional policy, an optional
active classification, and an output format (human-readable, JSON, or Mermaid).

#### Scenario: Scan a path against a policy
- **WHEN** the user runs the scan command with a path, a policy, and a classification
- **THEN** the path is scanned and detected flows are evaluated against the policy for that classification

### Requirement: CI exit code
The CLI SHALL exit with a non-zero status when any violation is found and a zero status otherwise.

#### Scenario: Violation fails the build
- **WHEN** a scan finds at least one violation
- **THEN** the CLI exits with a non-zero status

#### Scenario: Clean scan passes the build
- **WHEN** a scan finds no violations
- **THEN** the CLI exits with a zero status

### Requirement: Output formats
The CLI SHALL produce a human-readable report, a machine-readable JSON report, and a Mermaid
flow map of detected flows.

#### Scenario: JSON output requested
- **WHEN** the user requests JSON output
- **THEN** the CLI emits machine-readable findings

#### Scenario: Mermaid output requested
- **WHEN** the user requests Mermaid output
- **THEN** the CLI emits a flow map grouping each provider under its jurisdiction

### Requirement: Inventory mode without a policy
When no policy is provided, the CLI SHALL report detected flows and their jurisdictions and SHALL
exit zero.

#### Scenario: Scan with no policy
- **WHEN** the user runs a scan without providing a policy
- **THEN** the CLI reports detected flows and their jurisdictions and exits zero

### Requirement: Arrangement reference links
For a flagged cross-border flow, the report SHALL surface a reference link to the relevant
cross-border arrangement relevant to the declared home regime as context, without adjudicating
whether it applies.

#### Scenario: GBA flow shows the arrangement reference
- **WHEN** a flagged flow crosses between `hk` and `CN-GBA`
- **THEN** the report surfaces a reference link to the GBA Standard Contract as context

