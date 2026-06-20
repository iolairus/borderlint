## MODIFIED Requirements

### Requirement: Output formats
The CLI SHALL produce a human-readable report, a machine-readable JSON report, and a Mermaid
flow map of detected flows. Every Mermaid node and subgraph label SHALL be emitted as a quoted string,
with any embedded double quote replaced by `#quot;`, so a label containing Mermaid metacharacters
(parentheses, slashes) renders as valid Mermaid.

#### Scenario: JSON output requested
- **WHEN** the user requests JSON output
- **THEN** the CLI emits machine-readable findings

#### Scenario: Mermaid output requested
- **WHEN** the user requests Mermaid output
- **THEN** the CLI emits a flow map grouping each provider under its jurisdiction

#### Scenario: Mermaid labels with metacharacters are quoted
- **WHEN** a jurisdiction or provider label contains parentheses or a slash (for example `Unknown (region-dependent)` or `Custom / OpenAI-compatible endpoint`)
- **THEN** the Mermaid output emits that label as a quoted string valid for the Mermaid parser

#### Scenario: An embedded quote in a Mermaid label is escaped
- **WHEN** a label contains a double quote
- **THEN** it is emitted as `#quot;` in the Mermaid output
