## MODIFIED Requirements

### Requirement: Arrangement reference links
For a flagged cross-border flow, the report SHALL surface reference link(s) to the relevant
cross-border arrangement(s), drawn from a bundled arrangements list — each with a name, a URL, and a
one-line summary — selected by the flow's jurisdictions and the declared home location (or home
regime), as context only and without adjudicating whether any applies. For a flow spanning a Mainland
GBA city and a Special Administrative Region, the report SHALL surface the matching GBA Standard
Contract variant: the (Mainland, Hong Kong) contract when the SAR party is `hk`, and the (Mainland,
Macao) contract when the SAR party is `mo`.

#### Scenario: A Hong Kong–GBA flow surfaces the (Mainland, Hong Kong) Standard Contract
- **WHEN** the home location is `hk` (or home regime `pdpo`) and a flagged flow resolves to `CN-GBA`
- **THEN** the report surfaces the GBA Standard Contract (Mainland, Hong Kong), and not for a plain `cn` destination

#### Scenario: A Macao–GBA flow surfaces the (Mainland, Macao) Standard Contract
- **WHEN** the home location is `mo` and a flagged flow resolves to `CN-GBA` (or the home location is `CN-GBA` and a flagged flow resolves to `mo`)
- **THEN** the report surfaces the GBA Standard Contract (Mainland, Macao)

#### Scenario: A Mainland China flow surfaces the PIPL reference
- **WHEN** a flagged flow resolves to `cn` (Mainland China, outside the GBA)
- **THEN** the report surfaces the PIPL cross-border transfer reference

#### Scenario: An EU/EEA flow surfaces the GDPR reference
- **WHEN** a flagged flow resolves to an EU/EEA jurisdiction (the `eu` token or an EU/EEA member country code)
- **THEN** the report surfaces the GDPR transfers reference

### Requirement: Regime tags
The report SHALL tag a flagged flow with the data-protection regime(s) implicated — drawn from the
set {PDPO, PIPL, Macao PDPA} — derived from the declared home location (or home regime) and the flow's
destination jurisdiction, as informational context. A home location of `hk` implies PDPO, `mo` implies
Macao PDPA, and `CN-GBA` implies PIPL; a destination of `cn` or `CN-GBA` implies PIPL, `hk` implies
PDPO, and `mo` implies Macao PDPA. GDPR is surfaced as an arrangement reference only, never as a regime tag.

#### Scenario: HK entity sending to Mainland China
- **WHEN** the declared home location is `hk` (or home regime `pdpo`) and a flagged flow resolves to `cn` or `CN-GBA`
- **THEN** the flow is tagged with PDPO and PIPL

#### Scenario: Macao entity sending to the Mainland GBA
- **WHEN** the declared home location is `mo` and a flagged flow resolves to `CN-GBA`
- **THEN** the flow is tagged with Macao PDPA and PIPL

## ADDED Requirements

### Requirement: Home location within the GBA
The report SHALL accept an optional `home_location` of `hk`, `mo`, or `CN-GBA` in the policy,
identifying the entity's seat within the Greater Bay Area, and SHALL derive the home data-protection
regime from it — `hk` → PDPO, `mo` → Macao PDPA (Law 8/2005), `CN-GBA` → PIPL — and select the GBA
Standard Contract variant accordingly. When `home_location` is absent, the report SHALL continue to use
a declared `home_regime` (`pdpo` or `pipl`) unchanged.

#### Scenario: A Macao home location implies the Macao regime and contract
- **WHEN** the policy declares `home_location` `mo` and a flagged flow resolves to `CN-GBA`
- **THEN** the flow is tagged Macao PDPA (home) and the report surfaces the (Mainland, Macao) Standard Contract

#### Scenario: home_regime remains accepted
- **WHEN** the policy declares `home_regime` `pdpo` and no `home_location`
- **THEN** regime tags and arrangement references behave as before — PDPO home, the (Mainland, Hong Kong) Standard Contract
