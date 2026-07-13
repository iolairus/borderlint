# cli-and-reporting — delta for add-html-report-format

## ADDED Requirements

### Requirement: HTML report format
The CLI SHALL accept `--format html` on the scan command and emit a single, self-contained HTML
document to stdout. The document SHALL fetch no external resource when opened (no scripts,
stylesheets, fonts, or images loaded from a network), so that it renders fully when opened
offline or in an air-gapped environment. All content derived from the scanned repository
(file paths, evidence strings, model identifiers, waiver reasons) SHALL be HTML-escaped so that
scanned source text cannot inject markup or script into the report.

#### Scenario: HTML output requested
- **WHEN** the user runs a scan with `--format html`
- **THEN** the CLI emits one HTML document containing every reported flow

#### Scenario: The document is self-contained
- **WHEN** the HTML report is generated
- **THEN** it contains no element that fetches a remote resource — no external script, stylesheet, font, or image; reference hyperlinks (`<a href>`, e.g. arrangement links) are permitted because a browser does not fetch them on open

#### Scenario: Scanned content cannot inject markup
- **WHEN** a detected evidence string or file path contains HTML-significant characters (for example `<script>`)
- **THEN** the report renders them as escaped text, not as markup

### Requirement: HTML report content
The HTML report SHALL include: a metadata header stating the scanned path, the git commit of the
scanned repository ("unavailable" when it cannot be resolved), the knowledge base's
last-reviewed dates, and — when a policy is supplied — the policy file's SHA-256 digest and the
declared classification; the findings grouped by residency jurisdiction, each flow showing its
residency jurisdiction, sovereignty bloc, and provenance bloc together with its severity; and,
when at least one waiver is present, a waiver register listing each waived flow with its recorded
justification. In inventory mode (no policy) the report SHALL list flows and jurisdictions
without verdict severities. Applicable regime tags and arrangement references SHALL be surfaced
as in other report formats.

#### Scenario: Findings are grouped by jurisdiction with all three axes
- **WHEN** the HTML report is generated for a scan with findings in more than one jurisdiction
- **THEN** flows appear grouped under their residency jurisdiction, and each flow row shows residency, sovereignty, and provenance

#### Scenario: Policy metadata appears in the header
- **WHEN** a policy file and classification are supplied
- **THEN** the header includes the policy SHA-256 digest and the classification alongside the scanned path and KB review dates

#### Scenario: Waiver register is present when waivers exist
- **WHEN** at least one finding is waived via an inline waiver
- **THEN** the report contains a waiver register listing the waived flow and its justification

#### Scenario: Inventory mode renders without severities
- **WHEN** `--format html` is used without `--policy`
- **THEN** the report lists detected flows and their jurisdictions and contains no pass/fail verdicts

#### Scenario: A flagged cross-border flow surfaces its arrangement reference
- **WHEN** a flagged flow implicates a cross-border arrangement (for example an `hk` home with a `CN-GBA` destination)
- **THEN** the report surfaces the applicable regime tags and renders the arrangement reference as a hyperlink

## MODIFIED Requirements

### Requirement: Scan command
The CLI SHALL provide a `scan` command that takes a path to scan, an optional policy, an optional
active classification, and an output format (human-readable, JSON, Mermaid, SARIF, SBOM, evidence,
or HTML).

#### Scenario: Scan a path against a policy
- **WHEN** the user runs the scan command with a path, a policy, and a classification
- **THEN** the path is scanned and detected flows are evaluated against the policy for that classification

### Requirement: CI exit code
The CLI SHALL exit with a non-zero status when any violation is found and a zero status otherwise,
except when an artifact-export format (`--format sbom`, `--format evidence`, or `--format html`) is
requested — an export is not a gate and SHALL exit zero regardless of violations.

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

#### Scenario: HTML export does not gate
- **WHEN** `--format html` is requested and a scan finds a violation
- **THEN** the report records the failing findings and the CLI exits with a zero status
