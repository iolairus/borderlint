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

### Requirement: Output formats
The CLI SHALL produce a human-readable report, a machine-readable JSON report, and a Mermaid
flow map of detected flows. Every Mermaid node and subgraph label SHALL be emitted as a double-quoted
string in which Mermaid's escape prefix `#` is replaced by `#35;` and an embedded double quote by
`#quot;` — so that labels containing parentheses or slashes are carried inside the quotes rather than
breaking the flow map. In the Mermaid flow map, each jurisdiction subgraph SHALL be titled by its
jurisdiction code, and a provider that resolves to more than one jurisdiction SHALL render as a
distinct node under each of those jurisdictions, each with an edge from the application node.

#### Scenario: JSON output requested
- **WHEN** the user requests JSON output
- **THEN** the CLI emits machine-readable findings

#### Scenario: Mermaid output requested
- **WHEN** the user requests Mermaid output
- **THEN** the CLI emits a flow map grouping each provider under its jurisdiction, each subgraph titled by the jurisdiction code

#### Scenario: A multi-jurisdiction provider appears under each jurisdiction
- **WHEN** a provider resolves to more than one jurisdiction (for example AWS Bedrock to `us` and `de`)
- **THEN** the Mermaid flow map renders a distinct node for that provider under each jurisdiction's subgraph, each with an edge from the application node

#### Scenario: A label with metacharacters is double-quoted
- **WHEN** a jurisdiction or provider label contains parentheses or a slash (for example `Unknown (region-dependent)` or `Custom / OpenAI-compatible endpoint`)
- **THEN** the Mermaid output emits it as a double-quoted label with the parentheses or slash inside the quotes

#### Scenario: Mermaid escape characters are entity-escaped
- **WHEN** a label contains a `#` or a double quote
- **THEN** they are emitted as `#35;` and `#quot;` respectively

### Requirement: Inventory mode without a policy
When no policy is provided, the CLI SHALL report detected flows and their jurisdictions and SHALL
exit zero.

#### Scenario: Scan with no policy
- **WHEN** the user runs a scan without providing a policy
- **THEN** the CLI reports detected flows and their jurisdictions and exits zero

### Requirement: Arrangement reference links
For a flagged cross-border flow, the report SHALL surface reference link(s) to the relevant
cross-border arrangement(s), drawn from a bundled arrangements list — each with a name, a URL, and a
one-line summary — selected by the flow's jurisdictions and the declared home location or home regime,
as context only and without adjudicating whether any applies. When a `home_location` is declared, the
report SHALL surface the GBA Standard Contract variant matching the Special Administrative Region in the
flow — the (Mainland, Hong Kong) contract for a flow spanning `hk` and `CN-GBA`, and the (Mainland,
Macao) contract for a flow spanning `mo` and `CN-GBA` (a flow spanning both SARs surfaces both), where a
flow "spans" the jurisdictions appearing among the home location and the flagged destinations. A plain
`cn` destination SHALL NOT surface any GBA Standard Contract. When no `home_location` is declared, a
declared `home_regime` SHALL surface the existing GBA Standard Contract reference exactly as before.

#### Scenario: A Hong Kong–GBA flow surfaces the GBA Standard Contract
- **WHEN** a flagged flow crosses between `hk` and `CN-GBA` under a declared home regime
- **THEN** the report surfaces the GBA Standard Contract reference, and not for a plain `cn` destination

#### Scenario: A Macao–GBA flow surfaces the (Mainland, Macao) Standard Contract
- **WHEN** the home location is `mo` and a flagged flow resolves to `CN-GBA` (or the home location is `CN-GBA` and a flagged flow resolves to `mo`)
- **THEN** the report surfaces the (Mainland, Macao) GBA Standard Contract

#### Scenario: A flow spanning both SARs surfaces both contracts
- **WHEN** the home location is `CN-GBA` and flagged flows resolve to both `hk` and `mo`
- **THEN** the report surfaces both the (Mainland, Hong Kong) and the (Mainland, Macao) GBA Standard Contracts

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
set {PDPO, PIPL, Macao PDPA} — as informational context. When a `home_location` is declared, the tags
SHALL be derived from the home location and each flagged destination, where `hk` implies PDPO, `mo`
implies Macao PDPA, and `cn` or `CN-GBA` implies PIPL. When no `home_location` is declared, the tags
SHALL be derived from the declared `home_regime` and `cn`/`CN-GBA` destinations exactly as before
(`pdpo` → PDPO, `pipl` or a `cn`/`CN-GBA` destination → PIPL). GDPR is surfaced as an arrangement
reference only, never as a regime tag.

#### Scenario: HK entity sending to Mainland China
- **WHEN** the declared home regime is `pdpo` and a flagged flow resolves to `cn` or `CN-GBA`
- **THEN** the flow is tagged with PDPO and PIPL

#### Scenario: Macao entity sending to the Mainland GBA
- **WHEN** the declared home location is `mo` and a flagged flow resolves to `CN-GBA`
- **THEN** the flow is tagged with Macao PDPA and PIPL

#### Scenario: A Macao destination implies the Macao regime
- **WHEN** the declared home location is `hk` and a flagged flow resolves to `mo`
- **THEN** the flow is tagged with PDPO and Macao PDPA

### Requirement: Context does not change the verdict
Regime tags and arrangement references SHALL NOT change a finding's severity or the exit code, and
SHALL NOT appear as SARIF results or alter any SARIF result's level.

#### Scenario: Tags and references do not affect pass/fail
- **WHEN** a flagged flow is tagged and an arrangement reference is surfaced
- **THEN** its severity and the process exit code are identical to the same flow without tags or references

#### Scenario: SARIF is unaffected
- **WHEN** SARIF output is requested
- **THEN** regime tags and arrangement references add no results and change no result's level

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

### Requirement: SBOM diff mode
The CLI SHALL provide a `diff` command that takes two AI data-flow SBOM documents — a baseline and a
current one — and reports, in human-readable and JSON form, the data flows added and removed between
them. A flow is the pair (provider id, jurisdiction) for each jurisdiction in a component's
`jurisdictions` list; provider identity is the component id, not its display name. The command defines
its own exit status, independent of the policy-violation gate of `scan`: it SHALL exit 1 when the
current SBOM introduces a flow to a non-`local` jurisdiction (including `unknown`) that is absent from
the baseline, SHALL exit 0 otherwise (removed-only or `local`-only changes do not gate), and SHALL exit
2 when an input is not a valid `borderlint.ai-dataflow-sbom/1` document. Removed flows SHALL be reported
but SHALL NOT affect the exit status.

#### Scenario: A new cross-border flow gates the build
- **WHEN** the current SBOM contains a (provider, jurisdiction) flow to a non-`local` jurisdiction absent from the baseline
- **THEN** the command reports it as added and exits 1

#### Scenario: A new unknown-jurisdiction flow gates the build
- **WHEN** the only added flow is to the `unknown` jurisdiction
- **THEN** the command reports it as added and exits 1

#### Scenario: A new local-only flow does not gate
- **WHEN** the only added flow is to the `local` jurisdiction
- **THEN** the command reports it as added and exits 0

#### Scenario: Removed flows do not gate
- **WHEN** a flow present in the baseline is absent from the current SBOM and no non-`local` flow was added
- **THEN** the command reports it as removed and exits 0

#### Scenario: Swapping the inputs inverts added and removed
- **WHEN** the baseline and current documents are exchanged
- **THEN** a flow previously reported as added is reported as removed

#### Scenario: Non-SBOM input is rejected
- **WHEN** an input file is not a `borderlint.ai-dataflow-sbom/1` document
- **THEN** the command exits 2

### Requirement: Mermaid root node identifies the scanned codebase
The Mermaid flow map's application (root) node SHALL be labelled with the scanned codebase's name and,
when determinable, its version. The name SHALL be read from a PEP 621 `pyproject.toml` `[project]` table
or a `package.json` at the scan root, falling back to the scan directory's name; the version SHALL be a
git tag when one is available, else the version from the **same manifest that supplied the name**. When
no name is determinable the node SHALL use a generic label. Resolution is best-effort: it reads only the
scan root's manifests and a local `git` invocation, accesses no network, and SHALL NOT fail the scan if
git is absent or returns no tag. The label SHALL be a single line, escaped like any other Mermaid label.
Only the Mermaid root node is affected; other output formats are unchanged.

#### Scenario: package.json names the root node
- **WHEN** the scan root contains a `package.json` with name `acme-bot` and version `1.2.3` and is not a git repository
- **THEN** the Mermaid application node is labelled `acme-bot@1.2.3`

#### Scenario: pyproject [project] names the root node
- **WHEN** the scan root contains a `pyproject.toml` `[project]` table with name `acme` and version `0.4.0` and is not a git repository
- **THEN** the Mermaid application node is labelled `acme@0.4.0`

#### Scenario: a git tag supplies the version when git is available
- **WHEN** the scan root is a git repository whose latest tag is `v2.0.0` and git is available
- **THEN** the Mermaid application node's version is `v2.0.0`

#### Scenario: a manifest name without a version
- **WHEN** the scan root's manifest supplies a name but no version and no git tag is available
- **THEN** the Mermaid application node is labelled with the bare name and no `@`

#### Scenario: fallback to the directory name
- **WHEN** the scan root has no manifest name and no determinable version
- **THEN** the Mermaid application node is labelled with the scan directory's name

#### Scenario: a label with metacharacters stays single-line and escaped
- **WHEN** a resolved name contains a double quote, a `#`, or a newline
- **THEN** the Mermaid application node label is escaped (`#`→`#35;`, `"`→`#quot;`) and rendered on a single line

### Requirement: Home location within the GBA
The report SHALL accept an optional `home_location` of `hk`, `mo`, or `CN-GBA` in the policy,
identifying the entity's seat within the Greater Bay Area, and SHALL derive the home data-protection
regime from it — `hk` → PDPO, `mo` → Macao PDPA (Law 8/2005), `CN-GBA` → PIPL — and select the GBA
Standard Contract variant accordingly. When `home_location` is absent, the report SHALL use a declared
`home_regime` (`pdpo` or `pipl`) with its existing regime-tag and arrangement behaviour unchanged.

#### Scenario: A Macao home location implies the Macao regime and contract
- **WHEN** the policy declares `home_location` `mo` and a flagged flow resolves to `CN-GBA`
- **THEN** the flow is tagged Macao PDPA (home) and the report surfaces the (Mainland, Macao) Standard Contract

#### Scenario: home_regime pdpo is unchanged
- **WHEN** the policy declares `home_regime` `pdpo` and no `home_location`
- **THEN** regime tags and arrangement references behave as before — PDPO home, the GBA Standard Contract for a `CN-GBA` flow

#### Scenario: home_regime pipl is unchanged
- **WHEN** the policy declares `home_regime` `pipl` and no `home_location`, and a flagged flow resolves to `CN-GBA`
- **THEN** regime tags and arrangement references behave as before — a PIPL tag and the existing GBA Standard Contract reference

### Requirement: Provider category in output

Reports SHALL surface a provider's category so a data-at-rest sink is distinguishable from an
inference API. The category defaults to `inference` and is `vector_store` for managed vector
databases. The category MUST appear in the text, JSON, and SBOM outputs and MUST NOT change the
pass/fail verdict.

#### Scenario: Text report marks a vector store
- **WHEN** the text report includes a vector-store provider
- **THEN** its line is annotated as a vector store (e.g. `(vector store)`), distinct from an
  inference provider

#### Scenario: JSON and SBOM carry the category
- **WHEN** output is requested as JSON or SBOM
- **THEN** each finding/component includes a `category` field (`inference` or `vector_store`)

#### Scenario: Category does not affect the verdict
- **WHEN** the same flows are scanned
- **THEN** adding the category changes no severity — pass/fail depends only on jurisdiction and
  provider rules

