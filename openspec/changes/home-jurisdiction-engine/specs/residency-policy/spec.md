## ADDED Requirements

### Requirement: Home location declaration
The system SHALL allow a policy to declare an optional `home_location` as a lowercase ccTLD/ISO-3166
country code or a recognised special token. A `home_location` that is not well-formed (neither a
two-letter lowercase code nor a recognised special token) SHALL produce a warning and SHALL NOT fail
the run, because the home location drives only informational context — regime tags and arrangement
references — and never the residency verdict.

#### Scenario: A well-formed home location is accepted
- **WHEN** a policy declares `home_location` `jp`
- **THEN** the value is accepted without warning and used to derive informational context

#### Scenario: A malformed home location warns but does not fail
- **WHEN** a policy declares `home_location` `United Kingdom`
- **THEN** borderlint emits a warning and the run's exit code is not changed on account of the home location
