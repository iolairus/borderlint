## ADDED Requirements

### Requirement: Inline waiver annotations
The system SHALL recognise an inline waiver annotation — a `borderlint: allow` comment with a
justification — on the flagged line or the line immediately above it, and associate its
justification with that flow.

#### Scenario: Waiver on the flagged line
- **WHEN** a detected flow's line contains a `borderlint: allow <reason>` comment
- **THEN** that flow is associated with the waiver and its justification `<reason>`

#### Scenario: Waiver on the preceding line
- **WHEN** the line immediately above a detected flow contains a `borderlint: allow <reason>` comment
- **THEN** that flow is associated with the waiver and its justification `<reason>`
