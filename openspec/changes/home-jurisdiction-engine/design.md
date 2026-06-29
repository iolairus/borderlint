## Context

The residency verdict (`policy.evaluate`) is already jurisdiction-agnostic — it never reads
`home_location`. The only HK/Mainland/Macao hardcoding is the **context layer** in `report.py`:
`_REGIME_OF` (a 4-entry dict) and `_arrangements()` / `_regimes()`, which branch on
`home_location ∈ {hk, mo, CN-GBA}`. Adding home jurisdictions one-by-one in code would balloon those
branches. This change turns the context layer into a data lookup so later changes add jurisdictions as
data, mirroring how `providers.json` and `arrangements.json` already work. It ships **no new legal
claims** — only the engine and the `uk`→`gb` alias.

## Goals / Non-Goals

**Goals:**
- Replace `_REGIME_OF` with a bundled `regimes.json` keyed by jurisdiction.
- Make `_regimes()` and `_arrangements()` resolve any declared `home_location` via that data, with
  HK/Mainland/Macao output byte-identical to today.
- Accept any well-formed `home_location`; warn (never fail) on a malformed one.
- Normalise `uk` to `gb` wherever jurisdiction tokens are compared.

**Non-Goals:**
- Any new jurisdiction's regime/arrangement data (follow-on change).
- A full pairwise adequacy/transfer matrix — references stay context-only.
- ISO-3166 membership validation of `home_location` (format-level only here).

## Decisions

**1. Data file `borderlint/data/regimes.json`, loaded like `arrangements.json`.**
Schema is an envelope matching `arrangements.json`/`providers.json` (so it can carry provenance per
the `kb-freshness` discipline):
`{"updated": "YYYY-MM-DD", "regimes": {"<jurisdiction>": {"regime": "<tag>", "arrangements": ["<arrangement-id>", ...]}}}`,
loaded via `json.load(fh)["regimes"]`. `arrangement-id` references `arrangements.json`. Seeded with
exactly the current mappings (`hk`→PDPO, `mo`→Macao PDPA, `cn`/`CN-GBA`→PIPL) and **empty**
`arrangements` lists.
*Alternative — keep the hardcoded dict and just append entries:* rejected; the follow-on change adds
~10 jurisdictions plus legal reference links best reviewed as data (same discipline as provider
jurisdictions), and a data file keeps `report.py` stable.

**2. Split general (data) from special (code).** `regime` per jurisdiction is a flat fact → fully
data-driven via `regime_of(j)`. Arrangement *selection* is partly destination-conditional, so:
- The GBA-span variant selection, the plain-`cn`→PIPL reference, and the EU/EEA-destination→GDPR
  reference stay as code special-cases, preserved verbatim.
- `regimes.json[home].arrangements` is a flat, home-driven list surfaced for any flagged cross-border
  flow — the mechanism by which future single-reference jurisdictions (e.g. an APPI home) work without
  new code. Seeded entries keep it empty, so today's output is unchanged.
*Alternative — model everything as flat per-home arrangement lists:* rejected; the GBA facilitation is
pairwise (depends on which SAR the destination is), not a flat home fact.

**3. `uk`→`gb` normalisation at the comparison boundary.** A one-line `_norm(token)` applied in
`policy._allowed` and when reading `home_location`. *Alternative — add `uk` as a distinct entry in the
display/region maps:* rejected; it would fragment `gb`/`uk` everywhere. `.uk` is the ccTLD for ISO
`GB`, so the alias is unambiguous.

**4. `home_location` validation is format-level and warns on stderr.** Well-formed = a recognised
special token or a two-letter lowercase code (after `uk`→`gb`). A malformed value warns to **stderr**
(so machine output on stdout stays clean) and never changes the exit code. *Alternative — validate
against a bundled ISO-3166 list:* rejected; no stdlib list, bundling one is scope creep, and the
format check already catches the common error (a full country name or wrong case).
`# ponytail: format-level only; tighten to a known-set if typo'd-but-well-formed codes matter`.

## Risks / Trade-offs

- **Regime map and arrangement selection drift apart** → both live in `regimes.json`; regression tests
  assert hk/mo/cn/CN-GBA regime-tag and arrangement output is identical to pre-change.
- **Weak validation (`zz` passes the format check)** → accepted and documented; tightening is a future
  option, not a correctness bug (an unmapped home location degrades gracefully to no context).
- **`report.py` reads a second data file at import** → same proven pattern as `arrangements.json`; no
  new dependency, negligible cost.

## Migration Plan

Additive and backward-compatible. No existing policy file changes; `home_regime` keeps working;
`home_location` simply accepts more values. Rollback = revert the change (restores the hardcoded
`_REGIME_OF`); `regimes.json` is self-contained.

## Open Questions

- Should `home_location` validation later check ISO-3166 membership? Deferred.
- Does `eu` belong in `regimes.json` as a *home* (not just a destination)? Deferred to the wire-up change.
- `uk`→`gb` is normalised only for allow-lists and `home_location`, not for a *resolved* jurisdiction:
  a user endpoints map that resolves a flow to `uk` would not be normalised and would fail a `gb`
  allow-list. `uk` is not an ISO code, so this is niche and out of the alias requirement's contract;
  tighten by normalising at the resolution boundary if it ever bites.
- Scope: the `uk`→`gb` alias is separable from the engine refactor. Kept bundled because `uk` is in
  the home-location set this work series enables and the fix is a single normalisation; split into its
  own change only if review insists.
