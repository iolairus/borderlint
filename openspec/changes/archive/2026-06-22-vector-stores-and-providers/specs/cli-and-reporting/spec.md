## ADDED Requirements

### Requirement: Provider category in output

Reports SHALL surface a provider's category so a data-at-rest sink is distinguishable from an
inference API. The category defaults to `inference` and is `vector_store` for managed vector
databases. The category MUST appear in the text, JSON, and SBOM outputs and MUST NOT change the
pass/fail verdict.

#### Scenario: Text report marks a vector store
- **WHEN** the text report includes a vector-store provider
- **THEN** its line is annotated as a vector store (e.g. `(vector store)`), distinct from an
  inference provider

#### Scenario: JSON and SBOM carry the category
- **WHEN** output is requested as JSON or SBOM
- **THEN** each finding/component includes a `category` field (`inference` or `vector_store`)

#### Scenario: Category does not affect the verdict
- **WHEN** the same flows are scanned
- **THEN** adding the category changes no severity — pass/fail depends only on jurisdiction and
  provider rules
