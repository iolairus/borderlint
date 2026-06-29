## ADDED Requirements

### Requirement: United Kingdom token alias
The system SHALL treat the jurisdiction token `uk` as an alias for `gb` (ISO-3166 `GB`) wherever a
jurisdiction token is compared — in a classification allow-list and in a declared `home_location` — so
that a policy written with `uk` behaves identically to one written with `gb`.

#### Scenario: uk in an allow-list permits a gb flow
- **WHEN** a classification allow-list contains `uk` and a flow resolves to `gb`
- **THEN** the flow passes the residency check

#### Scenario: uk as a home location is treated as gb
- **WHEN** a policy declares `home_location` `uk`
- **THEN** it is treated identically to `home_location` `gb`
