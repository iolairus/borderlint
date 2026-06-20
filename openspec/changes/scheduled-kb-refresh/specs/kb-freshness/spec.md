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

### Requirement: Deterministic coverage diff
The coverage comparison SHALL be a pure, offline function of the bundled knowledge base and a
supplied upstream provider list, returning exactly the upstream providers not covered.

#### Scenario: Uncovered providers computed from a fixture
- **WHEN** the diff runs against a fixed upstream list and the bundled knowledge base
- **THEN** it returns exactly the upstream providers absent from the bundled knowledge base, with no network access

### Requirement: Human-assigned jurisdictions
The coverage check SHALL NOT auto-assign a jurisdiction or endpoint host to a discovered provider;
each emitted gap record carries no jurisdiction and no endpoint host, leaving them for human curation.

#### Scenario: Emitted gap record has no jurisdiction or endpoint
- **WHEN** the check surfaces a new provider
- **THEN** the emitted gap record carries no jurisdiction and no endpoint host

### Requirement: Knowledge base provenance
The bundled knowledge base SHALL carry a last-reviewed date as an ISO-8601 (`YYYY-MM-DD`) value in a
top-level metadata field, exposed when the knowledge base is loaded.

#### Scenario: KB carries an ISO date
- **WHEN** the bundled knowledge base is loaded
- **THEN** its last-reviewed date is available as an ISO-8601 `YYYY-MM-DD` value

### Requirement: Refresh does not affect scans
The coverage check SHALL be dev/CI-only; the scanner and knowledge-base load path SHALL perform no
network access.

#### Scenario: The scan path makes no network request
- **WHEN** the knowledge base is loaded and a scan runs
- **THEN** no network request is made
