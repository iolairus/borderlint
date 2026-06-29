## Why

borderlint's residency gate is already jurisdiction-agnostic, and the KB already resolves
hyperscaler regions for every major market. But the *context layer* — regime tags and cross-border
arrangement references — is hardcoded to Hong Kong / Mainland / Macao: regimes are limited to
{PDPO, PIPL, Macao PDPA} and arrangement selection only fires for `home_location` ∈ {hk, mo, CN-GBA}.
This blocks borderlint from being a useful tool for entities based elsewhere. This change makes the
context layer data-driven so new home jurisdictions can be added as data, not code — the
prerequisite refactor for adding APAC/EMEA home locations.

## What Changes

- Externalise the hardcoded regime mapping (`_REGIME_OF`) to a bundled `regimes.json` data file
  keyed by jurisdiction, each entry naming the regime and its cross-border arrangement reference(s).
- Generalise regime-tag and arrangement-reference resolution to look up that data for any declared
  `home_location`, while preserving the GBA-span and GDPR-on-EU-destination special cases verbatim.
- Accept any ccTLD/ISO `home_location` (not only hk/mo/CN-GBA); validate it and **warn** (never fail —
  the context layer is informational and must not break a build) when it is unrecognised.
- Normalise the `uk` jurisdiction token to `gb` wherever jurisdictions are compared, so `home_location:
  uk` and `uk` in an allow-list behave as `gb` (today they silently no-op).
- Seed `regimes.json` with the existing hk/mo/cn/CN-GBA mappings only — **no new legal claims**; this
  change ships zero new home jurisdictions and exists to unblock the ones that follow.

## Capabilities

### New Capabilities
<!-- none — this generalises existing behaviour rather than introducing a new capability -->

### Modified Capabilities
- `cli-and-reporting`: regime tags and arrangement references become data-driven and apply to any
  declared `home_location`, no longer limited to {PDPO, PIPL, Macao PDPA} or hk/mo/CN-GBA. Existing
  HK/Mainland/Macao output is unchanged.
- `residency-policy`: a policy MAY declare any ccTLD/ISO `home_location`; an unrecognised value is
  warned, not failed. The legacy `home_regime` path is unchanged.
- `jurisdiction-classification`: the `uk` token is an accepted alias for `gb` in policy allow-lists
  and `home_location`.

## Impact

- Code: `borderlint/report.py` (`_REGIME_OF`, `_regimes`, `_arrangements`), `borderlint/policy.py`
  (`_allowed`, home-location validation), new `borderlint/data/regimes.json`.
- Data: `regimes.json` added; `arrangements.json` unchanged (new arrangements come in a later change).
- Behaviour: additive and backward-compatible — the existing 79 tests stay green; new tests cover the
  `uk` alias, unknown-home warning, and data-driven equivalence for hk/mo/cn.
- No new runtime dependencies (stdlib json only).

## Non-goals

- Adding any new home jurisdiction's regime or legal references (jp/sg/my/id/uk/eu/ae/in/kr/au) — that
  is the follow-on research + wire-up change; this one only ships the engine + the `uk` alias.
- Adjudicating whether any arrangement actually applies — references remain context only.
- New native regional providers in the KB (separate enrichment change).
