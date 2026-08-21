# kb-freshness Delta

## ADDED Requirements

### Requirement: Data-practices staleness coverage
The scheduled coverage check SHALL include the data-practice knowledge base in its
staleness review: entries whose last-reviewed date exceeds the review interval SHALL be
reported for re-review, and providers present in the bundled provider knowledge base but
absent from the data-practice knowledge base SHALL be reported as curation gaps unless
suppressed by the curated suppression list. Gap records SHALL carry no fact values.

#### Scenario: A stale data-practices entry is reported
- **WHEN** the scheduled check runs and a data-practices entry's last-reviewed date exceeds the review interval
- **THEN** that entry is reported for re-review

#### Scenario: A provider without data-practices coverage is a gap
- **WHEN** the scheduled check runs and a bundled provider has no data-practices entry and is not suppressed
- **THEN** the provider is reported as a data-practices curation gap carrying no fact values
