## ADDED Requirements

### Requirement: Local endpoints are always permitted
A flow whose jurisdiction is `local` SHALL never be a residency violation, regardless of the
classification's allow-list, because local inference is not a cross-border transfer.

#### Scenario: Local flow under a strict policy
- **WHEN** a flow resolves to `local` and the active classification's allow-list does not list `local`
- **THEN** the flow passes
