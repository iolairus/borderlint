## MODIFIED Requirements

### Requirement: Arrangement reference links
For a flagged cross-border flow, the report SHALL surface reference link(s) to the relevant
cross-border arrangement(s), drawn from a bundled arrangements list — each with a name, a URL, and a
one-line summary — selected by the flow's jurisdictions and the declared home regime, as context
only and without adjudicating whether any applies.

#### Scenario: A Hong Kong–GBA flow surfaces the GBA Standard Contract
- **WHEN** a flagged flow crosses between `hk` and `CN-GBA` under a declared home regime
- **THEN** the report surfaces the GBA Standard Contract reference, and not for a plain `cn` destination

#### Scenario: A Mainland China flow surfaces the PIPL reference
- **WHEN** a flagged flow resolves to `cn` (Mainland China, outside the GBA)
- **THEN** the report surfaces the PIPL cross-border transfer reference

#### Scenario: An EU/EEA flow surfaces the GDPR reference
- **WHEN** a flagged flow resolves to an EU/EEA jurisdiction (the `eu` token or an EU/EEA member country code)
- **THEN** the report surfaces the GDPR transfers reference

## ADDED Requirements

### Requirement: Regime tags
The report SHALL tag a flagged flow with the data-protection regime(s) implicated — drawn from the
set {PDPO, PIPL} — derived from the declared home regime and the flow's destination jurisdiction, as
informational context. GDPR is surfaced as an arrangement reference only, never as a regime tag.

#### Scenario: HK entity sending to Mainland China
- **WHEN** the declared home regime is `pdpo` and a flagged flow resolves to `cn` or `CN-GBA`
- **THEN** the flow is tagged with PDPO and PIPL

### Requirement: Context does not change the verdict
Regime tags and arrangement references SHALL NOT change a finding's severity or the exit code, and
SHALL NOT appear as SARIF results or alter any SARIF result's level.

#### Scenario: Tags and references do not affect pass/fail
- **WHEN** a flagged flow is tagged and an arrangement reference is surfaced
- **THEN** its severity and the process exit code are identical to the same flow without tags or references

#### Scenario: SARIF is unaffected
- **WHEN** SARIF output is requested
- **THEN** regime tags and arrangement references add no results and change no result's level
