## MODIFIED Requirements

### Requirement: Arrangement reference links
For a flagged cross-border flow, the report SHALL surface reference link(s) to the relevant
cross-border arrangement(s), drawn from a bundled arrangements list — each with a name, a URL, and a
one-line summary — selected by the flow's jurisdictions and the declared home regime, as context
only and without adjudicating whether any applies.

#### Scenario: A GBA flow surfaces the GBA Standard Contract
- **WHEN** a flagged flow crosses between `hk` and `CN-GBA` or `cn` under a declared home regime
- **THEN** the report surfaces the GBA Standard Contract reference

#### Scenario: An EU-destination flow surfaces the GDPR reference
- **WHEN** a flagged flow resolves to an EU/EEA jurisdiction
- **THEN** the report surfaces the GDPR transfers reference

## ADDED Requirements

### Requirement: Regime tags
The report SHALL tag a flagged flow with the data-protection regime(s) implicated by the declared
home regime and the flow's destination jurisdiction, as informational context that does not affect
the pass/fail decision.

#### Scenario: HK entity sending to Mainland China
- **WHEN** the declared home regime is `pdpo` and a flagged flow resolves to `cn`
- **THEN** the flow is tagged with the implicated regimes PDPO and PIPL
