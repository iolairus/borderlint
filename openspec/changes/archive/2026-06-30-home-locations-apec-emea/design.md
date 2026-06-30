## Context

Change 1 (`home-jurisdiction-engine`) replaced the hardcoded HK/CN/MO regime logic with a bundled
`regimes.json` + `arrangements.json` lookup that already resolves *any* mapped `home_location`. Change 2
researched and cited the legal data for ten APAC/EMEA home locations. This change is the **data fill**:
seven entries into the existing maps, plus examples and docs. No engine code changes.

## Goals / Non-Goals

**Goals:**
- Wire the 7 live home locations (`jp/kr/sg/au/gb/eu/my`) into `regimes.json` + `arrangements.json`,
  verbatim from the discovery doc.
- Pin the coverage as a tested contract and document it.
- Keep HK/MO/CN output byte-identical.

**Non-Goals:**
- `ae/in/id` (deferred — instruments not operational).
- Any engine/verdict change; references stay context only.
- Member-state-specific EU handling or UAE free-zone regimes.

## Decisions

**1. Data-only — reuse the change-1 engine.** Add entries to the existing files; write no new code.
`regime_of()` and the home-driven `arrangements` list already surface them. *Alternative — special-case
any of these in `report.py`:* rejected; the whole point of change 1 was to make this data.

**2. Arrangement-id naming + `eu` reuse.** Ids are stable, lowercase, mechanism-scoped
(`appi_xborder`, `pipa_xborder`, `sg_pdpa_transfer`, `au_app8`, `uk_idta`, `my_pdpa_xborder`). `eu`
maps to the **existing** `gdpr` arrangement — no duplicate (and `eu` carries no regime tag, see
Decision 5). `gb` carries `uk_idta`; the shipped `uk`→`gb` alias means `home_location: uk` resolves
here with no extra entry.

**3. Regime-tag strings disambiguate.** `PDPA (SG)` and `PDPA (MY)` are distinct from the existing
`Macao PDPA` and from each other, so a tag is unambiguous in mixed output.

**4. Examples are minimal and representative.** Add a starter `examples/<region>/residency.json` for a
couple of home bases (e.g. `sg`, `gb`) rather than all seven — enough to show the pattern without
bloating the repo. *Alternative — one per home location:* rejected as low-value duplication.

**5. `eu` carries no regime tag — GDPR stays an arrangement reference.** `regimes.json["eu"]` is
`{"regime": null, "arrangements": ["gdpr"]}`, so `regime_of("eu")` is `None` and no tag is emitted; the
home-driven arrangements path still surfaces the `gdpr` reference for an `eu` home. *Alternative — tag
`eu` as GDPR:* rejected; it would violate the existing "Regime tags" invariant ("GDPR … never as a
regime tag") **and** change behaviour for every `eu`-*destination* flow. Treating GDPR uniformly as an
arrangement reference is the smaller, consistent change, and needs **no** MODIFIED on "Regime tags".

**6. Spec deltas: ADD coverage + MODIFY "Home location".** "Regime tags" says the map *includes* the
GBA set ("includes" is non-exhaustive), so the six tagged additions need no MODIFIED there. But
"Home location" used `uk` as its canonical *unmapped* example; `uk`/`gb` is now mapped, so that one
requirement is MODIFIED to repoint the example (and its test) to `br`. So: one ADDED requirement
(coverage) + one MODIFIED requirement ("Home location").

## Risks / Trade-offs

- **Legal currency** → the discovery doc status-checked each instrument (MY live; UK/JP/KR/SG/AU/EU
  live). References are informational, so drift is low-severity; the KB `updated` date and the doc
  record the as-of.
- **`eu` is coarse** (one token, no member-state specifics) → accepted; GDPR is EU-wide.
- **Source-URL permanence** → a couple of citations point at regulator landing pages; fine for a
  reference link, revisit if one rots.

## Migration Plan

Additive and backward-compatible. Existing policies are unaffected; new `home_location` values simply
resolve to context now. Ships in the next release. Rollback = revert the data entries.

## Open Questions

- When `ae/in/id` instruments go operational, wire them from the discovery doc's "Deferred" section.
- Should a future change add a one-per-home-location example set? Deferred — YAGNI until asked.
