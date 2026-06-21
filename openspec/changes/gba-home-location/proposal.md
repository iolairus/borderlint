## Why

borderlint's home model is `home_regime: pdpo|pipl` — binary, Hong-Kong-or-Mainland. But a GBA entity
can be seated in **Hong Kong, Macao, or a Mainland GBA city**, and each has its own data-protection
regime and its own GBA Standard Contract. Macao (the **Personal Data Protection Act, Law 8/2005**,
enforced by the GPDP) and the **(Mainland, Macao) Standard Contract** (facilitated by Macao's DSEDT +
CAC, the counterpart to the (Mainland, Hong Kong) one) are absent. This adds a `home_location` so a
Macao- or Mainland-seated GBA entity gets the right regime tags and the right cross-border arrangement.

## What Changes

- The policy MAY declare a **`home_location`** of `hk`, `mo`, or `CN-GBA`, deriving the home regime:
  `hk` → PDPO, `mo` → Macao PDPA (Law 8/2005), `CN-GBA` → PIPL.
- Add the **(Mainland, Macao) GBA Standard Contract** (DSEDT) to the bundled arrangements; surface the
  Hong-Kong or Macao Standard Contract **variant** by which Special Administrative Region the flow spans.
- Regime tags extend to **{PDPO, PIPL, Macao PDPA}**.
- `home_regime` (`pdpo`/`pipl`) stays accepted (back-compat); existing policies are unaffected.

## Capabilities

### Modified Capabilities
- `cli-and-reporting`: home location within the GBA drives regime tags and the GBA Standard Contract variant.

## Impact

- The report reads `home_location`, derives the regime, and selects the SC variant; one new
  `arrangements.json` entry (the Mainland-Macao SC). Reference-only — no verdict change. No new dependency.

## Non-goals

- Adjudicating Macao adequacy / Art. 19 (reference only, like every arrangement).
- New residency allow-list tokens — `mo` is already a supported destination jurisdiction.
- Home locations outside the GBA, or SAR-to-SAR (`hk`↔`mo`) flows, which no GBA Standard Contract covers.
