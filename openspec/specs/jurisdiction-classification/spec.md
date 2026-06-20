# jurisdiction-classification Specification

## Purpose
TBD - created by archiving change mvp-residency-scanner. Update Purpose after archive.
## Requirements
### Requirement: Bundled east-west provider knowledge base
The system SHALL ship a bundled knowledge base that maps AI providers — both Western and Chinese
(for example OpenAI, Anthropic, Google, Mistral, Cohere, Tencent Hunyuan, Alibaba DashScope,
DeepSeek) — to their SDK names, endpoint hosts, and a jurisdiction.

#### Scenario: Western and Chinese providers both resolve
- **WHEN** a detection identifies `openai` and another identifies `deepseek`
- **THEN** the first resolves to jurisdiction `us` and the second to jurisdiction `cn`

### Requirement: Jurisdiction codes and special tokens
The system SHALL express jurisdictions as lowercase ccTLD/ISO-3166 country codes, plus the special
tokens `CN-GBA` (the nine Mainland GBA cities) and `GBA` (an alias for `hk` plus `CN-GBA`).

#### Scenario: GBA alias expands
- **WHEN** the `GBA` token is evaluated
- **THEN** it is treated as the set containing `hk` and `CN-GBA`

### Requirement: Region-specific endpoint resolution
Where a provider exposes region-specific endpoints, the system SHALL resolve the jurisdiction from
the specific endpoint that was detected.

#### Scenario: International versus mainland endpoint
- **WHEN** a detection matches `dashscope-intl.aliyuncs.com` and another matches `dashscope.aliyuncs.com`
- **THEN** the first resolves to `sg` and the second to `cn`

### Requirement: Undetermined jurisdiction is unknown
The system SHALL mark a flow's jurisdiction as unknown when it cannot be determined from the
provider or endpoint alone, for example for region-in-endpoint providers such as Azure OpenAI or
Bedrock.

#### Scenario: Region-in-endpoint provider
- **WHEN** a detection identifies a provider whose region is not determinable from the evidence
- **THEN** the resolved jurisdiction is unknown

### Requirement: User-supplied knowledge base
The system SHALL allow the user to supply or override the bundled knowledge base.

#### Scenario: Custom provider definition
- **WHEN** the user supplies a knowledge base that defines an additional provider
- **THEN** detections for that provider resolve using the supplied definition

### Requirement: Resolve region-coded endpoint host
The system SHALL resolve a region-coded endpoint host to a jurisdiction when the region is present
in the matched text, before falling back to unknown.

#### Scenario: Bedrock host carries a Hong Kong region
- **WHEN** a detected endpoint contains `bedrock-runtime.ap-east-1.amazonaws.com`
- **THEN** the resolved jurisdiction is `hk`

#### Scenario: Bedrock host carries a Mainland China region
- **WHEN** a detected endpoint contains `bedrock-runtime.cn-north-1.amazonaws.com.cn`
- **THEN** the resolved jurisdiction is `cn`

#### Scenario: Region is not present in the host
- **WHEN** a detected endpoint is a standard `<resource>.openai.azure.com` host with no region token
- **THEN** the resolved jurisdiction is unknown

### Requirement: Knowledge base covers TypeScript and JavaScript packages
The knowledge base SHALL map providers to their TypeScript/JavaScript package names in addition to
their Python SDK names.

#### Scenario: A JavaScript package resolves to a provider
- **WHEN** the package `@anthropic-ai/sdk` is detected
- **THEN** it resolves to the Anthropic provider with jurisdiction `us`

#### Scenario: A non-US JavaScript package resolves
- **WHEN** the package `@mistralai/mistralai` is detected
- **THEN** it resolves to the Mistral provider with jurisdiction `eu`

### Requirement: Aggregator libraries resolve to unknown jurisdiction
A multi-provider aggregator or router library SHALL resolve to an unknown jurisdiction, because the
destination provider is selected at runtime.

#### Scenario: Aggregator jurisdiction is unknown
- **WHEN** a flow is detected for a known aggregator library (for example litellm)
- **THEN** its jurisdiction is unknown

