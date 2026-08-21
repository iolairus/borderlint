# kb-website Delta

## ADDED Requirements

### Requirement: Provider page data-practices section
Each provider page SHALL render a data-practices section when the provider has a curated
entry, stating the training default, retention window, subprocessor link, and
enterprise-tier note, each fact with its source citation rendered as a hyperlink and its
retrieval date. Pages for providers without a curated entry SHALL state that data
practices are not curated for that provider. Every data-practices rendering SHALL include
the advisory disclaimer.

#### Scenario: A curated provider page renders facts with citations
- **WHEN** the page for a provider with a curated data-practices entry is generated
- **THEN** it states the four facts, renders each citation as a hyperlink with its retrieval date, and includes the advisory disclaimer

#### Scenario: An uncurated provider page says so
- **WHEN** the page for a provider without a curated entry is generated
- **THEN** the data-practices section states that data practices are not curated for the provider
