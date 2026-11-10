# Proposal: kb-drift-resolution-10

## Why

The 2026-11-10 weekly freshness refresh (issue #39) reports three uncovered upstream
providers and thirteen unresolved model families (30 ids). The wave is dominated by a
single new namespace: `empiriolabs`, a US inference reseller whose 23-id catalog is
almost entirely disclosed third-party models (Perplexity, ByteDance Seed/Skylark,
StepFun, Alibaba Tongyi, Sakana Fugu) plus one first-party model. Joining it: Hostinger's
AI Router (eu) and Wally by RunAnywhere (us). Until each item is assigned by hand, these
flows classify as `unknown` and the review queue cannot converge.

## What Changes

- Add three bundled provider entries:
  - `empiriolabs` — EmpirioLabs.ai LLC (New Mexico LLC, Seattle; New Mexico governing
    law), a multi-vendor inference reseller: its ToS states it "connects users to
    various AI models from multiple sources", and each catalog page discloses the
    upstream model author. Endpoint `api.empiriolabs.ai`; jurisdiction and sovereignty
    `us`; category `aggregator` (proprietary models proxied, some open weights hosted on
    own GPUs). NO tier-2 default. The note records that the catalog is author-disclosed
    per model and that only `aplomb-1` is first-party.
  - `hostinger_router` — Hostinger AI Router, Hostinger's hosted OpenAI/Anthropic-
    compatible gateway to OpenAI/Anthropic/Google/xAI models, billed in Hostinger AI
    credits. Endpoint `router.hostinger.com`; jurisdiction and sovereignty `eu`
    (contracting entities Hostinger International Ltd/Cyprus, Hostinger Global S.à r.l/
    Luxembourg, Hostinger UAB/Lithuania; governing law Luxembourg); category
    `aggregator`. NO tier-2 default. The note records the group HQ (Kaunas) and that
    upstream inference locations are not disclosed.
  - `wally` — Wally, hosted inference by RunAnywhere, Inc. (Delaware C-corp, Redwood
    City CA; YC W26), serving a fixed catalog of open-weight models (DeepSeek, GLM) on
    its own hosted infrastructure with zero data retention by default. Endpoint
    `inference.runanywhere.ai`; jurisdiction and sovereignty `us`. NO tier-2 default
    (multi-lineage catalog). The note records that the served weights are cn-origin
    while the operator is us.
- Add provenance patterns for the resolvable families (all anchored; no dangerous bare
  stems):
  - `empiriolabs/perplexity-` → Perplexity, `us`: genuine Perplexity models
    (author-disclosed on the reseller's model pages), qualified so no bare
    `perplexity-` stem is claimed.
  - `seed-2-` → ByteDance, `cn`: the dash-normalized forms of Seed 2.0/2.1 (the
    existing `seed-2.` dot anchor misses `seed-2-0-code` etc.).
  - `step-3-` → StepFun, `cn`: dash-normalized Step 3.5/3.7 Flash (sibling of the
    existing `step-3.` dot anchor).
  - `stepaudio-` → StepFun, `cn`: StepAudio 2.5/3 Chat.
  - `tongyi-embedding-vision` → Alibaba, `cn`: Tongyi multimodal embedding models
    (Model Studio docs; Qwen3-based).
  - `skylark-embedding` → ByteDance, `cn`: Skylark (云雀) multimodal embedding on
    ModelArk/BytePlus. NO bare `skylark` stem (common English word).
  - `fugu-` → Sakana AI, `jp`: Sakana's Fugu orchestration models (the existing
    `sakana/` pattern cannot cover the reseller's unqualified `fugu-*` ids).
  - `aplomb-1` → `Alibaba (EmpirioLabs post-train)`, `cn`: Aplomb-1 is EmpirioLabs'
    first-party model, a documented fine-tune of Qwen3.5-4B (Qwen3-Omni audio encoder)
    — the fine-tunes-inherit-base rule assigns Alibaba's bloc with the org naming base
    and tuner.
  - `jina-reranker-m0` and `jina-reranker-v3.5` → `Alibaba (Jina AI post-train)`,
    `cn`: both rerankers are documented LoRA/post-train derivatives of Qwen bases
    (Qwen2-VL-2B-Instruct and Qwen3-0.6B respectively, per the HF cards) — exact
    version-anchored stems so the earlier jina-bert-based rerankers (own lineage, eu
    via the `jina_ai` default) are NOT swept into the cn claim.
  - `grok4.` → xAI, `us`: the undashed Grok 4.6 alias (xAI's official id is the dashed
    `grok-4.6`); dot-anchored, sibling of `grok-`.
  - `ripple-65b` → Ricursive Intelligence, `us`: from-scratch 64.8B Apache-2.0 model
    (Ricursive Intelligence, Palo Alto), version-anchored — NO bare `ripple` stem.
  - `rnj-1` → Essential AI, `us`: from-scratch 8B Apache-2.0 (Essential AI, San
    Francisco).
- Record one family as acknowledged residue: `together_ai/elorian-labs/glimpse-1.0` —
  Elorian AI (Palo Alto) post-trained Glimpse-1.0 from an UNNAMED open-weights base;
  lineage undisclosed, so accept unknown rather than guess a bloc (the Drex v1.0
  precedent).
- Bump the review dates of the touched knowledge-base files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `jurisdiction-classification`: three new hosted providers resolve with documented
  endpoint hosts and jurisdictions (us, eu, us).
- `model-provenance`: the drift-run families resolve — twelve via anchored patterns
  (including two dash-normalization anchors beside existing dot anchors), one honestly
  accepted as unknown residue.

## Impact

- `borderlint/data/providers.json` (+3 entries), `sovereignty.json` (+3 mappings),
  `provenance.json` (+13 patterns), `scripts/kb_drift_aliases.json` (+1 residue
  reason), tests.
- Issue #39's actionable sections drop from 3 providers + 13 families to zero. The
  data-practice gap queue grows 106 → 109 (three new providers join the standing
  backlog); residue grows by one id.

## Non-goals

- No data-practice curation: the gap queue stays the declared standing backlog.
- No scanner or checker changes: every item resolves via KB data.
- No bare `perplexity-` stem and no claim on Perplexity's own first-party route
  behavior — the pattern is qualified to the `empiriolabs/` reseller namespace.
- No bloc claim for Elorian's Glimpse-1.0 beyond the residue acknowledgment; if the
  base model is ever disclosed, a pattern replaces the residue entry.
- No reclassification of earlier Jina rerankers (v1/v2/v3): they are jina-bert-based
  own-lineage models covered by the existing `jina_ai` eu default; only the two
  Qwen-based ids get cn patterns.
- No tier-2 default for `empiriolabs` despite one first-party model: the catalog is
  overwhelmingly third-party.
