## ADDED Requirements

### Requirement: Knowledge base covers TypeScript and JavaScript packages
The knowledge base SHALL map providers to their TypeScript/JavaScript package names in addition to
their Python SDK names.

#### Scenario: A JavaScript package resolves to a provider
- **WHEN** the package `@anthropic-ai/sdk` is detected
- **THEN** it resolves to the Anthropic provider with jurisdiction `us`

#### Scenario: A non-US JavaScript package resolves
- **WHEN** the package `@mistralai/mistralai` is detected
- **THEN** it resolves to the Mistral provider with jurisdiction `eu`

### Requirement: Aggregator libraries resolve to unknown jurisdiction
A multi-provider aggregator or router library SHALL resolve to an unknown jurisdiction, because the
destination provider is selected at runtime.

#### Scenario: Aggregator jurisdiction is unknown
- **WHEN** a flow is detected for a known aggregator library (for example litellm)
- **THEN** its jurisdiction is unknown
