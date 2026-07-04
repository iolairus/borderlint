## ADDED Requirements

### Requirement: Model provenance coverage check
The scheduled check SHALL compare upstream model identifiers against the bundled provenance map
using the same resolution behaviour the scanner applies, counting an identifier as covered when
the identifier or its remainder after a provider-qualifying prefix resolves. Uncovered
identifiers SHALL be reported aggregated by model family, each family carrying a model count and
one example identifier. The report section SHALL be bounded in length and SHALL disclose how
many families were omitted when the bound is exceeded.

#### Scenario: A provider-qualified identifier counts as covered
- **WHEN** an upstream model identifier carries a provider-qualifying prefix and its remainder resolves via the provenance map
- **THEN** the identifier is not reported as uncovered

#### Scenario: An uncovered family is aggregated
- **WHEN** several upstream model identifiers of one family resolve to no provenance entry
- **THEN** the report lists that family once, with the number of identifiers and one example

#### Scenario: The section bound is disclosed
- **WHEN** the number of uncovered families exceeds the section bound
- **THEN** the section states how many further families were omitted

### Requirement: Sovereignty completeness check
The scheduled check SHALL report every bundled provider entry whose sovereignty bloc is missing
or outside the sovereignty bloc vocabulary, identifying the provider and the offending value.

#### Scenario: A provider without a sovereignty bloc is reported
- **WHEN** a bundled provider entry carries no sovereignty bloc
- **THEN** the report names that provider in the sovereignty section

#### Scenario: Complete entries raise nothing
- **WHEN** every bundled provider entry carries a bloc from the sovereignty vocabulary
- **THEN** the sovereignty section is empty

### Requirement: Knowledge base staleness warning
The scheduled check SHALL warn about each bundled knowledge base whose last-reviewed date is
older than the review interval, naming the knowledge base, its last-reviewed date, and its age.

#### Scenario: A stale knowledge base is flagged
- **WHEN** a bundled knowledge base's last-reviewed date is older than the review interval
- **THEN** the report includes a staleness warning naming it, its date, and its age

#### Scenario: A recently reviewed knowledge base is not flagged
- **WHEN** a bundled knowledge base's last-reviewed date is within the review interval
- **THEN** no staleness warning is raised for it

## MODIFIED Requirements

### Requirement: Scheduled coverage check
The system SHALL provide a scheduled job that periodically produces a freshness report covering:
upstream providers not yet in the bundled provider knowledge base, upstream model identifiers
not resolved by the bundled provenance map, bundled provider entries with missing or invalid
sovereignty blocs, and bundled knowledge bases whose last-reviewed date exceeds the review
interval. Sections with no items SHALL be omitted; when every section is empty, no review item
SHALL be raised; when a review item from a previous run is still open, it SHALL be updated
rather than duplicated.

#### Scenario: A new upstream provider is surfaced
- **WHEN** the scheduled check runs and the upstream list contains a provider absent from the bundled knowledge base
- **THEN** that provider is reported for review, with a prompt to assign endpoint host(s), a jurisdiction, and a sovereignty bloc by hand

#### Scenario: An uncovered model family is surfaced
- **WHEN** the scheduled check runs and an upstream model identifier resolves to no provenance entry
- **THEN** its family is reported for review in the provenance section

#### Scenario: No drift
- **WHEN** the scheduled check runs and every section of the freshness report is empty
- **THEN** no review item is raised

#### Scenario: A persistent condition does not duplicate the review item
- **WHEN** the scheduled check runs with a non-empty report and a review item from a previous run is still open
- **THEN** the open item is updated with the current report and no duplicate is raised

### Requirement: Deterministic coverage diff
Every freshness computation SHALL be a pure, offline function of the bundled knowledge bases,
supplied upstream data, and a supplied reference date, returning exactly the uncovered,
incomplete, or stale items, with no network access.

#### Scenario: Uncovered providers computed from a fixture
- **WHEN** the provider diff runs against a fixed upstream list and the bundled knowledge base
- **THEN** it returns exactly the upstream providers absent from the bundled knowledge base, with no network access

#### Scenario: Provenance and sovereignty checks computed from fixtures
- **WHEN** the model coverage, sovereignty completeness, and staleness checks run against fixed inputs
- **THEN** each returns exactly the uncovered families, incomplete entries, or stale knowledge bases, with no network access

### Requirement: Human-assigned jurisdictions
The coverage check SHALL NOT auto-assign a jurisdiction, endpoint host, sovereignty bloc, or
provenance bloc to any discovered item; each emitted gap record carries none of these, leaving
every assignment for human curation.

#### Scenario: Emitted gap record has no jurisdiction or endpoint
- **WHEN** the check surfaces a new provider
- **THEN** the emitted gap record carries no jurisdiction, no endpoint host, and no sovereignty bloc

#### Scenario: Uncovered model families carry no bloc
- **WHEN** the check surfaces an uncovered model family
- **THEN** the emitted record carries no provenance bloc
