## MODIFIED Requirements

### Requirement: Sovereignty bloc vocabulary
The system SHALL express sovereignty using the blocs `us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`,
`ca`, `jp`, `kr`, `sg`, `au`, `ae`, `ch`, `local`, and `unknown`. The `eu` bloc represents the EU/EEA
as a single compelled-disclosure unit. The `local` bloc represents self-hosted inference with no
external sovereign. The `unknown` bloc represents a sovereignty that cannot be statically
determined. The system SHALL NOT emit any sovereignty bloc outside this vocabulary. Every bloc
in the vocabulary SHALL have a source note in the bundled sovereignty map and a human-readable
display name in report output.

#### Scenario: A US-headquartered provider resolves to us sovereignty
- **WHEN** a flow is detected to OpenAI, Anthropic, Google Gemini, or AWS Bedrock
- **THEN** the flow's sovereignty is `us`

#### Scenario: A UK-headquartered provider resolves to uk sovereignty
- **WHEN** a flow is detected to Stability AI
- **THEN** the flow's sovereignty is `uk`

#### Scenario: A Russian provider resolves to ru sovereignty
- **WHEN** a flow is detected to GigaChat (Sber)
- **THEN** the flow's sovereignty is `ru`

#### Scenario: A new bloc is accepted in a sovereignty policy allow-list
- **WHEN** a policy's sovereignty block lists `jp` for a classification
- **THEN** the policy loads and flows with sovereignty `jp` pass the sovereignty check

#### Scenario: Every vocabulary bloc carries a source note
- **WHEN** the bundled sovereignty map is loaded
- **THEN** each bloc in the vocabulary has a source note

#### Scenario: The Swiss bloc is accepted in a sovereignty policy allow-list
- **WHEN** a policy's sovereignty block lists `ch` for a classification
- **THEN** the policy loads and flows with sovereignty `ch` pass the sovereignty check
