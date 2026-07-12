## MODIFIED Requirements

### Requirement: Scan command
The CLI SHALL provide a `scan` command that takes a path to scan, an optional policy, an optional
active classification, and an output format (human-readable, JSON, Mermaid, SARIF, SBOM, evidence, or shields.io badge endpoint).

#### Scenario: Scan a path against a policy
- **WHEN** the user runs the scan command with a path, a policy, and a classification
- **THEN** the path is scanned and detected flows are evaluated against the policy for that classification

### Requirement: CI exit code
The CLI SHALL exit with a non-zero status when any violation is found and a zero status otherwise,
except when an artifact-export format (`--format sbom`, `--format evidence`, or `--format badge`) is requested — an
export is not a gate and SHALL exit zero regardless of violations.

#### Scenario: Violation fails the build
- **WHEN** a scan finds at least one violation under a gating format
- **THEN** the CLI exits with a non-zero status

#### Scenario: Clean scan passes the build
- **WHEN** a scan finds no violations
- **THEN** the CLI exits with a zero status

#### Scenario: SBOM export does not gate
- **WHEN** `--format sbom` is requested and a scan finds a violation
- **THEN** the CLI exits with a zero status

#### Scenario: A failing state can still be filed as evidence
- **WHEN** the scan produces failing findings and the format is `evidence`
- **THEN** the document records the failures and the exit code is 0

#### Scenario: Badge export does not gate
- **WHEN** `--format badge` is requested and a scan finds a violation
- **THEN** the CLI exits with a zero status
