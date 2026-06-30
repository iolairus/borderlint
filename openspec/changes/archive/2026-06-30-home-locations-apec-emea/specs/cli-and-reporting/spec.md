## ADDED Requirements

### Requirement: Home jurisdiction coverage (APAC/EMEA)
The bundled regime map SHALL include the following home jurisdictions, each resolving to the stated
data-protection regime tag (where one applies) and surfacing the stated cross-border arrangement
reference for a flagged cross-border flow, as informational context only (never adjudicated, never
affecting the verdict or exit code):

- `jp` → APPI; reference: APPI cross-border transfer (Art. 28)
- `kr` → PIPA; reference: PIPA overseas transfer (Art. 28-8)
- `sg` → PDPA (SG); reference: PDPA Transfer Limitation Obligation (s.26)
- `au` → Privacy Act / APPs; reference: Australian Privacy Principle 8
- `gb` (and its `uk` alias) → UK GDPR / DPA 2018; reference: UK international data transfer (IDTA / Addendum)
- `eu` → no separate regime tag; reference: GDPR transfers (the existing `gdpr` arrangement). GDPR remains an arrangement reference, never a regime tag.
- `my` → PDPA (MY); reference: Malaysia PDPA cross-border transfer (s.129)

#### Scenario: A Japan home location surfaces APPI
- **WHEN** the policy declares `home_location` `jp` and a flagged flow resolves to a non-`jp` destination
- **THEN** the flow is tagged APPI and the report surfaces the APPI cross-border transfer reference

#### Scenario: A UK home location via the uk alias surfaces the IDTA
- **WHEN** the policy declares `home_location` `uk` and a flagged flow resolves to a non-`gb` destination
- **THEN** the home location is treated as `gb`, the flow is tagged UK GDPR / DPA 2018, and the report surfaces the UK international data transfer (IDTA / Addendum) reference

#### Scenario: An EU home location surfaces the GDPR reference, not a tag
- **WHEN** the policy declares `home_location` `eu` and a flagged flow resolves to a non-EU/EEA destination
- **THEN** the report surfaces the existing GDPR transfers reference, and GDPR is not added as a regime tag

#### Scenario: A Malaysia home location surfaces the s.129 reference
- **WHEN** the policy declares `home_location` `my` and a flagged flow resolves to a non-`my` destination
- **THEN** the flow is tagged PDPA (MY) and the report surfaces the Malaysia PDPA cross-border transfer (s.129) reference

#### Scenario: Coverage is context only
- **WHEN** any of these home locations is declared and a flow is flagged
- **THEN** the regime tag and arrangement reference do not change the finding's severity or the process exit code

#### Scenario: Existing GBA home locations are unchanged
- **WHEN** the policy declares `home_location` `hk` and a flagged flow resolves to `CN-GBA`
- **THEN** the flow is tagged PDPO and PIPL and the report surfaces the GBA Standard Contract, exactly as before this change

## MODIFIED Requirements

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
- **WHEN** the policy declares `home_location` `br` (Brazil, which has no entry in the bundled regime map) and a flagged flow resolves to `us`
- **THEN** no home regime tag and no home-derived arrangement reference are surfaced, and the run is not failed on account of the unmapped home location
