## Context

The `regime-tags-and-arrangements` change made the report derive regime tags and a GBA Standard
Contract reference from `home_regime: pdpo|pipl`. That binary can't express a Macao-seated entity, which
has a distinct regime (Macao PDPA, Law 8/2005) and a distinct Standard Contract (Mainland, Macao).

## Goals / Non-Goals

**Goals:** declare a GBA home location (hk/mo/CN-GBA); derive its regime; surface the matching SC
variant. **Non-Goals:** adjudication; new allow-list tokens; non-GBA homes; `hk`↔`mo` flows.

## Decisions

- **`home_location` is the richer primitive; the regime is derived.** `hk` → PDPO, `mo` → Macao PDPA,
  `CN-GBA` → PIPL. `home_regime` is kept as a back-compat alias (`pdpo` ⇒ `hk` behaviour, `pipl` ⇒
  `CN-GBA` behaviour) so existing policies are byte-for-byte unaffected when `home_location` is absent.
- **The GBA SC variant is chosen by the non-mainland party of the flow.** A flow spanning `CN-GBA` and
  `hk` → the (Mainland, Hong Kong) contract; spanning `CN-GBA` and `mo` → the (Mainland, Macao) contract.
  "Spanning" = the home location is one side and a flagged destination is the other. Each variant is a
  bundled arrangement with its own facilitating authority's URL (HK: Digital Policy Office; Macao: DSEDT).
- **Macao regime token = `Macao PDPA`** — unambiguous; bare `PDPA` collides with Singapore/Malaysia.
- **Reference-only and verdict-invariant.** Like all arrangement/tag context, `home_location` never
  changes the pass/fail decision — that stays the allow-list + deny-by-default.

## Risks / Trade-offs

- A direct `hk`↔`mo` flow (SAR-to-SAR, no Mainland party) surfaces no GBA SC → correct; no such contract
  exists. PIPL/GDPR references are unaffected.
- Coarse selection may surface an SC that doesn't strictly apply → acceptable, it is labelled context.
