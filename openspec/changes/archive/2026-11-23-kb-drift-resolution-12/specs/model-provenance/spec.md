## ADDED Requirements

### Requirement: Bedrock Geo CA qualifier is provenance-transparent

The provenance matcher SHALL treat the bounded leading `ca.` Bedrock inference-profile qualifier
like the existing geographic qualifiers and match the underlying model family. It SHALL NOT infer
Canadian provenance or residency from that qualifier.

#### Scenario: Geo CA Amazon and Anthropic ids resolve to their developers
- **WHEN** references `ca.amazon.nova-lite-v1:0`, `ca.anthropic.claude-haiku-5-5`, and
  `ca.anthropic.claude-sonnet-5-5` are matched
- **THEN** they resolve respectively to Amazon/us, Anthropic/us, and Anthropic/us

#### Scenario: Incomplete geographic ids remain unresolved
- **WHEN** references `ca`, `ca-central-1`, or `ca.unknown.model` are matched
- **THEN** none gains provenance from the `ca.` qualifier

### Requirement: Wave-12 source-backed model families resolve through anchored patterns

The bundled provenance map SHALL resolve the 41 directly attributable wave-12 ids using the exact
anchors, organisations, and blocs enumerated in design D2. These comprise Gnani Prisma/in; Gradium
TTS/eu; Vispark Vision/in; Jina v5 text/omni small/cn and nano/eu with their named base and
component organisations; Cohere Tiny Aya and North/ca; Respan Span/us; Baseten Bison and
Groundhog/us by Gemma inheritance; Ideogram/ca; Juggernaut Flux/eu by FLUX inheritance;
Sarvam-105B/in; Cartesia Sonic/us; Liquid d1/us; Adept Fuyu/us; Google Genie/us; Kev/cn and Tev1/cn
by Qwen inheritance; Kokoro/us by StyleTTS2 inheritance; and Zyphra Zamba2/us. Patterns SHALL use
the approved owner/version qualification and SHALL NOT introduce broad generic stems or new
multi-model provider defaults. Fine-tune organisation labels SHALL name both base and post-trainer.

#### Scenario: Mixed Jina backbones retain distinct provenance
- **WHEN** the four Jina v5 text/omni small/nano base ids and task-suffixed variants are matched
- **THEN** small variants resolve to cn/Alibaba with Jina post-training and nano variants to
  eu/EuroBERT with Jina post-training, with Qwen auxiliary encoders named where applicable

#### Scenario: Derivatives inherit disclosed bases
- **WHEN** references `baseten/decision-models/baseten-bison-latest`,
  `rundiffusion/juggernaut-pro-flux`, `openrouter/jaredpalmer/kev-4b`,
  `together_ai/hexgrad/kokoro-82m`, and `openrouter/togethercomputer/tev1-4b-experimental`
  are matched
- **THEN** they resolve respectively to us/Google, eu/Black Forest Labs, cn/Alibaba,
  us/Columbia University, and cn/Alibaba, with the post-trainer identified in each organisation

#### Scenario: Full provider and gateway keys resolve at runtime
- **WHEN** the fully qualified Together, OpenRouter, NIM, Cohere, and Gradium forms enumerated in
  design D2 are matched directly rather than through drift suffixes
- **THEN** each resolves to the same provenance as its canonical owner/model form

#### Scenario: Generic near-misses and future versions remain reviewable
- **WHEN** near-misses such as bare `prisma`, `default`, `sonic`, `d1`, `genie-5`, `north-star-1.0`,
  `jina-embeddings-v6-text-small`, `gradium-tts-202701`, or `vispark/visionary` are matched
- **THEN** none gains provenance through a wave-12 pattern

### Requirement: Pruna P-Image-Ideogram remains exact unknown-lineage residue

The full key `together_ai/prunaai/p-image-ideogram` SHALL be acknowledged individually because its
base checkpoint and fine-tune relationship are undisclosed. No Pruna or Ideogram provenance SHALL
be inferred from collaboration, namespace, or prompt-schema compatibility, and no prefix residue
SHALL hide future variants.

#### Scenario: Current id is acknowledged without assigning a bloc
- **WHEN** the drift check evaluates `together_ai/prunaai/p-image-ideogram`
- **THEN** the exact residue reason applies and no provenance match is invented

#### Scenario: Future variant remains actionable
- **WHEN** the drift check evaluates `together_ai/prunaai/p-image-ideogram-v2`
- **THEN** the exact residue entry does not acknowledge it

## MODIFIED Requirements

### Requirement: MAI, Ember, Aya Expanse, and companion model families resolve provenance
The bundled provenance map SHALL resolve the model families surfaced by the 2026-09-30
freshness run to their developer organisations' blocs, keeping the full literal as evidence:
Microsoft AI mai-cyber and mai-image, OpenAI fw-gpt-oss (Fireworks-on-Foundry
redistribution), and Google deep-research and virtual-try-on (bloc `us`); Cohere c4ai
(bloc `ca`); Zhipu's zai-org Hugging Face org and Fireworks Research's ember — a post-train
of Moonshot AI's Kimi K3 that inherits the base family's bloc (bloc `cn`); and Apodex's
apodex family, folded in as follow-on drift (bloc `us`). Together AI's Tev1-4B-experimental
SHALL resolve to bloc `cn`, organisation naming Alibaba's Qwen3.5-4B base and Together AI's
supervised fine-tune, through only the exact owner/version forms enumerated in design D2.
The former broad `together/` and `together_ai/together/` US patterns SHALL be removed rather
than left to misclassify present or future Qwen-derived models. The `prism/` and `sail/`
host route prefixes SHALL pass through so the platforms' third-party catalogs resolve via
the underlying publisher's patterns. Pattern stems MUST be specific enough that identifiers
outside these families do not resolve through them.

#### Scenario: Host-platform catalogs resolve through the passthrough
- **WHEN** model references `prism/deepseek-v4-flash` and `sail/zai-org/GLM-5.3` are detected
- **THEN** both resolve to bloc `cn` with developer organisations DeepSeek and Zhipu AI respectively

#### Scenario: Ember inherits the Kimi base bloc
- **WHEN** a model reference `openrouter/fireworks/ember-1` is detected
- **THEN** it resolves to bloc `cn` with an organisation label naming both Moonshot AI and the
  Fireworks post-train

#### Scenario: New MAI lines and FW redistribution resolve
- **WHEN** model references `azure_ai/MAI-Cyber-1-Flash`, `azure_ai/MAI-Image-2.6`, and
  `azure_ai/FW-GPT-OSS-120B` are detected
- **THEN** the first two resolve to bloc `us` with organisation Microsoft AI and the third to
  bloc `us` with organisation OpenAI

#### Scenario: Cohere For AI, Google, and Apodex families resolve
- **WHEN** model references `c4ai-aya-expanse-32b`,
  `gemini/deep-research-max-preview-04-2026`, `vertex_ai/virtual-try-on-001`, and
  `openrouter/apodex/apodex-1.1-mini:free` are detected
- **THEN** the first resolves to bloc `ca` and the other three to bloc `us`

#### Scenario: Tev1 inherits Qwen without a broad Together default
- **WHEN** references `tev1-4b-experimental`, `together/tev1-4b-experimental`,
  `together_ai/together/tev1-4b-experimental`, `togethercomputer/tev1-4b-experimental`, and
  `openrouter/togethercomputer/tev1-4b-experimental` are detected, followed by an unrelated
  `together/unknown-future-model`
- **THEN** every Tev1 form resolves to cn with Alibaba and Together AI named, while the unrelated
  future model does not inherit Together AI/us
