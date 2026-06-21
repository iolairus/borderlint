## Context

`regime-tags-and-arrangements` derives regime tags and a GBA Standard Contract reference from
`home_regime: pdpo|pipl`. That binary can't express a Macao-seated entity (regime: Macao PDPA, Law
8/2005; contract: the (Mainland, Macao) Standard Contract). `report._arrangements` / `_regimes` are the
baseline this must not regress.

## Goals / Non-Goals

**Goals:** declare a GBA home location (hk/mo/CN-GBA); derive its regime; surface the matching SC
variant — without regressing existing `home_regime` policies. **Non-Goals:** adjudication; new
allow-list tokens; non-GBA homes; `hk`↔`mo` flows.

## Decisions

- **Dual path — back-compat by construction.** When `home_location` is declared, the report uses the new
  span-based model below. When it is absent, the report runs the **existing `home_regime` code path
  unchanged** — so every current policy is byte-for-byte identical, and the old scenarios are retained
  verbatim. No attempt to "unify" the two (which is what would have regressed the `pipl`→HK-SC case).
- **Span model (home_location path).** A flow "spans" the jurisdictions appearing among `{home_location}`
  ∪ the flagged destinations. The (Mainland, Hong Kong) SC fires when `{hk, CN-GBA}` ⊆ span; the
  (Mainland, Macao) SC when `{mo, CN-GBA}` ⊆ span; both fire if both subsets are present. A plain `cn`
  destination is never part of a GBA span, so it never surfaces a Standard Contract.
- **Tags (home_location path).** `regime_of` applied to the home location and every flagged destination:
  `hk` → PDPO, `mo` → Macao PDPA, `cn`/`CN-GBA` → PIPL. So a `mo` destination contributes a Macao PDPA
  tag — this richer tagging exists only on the `home_location` path; the `home_regime` path keeps its
  narrower tag rule.
- **arrangements.json ids.** Keep `gba` as the (Mainland, Hong Kong) entry (same URL — back-compat); add
  `gba_mo` for the (Mainland, Macao) contract with Macao's DSEDT URL. Clarify `gba`'s display name to
  "GBA Standard Contract (Mainland, Hong Kong)".
- **Macao regime token = `Macao PDPA`** — unambiguous; bare `PDPA` collides with Singapore/Malaysia.
- **Reference-only and verdict-invariant.** `home_location` never touches the pass/fail path — that
  stays the allow-list + deny-by-default. `mo` is already a destination token; no allow-list change.

## Risks / Trade-offs

- A direct `hk`↔`mo` flow (no Mainland party) surfaces no GBA SC → correct; no such contract exists.
- Coarse span selection may surface an SC that doesn't strictly apply → acceptable, labelled context; the
  span rule is deterministic (subset test), so it is never ambiguous about which contracts fire.
