# jurisdiction-classification Delta

## MODIFIED Requirements

### Requirement: Bundled east-west provider knowledge base
The system SHALL ship a bundled knowledge base that maps AI providers — both Western and Chinese
(for example OpenAI, Anthropic, Google, Mistral, Cohere, Tencent Hunyuan, Alibaba DashScope,
DeepSeek, Xiaomi MiMo) — to their SDK names, endpoint hosts, and a jurisdiction.

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
