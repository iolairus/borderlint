# Proposal: kb-drift-resolution-3

## Why

The 2026-09-30 freshness run reports two uncovered upstream providers, nine unresolved model
families, and — for the first time — two knowledge bases past the 90-day review interval
(`arrangements.json`, `regimes.json`, both last reviewed 2026-06-30). Until each drift item is
assigned by hand and the legal references are re-reviewed, new flows classify as `unknown`
and the staleness section keeps the review queue from converging.

## What Changes

- Add two bundled provider entries, both San Francisco inference platforms serving
  open-weight third-party models:
  - `prism` — Prism Inference (YC-backed; endpoint `api.prisminference.com`), jurisdiction
    and sovereignty `us`.
  - `sail` — Sail Research (endpoint `api.sailresearch.com`), jurisdiction and sovereignty
    `us`.
- Add `prism/` and `sail/` as provenance passthroughs (host route prefixes carry no
  provenance; both catalogs then resolve via existing org patterns), plus the one org their
  catalogs surface that the map lacks: `zai-org/` (Zhipu's Hugging Face org) → `cn`.
- Add provenance patterns for the remaining families, blocs confirmed by the maintainer
  2026-10-02:
  - `us` — Microsoft AI `mai-cyber`/`mai-image` (the new MAI lines on Foundry), OpenAI
    `fw-gpt-oss` (Fireworks-on-Foundry redistribution, per the established FW-* precedent),
    Google `deep-research` and `virtual-try-on`, Together AI's own `together/` org (`Tev1`),
    and — folded in as follow-on drift when it appeared upstream 2026-10-01, per the
    PR #96 precedent — `apodex` (Apodex, Redwood City; own reasoning models, maintainer-
    confirmed 2026-10-02)
  - `ca` — Cohere `c4ai-` (Cohere For AI Aya Expanse, sibling of the existing `aya-`)
  - `cn` — `ember` → Moonshot AI (Fireworks Research's Ember-1 is a post-train of Kimi K3;
    fine-tunes inherit the base family's bloc, per the magnum precedent)
- Record structural residue for Fireworks' router endpoints
  (`fireworks_ai/accounts/fireworks/routers/` prefix — routing products, not models), and
  extend the existing Pareto composite-product judgment to its versioned releases
  (`openrouter/unbiased/pareto-` prefix, triggered by `pareto-26.10-preview`).
- Complete the 90-day review of `arrangements.json` and `regimes.json`: all ten arrangement
  summaries verified still accurate (the in-window legal changes — CAC's Jul-2026
  cross-border Q&A, Japan's promulgated-but-not-in-force APPI amendment, Korea's PIPA
  enforcement amendment effective 2026-09-11 — are administrative/enforcement-side and do
  not alter the summarized transfer mechanics), so the files' `updated` dates are bumped
  with the review evidence recorded in this change's design.
- Bump the review dates of the touched provider/provenance/sovereignty files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `jurisdiction-classification`: the two new providers resolve with jurisdiction `us`.
- `model-provenance`: the drift-run model families resolve to their developer
  organisations' blocs, including the Ember base-inheritance call and the two new host
  passthroughs.

## Impact

- `borderlint/data/providers.json` (+2 entries), `sovereignty.json` (+2 mappings),
  `provenance.json` (+2 passthroughs, +19 patterns), `scripts/kb_drift_aliases.json`
  (+2 residue entries), `arrangements.json` + `regimes.json` (review-date bumps only).
- Detection tests for the new endpoints and pattern resolutions; KB website and evidence
  pack render the new providers from bundled data with no code change.
- Issue #39's actionable sections drop from 2 providers + 9 families + 2 stale KBs to zero.

## Non-goals

- No data-practice curation: `prism` and `sail` join the gap queue honestly.
- No SDK keys for the new providers until official package coordinates are verified.
- No text changes to the arrangement summaries: the review confirmed them accurate, and the
  watch items (TC260's pending Macao GBA practice guide, Australia's tranche-2 exposure
  draft) are recorded in the design for the next review cycle, not speculatively encoded.
