## 1. Arrangement references

- [x] 1.1 Add 6 entries to `borderlint/data/arrangements.json` (`appi_xborder`, `pipa_xborder`, `sg_pdpa_transfer`, `au_app8`, `uk_idta`, `my_pdpa_xborder`) with name, one-line summary, and authoritative URL, verbatim from the discovery doc; bump `updated`.

## 2. Regime map

- [x] 2.1 Add 7 entries to `borderlint/data/regimes.json` (`jp`→APPI, `kr`→PIPA, `sg`→PDPA (SG), `au`→Privacy Act / APPs, `gb`→UK GDPR / DPA 2018, `my`→PDPA (MY)), each with its `arrangements` id(s); `eu` → `{"regime": null, "arrangements": ["gdpr"]}` (no regime tag — reuses the existing `gdpr` arrangement); bump `updated`.

## 3. Examples

- [x] 3.1 Add a starter `examples/<region>/residency.json` for a couple of representative home bases (e.g. `sg`, `gb`) showing `home_location` + a classification allow-list.

## 4. Docs

- [x] 4.1 README: list the supported home locations (the 7) in the Regimes/Scope section.
- [x] 4.2 CAPABILITIES: note APAC/EMEA home-location coverage as shipped; mention `ae/in/id` deferred.

## 5. Tests

- [x] 5.1 Per-region resolution: `home_location` `jp`→APPI tag + APPI reference; `uk`(alias)→UK GDPR tag + IDTA reference; `eu`→GDPR reference **and no GDPR regime tag**; `my`→PDPA (MY) tag + s.129 reference. (Requirement: Home jurisdiction coverage)
- [x] 5.2 Coverage is context only — a covered home location does not change severity or exit code. (Requirement: Home jurisdiction coverage)
- [x] 5.3 Repoint `test_unmapped_home_location_degrades_gracefully` from `home_location: uk` to `br` (uk/gb is now mapped). (Requirement: Home location — MODIFIED)
- [x] 5.4 Regression: hk/mo/cn/CN-GBA output unchanged; full suite green.

## 6. Validate

- [x] 6.1 `openspec validate home-locations-apec-emea --strict` passes; arrangement ids referenced in regimes.json all exist in arrangements.json.
