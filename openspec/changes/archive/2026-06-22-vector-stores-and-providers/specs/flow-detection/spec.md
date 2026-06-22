## ADDED Requirements

### Requirement: Detect managed vector-database usage

borderlint SHALL detect managed vector-database (vector DBaaS) usage — via the provider's SDK
import or its managed endpoint host — and treat it as an AI data flow subject to the residency
policy. Each such provider MUST carry the category `vector_store`. Because a vector cluster's
region is chosen per deployment, the default jurisdiction for a vector-store provider SHALL be
`unknown`, refined to a specific jurisdiction only when its endpoint host resolves one.

#### Scenario: Vector-store SDK import is detected
- **WHEN** Python source imports a managed vector-database SDK (e.g. `import pinecone`)
- **THEN** a detection is recorded for that provider with category `vector_store` and
  jurisdiction `unknown`

#### Scenario: Vector-store endpoint is detected
- **WHEN** a source or config file references a managed vector-database host (e.g. a
  `*.pinecone.io` URL)
- **THEN** a detection is recorded for that provider with category `vector_store`

#### Scenario: A vector-store flow is governed by the policy
- **WHEN** a vector-store detection resolves to `unknown` and the policy sets `on_unknown: fail`
- **THEN** the flow fails the build, exactly as any other unknown-jurisdiction flow would
