# jurisdiction-classification Delta

## MODIFIED Requirements

### Requirement: Bundled east-west provider knowledge base
The system SHALL ship a bundled knowledge base that maps AI providers — Western, Chinese, and
other blocs (for example OpenAI, Anthropic, Google, Mistral, Cohere, Tencent Hunyuan, Alibaba
DashScope, DeepSeek, Xiaomi MiMo, SCX.ai, AiHubMix, AWS Transcribe, TypeSafe AI, Prism
Inference, Sail Research, Bespoke Labs, Laya, Strands Decider, Microsoft 365 Copilot,
ScaleDown, CoralBricks, Inference APIs, Nace.AI, OpenInfer) — to their SDK names, endpoint
hosts, and a jurisdiction. A provider whose upstream API hostname is not documented MAY carry
no endpoint hosts; the entry still records the provider's jurisdiction and sovereignty and
MUST NOT carry a guessed hostname. A provider that is a self-hosted runtime — reachable only
at a deployer-supplied address, with no vendor-operated endpoint — SHALL carry jurisdiction
and sovereignty `local`. Where the documented API host is a shared multi-service surface (for
example `graph.microsoft.com`, which serves all Microsoft Graph traffic, not only Copilot),
the entry SHALL record the shared-surface caveat in its note.

#### Scenario: Western and Chinese providers both resolve
- **WHEN** a detection identifies `openai` and another identifies `deepseek`
- **THEN** the first resolves to jurisdiction `us` and the second to jurisdiction `cn`

#### Scenario: Xiaomi MiMo global platform resolves
- **WHEN** a detection matches `api.xiaomimimo.com`
- **THEN** it resolves to provider `xiaomi_mimo` with jurisdiction `unknown` (region-dependent:
  the international platform stores data in EU and Singapore data centres)

#### Scenario: Xiaomi MiMo Token Plan host resolves to cn
- **WHEN** a detection matches `token-plan-cn.xiaomimimo.com`
- **THEN** it resolves to provider `xiaomi_mimo` with jurisdiction `cn`

#### Scenario: SCX.ai endpoint resolves to au
- **WHEN** a detection matches `api.scx.ai`
- **THEN** it resolves to provider `scx_ai` with jurisdiction `au` and sovereignty bloc `au`

#### Scenario: Aggregator with undisclosed operator resolves to unknown
- **WHEN** a detection matches `aihubmix.com` or `api.inferera.com`
- **THEN** it resolves to provider `aihubmix` with jurisdiction `unknown` (the operating
  entity is undisclosed; third-party claims are not knowledge-base facts)

#### Scenario: AWS Transcribe regional host resolves
- **WHEN** a detection matches `transcribe.eu-west-1.amazonaws.com`
- **THEN** it resolves to provider `aws_transcribe` with the region-resolved jurisdiction
  and sovereignty bloc `us`

#### Scenario: Provider without documented endpoint carries no host
- **WHEN** the bundled knowledge base entry for `typesafe` is loaded
- **THEN** it carries jurisdiction `us` and sovereignty `us` with an empty endpoint list
  and a note recording that the upstream hostname is undocumented

#### Scenario: Open-weight host platforms resolve to us
- **WHEN** detections match `api.prisminference.com` and `api.sailresearch.com`
- **THEN** they resolve to providers `prism` and `sail` respectively, each with
  jurisdiction `us` and sovereignty bloc `us`

#### Scenario: Self-hosted decision runtimes resolve to local
- **WHEN** the bundled knowledge base entries for `bespoke`, `laya`, and `strands_decider`
  are loaded
- **THEN** each carries jurisdiction `local` and sovereignty `local` with an empty endpoint
  list and a note naming the vendor and the self-hosted, deployer-supplied-address mechanics

#### Scenario: Microsoft 365 Copilot resolves via the shared Graph host
- **WHEN** a detection matches `graph.microsoft.com`
- **THEN** it resolves to provider `microsoft_365_copilot` with jurisdiction `us` and
  sovereignty bloc `us`, and the entry's note records that the host is the shared Microsoft
  Graph surface, that the Copilot Chat API is a Graph beta (preview) endpoint, and that
  Microsoft chooses the served model

#### Scenario: ScaleDown resolves via its documented API host
- **WHEN** a detection matches `api.scaledown.xyz`
- **THEN** it resolves to provider `scaledown` with jurisdiction `us` and sovereignty bloc
  `us`, and the entry's note records that the API host is `.xyz` (distinct from the vendor's
  `.ai` marketing and docs hosts) and that ScaleDown, Inc. commits to US-only processing in
  its DPA

#### Scenario: Wave-7 hosted inference providers resolve to us
- **WHEN** detections match `inference.coralbricks.ai`, `api.inferenceapis.com`, and
  `api.openinfer.ai`
- **THEN** they resolve to providers `coralbricks`, `inferenceapis`, and `openinfer`
  respectively, each with jurisdiction `us` and sovereignty bloc `us`, and `inferenceapis`
  carries category `aggregator` (a gateway reselling Together AI and DeepInfra capacity)

#### Scenario: Nace resolves on both documented hostnames
- **WHEN** detections match `console.nace.ai` and `drex.nace.ai`
- **THEN** both resolve to provider `nace` with jurisdiction `us` and sovereignty bloc
  `us`, and the entry's note records that the two hostnames serve the same decision-model
  API (litellm's default and the vendor-documented alias)
