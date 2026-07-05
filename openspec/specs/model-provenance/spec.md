# model-provenance Specification

## Purpose
Model whose weights a flow runs: the bloc of the legal regime under which the model's developer
operates, as a third dimension orthogonal to residency (where the endpoint sits) and sovereignty
(who can compel disclosure from the serving provider). Provenance is resolved statically from
model references and first-party provider defaults; the map is advisory — it surfaces weight
origin and never adjudicates export-control applicability.
## Requirements
### Requirement: Provenance bloc vocabulary
The system SHALL express model provenance using the blocs `us`, `eu`, `cn`, `uk`, `ru`, `in`,
`il`, `ca`, `jp`, `kr`, `sg`, `au`, `ae`, `ch`, and `unknown` — the sovereignty vocabulary without
`local`, because model weights always have a developer. The `unknown` bloc represents a
provenance that cannot be statically determined. The system SHALL NOT emit any provenance value
outside this vocabulary, and SHALL reject a user-supplied provenance mapping that uses a token
outside it.

#### Scenario: Invalid provenance token in a user mapping is rejected
- **WHEN** a user-supplied knowledge base maps a model pattern to the bloc `overseas`
- **THEN** loading fails with an error naming the invalid token and the accepted vocabulary

#### Scenario: A flow with no matched model reference resolves to unknown
- **WHEN** a flow carries no matched model reference and its provider has no first-party default
- **THEN** the flow's provenance is `unknown`

#### Scenario: A new bloc is accepted in a user provenance mapping
- **WHEN** a user-supplied knowledge base maps an in-house model pattern to the bloc `sg`
- **THEN** loading succeeds and flows carrying that model reference resolve to `sg`

#### Scenario: A previously deferred family resolves to its developer's bloc
- **WHEN** a flow carries the model reference `tiiuae/falcon-180B` or `falcon-40b-instruct`
- **THEN** its provenance resolves to `ae`

#### Scenario: An org-anchored family resolves via its hub org
- **WHEN** a flow carries the model reference `aisingapore/gemma-sea-lion-v4-27b-it`
- **THEN** its provenance resolves to `sg`

#### Scenario: The Apertus family resolves to Switzerland
- **WHEN** a flow carries the model reference `swiss-ai/Apertus-70B-Instruct` or `apertus-70b-instruct`
- **THEN** its provenance resolves to `ch`

### Requirement: Bundled model provenance map
The system SHALL bundle a model provenance map that resolves model references to a developer
organisation and its provenance bloc, keyed by anchored model-identifier patterns covering:
managed-platform model identifiers, bare API model names, aggregator-qualified identifiers, and
model-hub repository identifiers. The map SHALL carry a last-reviewed date as an ISO-8601
(`YYYY-MM-DD`) value and an advisory note stating that it surfaces weight origin and never
adjudicates export-control applicability. Longest matching pattern SHALL win.

#### Scenario: A managed-platform model identifier resolves
- **WHEN** a flow carries the model reference `deepseek.r1-v1:0` on a managed platform
- **THEN** its provenance resolves to `cn`

#### Scenario: A bare API model name resolves
- **WHEN** a flow carries the model reference `claude-sonnet-4-6`
- **THEN** its provenance resolves to `us`

#### Scenario: A model-hub repository identifier resolves
- **WHEN** a flow carries the model reference `Qwen/Qwen2.5-72B-Instruct`
- **THEN** its provenance resolves to `cn`

### Requirement: Two-tier provenance resolution
The system SHALL resolve a flow's provenance in two tiers: (1) a model reference bound to the
flow resolves via the provenance map; (2) absent a bound model reference, a provider that serves
only its own models SHALL resolve to that organisation's bloc via a provider-level default in
the provenance map. Providers that serve third-party models SHALL have no provider-level default
and SHALL resolve to `unknown` absent a bound model reference.

#### Scenario: First-party provider without a model reference
- **WHEN** a flow is detected for a provider that serves only its own models and no model reference is bound
- **THEN** its provenance resolves to the provider organisation's bloc

#### Scenario: Multi-model host without a model reference
- **WHEN** a flow is detected for a provider that serves third-party models and no model reference is bound
- **THEN** its provenance resolves to `unknown`

#### Scenario: A bound model reference takes precedence
- **WHEN** a flow on a multi-model host carries a bound model reference that matches the map
- **THEN** the model reference's bloc is used, regardless of the provider

### Requirement: Aggregator-qualified identifiers resolve provenance
The system SHALL resolve a flow's provenance from an aggregator-qualified model identifier whose
organisation prefix matches the provenance map, even when the flow's residency and sovereignty
are `unknown`.

#### Scenario: Aggregator flow with a qualified identifier
- **WHEN** a flow through a multi-provider router carries the model reference `deepseek/deepseek-r1`
- **THEN** its provenance resolves to `cn` while residency and sovereignty remain `unknown`

### Requirement: Local model identifiers resolve provenance
The system SHALL resolve provenance for the identifier forms used by local LLM tooling:
(1) a redistributor-qualified identifier — a quantizer or community-conversion org (GGUF/MLX
hubs) followed by a model name — SHALL resolve by disregarding the redistributor org and
matching the remaining model name against the family prefixes, because the redistributor carries
no provenance; (2) a model-file reference ending `.gguf` SHALL match by its file basename,
ignoring directory components; (3) bare local-runtime model names (e.g. Ollama tags) SHALL be
covered by the family prefixes. Tool-name prefixes that merely resemble a model family SHALL NOT
match.

#### Scenario: An MLX community identifier resolves by its model name
- **WHEN** a flow carries the model reference `mlx-community/Qwen2.5-7B-Instruct-4bit`
- **THEN** its provenance resolves to `cn`

#### Scenario: A GGUF file path resolves by its basename
- **WHEN** a flow carries the model reference `models/qwen2.5-7b-instruct-q4_k_m.gguf`
- **THEN** its provenance resolves to `cn`

#### Scenario: A bare local-runtime tag resolves
- **WHEN** a flow carries the model reference `llama3.2`
- **THEN** its provenance resolves to `us`

#### Scenario: A tool name resembling a model family is not matched
- **WHEN** a scanned file contains the string literal `llama_index` or `llama-cpp-python`
- **THEN** no model reference is detected

### Requirement: User provenance overrides
The system SHALL accept provenance overrides from a user-supplied knowledge base; user entries
SHALL take precedence over bundled entries — including over longer bundled prefixes that would
otherwise win the longest-match — and SHALL be validated against the provenance bloc vocabulary.

#### Scenario: User maps an in-house model
- **WHEN** a user mapping assigns the pattern of an in-house model to the organisation's home bloc
- **THEN** flows carrying that model reference resolve to that bloc

#### Scenario: A shorter user pattern beats a longer bundled pattern
- **WHEN** a user mapping assigns `deepseek` to `eu` and the bundled map contains the longer prefix `deepseek-`
- **THEN** the model reference `deepseek-r1` resolves to `eu`

### Requirement: Base-family provenance for derived models
Fine-tuned and distilled model identifiers SHALL inherit the provenance bloc of their base model
family. The system SHALL NOT attempt derivative-weights lineage beyond the base family.

#### Scenario: A fine-tune resolves to its base family's bloc
- **WHEN** a flow carries a model reference for a fine-tune of a `us`-provenance base family
- **THEN** its provenance resolves to `us`

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
