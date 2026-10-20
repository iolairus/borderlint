# Proposal: kb-drift-resolution-7

## Why

The 2026-10-19 weekly freshness refresh (issue #39), confirmed by the 2026-10-20 local run,
reports four uncovered upstream providers and six unresolved model families — the largest
wave since wave 4, spanning four new hosting providers, two Alibaba video families, a
Google reranker line, Meta's SAM 3.1, Reflection AI's first open-weight model, and Nace's
Qwen-lineage decision models. Until each item is assigned by hand, these flows classify as
`unknown` and the review queue cannot converge.

## What Changes

- Add four bundled provider entries, all jurisdiction and sovereignty `us`:
  - `coralbricks` — CoralBricks (San Francisco) FP4 inference host for third-party open
    weights; endpoint `inference.coralbricks.ai` (litellm openai-like provider config).
  - `inferenceapis` — Inference APIs, a one-person US gateway/reseller over Together AI
    and DeepInfra; endpoint `api.inferenceapis.com`; category `aggregator`.
  - `nace` — Nace.AI, Inc. (Delaware corp, Palo Alto) decision-model API; endpoints
    `console.nace.ai` (litellm default) and `drex.nace.ai` (vendor-documented alias).
  - `openinfer` — OpenInfer, Inc. (San Mateo, CA) hosted open-weight serving; endpoint
    `api.openinfer.ai`.
- Add provenance patterns for the six families:
  - `us` — `semantic-ranker` + qualified `vertex_ai/semantic-ranker`: Google's Ranking
    API models on Vertex AI Agent Builder (Discovery Engine).
  - `us` — qualified `meta/sam` only: SAM 3.1 is Meta's Segment Anything line
    (facebookresearch/sam3, Meta Superintelligence Labs). NO bare `sam` stem under any
    circumstances — it prefix-matches `sambanova`, `samsung-*`, and worse.
  - `cn` — `happyhorse` (collision-free stem) and anchored `wan2.` / `wan3.` (never a
    bare `wan`, which would swallow every `wandb/<org>/<model>` id): Alibaba's
    closed-weight HappyHorse video family (lineage undisclosed — no Wan derivation is
    documented) and the Tongyi Wanxiang / Wan-AI video line.
  - `us` — Reflection AI's Beam (pretrained from scratch, Apache-2.0, 501B-A23B MoE):
    bare `beam` (collision-free in the current price map), HF-org `reflection/beam`, and
    the three observed host-qualified forms (`baseten/`, `together_ai/`, `nebius/`).
  - `cn` — Nace's Drex decision models, version by version per the
    fine-tunes-inherit-base rule: `drex-v1.5` (post-trained Xiaomi MiMo-V2.6-Distill-Qwen-9B)
    and `drex-v2.0` / current `drex-latest` (Qwen3.6-35B-A3B backbone) inherit Alibaba's
    bloc, org label naming base and tuner; bare stems plus qualified `nace/` forms and the
    open-weights HF org `nace-ai/` forms.
- Record `nace/drex-v1.0` as accept-unknown residue: its base lineage is undisclosed in
  every primary source, so no bloc is assigned — the honest answer.
- No tier-2 defaults for any of the four providers: three are multi-model hosts/gateways,
  and Nace's all-own-models surface is mixed-lineage with one undisclosed version.
- Bump the review dates of the touched knowledge-base files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `jurisdiction-classification`: four new hosted providers resolve with documented
  endpoint hosts, jurisdiction `us`.
- `model-provenance`: the drift-run families resolve to their developers' blocs,
  including the Qwen-inheritance calls on Drex and the collision guards on `sam`/`wan`.

## Impact

- `borderlint/data/providers.json` (+4 entries), `sovereignty.json` (+4 `us` mappings),
  `provenance.json` (+19 patterns), `scripts/kb_drift_aliases.json` (+1 residue entry),
  tests.
- Issue #39's actionable sections drop from 4 providers + 6 families to zero. The
  data-practice gap queue grows 94 → 98 as the four new providers join the standing
  backlog.

## Non-goals

- No data-practice curation: the gap queue stays the declared standing backlog.
- No scanner or checker changes: every item resolves via KB data or an aliases entry.
- No bare `sam`, `wan`, `classify`-style generic stems — collision guards are explicit.
- No qualified `dashscope/` patterns for wan/happyhorse: the `dashscope/qwen-*` precedent
  leaves namespaced DashScope ids to the tier-2 `alibaba_dashscope` default (same bloc);
  bare stems cover both the drift suffix walk and un-namespaced literals.
- No pattern for `drex-max` (vendor-catalog newest, not yet in litellm's price map) and
  none for `semantic-ranker-*-005` (in Google's docs since 2026-09-01 but absent
  upstream): both surface in the drift report the week litellm picks them up, and the
  anchored stems already cover their shapes.
- No modelling of CoralBricks' SCC-based outside-US processing or OpenInfer's
  customer-selected regions: provider jurisdiction only.
