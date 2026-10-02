# Design: kb-drift-resolution-3

## Context

The 2026-09-30 run surfaced a modest wave (2 providers, 9 families) plus the first firing of
the 90-day staleness clock on the two legal-reference KBs. Research resolved every unknown —
and overturned both working hypotheses: litellm's `prism` is Prism Inference (SF, YC), not
PrismML; `sail` is Sail Research (SF, Kleiner/Sequoia-backed agent-infra), not Sea AI Lab.
The maintainer confirmed all blocs and the stale-KB treatment on 2026-10-02.

## Goals / Non-Goals

**Goals:**

- Drain the provider, model-family, and stale-KB sections to zero actionable items.
- Apply the fine-tune base-inheritance rule consistently to Ember-1, the highest-profile
  case yet.
- Complete the legal-reference review with recorded evidence, not a bare date bump.

**Non-Goals:**

- No data-practice curation; no SDK keys until verified; no speculative encoding of pending
  legislation.

## Decisions

### D1: `prism/` and `sail/` are passthroughs; `zai-org/` is the one missing org

Both platforms serve third-party open weights under their route prefix — Prism with bare
basenames (`prism/deepseek-v4-flash`), Sail with Hugging Face org paths
(`sail/zai-org/GLM-5.3`). The route prefix carries no provenance, so both join the
passthrough list (the `aihubmix/` precedent); after the single strip, every catalog id
resolves via existing org or family patterns except Zhipu's HF org `zai-org/`, which gains
a pattern. Sail's `nvidia/Gemma-4-31B-IT-NVFP4` resolves via `nvidia/` — NVIDIA's FP4
build of a Google base, both `us`, so the org-level match is bloc-correct.

### D2: Ember-1 inherits Kimi K3's bloc

Fireworks Research's Ember-1 is a post-train of Moonshot AI's open-weight Kimi K3
(multi-source confirmed; ~40% shorter reasoning traces, weights unreleased). The provenance
map's standing rule — fine-tunes and distillations inherit the base family's bloc — applies
regardless of the tuner's nationality, exactly as it did for Anthracite's magnum
(Qwen2.5 → `cn`). Ember therefore resolves `cn` with org label
"Moonshot AI (Fireworks Ember post-train)", keeping the evidence self-explanatory. The
pattern set is the most specific covering the member (`ember-`, `openrouter/fireworks/ember`)
— deliberately NOT an `openrouter/fireworks/` org pattern, since future Fireworks releases
may carry different bases and should surface as fresh drift.

### D3: Stem discipline (standing rule)

Generic stems stay qualified: `deep-research` not `deep`; `mai-cyber`/`mai-image` extend the
existing specific MAI set rather than widening to `mai-`; `virtual-try-on` not `virtual`;
`c4ai-` is inherently qualified. Hub-qualified route literals follow the established
precedent for the observed `azure_ai`/`gemini`/`vertex_ai`/`together_ai` forms.

### D4: Fireworks' router endpoints are structural residue

`fireworks_ai/accounts/fireworks/routers/auto`, `…/auto-instant`, and `…/firerouter` are
routing products, not models — the `azure_ai/model-router` mould. One prefix residue entry
(`fireworks_ai/accounts/fireworks/routers/`) acknowledges all current and future router ids
with the reason recorded.

### D5: The stale-KB review bumps dates on recorded evidence, no summary edits

The 90-day review (evidence gathered 2026-10-02) verified all ten arrangement summaries
against the Jun–Oct 2026 window. Three in-window legal developments were found, none
altering a summarized transfer mechanic: the CAC's 2026-07-24 cross-border Q&A (administration
of the unchanged three statutory routes), Japan's APPI amendment (promulgated 2026-07-17,
entry into force by cabinet order no later than ~Jul 2028 — Art. 28 mechanics unchanged
today), and Korea's PIPA amendment (in force 2026-09-11 — enforcement-side; Art. 28-8
transfer bases structurally unchanged). The stored GBA URL was verified live at its current
path. Watch items for the next review cycle: TC260's draft Macao GBA practice guide (public
comment closed Dec 2025, finalization pending) and Australia's tranche-2 exposure draft
(Aug–Sep 2026, nothing in force). Per the maintainer's call, summaries stay as written and
both files' `updated` dates are bumped; this design section is the review record.

### D6: Follow-on drift folded in with confirmation, not silently

Two items appeared upstream between the 2026-09-30 enumeration and implementation:
`pareto-26.10-preview` (a versioned release of the already-judged composite product — the
residue gains an `openrouter/unbiased/pareto-` prefix carrying the same judgment) and
`apodex` (Apodex, Redwood City, CA — own verification-centric reasoning models, OpenRouter
listing 2026-10-01; patterns `apodex/`/`apodex-` → `us`, maintainer-confirmed 2026-10-02).
This follows the PR #96 follow-on precedent: late-arriving drift is folded in only with a
recorded confirmation, never auto-assigned. Apodex's base lineage is not publicly named
(moderate confidence it is own work); a future lineage disclosure is ordinary drift-review
material.

## Risks / Trade-offs

- [Ember's `cn` provenance may surprise users who see only the Fireworks brand] → the org
  label names both lineage and tuner; the KB-site provenance note already explains the
  inheritance rule.
- [`prism/`/`sail/` passthroughs hide future platform-only ids] → they do not: an unmatched
  basename after the strip is still uncovered and surfaces as drift.
- [Korea PIPA "structurally unchanged" rests on secondary commentary (moderate confidence)]
  → the summary describes the Art. 28-8 bases generically and remains correct even if
  subsidiary notice details shifted; next cycle re-checks with primary sources.

## Open Questions

- (none — all blocs and the stale-KB treatment confirmed 2026-10-02)
