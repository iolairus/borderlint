## MODIFIED Requirements

### Requirement: Arrangement reference links
For a flagged cross-border flow, the report SHALL surface reference link(s) to the relevant
cross-border arrangement(s), drawn from a bundled arrangements list — each with a name, a URL, and a
one-line summary — selected by the flow's jurisdictions and the declared home location or home regime,
as context only and without adjudicating whether any applies. When a `home_location` is declared, the
report SHALL surface the cross-border arrangement reference(s) mapped to that home location in the
bundled regime map; a home location that maps to no arrangement SHALL surface no home-derived
reference. The Greater Bay Area facilitation is one such mapping: the report SHALL surface the GBA
Standard Contract variant matching the Special Administrative Region in the flow — the (Mainland, Hong
Kong) contract for a flow spanning `hk` and `CN-GBA`, and the (Mainland, Macao) contract for a flow
spanning `mo` and `CN-GBA` (a flow spanning both SARs surfaces both), where a flow "spans" the
jurisdictions appearing among the home location and the flagged destinations. A plain `cn` destination
SHALL NOT surface any GBA Standard Contract. A flagged flow to an EU/EEA jurisdiction SHALL surface the
GDPR transfers reference. When no `home_location` is declared, a declared `home_regime` SHALL surface
the existing GBA Standard Contract reference exactly as before.

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

#### Scenario: A home location with no mapped arrangement surfaces none
- **WHEN** the declared `home_location` maps to no cross-border arrangement in the bundled regime map and a flagged flow resolves to a non-EU/EEA destination
- **THEN** no home-derived arrangement reference is surfaced and the flow is still reported

### Requirement: Regime tags
The report SHALL tag a flagged flow with the data-protection regime(s) implicated, drawn from the
bundled regime map, as informational context. When a `home_location` is declared, the tags SHALL be
derived from the regime mapped to the home location and the regime mapped to each flagged destination;
a jurisdiction with no mapped regime SHALL contribute no tag. The bundled map includes `hk` → PDPO,
`mo` → Macao PDPA, and `cn`/`CN-GBA` → PIPL. When no `home_location` is declared, the tags SHALL be
derived from the declared `home_regime` and `cn`/`CN-GBA` destinations exactly as before (`pdpo` →
PDPO, `pipl` or a `cn`/`CN-GBA` destination → PIPL). GDPR is surfaced as an arrangement reference only,
never as a regime tag.

#### Scenario: HK entity sending to Mainland China
- **WHEN** the declared home regime is `pdpo` and a flagged flow resolves to `cn` or `CN-GBA`
- **THEN** the flow is tagged with PDPO and PIPL

#### Scenario: Macao entity sending to the Mainland GBA
- **WHEN** the declared home location is `mo` and a flagged flow resolves to `CN-GBA`
- **THEN** the flow is tagged with Macao PDPA and PIPL

#### Scenario: A Macao destination implies the Macao regime
- **WHEN** the declared home location is `hk` and a flagged flow resolves to `mo`
- **THEN** the flow is tagged with PDPO and Macao PDPA

#### Scenario: An unmapped jurisdiction contributes no regime tag
- **WHEN** the declared home location maps to no regime and a flagged flow resolves to a destination that maps to no regime
- **THEN** no regime tag is surfaced for that flow

## REMOVED Requirements

### Requirement: Home location within the GBA
**Reason**: Superseded by the general "Home location" requirement — `home_location` is no longer limited to the Greater Bay Area seats.
**Migration**: The hk/mo/CN-GBA behaviour is preserved verbatim by the bundled regime map; declare the same `home_location` value as before. See "Home location", "Regime tags", and "Arrangement reference links".

## ADDED Requirements

### Requirement: Home location
The report SHALL accept an optional `home_location` in the policy, expressed as a lowercase
ccTLD/ISO-3166 country code or a recognised special token, identifying the entity's seat, and SHALL
derive the home data-protection regime tag and cross-border arrangement reference(s) from the bundled
regime map. The Greater Bay Area seats `hk`, `mo`, and `CN-GBA` map respectively to PDPO, Macao PDPA,
and PIPL and select the GBA Standard Contract variant. A `home_location` with no entry in the bundled
regime map SHALL derive no home regime tag and no home-derived arrangement reference, without failing
the run. When `home_location` is absent, the report SHALL use a declared `home_regime` (`pdpo` or
`pipl`) with its existing regime-tag and arrangement behaviour unchanged.

#### Scenario: A Macao home location implies the Macao regime and contract
- **WHEN** the policy declares `home_location` `mo` and a flagged flow resolves to `CN-GBA`
- **THEN** the flow is tagged Macao PDPA (home) and the report surfaces the (Mainland, Macao) Standard Contract

#### Scenario: home_regime pdpo is unchanged
- **WHEN** the policy declares `home_regime` `pdpo` and no `home_location`
- **THEN** regime tags and arrangement references behave as before — PDPO home, the GBA Standard Contract for a `CN-GBA` flow

#### Scenario: home_regime pipl is unchanged
- **WHEN** the policy declares `home_regime` `pipl` and no `home_location`, and a flagged flow resolves to `CN-GBA`
- **THEN** regime tags and arrangement references behave as before — a PIPL tag and the existing GBA Standard Contract reference

#### Scenario: An unmapped home location degrades gracefully
- **WHEN** the policy declares `home_location` `uk` (an alias for `gb`, which has no entry in the bundled regime map in this change) and a flagged flow resolves to `us`
- **THEN** no home regime tag and no GBA Standard Contract are surfaced, and the run is not failed on account of the unmapped home location
