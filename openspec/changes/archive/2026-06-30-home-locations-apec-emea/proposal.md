## Why

Change 1 made borderlint's regime/arrangement context layer data-driven, and change 2 produced the
verified, cited legal data for ten APAC/EMEA home locations. This change wires the **seven with live
cross-border instruments** into the bundled data so an entity based in Japan, Korea, Singapore,
Australia, the UK, the EU, or Malaysia gets a correct regime tag and a cross-border reference for a
flagged flow — the first user-visible payoff of the home-jurisdiction work.

## What Changes

- Add seven `regimes.json` entries (`jp`→APPI, `kr`→PIPA, `sg`→PDPA (SG), `au`→Privacy Act/APPs,
  `gb`→UK GDPR/DPA 2018, `eu`→GDPR, `my`→PDPA (MY)), each pointing at its cross-border arrangement
  id. `gb` doubles as `uk` via the shipped alias; `eu` reuses the existing `gdpr` arrangement.
- Add six `arrangements.json` entries (`appi_xborder`, `pipa_xborder`, `sg_pdpa_transfer`, `au_app8`,
  `uk_idta`, `my_pdpa_xborder`) with name, one-line summary, and an authoritative URL — sourced and
  status-checked in `backlog/discovery/home-locations-research.md`.
- Add a couple of starter example policies under `examples/` for representative home bases.
- Refresh README and CAPABILITIES to list the supported home locations.
- **Defer** `ae`/`in`/`id` — their instruments are enacted but not operational; research is parked in
  the discovery doc.

## Capabilities

### New Capabilities
<!-- none — extends existing behaviour -->

### Modified Capabilities
- `cli-and-reporting`:
  - ADD a "Home jurisdiction coverage (APAC/EMEA)" requirement pinning, as a tested contract, that each
    of the seven home locations resolves to its regime tag (where one applies) and surfaces its
    cross-border arrangement reference for a flagged flow.
  - MODIFY "Home location" — its "unmapped home degrades gracefully" scenario used `uk` as the
    canonical *unmapped* example; `uk`/`gb` is now mapped, so the example is repointed to `br`.
  - "Regime tags" is **unchanged**: `eu` is deliberately given **no** regime tag (it surfaces the
    `gdpr` arrangement reference only), preserving the existing invariant "GDPR … never as a regime
    tag." "Arrangement reference links" is unchanged.

## Impact

- Data: `borderlint/data/regimes.json` (+7 entries), `borderlint/data/arrangements.json` (+6 entries).
- Docs/examples: `examples/<region>/residency.json`, README, CAPABILITIES.
- Code: none — the change-1 engine already resolves any mapped `home_location`. No new runtime deps.
- Tests: per-region resolution (`home_location: jp` → APPI tag + APPI reference; `uk` → UK IDTA tag +
  reference; `eu` → GDPR reference but no GDPR tag; `my` → s.129). hk/mo/cn output is unchanged; the one
  unmapped-example test (`home_location: uk`) is repointed to `br` since `uk`/`gb` is now mapped.
- Verdict logic untouched — regime tags and references remain context only, never gating.

## Non-goals

- `ae`/`in`/`id` and any other home location not in the seven (deferred or out of scope).
- Adjudicating whether a transfer is lawful — references stay informational.
- A pairwise adequacy matrix, member-state-specific EU handling, or UAE free-zone (DIFC/ADGM) regimes.
- New providers or destination-resolution changes (separate KB track).
