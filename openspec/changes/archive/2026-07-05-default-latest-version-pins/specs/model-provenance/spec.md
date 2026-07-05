## MODIFIED Requirements

### Requirement: Version-pinned model identifiers resolve provenance
The system SHALL resolve a model identifier carrying a single trailing version suffix — an `@`
followed by a digit-led version token, or the literal meta-version tokens `default` or `latest`
— by matching its base identifier (the part before the `@`) against the provenance map, while
keeping the full literal as evidence. A trailing `@` segment that is neither digit-led nor one
of the two meta-version tokens SHALL NOT be treated as a version suffix, and the literal SHALL
remain unmatched.

#### Scenario: A Vertex version-pinned identifier resolves
- **WHEN** a flow carries the model reference `claude-3-5-haiku@20241022`
- **THEN** its provenance resolves to `us` and the evidence carries the full literal including the suffix

#### Scenario: A Bedrock-style aggregator version-pinned identifier resolves
- **WHEN** a flow carries the model reference `anthropic.claude-haiku-4-5@20251001`
- **THEN** its provenance resolves to `us`

#### Scenario: A meta-version pin resolves
- **WHEN** a flow carries the model reference `mistral-large@latest` or `claude-fable-5@default`
- **THEN** its provenance resolves to the base identifier's bloc (`eu` and `us` respectively)

#### Scenario: An email address is not a model reference
- **WHEN** a scanned file contains the string literal `gemini-team@google.com`
- **THEN** no model reference is detected, because the `@` segment is neither digit-led nor a meta-version token

#### Scenario: The version never changes the bloc
- **WHEN** two flows carry `mistral-large` and `mistral-large@2407`
- **THEN** both resolve to the same provenance bloc
