## MODIFIED Requirements

### Requirement: CI exit code
The CLI SHALL exit with a non-zero status when any violation is found and a zero status otherwise,
except when an artifact-export format (`--format sbom`) is requested — an export is not a gate and
SHALL exit zero regardless of violations.

#### Scenario: Violation fails the build
- **WHEN** a scan finds at least one violation under a gating format
- **THEN** the CLI exits with a non-zero status

#### Scenario: Clean scan passes the build
- **WHEN** a scan finds no violations
- **THEN** the CLI exits with a zero status

#### Scenario: SBOM export does not gate
- **WHEN** `--format sbom` is requested and a scan finds a violation
- **THEN** the CLI exits with a zero status

## ADDED Requirements

### Requirement: AI data-flow SBOM export
The CLI SHALL provide a `--format sbom` export that emits a policy-independent JSON inventory of every
detected AI flow, under an envelope carrying a schema identifier (`borderlint.ai-dataflow-sbom/1`), the
borderlint version, and the KB review date. Each component SHALL list a provider's id, name, sorted
resolved jurisdiction(s), and call sites — each with `file`, `line`, `kind`, `evidence`, and
`jurisdiction`. The document SHALL contain no per-flow severity, level, or verdict field. The export
SHALL be deterministic: every list (components, sites, jurisdictions) is totally ordered, object keys
are sorted, and no wall-clock timestamp is emitted — so two runs of the same version over the same tree
produce byte-identical output.

#### Scenario: SBOM lists every detected flow under the envelope
- **WHEN** `--format sbom` runs over a path with AI provider usage
- **THEN** the output is a JSON document whose envelope carries the schema id, the borderlint version, and the KB date, and whose components list each provider with its jurisdiction(s) and call sites

#### Scenario: Inventory mode requires no policy
- **WHEN** `--format sbom` runs without a policy
- **THEN** the document lists every detected flow and the CLI exits zero

#### Scenario: Policy-independent and non-gating
- **WHEN** `--format sbom` runs with a policy under which a detected flow would fail
- **THEN** the document still lists that flow with no severity, level, or verdict field, and the process exits zero

#### Scenario: Deterministic output
- **WHEN** the same path is scanned twice with `--format sbom`
- **THEN** the two outputs are byte-identical, with every list totally ordered, object keys sorted, and no timestamp present
