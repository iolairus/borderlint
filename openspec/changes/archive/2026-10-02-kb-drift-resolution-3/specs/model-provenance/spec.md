# model-provenance Delta

## ADDED Requirements

### Requirement: MAI, Ember, Aya Expanse, and companion model families resolve provenance
The bundled provenance map SHALL resolve the model families surfaced by the 2026-09-30
freshness run to their developer organisations' blocs, keeping the full literal as evidence:
Microsoft AI mai-cyber and mai-image, OpenAI fw-gpt-oss (Fireworks-on-Foundry
redistribution), Google deep-research and virtual-try-on, and Together AI's together org
(bloc `us`); Cohere c4ai (bloc `ca`); Zhipu's zai-org Hugging Face org and Fireworks
Research's ember — a post-train of Moonshot AI's Kimi K3 that inherits the base family's
bloc (bloc `cn`); and Apodex's apodex family, folded in as follow-on drift (bloc `us`). The
`prism/` and `sail/` host route prefixes SHALL pass through so the platforms' third-party
catalogs resolve via the underlying publisher's patterns. Pattern
stems MUST be specific enough that identifiers outside these families do not resolve
through them.

#### Scenario: Host-platform catalogs resolve through the passthrough
- **WHEN** model references `prism/deepseek-v4-flash` and `sail/zai-org/GLM-5.3` are
  detected
- **THEN** both resolve to bloc `cn` with developer organisations DeepSeek and Zhipu AI
  respectively

#### Scenario: Ember inherits the Kimi base bloc
- **WHEN** a model reference `openrouter/fireworks/ember-1` is detected
- **THEN** it resolves to bloc `cn` with an organisation label naming both Moonshot AI and
  the Fireworks post-train

#### Scenario: New MAI lines and FW redistribution resolve
- **WHEN** model references `azure_ai/MAI-Cyber-1-Flash`, `azure_ai/MAI-Image-2.6`, and
  `azure_ai/FW-GPT-OSS-120B` are detected
- **THEN** the first two resolve to bloc `us` with organisation Microsoft AI and the third
  to bloc `us` with organisation OpenAI

#### Scenario: Cohere For AI, Google, and Apodex families resolve
- **WHEN** model references `c4ai-aya-expanse-32b`,
  `gemini/deep-research-max-preview-04-2026`, `vertex_ai/virtual-try-on-001`, and
  `openrouter/apodex/apodex-1.1-mini:free` are detected
- **THEN** the first resolves to bloc `ca` and the other three to bloc `us`

#### Scenario: Generic stems do not over-match
- **WHEN** unrelated model references sharing a generic stem prefix (for example a
  hypothetical `deepfake-detector-2`, `virtual-assistant-1`, or `embering-7b`) are detected
- **THEN** they do not resolve through the new patterns and keep provenance `unknown`
