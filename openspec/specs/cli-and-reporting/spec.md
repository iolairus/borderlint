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
For a flagged cross-border flow, the report SHALL surface reference link(s) to the relevant
cross-border arrangement(s), drawn from a bundled arrangements list — each with a name, a URL, and a
one-line summary — selected by the flow's jurisdictions and the declared home regime, as context
only and without adjudicating whether any applies.

#### Scenario: A Hong Kong–GBA flow surfaces the GBA Standard Contract
- **WHEN** a flagged flow crosses between `hk` and `CN-GBA` under a declared home regime
- **THEN** the report surfaces the GBA Standard Contract reference, and not for a plain `cn` destination

#### Scenario: A Mainland China flow surfaces the PIPL reference
- **WHEN** a flagged flow resolves to `cn` (Mainland China, outside the GBA)
- **THEN** the report surfaces the PIPL cross-border transfer reference

#### Scenario: An EU/EEA flow surfaces the GDPR reference
- **WHEN** a flagged flow resolves to an EU/EEA jurisdiction (the `eu` token or an EU/EEA member country code)
- **THEN** the report surfaces the GDPR transfers reference

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

### Requirement: Regime tags
The report SHALL tag a flagged flow with the data-protection regime(s) implicated — drawn from the
set {PDPO, PIPL} — derived from the declared home regime and the flow's destination jurisdiction, as
informational context. GDPR is surfaced as an arrangement reference only, never as a regime tag.

#### Scenario: HK entity sending to Mainland China
- **WHEN** the declared home regime is `pdpo` and a flagged flow resolves to `cn` or `CN-GBA`
- **THEN** the flow is tagged with PDPO and PIPL

### Requirement: Context does not change the verdict
Regime tags and arrangement references SHALL NOT change a finding's severity or the exit code, and
SHALL NOT appear as SARIF results or alter any SARIF result's level.

#### Scenario: Tags and references do not affect pass/fail
- **WHEN** a flagged flow is tagged and an arrangement reference is surfaced
- **THEN** its severity and the process exit code are identical to the same flow without tags or references

#### Scenario: SARIF is unaffected
- **WHEN** SARIF output is requested
- **THEN** regime tags and arrangement references add no results and change no result's level

