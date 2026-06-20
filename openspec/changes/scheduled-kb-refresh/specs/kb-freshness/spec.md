## ADDED Requirements

### Requirement: Scheduled coverage check
The system SHALL provide a scheduled job that periodically compares the bundled provider knowledge
base against a maintained upstream provider list and reports providers that are not yet covered.

#### Scenario: A new upstream provider is surfaced
- **WHEN** the scheduled check runs and the upstream list contains a provider absent from the bundled knowledge base
- **THEN** that provider is reported for review, for example in an opened pull request or issue

#### Scenario: No drift
- **WHEN** the scheduled check runs and the bundled knowledge base already covers every upstream provider
- **THEN** no review item is raised

### Requirement: Human-assigned jurisdictions
The coverage check SHALL NOT auto-assign a jurisdiction or endpoint host to a discovered provider;
discovered gaps are surfaced for human curation only.

#### Scenario: Discovered gap is not auto-merged
- **WHEN** the check surfaces a new provider
- **THEN** no jurisdiction or endpoint is assigned automatically, and a person assigns them

### Requirement: Knowledge base provenance
The bundled knowledge base SHALL carry a last-reviewed date.

#### Scenario: KB carries a date
- **WHEN** the bundled knowledge base is loaded
- **THEN** a last-reviewed date is available
