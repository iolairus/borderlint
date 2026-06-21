## 1. Home location

- [ ] 1.1 Read `home_location` (`hk` | `mo` | `CN-GBA`) from the policy and derive the home regime (`hk`→PDPO, `mo`→Macao PDPA, `CN-GBA`→PIPL); when absent, fall back to `home_regime` (`pdpo`→`hk` behaviour, `pipl`→`CN-GBA` behaviour) so existing policies are unaffected

## 2. Arrangements + tags

- [ ] 2.1 Add the (Mainland, Macao) GBA Standard Contract to `arrangements.json` (DSEDT URL) alongside the existing (Mainland, Hong Kong) one
- [ ] 2.2 Select the GBA Standard Contract variant by the non-mainland party of the flow: the Hong Kong contract for an `hk`↔`CN-GBA` flow, the Macao contract for an `mo`↔`CN-GBA` flow
- [ ] 2.3 Extend the regime-tag set to {PDPO, PIPL, Macao PDPA}, derived from the home location (or home regime) and the destination jurisdiction

## 3. Tests

- [ ] 3.1 Tests: home `mo` + `CN-GBA` flow → Macao SC surfaced + tagged Macao PDPA/PIPL; home `hk` + `CN-GBA` → HK SC + PDPO/PIPL (unchanged); home `CN-GBA` + `mo` flow → Macao SC; `home_regime` `pdpo` with no `home_location` → unchanged behaviour; a `cn` (non-GBA) flow still → PIPL reference and no Standard Contract
