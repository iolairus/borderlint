## MODIFIED Requirements

### Requirement: The report leads with an actionable summary
The freshness report SHALL open with a one-line summary stating the count of actionable
providers, actionable model families, providers with SDK-key gaps, and acknowledged residue
identifiers, so a reader can tell whether anything requires a decision without reading the
sections. The summary line SHALL also state the run's reference date as `checked YYYY-MM-DD`,
so two runs with identical findings produce different report bodies and the review item's
in-place update is never a no-op.

#### Scenario: The summary line reflects the sections
- **WHEN** the report renders with two actionable providers, three actionable families, one provider with SDK-key gaps, and ten acknowledged residue identifiers
- **THEN** the leading line states those four counts

#### Scenario: Nothing actionable is visible at a glance
- **WHEN** every section except the residue section is empty
- **THEN** the summary line states zero actionable items

#### Scenario: The summary line states the run date
- **WHEN** the report renders with non-empty findings and reference date 2026-07-20
- **THEN** the summary line states `checked 2026-07-20`

#### Scenario: Identical findings on different dates still update the review item
- **WHEN** two runs on different reference dates produce identical findings
- **THEN** the two report bodies differ in the run date, so updating the open review item is not a content no-op
