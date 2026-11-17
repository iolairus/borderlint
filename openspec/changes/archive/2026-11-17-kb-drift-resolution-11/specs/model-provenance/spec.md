## ADDED Requirements

### Requirement: Replicate hosting namespace is provenance-transparent

The provenance matcher SHALL treat the leading `replicate/` namespace as a hosting qualifier and
strip it before applying anchored model-family patterns. Owner and publisher namespaces following
it SHALL remain load-bearing; no Replicate provider-level provenance default SHALL be added.

#### Scenario: SDK and LiteLLM-qualified forms agree
- **GIVEN** an owner-qualified pattern resolves `recraft-ai/recraft-v3`
- **WHEN** references `recraft-ai/recraft-v3` and `replicate/recraft-ai/recraft-v3` are matched
- **THEN** both resolve to the same Recraft organisation and `us` bloc

#### Scenario: Hosting namespace does not make tools into models
- **WHEN** an exact Replicate tool or undisclosed-lineage id is listed in the wave-11 residue set
- **THEN** it remains without a provenance match and the residue entry applies only to that exact id

### Requirement: Wave-11 model families resolve through anchored patterns

The bundled provenance map SHALL resolve the source-backed wave-11 families using the exact
patterns and organisations specified in design: OpenAI CSAM/us; TypeSafe Jev/us; Alibaba Wan/cn;
Bria/il; ElevenLabs/us; HeyGen Avatar/us; Ideogram/ca; Inworld/us; Kuaishou Kling/cn; Lightricks
LTX/il; Luma Photon/us; Real-ESRGAN/cn; Isaac/cn by Qwen inheritance; PlayAI/us; Pruna's disclosed
FLUX/eu, HiDream/cn, Wan/cn, and LTX/il derivatives; QuiverAI/ca; Recraft/us; Resemble AI/us;
Sync Labs/us; and Nace's pinned open Max v1/cn. Every pattern SHALL be owner-qualified except the
distinctive bare stems explicitly approved in design D3. Fine-tunes and optimized deployments
SHALL name the base and post-trainer/optimizer in their organisation labels.

#### Scenario: Named model variants share their family provenance
- **WHEN** references include `replicate/ideogram-ai/ideogram-v3-turbo`,
  `replicate/wan-video/wan-2.7-videoedit`, `replicate/lightricks/ltx-2.3-pro`,
  `replicate/recraft-ai/recraft-v4.1-utility-pro`, and `replicate/resemble-ai/chatterbox-turbo`
- **THEN** they resolve respectively to ca/Ideogram AI, cn/Alibaba Wan, il/Lightricks, us/Recraft,
  and us/Resemble AI

#### Scenario: Derivatives retain base-weight provenance
- **WHEN** references include `replicate/prunaai/flux-fast`,
  `replicate/prunaai/hidream-l1-fast`, and `replicate/perceptron-ai-inc/isaac-0.1`
- **THEN** they resolve to eu with Black Forest Labs and Pruna identified, cn with HiDream and
  Pruna identified, and cn with Alibaba Qwen plus Perceptron/Google components identified

#### Scenario: Full runtime ids resolve beyond drift suffixes
- **WHEN** references `vercel_ai_gateway/typesafe-ai/jev` and
  `openrouter/perceptron/isaac-0.1` are matched directly
- **THEN** the first resolves to us/TypeSafe AI and the second to cn with Alibaba Qwen plus
  Perceptron/Google components identified

#### Scenario: Isaac overrides only its OpenRouter Perceptron family
- **WHEN** references `openrouter/perceptron/isaac-0.1` and
  `openrouter/perceptron/perceptron-mk1` are matched directly
- **THEN** Isaac resolves to cn while the other Perceptron model retains us/Perceptron AI

#### Scenario: Generic near-misses remain unresolved
- **WHEN** references such as `replicate/luma/photography`, `replicate/quiverai/arrow-2`,
  `replicate/lightricks/ltx-9`, `wan-9`, `react-2`, or `recraft-v4` without an approved namespace
  are evaluated
- **THEN** none gains provenance through an overbroad wave-11 pattern

### Requirement: Wave-11 tools and undisclosed lineage remain exact residue

The 57 full-key ids enumerated in design's exact-residue section SHALL be acknowledged individually
as search/tool/pipeline operations or models with undisclosed lineage: 55 ids from the original
145-id fixture (including `webiq/search`), plus the two non-fixture Nace routes
`nace/drex-latest` and `nace/drex-v1.5`. No whole-provider, whole-publisher, or generic family
residue prefix SHALL be added, and future variants SHALL remain reviewable.

#### Scenario: Composite applications do not inherit component provenance
- **WHEN** the drift check evaluates `replicate/flux-kontext-apps/cartoonify`,
  `replicate/elevenlabs/dubbing`, and `replicate/veed/fabric-1.0`
- **THEN** each is acknowledged by its exact residue entry and no provenance bloc is inferred from
  a component, developer domicile, or product name

#### Scenario: Future variants are not swallowed
- **WHEN** a new id differs from an exact residue key, for example
  `replicate/veed/fabric-2.0`
- **THEN** the exact residue entry does not acknowledge it

## MODIFIED Requirements

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
- The active Drex v2.0 forms `drex-v2.0`, `nace/drex-v2.0`, and `nace-ai/drex-v2.0`, and
  the immutable HF checkpoints `nace-ai/drex-v1.5` and `nace-ai/drex-max-v1` → bloc `cn`,
  organisation naming base and tuner (`Alibaba (Nace Drex post-train)`): v2.0 uses a
  Qwen3.6-35B-A3B backbone, HF v1.5 post-trains Xiaomi MiMo-V2.6-Distill-Qwen-9B, and Max
  v1 declares Qwen3.8-27B as its base, so the fine-tunes-inherit-base rule assigns Alibaba's
  bloc. The bare and `nace/` API forms `drex-v1.5`, `nace/drex-v1.5`, `drex-latest`,
  `nace/drex-latest`, `drex-max`, `nace/drex-max`, `drex-max-v1.1`, and
  `nace/drex-max-v1.1` SHALL NOT inherit checkpoint lineage and SHALL keep provenance
  `unknown`. `nace/drex-v1.0` SHALL remain unresolved (lineage undisclosed in primary sources)
  and retain its existing accept-unknown residue. None of the wave-7 providers SHALL carry a
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

#### Scenario: Active Drex and immutable HF checkpoints inherit the Qwen bloc
- **WHEN** model references `drex-v2.0`, `nace/drex-v2.0`, `nace-ai/drex-v2.0`,
  `nace-ai/drex-v1.5`, and `nace-ai/drex-max-v1` are detected
- **THEN** each resolves to bloc `cn` with the organisation label naming base and tuner
  (`Alibaba (Nace Drex post-train)`), per the fine-tunes-inherit-base rule

#### Scenario: Drex API v1.5, latest, Max, and v1.1 stay honestly unknown
- **WHEN** model references `drex-v1.5`, `nace/drex-v1.5`, `drex-latest`,
  `nace/drex-latest`, `drex-max`, `nace/drex-max`, `drex-max-v1.1`, and
  `nace/drex-max-v1.1` are detected
- **THEN** none inherits the cn checkpoint provenance and each keeps provenance `unknown`

#### Scenario: Drex v1.0 stays honestly unknown
- **WHEN** a model reference `nace/drex-v1.0` is detected
- **THEN** it matches no pattern (its base lineage is undisclosed in primary sources) and
  keeps provenance `unknown`

#### Scenario: Wave-7 providers carry no tier-2 defaults
- **WHEN** unbound flows on providers `coralbricks`, `inferenceapis`, `nace`, and
  `openinfer` carry no model reference
- **THEN** each keeps provenance `unknown` (multi-vendor hosts; Nace's lineage is mixed
  with undisclosed API versions)
