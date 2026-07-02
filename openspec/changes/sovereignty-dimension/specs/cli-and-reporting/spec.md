## MODIFIED Requirements

### Requirement: Output formats
The CLI SHALL produce a human-readable report, a machine-readable JSON report, and a Mermaid
flow map of detected flows. Every Mermaid node and subgraph label SHALL be emitted as a double-quoted
string in which Mermaid's escape prefix `#` is replaced by `#35;` and an embedded double quote by
`#quot;` — so that labels containing parentheses or slashes are carried inside the quotes rather than
breaking the flow map. In the Mermaid flow map, each jurisdiction subgraph SHALL be titled by its
jurisdiction code, and a provider that resolves to more than one jurisdiction SHALL render as a
distinct node under each of those jurisdictions, each with an edge from the application node. The
text report SHALL include a sovereignty column per flow, the JSON report SHALL include a
`sovereignty` field per finding, and the Mermaid node label SHALL append the sovereignty bloc
alongside the jurisdiction. Sovereignty SHALL be surfaced as additional information and SHALL NOT
replace the residency jurisdiction in any output.

#### Scenario: JSON output requested
- **WHEN** the user requests JSON output
- **THEN** the CLI emits machine-readable findings, each carrying a `sovereignty` field

#### Scenario: Mermaid output requested
- **WHEN** the user requests Mermaid output
- **THEN** the CLI emits a flow map grouping each provider under its jurisdiction, each subgraph titled by the jurisdiction code, with each node label appending the sovereignty bloc

#### Scenario: A multi-jurisdiction provider appears under each jurisdiction
- **WHEN** a provider resolves to more than one jurisdiction (for example AWS Bedrock to `us` and `de`)
- **THEN** the Mermaid flow map renders a distinct node for that provider under each jurisdiction's subgraph, each with an edge from the application node

#### Scenario: A label with metacharacters is double-quoted
- **WHEN** a jurisdiction or provider label contains parentheses or a slash (for example `Unknown (region-dependent)` or `Custom / OpenAI-compatible endpoint`)
- **THEN** the Mermaid output emits it as a double-quoted label with the parentheses or slash inside the quotes

#### Scenario: Mermaid escape characters are entity-escaped
- **WHEN** a label contains a `#` or a double quote
- **THEN** they are emitted as `#35;` and `#quot;` respectively

#### Scenario: Sovereignty appears alongside residency in the text report
- **WHEN** a flow is reported in the human-readable text output
- **THEN** the row includes both the residency jurisdiction and the sovereignty bloc

## ADDED Requirements

### Requirement: Sovereignty reason in findings
The CLI SHALL surface a `sovereignty` finding reason, distinct from `residency`,
`denied_provider`, and `unknown`, whenever a flow's sovereignty is outside the declared
allow-list for the active classification. The reason SHALL appear in the text and JSON reports
and SHALL contribute to the exit code only when `sovereignty` is in `fail_on`.

#### Scenario: A sovereignty mismatch is reported as a reason
- **WHEN** a flow's sovereignty is outside the active classification's sovereignty allow-list
- **THEN** the finding's reasons include `sovereignty`

#### Scenario: Sovereignty reason does not fail by default
- **WHEN** a finding's only reason is `sovereignty` and `fail_on` does not include `sovereignty`
- **THEN** the finding is a warning and the run's exit code is unchanged on its account
