# model-provenance Delta

## ADDED Requirements

### Requirement: Semantic-ranker, SAM, Alibaba video, Beam, and Drex families resolve provenance
The bundled provenance map SHALL resolve the following drift-run families, all patterns
matched case-insensitively, anchored, longest-first per the existing matching rules:

- `semantic-ranker` and the qualified `vertex_ai/semantic-ranker` → bloc `us`,
  organisation Google (the Ranking API models on Vertex AI Agent Builder).
- The qualified `meta/sam` form → bloc `us`, organisation Meta (the Segment Anything
  line). NO bare `sam` stem SHALL exist — it prefix-matches unrelated identifiers such
  as `sambanova`.
- `happyhorse` → bloc `cn`, organisation Alibaba (closed, API-only video family; base
  lineage undisclosed, so no tuner/base label). `wan2.` and `wan3.` → bloc `cn`,
  organisation naming the Wan-AI publishing line. NO bare `wan` stem SHALL exist — it
  prefix-matches every `wandb/<org>/<model>` identifier.
- `beam`, the HF-org form `reflection/beam`, and the three observed host-qualified forms
  `baseten/reflection/beam`, `together_ai/reflection/beam`, `nebius/reflection/beam` →
  bloc `us`, organisation Reflection AI (Beam 1.0, pretrained from scratch, Apache-2.0).
- The Drex versioned forms `drex-v1.5`, `drex-v2.0`, and `drex-latest` — bare and
  qualified under `nace/`, plus the versioned forms under the open-weights HF org
  `nace-ai/` (`nace-ai/drex-v1.5`, `nace-ai/drex-v2.0`; HF repos are versioned, so no
  `nace-ai/drex-latest`) — → bloc `cn`,
  organisation naming base and tuner (`Alibaba (Nace Drex post-train)`): v1.5 post-trains
  Xiaomi MiMo-V2.6-Distill-Qwen-9B and v2.0 (the current `-latest` target) uses a
  Qwen3.6-35B-A3B backbone, so the fine-tunes-inherit-base rule assigns Alibaba's bloc.
  `nace/drex-v1.0` SHALL remain unresolved (lineage undisclosed in primary sources) and
  be recorded as accept-unknown residue. None of the wave-7 providers SHALL carry a
  tier-2 provenance default.

#### Scenario: Google rerankers resolve on both forms
- **WHEN** model references `vertex_ai/semantic-ranker-default` and
  `semantic-ranker-fast-004` are detected
- **THEN** both resolve to bloc `us` with organisation Google

#### Scenario: SAM resolves only under the Meta namespace
- **WHEN** a model reference `meta/sam-3.1` is detected, and separately a hypothetical
  `sam-3.1` or `sambanova-custom` reference is detected
- **THEN** the first resolves to bloc `us` with organisation Meta, while the others match
  no new pattern (no bare `sam` stem exists) and keep their prior resolution

#### Scenario: Alibaba video families resolve; wandb ids are untouched
- **WHEN** model references `happyhorse-1.0-i2v`, `wan2.7-i2v`, and `wan3.0-video` are
  detected, and separately a `wandb/some-org/some-model` reference is detected
- **THEN** the first three resolve to bloc `cn` with the Alibaba organisation labels,
  while the `wandb` reference matches no new pattern (no bare `wan` stem exists)

#### Scenario: Beam resolves across its distribution forms
- **WHEN** model references `beam-1.0`, `reflection/Beam-1.0-501B-A23B`,
  `baseten/reflection/Beam-1.0`, `together_ai/reflection/Beam-1.0-501B-A23B`, and
  `nebius/reflection/beam` are detected
- **THEN** each resolves to bloc `us` with organisation Reflection AI

#### Scenario: Drex inherits the Qwen bloc version by version
- **WHEN** model references `nace/drex-v1.5`, `drex-v2.0`, `nace-ai/drex-v2.0`, and
  `drex-latest` are detected
- **THEN** each resolves to bloc `cn` with the organisation label naming base and tuner
  (`Alibaba (Nace Drex post-train)`), per the fine-tunes-inherit-base rule

#### Scenario: Drex v1.0 stays honestly unknown
- **WHEN** a model reference `nace/drex-v1.0` is detected
- **THEN** it matches no pattern (its base lineage is undisclosed in primary sources) and
  keeps provenance `unknown`

#### Scenario: Wave-7 providers carry no tier-2 defaults
- **WHEN** unbound flows on providers `coralbricks`, `inferenceapis`, `nace`, and
  `openinfer` carry no model reference
- **THEN** each keeps provenance `unknown` (multi-vendor hosts; Nace's lineage is mixed
  with one undisclosed version)
