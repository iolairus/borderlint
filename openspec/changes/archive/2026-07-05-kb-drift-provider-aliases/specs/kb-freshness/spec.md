## ADDED Requirements

### Requirement: Upstream provider aliases and out-of-scope names are suppressed
The scheduled check SHALL exclude from the new-provider section any upstream name that is
either mapped as an alias of a covered provider or marked out-of-scope with a stated reason,
via a curated suppression list consumed only by the check — never by the scanner. An alias
whose target provider id is absent from the bundled knowledge base SHALL fail the check
loudly; an out-of-scope entry without a reason SHALL fail the check loudly. Names that are
neither aliased nor ignored SHALL continue to surface.

#### Scenario: A route alias of a covered provider is suppressed
- **WHEN** the upstream list contains a name mapped as an alias of a provider present in the bundled knowledge base
- **THEN** the name does not appear in the new-provider section

#### Scenario: An out-of-scope tool is suppressed with a reason
- **WHEN** the upstream list contains a name marked out-of-scope with a stated reason
- **THEN** the name does not appear in the new-provider section

#### Scenario: An alias to a missing provider fails loudly
- **WHEN** the suppression list maps an upstream name to a provider id absent from the bundled knowledge base
- **THEN** the check fails with an error naming the alias and the missing id

#### Scenario: An ignore without a reason fails loudly
- **WHEN** the suppression list marks an upstream name out-of-scope with an empty reason
- **THEN** the check fails with an error naming the entry

#### Scenario: An unlisted upstream name still surfaces
- **WHEN** the upstream list contains a name that is neither covered, aliased, nor ignored
- **THEN** the name appears in the new-provider section as before

#### Scenario: The scanner never reads the suppression list
- **WHEN** the knowledge base is loaded and a scan runs
- **THEN** the suppression list is not consulted and detection behavior is unchanged

## MODIFIED Requirements

### Requirement: Scheduled coverage check
The system SHALL provide a scheduled job that periodically produces a freshness report covering:
upstream providers not yet in the bundled provider knowledge base and not suppressed by the
curated alias/ignore list, upstream model identifiers not resolved by the bundled provenance
map, bundled provider entries with missing or invalid sovereignty blocs, and bundled knowledge
bases whose last-reviewed date exceeds the review interval. Sections with no items SHALL be
omitted; when every section is empty, no review item SHALL be raised; when a review item from a
previous run is still open, it SHALL be updated rather than duplicated.

#### Scenario: A new upstream provider is surfaced
- **WHEN** the scheduled check runs and the upstream list contains a provider absent from the bundled knowledge base and not suppressed by the alias/ignore list
- **THEN** that provider is reported for review, with a prompt to assign endpoint host(s), a jurisdiction, and a sovereignty bloc by hand — or to record it as an alias or out-of-scope entry

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
supplied upstream data, a supplied curated suppression list, and a supplied reference date,
returning exactly the uncovered, incomplete, or stale items, with no network access.

#### Scenario: Uncovered providers computed from a fixture
- **WHEN** the provider diff runs against a fixed upstream list, the bundled knowledge base, and a fixed suppression list
- **THEN** it returns exactly the upstream providers absent from the bundled knowledge base and not suppressed, with no network access

#### Scenario: Provenance and sovereignty checks computed from fixtures
- **WHEN** the model coverage, sovereignty completeness, and staleness checks run against fixed inputs
- **THEN** each returns exactly the uncovered families, incomplete entries, or stale knowledge bases, with no network access
