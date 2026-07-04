## MODIFIED Requirements

### Requirement: Provenance bloc vocabulary
The system SHALL express model provenance using the blocs `us`, `eu`, `cn`, `uk`, `ru`, `in`,
`il`, `ca`, `jp`, `kr`, `sg`, `au`, `ae`, and `unknown` — the sovereignty vocabulary without
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
