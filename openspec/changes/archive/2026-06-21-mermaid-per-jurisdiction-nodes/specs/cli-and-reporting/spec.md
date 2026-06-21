## MODIFIED Requirements

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
