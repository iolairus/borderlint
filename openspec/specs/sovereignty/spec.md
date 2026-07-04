# sovereignty Specification

## Purpose
Model which government can compel disclosure of a flow's data, as a dimension orthogonal to
residency (where the endpoint physically sits). Sovereignty is derived from the provider's home
legal regime, not the endpoint region. The map is advisory: it surfaces compelled-disclosure
exposure and never adjudicates whether a given statute legally applies.

## Requirements
### Requirement: Sovereignty is a distinct per-flow attribute
The system SHALL resolve, for every detected flow, a **sovereignty** bloc that represents the
government able to compel disclosure of that flow's data, as an attribute distinct from the
flow's jurisdiction (residency). Sovereignty reflects the provider's home legal regime for
compelled disclosure, not the endpoint region. The system SHALL NOT derive sovereignty from the
endpoint region alone.

#### Scenario: Residency and sovereignty diverge for a US provider in a non-US region
- **WHEN** a flow is detected to AWS Bedrock in `ap-east-1` (residency `hk`)
- **THEN** the flow's sovereignty is `us` while its residency remains `hk`

#### Scenario: A Chinese provider's sovereignty matches its residency
- **WHEN** a flow is detected to DeepSeek (residency `cn`)
- **THEN** the flow's sovereignty is `cn`

### Requirement: Sovereignty bloc vocabulary
The system SHALL express sovereignty using the blocs `us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`,
`ca`, `jp`, `kr`, `sg`, `au`, `ae`, `local`, and `unknown`. The `eu` bloc represents the EU/EEA
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

### Requirement: Bundled sovereignty knowledge base
The system SHALL ship a bundled sovereignty map keyed by provider id, covering every provider in
the bundled provider knowledge base, and SHALL allow a per-endpoint-host sovereignty override for
the rare case of a ring-fenced subsidiary under a different sovereign. The map SHALL carry an
`updated` date and a `source` note per bloc. The map is advisory: it SHALL NOT adjudicate whether
a given statute legally applies.

#### Scenario: A bundled provider resolves via the sovereignty map
- **WHEN** a flow is detected for a provider present in the sovereignty map
- **THEN** the flow's sovereignty is the map's value for that provider

#### Scenario: A ring-fenced subsidiary overrides the provider sovereignty
- **WHEN** a provider KB entry defines a host-level `sovereignty` override
- **THEN** a flow to that host resolves to the overridden sovereignty, taking precedence over the provider-level value

### Requirement: Aggregators and custom endpoints resolve to unknown sovereignty
A multi-provider aggregator/router library, and a custom OpenAI-compatible endpoint whose host is not in the knowledge base, SHALL resolve to sovereignty `unknown`, because the destination provider — and thus its sovereign — is selected at runtime and cannot be statically determined. Such flows MUST be governed by the `on_unknown` policy setting.

#### Scenario: An aggregator's sovereignty is unknown
- **WHEN** a flow is detected for litellm, langchain, or openrouter
- **THEN** the flow's sovereignty is `unknown`

#### Scenario: A custom endpoint's sovereignty is unknown
- **WHEN** a flow is detected to a host not in the knowledge base and not a loopback host
- **THEN** the flow's sovereignty is `unknown`

### Requirement: Loopback flows resolve to local sovereignty
A loopback or self-hosted inference endpoint SHALL resolve to sovereignty `local`, because no
external government can compel disclosure of data that never leaves the operator's own host.

#### Scenario: A local inference server has local sovereignty
- **WHEN** a flow is detected to `http://localhost:8080` or to the Ollama provider
- **THEN** the flow's sovereignty is `local`

### Requirement: User-supplied sovereignty overrides
The system SHALL merge a user-supplied sovereignty map with the bundled one: user entries add to
the bundled providers and, on a provider-id conflict, take precedence. A user-supplied
per-endpoint-host sovereignty SHALL take precedence over any bundled or provider-level value.

#### Scenario: A user overrides a provider's sovereignty
- **WHEN** a user-supplied sovereignty map defines a sovereignty for a provider id that also exists in the bundled map
- **THEN** the user-supplied sovereignty takes precedence for that provider

#### Scenario: A user adds a sovereignty for a custom provider
- **WHEN** a user-supplied sovereignty map defines a sovereignty for a provider not in the bundled map
- **THEN** flows for that provider resolve to the user-supplied sovereignty
