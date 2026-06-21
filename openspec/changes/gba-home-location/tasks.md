## 1. Home location (dual path)

- [ ] 1.1 Read `home_location` (`hk` | `mo` | `CN-GBA`) from the policy. When present, use the span-based selection + location-derived tags below. When absent, leave the existing `home_regime` code path (`_arrangements` / `_regimes`) **unchanged** — existing policies must be byte-for-byte identical

## 2. Arrangements + tags (home_location path)

- [ ] 2.1 `arrangements.json`: keep `gba` as the (Mainland, Hong Kong) entry (same URL); add `gba_mo` — the (Mainland, Macao) GBA Standard Contract — with Macao's DSEDT URL; clarify `gba`'s name as "(Mainland, Hong Kong)"
- [ ] 2.2 Select the SC variant by the SAR in the flow span (`{home_location}` ∪ flagged destinations): the Hong Kong contract when `{hk, CN-GBA}` ⊆ span, the Macao contract when `{mo, CN-GBA}` ⊆ span, both when both; never for a plain `cn` destination
- [ ] 2.3 Derive regime tags from {PDPO, PIPL, Macao PDPA} via `regime_of` over the home location and each flagged destination: `hk`→PDPO, `mo`→Macao PDPA, `cn`/`CN-GBA`→PIPL

## 3. Tests

- [ ] 3.1 `home_location` path: `mo` + `CN-GBA` → Macao SC + tags {Macao PDPA, PIPL}; `hk` + `CN-GBA` → HK SC + {PDPO, PIPL}; `CN-GBA` + flows to both `hk` and `mo` → both SCs; `hk` + `mo` destination → tags {PDPO, Macao PDPA}; a plain `cn` flow → PIPL reference and no Standard Contract
- [ ] 3.2 Back-compat (no `home_location`): `home_regime` `pdpo` → HK SC + {PDPO, PIPL} unchanged; `home_regime` `pipl` + `CN-GBA` → existing GBA reference + PIPL tag unchanged; a `mo` destination under `home_regime` only → no Macao PDPA tag (old behaviour preserved)
