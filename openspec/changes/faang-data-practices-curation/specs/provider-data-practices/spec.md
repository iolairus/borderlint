# provider-data-practices Delta

## ADDED Requirements

### Requirement: Curated facts for FAANG first-party AI platforms
The bundled data-practice knowledge base SHALL carry cited entries for `meta_llama`,
`vertex_ai`, `azure_foundry`, and `github_copilot`: each stating the training default for
customer API/platform traffic, the retention posture, and the enterprise/tier distinction where
the platform's terms make one, every non-null fact citing its platform-specific document — Meta
Model API terms, Google Cloud Service Specific Terms "Training restriction" and its generative-AI
zero-data-retention documentation, Microsoft Foundry data-privacy documentation, and GitHub
Generative AI Services Terms respectively. Where a platform's training commitment is tier- or
service-dependent (e.g. Meta's Standard vs Discounted services), the entry SHALL state the
primary default and disclose the split in the tier fact's locator. Facts the cited documents do
not state SHALL remain null with a scope caveat where the omission could mislead.

#### Scenario: Meta Llama entry discloses its service-tier split
- **WHEN** data practices render for `meta_llama`
- **THEN** the training default reflects the Standard Services commitment (content not used to train Meta Models) and the tier fact discloses that Discounted Services may train on content by default

#### Scenario: Vertex entry cites the training restriction and retention paths
- **WHEN** data practices render for `vertex_ai`
- **THEN** the training default cites Google Cloud's training restriction (no training without prior permission), and retention notes the abuse-monitoring logging exemption path and per-feature retention conditions

#### Scenario: Azure Foundry mirrors its sibling posture
- **WHEN** data practices render for `azure_foundry`
- **THEN** the entry states customer data is not used to train foundation models, citing Microsoft Foundry's data-privacy documentation

#### Scenario: GitHub Copilot cites the current generative-AI terms
- **WHEN** data practices render for `github_copilot`
- **THEN** the training default cites the GitHub Generative AI Services Terms (Inputs/Outputs not used to train without documented instruction), and retention notes that per-product retention varies by documented feature

### Requirement: Complete citations without stale notes
Each of the four new entries SHALL cite every non-null fact with a source URL, locator, and
retrieval date, and SHALL NOT claim sources were unreachable; undocumented facts SHALL remain
null.

#### Scenario: Citations complete across the four entries
- **WHEN** the four entries are loaded
- **THEN** every non-null fact has a complete citation and no entry claims unavailability
