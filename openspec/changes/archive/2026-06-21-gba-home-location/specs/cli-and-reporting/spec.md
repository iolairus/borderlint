## MODIFIED Requirements

### Requirement: Arrangement reference links
For a flagged cross-border flow, the report SHALL surface reference link(s) to the relevant
cross-border arrangement(s), drawn from a bundled arrangements list — each with a name, a URL, and a
one-line summary — selected by the flow's jurisdictions and the declared home location or home regime,
as context only and without adjudicating whether any applies. When a `home_location` is declared, the
report SHALL surface the GBA Standard Contract variant matching the Special Administrative Region in the
flow — the (Mainland, Hong Kong) contract for a flow spanning `hk` and `CN-GBA`, and the (Mainland,
Macao) contract for a flow spanning `mo` and `CN-GBA` (a flow spanning both SARs surfaces both), where a
flow "spans" the jurisdictions appearing among the home location and the flagged destinations. A plain
`cn` destination SHALL NOT surface any GBA Standard Contract. When no `home_location` is declared, a
declared `home_regime` SHALL surface the existing GBA Standard Contract reference exactly as before.

#### Scenario: A Hong Kong–GBA flow surfaces the GBA Standard Contract
- **WHEN** a flagged flow crosses between `hk` and `CN-GBA` under a declared home regime
- **THEN** the report surfaces the GBA Standard Contract reference, and not for a plain `cn` destination

#### Scenario: A Macao–GBA flow surfaces the (Mainland, Macao) Standard Contract
- **WHEN** the home location is `mo` and a flagged flow resolves to `CN-GBA` (or the home location is `CN-GBA` and a flagged flow resolves to `mo`)
- **THEN** the report surfaces the (Mainland, Macao) GBA Standard Contract

#### Scenario: A flow spanning both SARs surfaces both contracts
- **WHEN** the home location is `CN-GBA` and flagged flows resolve to both `hk` and `mo`
- **THEN** the report surfaces both the (Mainland, Hong Kong) and the (Mainland, Macao) GBA Standard Contracts

#### Scenario: A Mainland China flow surfaces the PIPL reference
- **WHEN** a flagged flow resolves to `cn` (Mainland China, outside the GBA)
- **THEN** the report surfaces the PIPL cross-border transfer reference

#### Scenario: An EU/EEA flow surfaces the GDPR reference
- **WHEN** a flagged flow resolves to an EU/EEA jurisdiction (the `eu` token or an EU/EEA member country code)
- **THEN** the report surfaces the GDPR transfers reference

### Requirement: Regime tags
The report SHALL tag a flagged flow with the data-protection regime(s) implicated — drawn from the
set {PDPO, PIPL, Macao PDPA} — as informational context. When a `home_location` is declared, the tags
SHALL be derived from the home location and each flagged destination, where `hk` implies PDPO, `mo`
implies Macao PDPA, and `cn` or `CN-GBA` implies PIPL. When no `home_location` is declared, the tags
SHALL be derived from the declared `home_regime` and `cn`/`CN-GBA` destinations exactly as before
(`pdpo` → PDPO, `pipl` or a `cn`/`CN-GBA` destination → PIPL). GDPR is surfaced as an arrangement
reference only, never as a regime tag.

#### Scenario: HK entity sending to Mainland China
- **WHEN** the declared home regime is `pdpo` and a flagged flow resolves to `cn` or `CN-GBA`
- **THEN** the flow is tagged with PDPO and PIPL

#### Scenario: Macao entity sending to the Mainland GBA
- **WHEN** the declared home location is `mo` and a flagged flow resolves to `CN-GBA`
- **THEN** the flow is tagged with Macao PDPA and PIPL

#### Scenario: A Macao destination implies the Macao regime
- **WHEN** the declared home location is `hk` and a flagged flow resolves to `mo`
- **THEN** the flow is tagged with PDPO and Macao PDPA

## ADDED Requirements

### Requirement: Home location within the GBA
The report SHALL accept an optional `home_location` of `hk`, `mo`, or `CN-GBA` in the policy,
identifying the entity's seat within the Greater Bay Area, and SHALL derive the home data-protection
regime from it — `hk` → PDPO, `mo` → Macao PDPA (Law 8/2005), `CN-GBA` → PIPL — and select the GBA
Standard Contract variant accordingly. When `home_location` is absent, the report SHALL use a declared
`home_regime` (`pdpo` or `pipl`) with its existing regime-tag and arrangement behaviour unchanged.

#### Scenario: A Macao home location implies the Macao regime and contract
- **WHEN** the policy declares `home_location` `mo` and a flagged flow resolves to `CN-GBA`
- **THEN** the flow is tagged Macao PDPA (home) and the report surfaces the (Mainland, Macao) Standard Contract

#### Scenario: home_regime pdpo is unchanged
- **WHEN** the policy declares `home_regime` `pdpo` and no `home_location`
- **THEN** regime tags and arrangement references behave as before — PDPO home, the GBA Standard Contract for a `CN-GBA` flow

#### Scenario: home_regime pipl is unchanged
- **WHEN** the policy declares `home_regime` `pipl` and no `home_location`, and a flagged flow resolves to `CN-GBA`
- **THEN** regime tags and arrangement references behave as before — a PIPL tag and the existing GBA Standard Contract reference
