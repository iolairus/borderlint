## Why

A flagged cross-border flow today surfaces only the GBA Standard Contract and gives no sense of
*which data-protection regimes* are in play. HK/GBA teams need the regulatory context: which regime
governs the transfer (PDPO / PIPL / GDPR) and which cross-border arrangement(s) *could* apply — as
reviewed context, never enforcement. This adds regime tags and a list-driven arrangements reference.

## What Changes

- **Regime tags** — tag each flagged flow with the data-protection regime(s) implicated, derived
  from the declared home regime and the flow's destination jurisdiction (e.g. PDPO → PIPL for an HK
  entity sending to Mainland China).
- **Arrangements reference list** — replace the single hardcoded GBA reference with a **bundled
  list** (GBA Standard Contract, PIPL cross-border transfer, GDPR Chapter V / SCCs), surfacing the
  arrangement(s) relevant to the flow's jurisdictions and home regime. Reference only — never
  adjudicated or enforced.

## Capabilities

### Modified Capabilities
- `cli-and-reporting`: regime tags on flagged flows; arrangement references drawn from a bundled list
  rather than a single hardcoded scheme.

## Impact

- A bundled `arrangements.json` (name / URL / one-line summary / applicability) and report logic to
  select arrangements and compute regime tags from (home regime, jurisdiction). No scanner or policy
  change; no new dependency.

## Non-goals

- Enforcing or adjudicating any arrangement — selection is heuristic context; applicability is the
  user's legal call.
- A complete global regime map — v1 covers PDPO, PIPL/GBA, and GDPR, matching the HK/GBA lens.
