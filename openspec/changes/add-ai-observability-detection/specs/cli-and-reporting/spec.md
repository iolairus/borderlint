# cli-and-reporting Delta

## MODIFIED Requirements

### Requirement: Provider category in output

Reports SHALL surface a provider's category so a data-at-rest sink or observability destination is
distinguishable from an inference API. The category defaults to `inference`, is `vector_store` for managed vector
databases, and is `observability` for Langfuse and LangSmith. The category MUST appear in the text, JSON, and SBOM outputs and MUST NOT change the
pass/fail verdict. Text output SHALL annotate observability providers as `(observability)`.

#### Scenario: Text report marks a vector store
- **WHEN** the text report includes a vector-store provider
- **THEN** its line is annotated as a vector store (e.g. `(vector store)`), distinct from an
  inference provider

#### Scenario: JSON and SBOM carry the category
- **WHEN** output is requested as JSON or SBOM
- **THEN** each finding/component includes a `category` field (`inference`, `vector_store`, or `observability`)

#### Scenario: Category does not affect the verdict
- **WHEN** the same flows are scanned
- **THEN** adding the category changes no severity — pass/fail depends only on jurisdiction and
  provider rules

#### Scenario: Text report marks observability
- **WHEN** a text report includes a Langfuse or LangSmith provider
- **THEN** its provider line is annotated `(observability)`

#### Scenario: JSON and SBOM carry observability category
- **WHEN** a scan with a Langfuse or LangSmith finding renders as JSON or SBOM
- **THEN** the existing category field contains `observability`

#### Scenario: Observability category does not affect the verdict
- **WHEN** an observability flow is evaluated under a residency or unknown-jurisdiction policy
- **THEN** severity and exit status depend on the existing policy rules, not the provider category
