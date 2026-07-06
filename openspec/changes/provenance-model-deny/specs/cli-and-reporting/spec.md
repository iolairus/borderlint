## ADDED Requirements

### Requirement: The model's developer organisation is reported
Report output SHALL name the model's developer organisation, when the provenance map knows it,
alongside the model identifier: as a field in the JSON report, beside the model in the text
report, and per site in the SBOM. The `model_denied` reason SHALL have a human-readable
description in report output. Findings whose model resolved without a known organisation SHALL
render exactly as before.

#### Scenario: JSON carries the organisation
- **WHEN** the JSON report renders a finding whose model reference resolved via a map pattern carrying an organisation
- **THEN** the finding object includes a `model_org` field naming it

#### Scenario: Text names the organisation beside the model
- **WHEN** the text report renders a flow with a bound model whose organisation is known
- **THEN** the model annotation names the organisation

#### Scenario: Unknown organisation changes nothing
- **WHEN** a finding's model resolved via a user-KB pattern with no organisation
- **THEN** the report renders as before, with no empty organisation field
