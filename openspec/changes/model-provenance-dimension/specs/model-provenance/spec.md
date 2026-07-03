## ADDED Requirements

### Requirement: Provenance bloc vocabulary
The system SHALL express model provenance using the blocs `us`, `eu`, `cn`, `uk`, `ru`, `in`,
`il`, `ca`, and `unknown` — the sovereignty vocabulary without `local`, because model weights
always have a developer. The `unknown` bloc represents a provenance that cannot be statically
determined. The system SHALL NOT emit any provenance value outside this vocabulary, and SHALL
reject a user-supplied provenance mapping that uses a token outside it.

#### Scenario: Invalid provenance token in a user mapping is rejected
- **WHEN** a user-supplied knowledge base maps a model pattern to the bloc `overseas`
- **THEN** loading fails with an error naming the invalid token and the accepted vocabulary

#### Scenario: Unmatched model reference resolves to unknown
- **WHEN** a model reference matches no pattern in the provenance map
- **THEN** its provenance is `unknown`

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

### Requirement: User provenance overrides
The system SHALL accept provenance overrides from a user-supplied knowledge base; user entries
SHALL take precedence over bundled entries and SHALL be validated against the provenance bloc
vocabulary.

#### Scenario: User maps an in-house model
- **WHEN** a user mapping assigns the pattern of an in-house model to the organisation's home bloc
- **THEN** flows carrying that model reference resolve to that bloc

### Requirement: Base-family provenance for derived models
Fine-tuned and distilled model identifiers SHALL inherit the provenance bloc of their base model
family. The system SHALL NOT attempt derivative-weights lineage beyond the base family.

#### Scenario: A fine-tune resolves to its base family's bloc
- **WHEN** a flow carries a model reference for a fine-tune of a `us`-provenance base family
- **THEN** its provenance resolves to `us`
