# model-provenance Specification

## Purpose
Model whose weights a flow runs: the bloc of the legal regime under which the model's developer
operates, as a third dimension orthogonal to residency (where the endpoint sits) and sovereignty
(who can compel disclosure from the serving provider). Provenance is resolved statically from
model references and first-party provider defaults; the map is advisory — it surfaces weight
origin and never adjudicates export-control applicability.
## Requirements
### Requirement: Provenance bloc vocabulary
The system SHALL express model provenance using the blocs `us`, `eu`, `cn`, `uk`, `ru`, `in`,
`il`, `ca`, `jp`, `kr`, `sg`, `au`, `ae`, `ch`, and `unknown` — the sovereignty vocabulary without
`local`, because model weights always have a developer. The `unknown` bloc represents a
provenance that cannot be statically determined. The system SHALL NOT emit any provenance value
outside this vocabulary, and SHALL reject a user-supplied provenance mapping that uses a token
outside it.

#### Scenario: Invalid provenance token in a user mapping is rejected
- **WHEN** a user-supplied knowledge base maps a model pattern to the bloc `overseas`
- **THEN** loading fails with an error naming the invalid token and the accepted vocabulary

#### Scenario: A flow with no matched model reference resolves to unknown
- **WHEN** a flow carries no matched model reference and its provider has no first-party default
- **THEN** the flow's provenance is `unknown`

#### Scenario: A new bloc is accepted in a user provenance mapping
- **WHEN** a user-supplied knowledge base maps an in-house model pattern to the bloc `sg`
- **THEN** loading succeeds and flows carrying that model reference resolve to `sg`

#### Scenario: A previously deferred family resolves to its developer's bloc
- **WHEN** a flow carries the model reference `tiiuae/falcon-180B` or `falcon-40b-instruct`
- **THEN** its provenance resolves to `ae`

#### Scenario: An org-anchored family resolves via its hub org
- **WHEN** a flow carries the model reference `aisingapore/gemma-sea-lion-v4-27b-it`
- **THEN** its provenance resolves to `sg`

#### Scenario: The Apertus family resolves to Switzerland
- **WHEN** a flow carries the model reference `swiss-ai/Apertus-70B-Instruct` or `apertus-70b-instruct`
- **THEN** its provenance resolves to `ch`

### Requirement: Bundled model provenance map
The system SHALL bundle a model provenance map that resolves model references to a developer
organisation and its provenance bloc, keyed by anchored model-identifier patterns covering:
managed-platform model identifiers, bare API model names, aggregator-qualified identifiers, and
model-hub repository identifiers. The map SHALL carry a last-reviewed date as an ISO-8601
(`YYYY-MM-DD`) value and an advisory note stating that it surfaces weight origin and never
adjudicates export-control applicability. Longest matching pattern SHALL win.

#### Scenario: A managed-platform model identifier resolves
- **WHEN** a flow carries the model reference `deepseek.r1-v1:0` on a managed platform
- **THEN** its provenance resolves to `cn`

#### Scenario: A bare API model name resolves
- **WHEN** a flow carries the model reference `claude-sonnet-4-6`
- **THEN** its provenance resolves to `us`

#### Scenario: A model-hub repository identifier resolves
- **WHEN** a flow carries the model reference `Qwen/Qwen2.5-72B-Instruct`
- **THEN** its provenance resolves to `cn`

### Requirement: Two-tier provenance resolution
The system SHALL resolve a flow's provenance in two tiers: (1) a model reference bound to the
flow resolves via the provenance map; (2) absent a bound model reference, a provider that serves
only its own models SHALL resolve to that organisation's bloc via a provider-level default in
the provenance map. Providers that serve third-party models SHALL have no provider-level default
and SHALL resolve to `unknown` absent a bound model reference.

#### Scenario: First-party provider without a model reference
- **WHEN** a flow is detected for a provider that serves only its own models and no model reference is bound
- **THEN** its provenance resolves to the provider organisation's bloc

#### Scenario: Multi-model host without a model reference
- **WHEN** a flow is detected for a provider that serves third-party models and no model reference is bound
- **THEN** its provenance resolves to `unknown`

#### Scenario: A bound model reference takes precedence
- **WHEN** a flow on a multi-model host carries a bound model reference that matches the map
- **THEN** the model reference's bloc is used, regardless of the provider

### Requirement: Aggregator-qualified identifiers resolve provenance
The system SHALL resolve a flow's provenance from an aggregator-qualified model identifier whose
organisation prefix matches the provenance map, even when the flow's residency and sovereignty
are `unknown`.

#### Scenario: Aggregator flow with a qualified identifier
- **WHEN** a flow through a multi-provider router carries the model reference `deepseek/deepseek-r1`
- **THEN** its provenance resolves to `cn` while residency and sovereignty remain `unknown`

### Requirement: Local model identifiers resolve provenance
The system SHALL resolve provenance for the identifier forms used by local LLM tooling:
(1) a redistributor-qualified identifier — a quantizer or community-conversion org (GGUF/MLX
hubs) followed by a model name — SHALL resolve by disregarding the redistributor org and
matching the remaining model name against the family prefixes, because the redistributor carries
no provenance; (2) a model-file reference ending in a model-file
extension (`.gguf`, `.onnx`, `.safetensors`) SHALL match by its file basename, ignoring
directory components; (3) bare local-runtime model names (e.g. Ollama tags) SHALL be
covered by the family prefixes; (4) a leading namespace segment that carries no provenance of its
own SHALL likewise be disregarded, namely a **host-like** segment (one containing a dot — a registry
or mirror host) and a curated local-runtime launcher name (`ollama/`, `vllm/`, `lmstudio/`), because
such a segment names where the weights were pulled from, not who developed them. Candidate forms SHALL
be tried most-qualified first, so an identifier that already resolves continues to resolve unchanged.
Once at least one host-like segment has been disregarded the reference is demonstrably an image or
registry path, and the final segment alone SHALL also be tried. An arbitrary leading segment that is
neither host-like nor a curated launcher name SHALL NOT be disregarded. Tool-name prefixes that merely
resemble a model family SHALL NOT match.

Two consequences of that fallback are accepted and recorded in the change's design (Risks, R1/R2) rather
than hidden: an internal reference whose final segment merely *begins* with a family prefix acquires that
family's provenance, and a URL that carries its scheme resolves nothing at all.

#### Scenario: An MLX community identifier resolves by its model name
- **WHEN** a flow carries the model reference `mlx-community/Qwen2.5-7B-Instruct-4bit`
- **THEN** its provenance resolves to `cn`

#### Scenario: A GGUF file path resolves by its basename
- **WHEN** a flow carries the model reference `models/qwen2.5-7b-instruct-q4_k_m.gguf`
- **THEN** its provenance resolves to `cn`

#### Scenario: A bare local-runtime tag resolves
- **WHEN** a flow carries the model reference `llama3.2`
- **THEN** its provenance resolves to `us`

#### Scenario: A tool name resembling a model family is not matched
- **WHEN** a scanned file contains the string literal `llama_index` or `llama-cpp-python`
- **THEN** no model reference is detected

#### Scenario: An ONNX file path resolves by its basename
- **WHEN** a flow carries the model reference `models/clip-vit-b-32.onnx`
- **THEN** its provenance resolves to `us`

#### Scenario: A safetensors path resolves by its basename
- **WHEN** a flow carries the model reference `weights/qwen2.5-vl-3b.safetensors`
- **THEN** its provenance resolves to `cn`

#### Scenario: An unlisted extension gets no basename treatment
- **WHEN** a flow carries the model reference `dir/qwen2.5.zip`
- **THEN** no basename matching occurs and the whole path faces anchored matching, resolving nothing

#### Scenario: A runtime-qualified identifier resolves by its model name
- **WHEN** flows carry the model references `ollama/deepseek-r1`, `vllm/deepseek-r1` and
  `lmstudio/qwen2.5-7b-instruct`
- **THEN** all three resolve to bloc `cn` with developer organisations DeepSeek, DeepSeek and Alibaba
  respectively

#### Scenario: A registry-host-qualified identifier resolves by its model name
- **WHEN** flows carry the model references `mirror.internal/deepseek-r1` and
  `huggingface.co/TheBloke/deepseek-coder-33B-AWQ`
- **THEN** both resolve to bloc `cn` with organisation DeepSeek, the second reaching the family name
  only after the host segment and then the redistributor org are disregarded

#### Scenario: A multi-segment image reference resolves by its final segment
- **WHEN** a flow carries the model reference `docker.io/library/llama3:8b`
- **THEN** its provenance resolves to `us` with organisation Meta

#### Scenario: An unqualified path segment is not disregarded
- **WHEN** a scanned file contains the string literal `src/deepseek/client.py`
- **THEN** no model reference is detected, because `src` is neither host-like nor a curated launcher name

#### Scenario: A near-miss internal image name stays unmatched
- **WHEN** flows carry the model references `docker.io/library/sonarqube`,
  `registry.corp/ml/internal-router` and `gcr.io/my-project/deploy-tool`
- **THEN** none of them resolves to a bloc, pinning the boundary of the final-segment fallback: dropping
  the host must still leave a segment that starts with a known family prefix

#### Scenario: An internal name beginning with a family prefix acquires that provenance (accepted)
- **WHEN** a flow carries the model reference `registry.corp/ml/mistral-serving`
- **THEN** it resolves to `eu` with organisation Mistral AI, and the finding's evidence is the original
  literal rather than the stripped form, so the attribution is auditable (design R1)

#### Scenario: A URL carrying its scheme resolves nothing (documented limit)
- **WHEN** a scanned file contains the string literal `https://huggingface.co/TheBloke/deepseek-coder-33B-AWQ`
- **THEN** no model reference is detected, because `https:` is not host-like so no segment is ever
  disregarded; the scheme-less `huggingface.co/…` form is the one that resolves (design R2)
### Requirement: User provenance overrides
The system SHALL accept provenance overrides from a user-supplied knowledge base; user entries
SHALL take precedence over bundled entries — including over longer bundled prefixes that would
otherwise win the longest-match — and SHALL be validated against the provenance bloc vocabulary.

#### Scenario: User maps an in-house model
- **WHEN** a user mapping assigns the pattern of an in-house model to the organisation's home bloc
- **THEN** flows carrying that model reference resolve to that bloc

#### Scenario: A shorter user pattern beats a longer bundled pattern
- **WHEN** a user mapping assigns `deepseek` to `eu` and the bundled map contains the longer prefix `deepseek-`
- **THEN** the model reference `deepseek-r1` resolves to `eu`

### Requirement: Base-family provenance for derived models
Fine-tuned and distilled model identifiers SHALL inherit the provenance bloc of their base model
family. The system SHALL NOT attempt derivative-weights lineage beyond the base family.

#### Scenario: A fine-tune resolves to its base family's bloc
- **WHEN** a flow carries a model reference for a fine-tune of a `us`-provenance base family
- **THEN** its provenance resolves to `us`

### Requirement: Version-pinned model identifiers resolve provenance
The system SHALL resolve a model identifier carrying a single trailing version suffix — an `@`
followed by a digit-led version token, or the literal meta-version tokens `default` or `latest`
— by matching its base identifier (the part before the `@`) against the provenance map, while
keeping the full literal as evidence. A trailing `@` segment that is neither digit-led nor one
of the two meta-version tokens SHALL NOT be treated as a version suffix, and the literal SHALL
remain unmatched.

#### Scenario: A Vertex version-pinned identifier resolves
- **WHEN** a flow carries the model reference `claude-3-5-haiku@20241022`
- **THEN** its provenance resolves to `us` and the evidence carries the full literal including the suffix

#### Scenario: A Bedrock-style aggregator version-pinned identifier resolves
- **WHEN** a flow carries the model reference `anthropic.claude-haiku-4-5@20251001`
- **THEN** its provenance resolves to `us`

#### Scenario: A meta-version pin resolves
- **WHEN** a flow carries the model reference `mistral-large@latest` or `claude-fable-5@default`
- **THEN** its provenance resolves to the base identifier's bloc (`eu` and `us` respectively)

#### Scenario: An email address is not a model reference
- **WHEN** a scanned file contains the string literal `gemini-team@google.com`
- **THEN** no model reference is detected, because the `@` segment is neither digit-led nor a meta-version token

#### Scenario: The version never changes the bloc
- **WHEN** two flows carry `mistral-large` and `mistral-large@2407`
- **THEN** both resolve to the same provenance bloc

### Requirement: MiMo model identifiers resolve provenance
The bundled provenance map SHALL resolve MiMo model identifiers — bare (`mimo-v2.5-pro`) and
provider-qualified (`xiaomi/mimo-…`, `novita/xiaomimimo/…`) — to the provenance bloc of their
developer organisation, Xiaomi (bloc `cn`), keeping the full literal as evidence.

#### Scenario: Bare MiMo identifier resolves
- **WHEN** a model reference `mimo-v2.5-pro` is detected
- **THEN** it resolves to provenance bloc `cn` with developer organisation Xiaomi

#### Scenario: Provider-qualified MiMo identifier resolves
- **WHEN** model references `xiaomi/mimo-v2.5-pro` and `novita/xiaomimimo/mimo-v2-flash` are detected
- **THEN** both resolve to provenance bloc `cn`

### Requirement: Seed, MAI, Laguna, Mellum, and Macaron model families resolve provenance
The bundled provenance map SHALL resolve model identifiers of the twelve families surfaced by
the 2026-09-07 freshness run — ByteDance Seed, Baidu CoBuddy, and StepFun Step (bloc `cn`);
Microsoft MAI, Google nano-banana, Microsoft Research multilingual-e5, Thinking Machines Lab
Inkling, poolside Laguna, PrismML Ternary-Bonsai, and BigScience mt0 (bloc `us`); JetBrains
Mellum (bloc `eu`); MindAI Macaron (bloc `sg`) — to their developer organisations' blocs,
keeping the full literal as evidence. Pattern stems MUST be specific enough that identifiers
outside these families do not resolve through them.

#### Scenario: Chinese-bloc family resolves
- **WHEN** a model reference `deepinfra/ByteDance/Seed-1.8` is detected
- **THEN** it resolves to provenance bloc `cn` with developer organisation ByteDance

#### Scenario: US-bloc family resolves
- **WHEN** a model reference `deepinfra/thinkingmachines/Inkling` is detected
- **THEN** it resolves to provenance bloc `us` with developer organisation Thinking Machines Lab

#### Scenario: EU and Singapore families resolve
- **WHEN** model references `wandb/JetBrains/Mellum2-12B-A2.5B-Instruct` and
  `novita/mindai/macaron-v1-tall` are detected
- **THEN** the first resolves to provenance bloc `eu` and the second to bloc `sg`

#### Scenario: Generic stems do not over-match
- **WHEN** an unrelated model reference sharing a generic stem prefix (for example a
  hypothetical `seedling-1b` or `stepwise-2`) is detected
- **THEN** it does not resolve through the new patterns and keeps provenance `unknown`

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

### Requirement: Nimble, Laya, Strands Decider, and Clef model families resolve provenance
The bundled provenance map SHALL resolve the model families surfaced by the 2026-10-05
freshness run to their base families' blocs, keeping the full literal as evidence: Bespoke
Nimble (LoRA on Qwen3.5-9B) and Strands Decider (LoRA + pointer head on Qwen3.5-2B,
AWS-published) inherit Alibaba's bloc (bloc `cn`); the three Laya checkpoints inherit their
encoder bases' bloc — ModernBERT-large (Answer.AI/LightOn, assigned via the Answer.AI-led
release) for english and typed-decisions, JHU mmBERT for multilingual — and Cloudflare's
clef line resolves as Cloudflare's own (bloc `us`). Because the name collides with the
existing Nimbleway provider, a bare `nimble` stem SHALL NOT exist: Bespoke's model resolves
only via qualified forms. Pattern stems MUST be specific enough that identifiers outside
these families do not resolve through them.

#### Scenario: Qwen adapters inherit Alibaba's bloc
- **WHEN** model references `bespokelabs/Bespoke-Nimble-9B` and
  `strands-decider-2B-hobson-v19` are detected (the route-prefixed litellm forms are
  covered by the freshness checker's suffix walk)
- **THEN** both resolve to bloc `cn` with organisation labels naming Alibaba and the
  respective tuner (Bespoke, AWS Strands)

#### Scenario: Qualified Nimble route forms resolve without a bare stem
- **WHEN** model references `bespoke/nimble` and `bespoke/nimble-latest` are detected
- **THEN** both resolve to bloc `cn`

#### Scenario: Laya checkpoints inherit encoder-base blocs
- **WHEN** model references `laya/english`, `laya/multilingual`, and
  `laya/typed-decisions` are detected
- **THEN** all three resolve to bloc `us` with organisation labels naming the encoder base
  and the Laya tune

#### Scenario: Clef resolves via the hub-qualified pattern
- **WHEN** model references `cloudflare/@cf/cloudflare/clef-flash` and `cloudflare/clef`
  are detected by the freshness checker's suffix walk
- **THEN** both are covered by the `cloudflare/clef` pattern resolving to bloc `us` with
  organisation Cloudflare

#### Scenario: Generic stems do not over-match
- **WHEN** unrelated model references sharing a stem prefix (for example a hypothetical
  `nimble-search-1` or `clefable-2b`) are detected
- **THEN** `nimble-search-1` does not resolve through any new pattern (no bare `nimble`
  stem exists) and `clefable-2b` does not resolve through the clef pattern; both keep
  provenance `unknown`

### Requirement: Bedrock India-region prefix and azure/whisper form resolve provenance
The bundled provenance map SHALL treat the Bedrock cross-region inference-profile prefix
`in.` (India) as a passthrough org: the prefix carries no provenance, so it is stripped and
the remainder matched against the family patterns, exactly as the existing `us.`, `eu.`,
`apac.`, `au.`, `jp.`, `global.`, and `us-gov.` region prefixes are. The map SHALL also
resolve the qualified `azure/whisper` form — the same OpenAI model already covered as
`azure_ai/whisper`, now carried by litellm under the `azure` provider namespace — to OpenAI
(bloc `us`). A bare `whisper` stem SHALL NOT exist: the name collides with unrelated
identifiers (for example `whispering-pines`), so the model resolves only via qualified
forms.

#### Scenario: India-region inference profile resolves through the passthrough
- **WHEN** a model reference `in.moonshotai.kimi-k3` is detected
- **THEN** the `in.` region prefix is stripped and the remainder resolves through the
  `moonshotai.` pattern to bloc `cn` with organisation Moonshot AI

#### Scenario: azure/whisper resolves like azure_ai/whisper
- **WHEN** a model reference `azure/whisper` is detected
- **THEN** it resolves to bloc `us` with organisation OpenAI

#### Scenario: Generic stems do not over-match
- **WHEN** unrelated model references sharing a stem prefix (for example a hypothetical
  `whispering-pines` or `in.inhouse-7b` with no family pattern for the remainder) are
  detected
- **THEN** `whispering-pines` does not resolve through any new pattern (no bare `whisper`
  stem exists) and `in.inhouse-7b` strips the region prefix but matches no family pattern;
  both keep provenance `unknown`
### Requirement: MAI-Code, ScaleDown, Copilot Chat, and Microsoft Decision families resolve provenance
The bundled provenance map SHALL resolve the following drift-run families, all patterns
matched case-insensitively, anchored, longest-first per the existing matching rules:

- `mai-code` and the qualified `github_copilot/mai-code` → bloc `us`, organisation
  Microsoft AI (the MAI-Code in-house coding-model family, per the official
  `microsoft/MAI-Code` repository), mirroring the existing `mai-*` bare/qualified
  convention.
- `scaledown/` as an org-namespace prefix → bloc `us`, organisation ScaleDown, covering
  every endpoint name behind it (`classify`, `compress`, `decisions`, `extract`,
  `summarize`): ScaleDown serves its own task-specific small language models. NO bare
  `classify`, `compress`, `decisions`, `extract`, or `summarize` stem SHALL exist — each
  is a generic English word that would over-match unrelated identifiers. The map's tier-2
  provider defaults SHALL map `scaledown` → `us` (a first-party-only provider).
- The qualified `microsoft_365_copilot/chat` form → bloc `us`, organisation Microsoft.
  NO bare `chat` stem SHALL exist. The provider SHALL carry NO tier-2 default: Microsoft
  routes Copilot across model vendors, so unbound flows remain `unknown`.
- `microsoft-decision` and the qualified `azure_ai/microsoft-decision` → bloc `cn`,
  organisation naming base and tuner (`Alibaba (Microsoft Decision-1 post-training)`):
  Microsoft-Decision-1 is Microsoft-published but documented by Microsoft as post-trained
  on Qwen3.5-9B, so the fine-tunes-inherit-base rule assigns Alibaba's bloc (the Bespoke
  Nimble LoRA precedent).

#### Scenario: MAI-Code resolves on both surfaces
- **WHEN** model references `github_copilot/mai-code-1.1-flash` and `mai-code-1-flash` are
  detected
- **THEN** the first resolves through the qualified pattern and the second through the
  bare stem, both to bloc `us` with organisation Microsoft AI

#### Scenario: ScaleDown endpoint names resolve only under the namespace
- **WHEN** model references `scaledown/classify`, `scaledown/compress`,
  `scaledown/decisions`, `scaledown/extract`, and `scaledown/summarize` are detected
- **THEN** each resolves to bloc `us` with organisation ScaleDown

#### Scenario: Generic stems do not over-match
- **WHEN** unrelated model references sharing a stem (for example a hypothetical
  `chat-with-pdfs`, `classification-9b`, or `summarize-pro-2`) are detected
- **THEN** none resolves through any new pattern (no bare `chat`, `classify`,
  `summarize`, or sibling stems exist); each keeps provenance `unknown` unless an
  existing pattern independently covers it

#### Scenario: Copilot Chat resolves qualified; unbound Copilot flows stay unknown
- **WHEN** a model reference `microsoft_365_copilot/chat` is detected, and separately an
  unbound flow on provider `microsoft_365_copilot` carries no model reference
- **THEN** the reference resolves to bloc `us` with organisation Microsoft, and the
  unbound flow keeps provenance `unknown` (the provider has no tier-2 default — Copilot
  routes across model vendors)

#### Scenario: Microsoft-Decision-1 inherits the Qwen bloc
- **WHEN** model references `azure_ai/Microsoft-Decision-1` and `Microsoft-Decision-1`
  are detected
- **THEN** both resolve to bloc `cn` with the organisation label naming base and tuner
  (`Alibaba (Microsoft Decision-1 post-training)`), per the fine-tunes-inherit-base rule
  — publisher branding does not override weight lineage

#### Scenario: Unbound ScaleDown flows inherit the first-party default
- **WHEN** an unbound flow on provider `scaledown` carries no model reference
- **THEN** it resolves provenance `us` via the tier-2 provider default (ScaleDown serves
  only its own models)
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
### Requirement: Azure region-namespace o-series, Clairic, Step-5, and Baseten decision models resolve provenance
The bundled provenance map SHALL resolve the following drift-run families, all patterns
matched case-insensitively, anchored, longest-first per the existing matching rules:

- The qualified `azure/eu/o1`, `azure/eu/o3`, `azure/us/o1`, and `azure/us/o3` forms →
  bloc `us`, organisation OpenAI: the Azure namespace has grown region segments, and
  only the bare forms fail to resolve (versioned siblings already match the
  dash-anchored `o1-`/`o3-`/`o4-` patterns via the suffix walk). NO bare `o1` or `o3`
  stem SHALL be added — the dash anchor is what keeps those short stems safe, and the
  region segments SHALL NOT be added to the passthrough orgs (stripping them would
  expose exactly that bare-stem surface).
- The hub-qualified `cloudflare/clairic` form → bloc `us`, organisation Cloudflare (the
  wave-4 `clef` precedent: the `@cf/cloudflare/clairic` form is covered through it via
  the suffix walk). Clairic is Cloudflare's own Workers AI extraction model with no
  disclosed base lineage — own model until lineage says otherwise.
- `step-5` (version-anchored, matching the existing `step-3.` convention) and the
  qualified `opencode_go/step-5` form → bloc `cn`, organisation StepFun (Shanghai
  entity, CAC-filed; Step 5 Preview is open weights under the StepFun Model License).
  NO bare `step` stem SHALL exist.
- The four documented Baseten decision-model forms —
  `baseten/decision-models/baseten-elephant`, `baseten/decision-models/baseten-mammoth`,
  and the HF-org forms `baselabs/elephant`, `baselabs/mammoth` → bloc `cn`, organisation
  naming base and tuner (`Alibaba (Base Labs post-train)`): elephant-1 and mammoth-1 are
  Base Labs full fine-tunes of Qwen3.5-9B and Qwen3.5-27B respectively (stated on the HF
  cards), so the fine-tunes-inherit-base rule assigns Alibaba's bloc. NO bare
  `elephant`/`mammoth` stems and NO `baseten/decision-models/` namespace wildcard SHALL
  exist — a future Baseten decision model on a non-Qwen base must surface in the drift
  report rather than inherit silently.

The `opencode_go` provider SHALL carry NO tier-2 provenance default: it is a
multi-vendor subscription gateway, and its catalog resolves model-by-model through the
existing family patterns.

#### Scenario: Azure region-namespace bare forms resolve qualified
- **WHEN** model references `azure/eu/o1`, `azure/eu/o3`, `azure/us/o1`, and
  `azure/us/o3` are detected
- **THEN** all four resolve to bloc `us` with organisation OpenAI

#### Scenario: Azure region-namespace versioned forms stay covered
- **WHEN** the drift coverage check evaluates the `azure/eu/o*` and `azure/us/o*` id
  sets (e.g. `azure/eu/o1-mini`, `azure/us/o4-mini-2025-04-16`)
- **THEN** every id counts as covered — the bare forms via the new qualified patterns,
  the versioned forms via the suffix walk against the pre-existing dash-anchored
  `o1-`/`o3-`/`o4-` patterns, which are unchanged

#### Scenario: Baseten decision models inherit the Qwen bloc
- **WHEN** model references `baseten/decision-models/baseten-elephant-9b-latest`,
  `baseten/decision-models/baseten-mammoth-27b-latest`, `baselabs/elephant-1`, and
  `baselabs/mammoth-1` are detected
- **THEN** each resolves to bloc `cn` with the organisation label naming base and tuner
  (`Alibaba (Base Labs post-train)`), per the fine-tunes-inherit-base rule, and no bare
  `elephant` or `mammoth` stem exists

#### Scenario: Clairic resolves qualified; the hub form is covered by the suffix walk
- **WHEN** a model reference `cloudflare/clairic` is detected, and the drift coverage
  check evaluates `cloudflare/@cf/cloudflare/clairic`
- **THEN** the reference resolves to bloc `us` with organisation Cloudflare, and the hub
  form counts as covered via the suffix walk against the same pattern (the wave-4 `clef`
  precedent)

#### Scenario: Step-5 resolves bare and qualified
- **WHEN** model references `step-5-preview` and `opencode_go/step-5-preview` are
  detected
- **THEN** both resolve to bloc `cn` with organisation StepFun

#### Scenario: Short stems stay guarded
- **WHEN** hypothetical references `o1-preview-clone`, `step-up-7b`, or `o3unknown` are
  detected
- **THEN** none resolves through any new pattern (no bare `o1`, `o3`, or `step` stems
  exist); `o1-preview-clone` still resolves through the pre-existing dash-anchored
  `o1-` pattern exactly as before, and `step-up-7b` keeps provenance `unknown`

#### Scenario: OpenCode Go catalog is covered model-by-model; unbound flows stay unknown
- **WHEN** the drift coverage check evaluates the `opencode_go` catalog (e.g.
  `opencode_go/kimi-k3`, `opencode_go/beam-free`), and separately an unbound flow on
  provider `opencode_go` carries no model reference
- **THEN** every catalog id except the newly-patterned `step-5-preview` counts as covered
  via the suffix walk against the existing family patterns (Moonshot, Reflection AI, and
  so on), and the unbound flow keeps provenance `unknown` (no tier-2 default on a
  multi-vendor gateway)

### Requirement: Wave-9 provider defaults and anchored patterns resolve the drift families
The bundled provenance map SHALL resolve the following drift-run families, all patterns
matched case-insensitively, anchored, longest-first per the existing matching rules:

- Tier-2 provider default `soniox` → bloc `us`: Soniox is a first-party-only provider
  (its ToS forbids reselling the service and its catalog is exclusively its own speech
  models), which is exactly the provider-default contract. The whole `stt` family —
  the legacy unversioned `stt-rt-preview` form and the versioned `stt-rt-v3…v5` /
  `stt-async-*` ids — resolves through it. NO bare `stt`, `stt-rt`, or `stt-async`
  stem SHALL be added: speech-to-text shorthand is generic vocabulary that no single
  vendor may claim.
- `eu-jeff` → bloc `eu`, organisation Bevelites (eu/jev): eu/jev serves only its own
  decision model, so the dash-anchored brand stem is safe to claim; model references
  (`eu-jeff-latest`, `eu-jeff-1.0.0`, and the `eu_jev/`-qualified forms via the suffix
  walk) resolve at the pattern tier. The vendor discloses no base-model lineage, so
  the classification is by operator (Bevelites GmbH, Germany) — if lineage is ever
  disclosed, the pattern SHALL be revisited. A tier-2 provider default `eu_jev` →
  `eu` SHALL also exist: the provider is first-party-only, so unbound flows on the
  provider resolve by operator too. (The drift coverage check only credits provider
  defaults for speech-category providers, so the pattern — not the default — is what
  covers the `eu_jev/eu-jeff-*` ids there.)
- `lfm2.` → bloc `us`, organisation Liquid AI: LFM2.5 is Liquid AI's own architecture
  (MIT CSAIL spin-out) with extended pre-training over LFM2 — dot-anchored per the
  `step-3.` convention, covering LFM2.5 and future LFM2.x point releases. NO bare
  `lfm` stem SHALL exist.
- `baseten/decision-models/baseten-joey` → bloc `cn`, organisation naming base and
  tuner (`Alibaba (Base Labs post-train)`): joey-1 is post-trained from Qwen3.5-2B
  (Baseten's own announcement), so the fine-tunes-inherit-base rule assigns Alibaba's
  bloc — the same org label as the wave-8 elephant/mammoth entries. NO
  `baseten/decision-models/` namespace wildcard SHALL exist: a future Base Labs model
  on a non-Qwen base must surface in the drift report rather than inherit silently.
- `motif-3` → bloc `kr`, organisation Motif Technologies: Motif-3 is a from-scratch
  314B MoE ("fully in-house, proprietary design" per the model card) from a Korean
  sovereign-AI national-team lab. Version-anchored; NO bare `motif` stem SHALL exist
  (common English word).
- The providers `streamlake`, `kyma`, `aiand`, `clf_ai_gateway`, `zerogpu`, and
  `refuseless` SHALL carry NO tier-2 provenance default: each is multi-vendor
  (or, for refuseless, multi-lineage), so their catalogs resolve model-by-model through
  the existing family patterns. (`bigmodel` is not a new provider: it aliases to the
  existing `zhipu` entry, whose pre-existing tier-2 `cn` default is unchanged — honest
  for the whole current catalog since the third-party Vidu models are also cn-bloc.)
- The families `abliteration/` (catalog placeholder ids on a non-provider namespace,
  per-id lineage undisclosed) and `kyma/sonar` (upstream model not identified in any
  primary source) SHALL remain provenance `unknown`, recorded as acknowledged residue
  in `scripts/kb_drift_aliases.json` with dated judgments — accept unknown rather than
  guess a bloc (the Drex v1.0 precedent).

#### Scenario: Soniox speech flows resolve through the provider default
- **WHEN** an unbound flow on provider `soniox` carries no model reference, and the
  drift coverage check evaluates the `soniox/stt-*` id set (e.g. `soniox/stt-rt-preview`,
  `soniox/stt-rt-v5`, `soniox/stt-async-v5`)
- **THEN** the unbound flow resolves to bloc `us` via the tier-2 provider default,
  every id in the set counts as covered (the first-party speech-provider rule), and
  no bare `stt` stem exists in the pattern map

#### Scenario: eu/jev model ids resolve via the brand stem; unbound flows via the default
- **WHEN** a model reference `eu-jeff-1.0.0` is detected, the drift coverage check
  evaluates the qualified forms `eu_jev/eu-jeff-1.0.0` and `eu_jev/eu-jeff-latest`,
  and separately an unbound flow on provider `eu_jev` carries no model reference
- **THEN** the reference resolves to bloc `eu` with organisation Bevelites (eu/jev)
  via the `eu-jeff` pattern, the qualified forms count as covered via the drift
  check's suffix walk against the same pattern, and the unbound flow resolves to bloc
  `eu` via the tier-2 provider default — both classifying by operator while the
  vendor's base-model lineage remains undisclosed

#### Scenario: LFM2.5 resolves via the dot-anchored stem
- **WHEN** a model reference `lfm2.5-7b-chat` is detected, and the drift coverage
  check evaluates the qualified form `zerogpu/LFM2.5-1.2B-Instruct`
- **THEN** the reference resolves to bloc `us` with organisation Liquid AI via the
  `lfm2.` anchor, and the qualified form counts as covered via the drift check's
  suffix walk against the same pattern

#### Scenario: Baseten's joey inherits the Qwen bloc
- **WHEN** a model reference `baseten/decision-models/baseten-joey-2b-latest` is
  detected
- **THEN** it resolves to bloc `cn` with the organisation label naming base and tuner
  (`Alibaba (Base Labs post-train)`), per the fine-tunes-inherit-base rule

#### Scenario: Motif-3 resolves to kr via the version anchor
- **WHEN** a model reference `motif-3` is detected, and the drift coverage check
  evaluates the qualified form `aiand/motif-technologies/motif-3`
- **THEN** the reference resolves to bloc `kr` with organisation Motif Technologies
  via the version-anchored `motif-3` pattern, and the qualified form counts as
  covered via the drift check's suffix walk against the same pattern

#### Scenario: Guarded stems stay unknown
- **WHEN** hypothetical references `stt-9-ultra`, `lfma-7b`, or
  `motif-blank-7b` are detected
- **THEN** none resolves through any pattern (no bare `stt`, `stt-rt`, `stt-async`,
  `lfm`, or `motif` stems exist) and each keeps provenance `unknown` — while a form
  like `lfm-turbo-7b` continues to resolve through the pre-existing dash-anchored
  `lfm-` pattern, exactly as before this wave

#### Scenario: Multi-vendor wave-9 providers carry no tier-2 default
- **WHEN** unbound flows on providers `streamlake`, `kyma`, `aiand`,
  `clf_ai_gateway`, `zerogpu`, or `refuseless` carry no model reference
- **THEN** each keeps provenance `unknown` (no tier-2 default on a multi-vendor or
  multi-lineage provider)

#### Scenario: Refuseless catalog ids resolve through existing base patterns
- **WHEN** the drift coverage check evaluates the `refuseless` catalog (e.g.
  `refuseless/glm-5.3-abliterated`, `refuseless/deepseek-v4.1-flash-abliterated`)
- **THEN** every id counts as covered via the suffix walk against the pre-existing
  anchored GLM and DeepSeek family patterns, which are unchanged

#### Scenario: Acknowledged residue stays unknown
- **WHEN** model references `abliteration/abliterated-model` and `kyma/sonar` are
  detected
- **THEN** both keep provenance `unknown`, and the drift report carries them only as
  acknowledged residue with dated judgments in `scripts/kb_drift_aliases.json`
