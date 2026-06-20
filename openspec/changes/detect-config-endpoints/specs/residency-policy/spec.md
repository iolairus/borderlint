## ADDED Requirements

### Requirement: Local endpoints are not a residency violation
A flow whose jurisdiction is `local` SHALL NOT count as a residency (allow-list) violation,
regardless of the classification's allow-list, because local inference is not a cross-border
transfer. This exemption applies to the jurisdiction allow-list only; provider deny-lists and other
policy checks still apply.

#### Scenario: Local flow under a strict allow-list
- **WHEN** a flow resolves to `local` and the active classification's allow-list does not list `local`
- **THEN** the flow passes the residency check
