## ADDED Requirements

### Requirement: Wave-12 data-practice entries reflect current scoped facts

The nine stale entries not covered by the CN or FAANG requirements below SHALL be refreshed using
the provider-authored sources and exact scope limits in design D4: Alibaba DashScope retains
training `no` but removes its unsupported deletion promise; Anthropic gains its DPA-identified
subprocessor URL; Azure OpenAI records the Modified Abuse Monitoring cutoff; Google Gemini retains
Paid Service training `no` while correcting unpaid/paid retention and subprocessors; Moonshot adds
enterprise ZDR and exclusions without changing its general `opt-out`; NVIDIA NIM records hosted
trial API training `yes`, session/fine-tuning retention, and the production/self-hosted boundary;
OpenAI corrects endpoint-specific retention and its subprocessor locator; and Xiaomi MiMo retains
international training `no` while adding Team and regional-service facts. DeepSeek is addressed by
the CN requirement and is the only date-only review in this wave.

#### Scenario: Null training values change only with direct evidence
- **WHEN** the refreshed AWS Bedrock and NVIDIA NIM entries are loaded
- **THEN** their training defaults are respectively `no` and hosted-trial `yes`, each citing the
  scoped current source rather than an inferred practice

#### Scenario: Enterprise exceptions do not overwrite general defaults
- **WHEN** Moonshot facts are rendered
- **THEN** the entry still reports general `opt-out` alongside enterprise no-training/ZDR terms

#### Scenario: Undocumented facts remain explicit nulls
- **WHEN** a refreshed source does not publish a suitable fact or provider-specific subprocessor
  list
- **THEN** the corresponding field remains null and does not claim that the practice or
  subprocessors do not exist

## MODIFIED Requirements

### Requirement: Curated facts for the top CN token-volume providers
The bundled data-practice knowledge base SHALL carry cited entries for `deepseek`,
`tencent_hunyuan`, and `zhipu`. DeepSeek SHALL retain training default `opt-out` (policy-level
right, no documented API carve-out), PRC residency, and purpose-bound retention with no fixed
window. Tencent TokenHub SHALL state training default `no`; with ZDR activated in Singapore,
Frankfurt, or Silicon Valley it does not store Customer Content or Service Generated Content, and
otherwise generally retains those categories up to 30 days after the task request, with separate
configuration/diagnostic/billing limits. Zhipu SHALL distinguish domestic BigModel from
international Z.ai: identifiable domestic customer API content retains training default `no` with
anonymisation, generated-data optimisation, and non-personal-content exceptions quoted in locators;
domestic retention remains China-based/minimum-necessary with statutory and backup limits, while
Z.ai generally processes other Customer Data in Singapore and processes API content in real time
without server storage. Domestic subprocessors SHALL be scoped to their account/payment/analytics
surfaces and SHALL NOT be presented as an international Z.ai list.

#### Scenario: DeepSeek entry retains the policy-level opt-out posture
- **WHEN** the evidence pack or KB website renders data practices for `deepseek`
- **THEN** the training default reads opt-out with a citation noting no self-serve API opt-out is
  documented, and the retention fact cites PRC processing and storage

#### Scenario: TokenHub states training and ZDR scope
- **WHEN** data practices render for `tencent_hunyuan`
- **THEN** training default is `no`, and retention identifies both the three-region ZDR behavior
  and the otherwise-general 30-day content window

#### Scenario: Zhipu separates domestic and international processing
- **WHEN** data practices render for `zhipu`
- **THEN** domestic BigModel's training exceptions and China retention are not applied to Z.ai,
  whose real-time API content and Singapore Customer Data posture are stated separately

### Requirement: Curated facts for FAANG first-party AI platforms
The bundled data-practice knowledge base SHALL carry cited entries for `meta_llama`, `vertex_ai`,
`azure_foundry`, and `github_copilot`, each stating the scoped training default, retention posture,
and enterprise/tier distinction. Meta Standard Services SHALL retain training `no`; Contributor
Services (replacing Discounted Services) and Coding Harness defaults SHALL be disclosed, and
authorised Hosted Platforms SHALL remain separate. Vertex SHALL retain training `no` while its
retention fact enumerates the feature/model/contract-dependent behavior in design D4 rather than
implying universal ZDR. Azure Foundry SHALL retain training `no`, use live canonical privacy URLs,
and qualify Modified Abuse Monitoring by the 2026-11-01 model-availability cutoff and future
withdrawal notice. GitHub SHALL retain the volume-licensed commercial training `no`, disclose
individual-plan opt-out behavior, and cite feature-specific retention. Every non-null fact SHALL
cite its current platform-specific document; undocumented facts SHALL remain null.

#### Scenario: Meta Llama entry discloses its current service-tier split
- **WHEN** data practices render for `meta_llama`
- **THEN** the training default reflects Standard Services, and the tier fact identifies
  Contributor Services, Coding Harness defaults, and the separate Hosted Platform relationship

#### Scenario: Vertex entry cites training restriction and scoped retention paths
- **WHEN** data practices render for `vertex_ai`
- **THEN** the training default cites the no-training restriction, and retention covers the
  grounding, caching, Interactions, partner-model, and feature-specific windows without presenting
  ZDR as universally available

#### Scenario: Azure Foundry states current MAM limits
- **WHEN** data practices render for `azure_foundry`
- **THEN** it states customer data is not used to train foundation models and explains that MAM
  continues for pre-cutoff approvals but will become unavailable for later models on a future
  announced date with at least 30 days' notice

#### Scenario: GitHub Copilot distinguishes commercial and individual plans
- **WHEN** data practices render for `github_copilot`
- **THEN** the primary training default is scoped to commercial customers, individual opt-out
  behavior is visible, and retention cites current product/feature documentation
