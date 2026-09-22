# model-provenance Delta

## ADDED Requirements

### Requirement: LongCat, Nex, Agnes, Jev, and companion model families resolve provenance
The bundled provenance map SHALL resolve the model families surfaced by the 2026-09-21
freshness run to their developer organisations' blocs, keeping the full literal as evidence:
Nex AGI, Dots Studio (Xiaohongshu), Meituan LongCat, Tencent Hunyuan hy3/hy4, ByteDance's
bytedance-seed publisher org, Anthracite magnum, and AionLabs aion (bloc `cn`); TypeSafe jev, Relace, Inference.net schematron,
Perceptron, Arcee trinity, Writer palmyra, Perplexity sonar, Reka, the azure_ai whisper
form, Sao10K l3-series, and aion-rp (bloc `us`); Black Forest Labs flux and TheDrummer's
cydonia/skyfall/unslopnemo (bloc `eu`); Agnes AI (bloc `sg`). Fine-tuned families SHALL
carry the bloc of their base family's developer. Pattern stems MUST be specific enough that
identifiers outside these families do not resolve through them.

#### Scenario: Aggregator rebadges resolve through the passthrough to the underlying developer
- **WHEN** model references `aihubmix/coding-glm-5.3` and `aihubmix/coding-kimi-k3` are
  detected
- **THEN** both resolve to bloc `cn` with developer organisations Zhipu AI and Moonshot AI
  respectively

#### Scenario: Fine-tuned families inherit the base bloc
- **WHEN** model references `openrouter/anthracite-org/magnum-v4-72b` (Qwen2.5 base) and
  `openrouter/thedrummer/cydonia-24b-v4.1` (Mistral Small base) are detected
- **THEN** the first resolves to bloc `cn` and the second to bloc `eu`

#### Scenario: A publisher's exception family outranks its default
- **WHEN** model references `openrouter/aion-labs/aion-2.0` and
  `openrouter/aion-labs/aion-rp-llama-3.1-8b` are detected
- **THEN** the first resolves to bloc `cn` (DeepSeek derivative) and the second to bloc `us`
  (Llama-3.1 base), the longer prefix winning

#### Scenario: New-bloc and namespace families resolve
- **WHEN** model references `aihubmix/agnes-2.5-flash`, `openrouter/perplexity/sonar`, and
  `azure_ai/whisper` are detected
- **THEN** they resolve to blocs `sg`, `us`, and `us` respectively

#### Scenario: Generic stems do not over-match
- **WHEN** unrelated model references sharing a generic stem prefix (for example a
  hypothetical `l2-classic`, `hy-line-2`, or `coding-copilot-x`) are detected
- **THEN** they do not resolve through the new patterns and keep provenance `unknown`
