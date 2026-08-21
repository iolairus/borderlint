# policy-init Delta

## ADDED Requirements

### Requirement: Profile flag
The `init` command SHALL accept an optional `--profile <id>` flag that pre-seeds the
interview from the named bundled regulator profile; without the flag, the wizard SHALL behave
exactly as before. In non-interactive mode, the profile defaults SHALL compose with observed
jurisdictions by union, and the home base SHALL be pre-seeded in every class allow-list as
usual.

#### Scenario: Default behaviour unchanged without the flag
- **WHEN** init runs without `--profile`
- **THEN** the interview, walk, and emitted policy match the pre-profile behaviour exactly

#### Scenario: Non-interactive composition
- **WHEN** init runs with `--home hk --classes customer-pii --profile hkma`
- **THEN** the customer-pii allow-list is the union of the profile defaults, the observed jurisdictions, and `hk`

#### Scenario: Interactive walk starts from the seed
- **WHEN** init runs interactively with a profile
- **THEN** each handled class's walk offers the seeded jurisdictions with keep as the default answer, droppable by the operator
