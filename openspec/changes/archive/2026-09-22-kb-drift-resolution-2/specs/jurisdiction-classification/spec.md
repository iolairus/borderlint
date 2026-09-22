# jurisdiction-classification Delta

## MODIFIED Requirements

### Requirement: Bundled east-west provider knowledge base
The system SHALL ship a bundled knowledge base that maps AI providers — Western, Chinese, and
other blocs (for example OpenAI, Anthropic, Google, Mistral, Cohere, Tencent Hunyuan, Alibaba
DashScope, DeepSeek, Xiaomi MiMo, SCX.ai, AiHubMix, AWS Transcribe, TypeSafe AI) — to their
SDK names, endpoint hosts, and a jurisdiction. A provider whose upstream API hostname is not
documented MAY carry no endpoint hosts; the entry still records the provider's jurisdiction
and sovereignty and MUST NOT carry a guessed hostname.

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
