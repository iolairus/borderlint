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
tokens `CN-GBA` (the nine Mainland GBA cities), `GBA` (an alias for `hk` plus `CN-GBA`), and `local`
(a loopback / on-host inference endpoint, which is not a cross-border transfer).

#### Scenario: GBA alias expands
- **WHEN** the `GBA` token is evaluated
- **THEN** it is treated as the set containing `hk` and `CN-GBA`

#### Scenario: local is a recognised token
- **WHEN** a flow resolves to `local`
- **THEN** it is a valid jurisdiction value, distinct from a country code and from `unknown`

### Requirement: Region-specific endpoint resolution
Where a provider exposes region-specific endpoints, the system SHALL resolve the jurisdiction from
the specific endpoint that was detected.

#### Scenario: International versus mainland endpoint
- **WHEN** a detection matches `dashscope-intl.aliyuncs.com` and another matches `dashscope.aliyuncs.com`
- **THEN** the first resolves to `sg` and the second to `cn`

#### Scenario: Aliyun mainland and Hong Kong regional hosts
- **WHEN** a detection matches a PAI-EAS host carrying an Aliyun region token (for example `svc.cn-hangzhou.pai-eas.aliyuncs.com` or `svc.cn-hongkong.pai-eas.aliyuncs.com`)
- **THEN** the first resolves to `cn` and the second to `hk`

#### Scenario: Aliyun international regional host
- **WHEN** a detection matches a PAI-EAS host in an Aliyun international region (for example `svc.ap-southeast-1.pai-eas.aliyuncs.com`)
- **THEN** it resolves to that region's jurisdiction (`sg`)

#### Scenario: Unmapped Aliyun region token degrades to unknown
- **WHEN** a detection matches a PAI-EAS host whose region token is not in the Aliyun map
- **THEN** the jurisdiction resolves to `unknown`, never to a guessed jurisdiction

### Requirement: Undetermined jurisdiction is unknown
The system SHALL mark a flow's jurisdiction as unknown when it cannot be determined from the
provider or endpoint alone, for example for region-in-endpoint providers such as Azure OpenAI or
Bedrock.

#### Scenario: Region-in-endpoint provider
- **WHEN** a detection identifies a provider whose region is not determinable from the evidence
- **THEN** the resolved jurisdiction is unknown

### Requirement: User-supplied knowledge base
The system SHALL merge a user-supplied knowledge base with the bundled one: user entries add to the
bundled providers and, on a host, SDK, or package conflict, take precedence. A user-supplied host
SHALL be resolved in preference to any bundled host. The user-supplied knowledge base does not
replace the bundled one.

#### Scenario: Custom provider added alongside bundled
- **WHEN** the user supplies a knowledge base defining an additional provider
- **THEN** detections for that provider resolve using the supplied definition, and bundled providers still resolve

#### Scenario: User entry overrides a bundled host
- **WHEN** a user entry defines a host that also exists in the bundled knowledge base
- **THEN** the user entry's jurisdiction takes precedence over the bundled host

#### Scenario: User overrides a bundled provider
- **WHEN** a user entry defines a provider whose id, SDK, or package name also exists in the bundled knowledge base
- **THEN** the user definition takes precedence for that provider

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

### Requirement: Unrecognised configured host resolves to unknown
The system SHALL resolve an endpoint detected via a configuration key or client override to an
unknown jurisdiction when its host is not in the knowledge base and is not a loopback host, so that
the policy governs it.

#### Scenario: Custom OpenAI-compatible host
- **WHEN** a configured endpoint host (for example `llm.acme.cn`) is not in the knowledge base
- **THEN** its jurisdiction is unknown

### Requirement: Loopback endpoints are local
A loopback or localhost endpoint SHALL resolve to the `local` jurisdiction.

#### Scenario: Local inference server
- **WHEN** a configured endpoint points at `http://localhost:8080` or `http://127.0.0.1`
- **THEN** its jurisdiction is `local` (a loopback host takes precedence over the unknown-host rule)

### Requirement: Endpoint-to-jurisdiction registry
The system SHALL accept a simple endpoints map (host to jurisdiction code) in a user-supplied file
and resolve those hosts to the given jurisdiction, merged additively with the bundled knowledge base.
Each mapped jurisdiction MUST be a recognised token — a ccTLD/ISO country code, or one of `CN-GBA`,
`GBA`, `local`, `unknown`; an unrecognised token SHALL be rejected with an error.

#### Scenario: Internal regional endpoints resolve
- **WHEN** a user file maps `llm-cn.acme.com` to `cn`, `llm-sg.acme.com` to `sg`, and `llm-hk.acme.com` to `hk`
- **THEN** a flow to each host resolves to its mapped jurisdiction (`cn`, `sg`, and `hk` respectively)

#### Scenario: Invalid jurisdiction token is rejected
- **WHEN** a user file maps a host to an unrecognised token (for example `overseas`)
- **THEN** the system rejects it with an error

### Requirement: Resolve GCP (Vertex AI) region-coded endpoint host

borderlint SHALL resolve a Google Vertex AI endpoint host that carries a GCP region
(`<region>-aiplatform.googleapis.com`, or the `aiplatform.<us|eu>.rep.googleapis.com` multi-region
form) to the corresponding jurisdiction. When the host carries no region (the global
`aiplatform.googleapis.com` endpoint), the jurisdiction SHALL be `unknown`.

#### Scenario: Regional Vertex host resolves
- **WHEN** an endpoint reference contains `asia-east2-aiplatform.googleapis.com`
- **THEN** the flow resolves to jurisdiction `hk`

#### Scenario: A European Vertex region resolves
- **WHEN** an endpoint reference contains `europe-west4-aiplatform.googleapis.com`
- **THEN** the flow resolves to jurisdiction `nl`

#### Scenario: The global Vertex endpoint is unknown
- **WHEN** an endpoint reference contains the regionless `aiplatform.googleapis.com`
- **THEN** the flow resolves to jurisdiction `unknown`

### Requirement: United Kingdom token alias
The system SHALL treat the jurisdiction token `uk` as an alias for `gb` (ISO-3166 `GB`) wherever a
jurisdiction token is compared — in a classification allow-list and in a declared `home_location` — so
that a policy written with `uk` behaves identically to one written with `gb`.

#### Scenario: uk in an allow-list permits a gb flow
- **WHEN** a classification allow-list contains `uk` and a flow resolves to `gb`
- **THEN** the flow passes the residency check

#### Scenario: uk as a home location is treated as gb
- **WHEN** a policy declares `home_location` `uk`
- **THEN** it is treated identically to `home_location` `gb`

### Requirement: Each resolved flow carries a sovereignty bloc
In addition to a jurisdiction (residency), each resolved flow SHALL carry a sovereignty bloc
resolved from the provider knowledge base. The sovereignty bloc SHALL be one of the values defined
by the sovereignty vocabulary. A provider KB entry MAY declare an optional `sovereignty` field; a
host-level `sovereignty` override on a KB entry SHALL take precedence over the provider-level value.

#### Scenario: A provider KB entry declares its sovereignty
- **WHEN** a provider KB entry declares `sovereignty: us`
- **THEN** a flow to that provider resolves to sovereignty `us` regardless of the endpoint region

#### Scenario: A host-level sovereignty override takes precedence
- **WHEN** a provider KB entry declares a host with a `sovereignty` override distinct from the provider-level value
- **THEN** a flow to that host resolves to the host-level sovereignty

### Requirement: Region-in-endpoint providers inherit provider sovereignty
For a region-in-endpoint provider (AWS Bedrock, Azure OpenAI, Vertex AI), the resolved sovereignty SHALL be the provider's sovereignty, independent of the region resolved for residency. The endpoint region determines residency only; it SHALL NOT determine sovereignty. This requirement MUST hold for every region-in-endpoint provider in the knowledge base.

#### Scenario: Bedrock sovereignty is the provider's, not the region's
- **WHEN** a flow is detected to AWS Bedrock in `ap-east-1` (residency `hk`)
- **THEN** the flow's sovereignty is `us` (AWS's home sovereign), not `hk`

