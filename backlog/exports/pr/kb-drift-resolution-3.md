# fix(kb): resolve Sep-30 drift — Prism, Sail, Ember inheritance, MAI lines; 90-day legal review

## Summary

The 2026-09-30 freshness run reported two uncovered providers, nine unresolved model families, and — for the first time — two knowledge bases past the 90-day review interval. This change drains every section to zero: two new provider entries (both SF open-weight hosts), two route passthroughs with the one missing org pattern, provenance for the remaining families including the highest-profile base-inheritance call yet (Fireworks' Ember-1 → `cn` via its Kimi K3 base), two residue judgments, and a completed, evidence-recorded legal review of `arrangements.json` and `regimes.json`.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/kb-drift-resolution-3/` |
| Spec deltas | MODIFIED `jurisdiction-classification` — Bundled east-west provider knowledge base (Prism/Sail scenario); ADDED `model-provenance` — MAI, Ember, Aya Expanse, and companion model families resolve provenance |

## Changes

- **Providers** — `prism` (Prism Inference, YC-backed, `api.prisminference.com`) and `sail` (Sail Research, Kleiner/Sequoia-backed, `api.sailresearch.com`), both San Francisco, jurisdiction and sovereignty `us`. Research overturned both working hypotheses: litellm's `prism` is not PrismML, and `sail` is not Sea AI Lab.
- **Passthroughs** — `prism/` and `sail/` route prefixes carry no provenance; both catalogs resolve via existing publisher org patterns, verified live against 20 real ids. The one org the map lacked, `zai-org/` (Zhipu's HF org), gains a pattern.
- **Ember-1 → `cn`** — Fireworks Research's Ember-1 is a post-train of Moonshot's Kimi K3 (multi-source confirmed). The standing fine-tunes-inherit-base-bloc rule applies exactly as it did for Anthracite's magnum: bloc `cn`, org label "Moonshot AI (Fireworks Ember post-train)". Deliberately no broad `openrouter/fireworks/` pattern, so future Fireworks releases on different bases surface as fresh drift.
- **Remaining families** — Microsoft AI `mai-cyber`/`mai-image`, OpenAI `fw-gpt-oss` (FW-on-Foundry precedent), Google `deep-research` + `virtual-try-on`, Together AI's `together/` org → `us`; Cohere `c4ai-` (Aya Expanse) → `ca`. Follow-on drift folded in with recorded confirmation per the PR #96 precedent (design D6): `apodex` → Apodex (Redwood City) `us`, and the Pareto composite-product residue extended to versioned releases.
- **Residue** — `fireworks_ai/accounts/fireworks/routers/` prefix (routing products, not models).
- **90-day legal review (design D5)** — all ten transfer-arrangement summaries verified current for the Jun–Oct 2026 window. Three in-window developments documented, none altering a summarized transfer mechanic: CAC's 2026-07-24 cross-border Q&A, Japan's APPI amendment (promulgated 2026-07-17, in force ~2028), Korea's PIPA amendment (in force 2026-09-11, enforcement-side). Watch items queued for next cycle: TC260's pending Macao GBA practice guide, Australia's tranche-2 exposure draft. `arrangements.json` and `regimes.json` dates bumped; summaries unchanged.

## Verification

- [x] `openspec validate kb-drift-resolution-3 --strict` passes
- [x] All tasks in tasks.md checked
- [x] Tests covering each acceptance scenario (200 passed; `scripts/kb_drift.py` reports 0 actionable providers, 0 model families, 0 stale KBs)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
