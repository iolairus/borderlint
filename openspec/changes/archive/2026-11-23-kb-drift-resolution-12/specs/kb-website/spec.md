## ADDED Requirements

### Requirement: Provider pages tolerate jurisdictions without a single regime

The KB-site generator SHALL omit null regime names for jurisdiction references such as `eu` and
continue building all provider pages. It SHALL NOT invent a regime label or fail site generation.

#### Scenario: Gradium EU endpoint does not break generation
- **WHEN** the bundled provider KB includes Gradium with an `eu` endpoint jurisdiction and the EU
  jurisdiction reference has no single regime name
- **THEN** site generation succeeds, Gradium's page renders its residency facts, and no null regime
  name is rendered
