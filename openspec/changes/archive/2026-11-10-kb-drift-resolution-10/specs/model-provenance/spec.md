# model-provenance Delta

## ADDED Requirements

### Requirement: Wave-10 reseller families, dash-normalized anchors, and new labs resolve provenance
The bundled provenance map SHALL resolve the following drift-run families, all patterns
matched case-insensitively, anchored, longest-first per the existing matching rules:

- `empiriolabs/perplexity-` → bloc `us`, organisation Perplexity: the reseller's
  `perplexity-*` ids are genuine Perplexity models (author disclosed on the vendor's
  own model pages). The pattern is qualified to the reseller namespace — NO bare
  `perplexity-` stem SHALL be added.
- `seed-2-` → bloc `cn`, organisation ByteDance, and `step-3-` → bloc `cn`,
  organisation StepFun: dash-normalized forms of families whose dot-anchored patterns
  (`seed-2.`, `step-3.`) already exist. Both SHALL remain version-anchored; no bare
  `seed` or `step` stem.
- `stepaudio-` → bloc `cn`, organisation StepFun; `tongyi-embedding-vision` → bloc
  `cn`, organisation Alibaba; `skylark-embedding` → bloc `cn`, organisation ByteDance.
  NO bare `skylark` stem SHALL exist (common English word).
- `fugu-` → bloc `jp`, organisation Sakana AI: Sakana's Fugu orchestration models;
  the existing `sakana/` pattern cannot cover the reseller's unqualified `fugu-*` ids.
- `aplomb-1` → bloc `cn`, organisation naming base and tuner (`Alibaba (EmpirioLabs
  post-train)`): EmpirioLabs' first-party model is a documented fine-tune of
  Qwen3.5-4B, so the fine-tunes-inherit-base rule applies.
- `jina-reranker-m0` and `jina-reranker-v3.5` → bloc `cn`, organisation naming base
  and tuner (`Alibaba (Jina AI post-train)`): both rerankers document Qwen bases on
  their HF cards (Qwen2-VL-2B-Instruct and Qwen3-0.6B). The patterns are exact
  version-anchored stems so the jina-bert-based v1/v2/v3 line (own lineage, covered by
  the `jina_ai` tier-2 `eu` default, which is unchanged) is NOT swept into the cn
  claim.
- `grok4.` → bloc `us`, organisation xAI: the undashed Grok 4.6 alias (official id is
  dashed `grok-4.6`); dot-anchored, sibling of the existing `grok-` pattern.
- `ripple-65b` → bloc `us`, organisation Ricursive Intelligence (from-scratch 64.8B,
  Apache-2.0); `rnj-1` → bloc `us`, organisation Essential AI (from-scratch 8B,
  Apache-2.0). Both version-anchored — NO bare `ripple` or `rnj` stem.
- `together_ai/elorian-labs/glimpse-1.0` SHALL remain provenance `unknown`, recorded
  as acknowledged residue: Elorian AI post-trained it from an unnamed open-weights
  base, and lineage undisclosed means accept unknown rather than guess a bloc (the
  Drex v1.0 precedent).
- The providers `empiriolabs`, `hostinger_router`, and `wally` SHALL carry NO tier-2
  provenance default: all three serve multi-vendor catalogs.

#### Scenario: Reseller Perplexity ids resolve qualified
- **WHEN** model references `empiriolabs/perplexity-sonar-pro` and
  `empiriolabs/perplexity-advanced-deep-research` are detected
- **THEN** both resolve to bloc `us` with organisation Perplexity via the qualified
  `empiriolabs/perplexity-` pattern, and no bare `perplexity-` stem exists

#### Scenario: Dash-normalized Seed and Step forms resolve beside the dot anchors
- **WHEN** model references `seed-2-0-pro`, `seed-2-1-turbo`, `step-3-5-flash`,
  `step-3-5-flash-2603`, and `step-3-7-flash` are detected
- **THEN** the seed forms resolve to bloc `cn` with organisation ByteDance and the step
  forms to bloc `cn` with organisation StepFun, via the dash anchors — while the
  pre-existing dot-anchored forms (`seed-2.0-pro`, `step-3.5-flash`) resolve exactly as
  before

#### Scenario: StepAudio, Tongyi, and Skylark forms resolve to cn
- **WHEN** model references `stepaudio-2-5-chat`, `tongyi-embedding-vision-flash`, and
  `skylark-embedding-vision` are detected
- **THEN** they resolve to bloc `cn` with organisations StepFun, Alibaba, and ByteDance
  respectively, and no bare `skylark` stem exists

#### Scenario: Fugu resolves to Sakana AI
- **WHEN** model references `fugu-max` and `fugu-ultra-v2-0` are detected
- **THEN** both resolve to bloc `jp` with organisation Sakana AI

#### Scenario: Aplomb-1 inherits the Qwen bloc
- **WHEN** a model reference `aplomb-1` is detected
- **THEN** it resolves to bloc `cn` with the organisation label naming base and tuner
  (`Alibaba (EmpirioLabs post-train)`), per the fine-tunes-inherit-base rule

#### Scenario: Qwen-based Jina rerankers inherit cn; the jina-bert line stays eu
- **WHEN** model references `jina-reranker-m0` and `jina-reranker-v3.5` are detected,
  and separately an unbound flow on provider `jina_ai` carries no model reference
- **THEN** both reranker references resolve to bloc `cn` with the organisation label
  naming base and tuner (`Alibaba (Jina AI post-train)`), and the unbound flow resolves
  to bloc `eu` via the unchanged `jina_ai` tier-2 default

#### Scenario: Undashed grok4.6 resolves via the dot anchor
- **WHEN** model references `gmi/xai/grok4.6` and a bare `grok4.6` are detected
- **THEN** the bare reference resolves to bloc `us` with organisation xAI via the
  `grok4.` anchor, and the qualified form counts as covered via the drift check's
  suffix walk against the same pattern

#### Scenario: Ripple and Rnj-1 resolve to their from-scratch US labs
- **WHEN** model references `gmi/gmicloud/Ripple-65B-Preview`,
  `together_ai/ricursive-ai/Ripple-65B-Preview`, and
  `together_ai/essentialai/rnj-1-instruct` are evaluated by the drift coverage check
- **THEN** all three count as covered via the suffix walk against the `ripple-65b` and
  `rnj-1` patterns, and a bare detected reference `ripple-65b-preview` resolves to bloc
  `us` with organisation Ricursive Intelligence

#### Scenario: Guarded stems stay unknown
- **WHEN** hypothetical references `seed-9`, `step-up-7b`, `skylark-7b`,
  `ripple-effect-3b`, or `perplexity-clone` are detected
- **THEN** none resolves through any new pattern (no bare `seed`, `step`, `skylark`,
  `ripple`, or `perplexity-` stems exist) and each keeps provenance `unknown`

#### Scenario: Glimpse-1.0 stays unknown as acknowledged residue
- **WHEN** the drift coverage check evaluates `together_ai/elorian-labs/glimpse-1.0`
- **THEN** the id keeps provenance `unknown` and the drift report carries it only as
  acknowledged residue with a dated judgment in `scripts/kb_drift_aliases.json`

#### Scenario: Wave-10 providers carry no tier-2 default
- **WHEN** unbound flows on providers `empiriolabs`, `hostinger_router`, or `wally`
  carry no model reference
- **THEN** each keeps provenance `unknown` (no tier-2 default on a multi-vendor
  catalog)
