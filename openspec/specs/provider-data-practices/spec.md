# provider-data-practices Specification

## Purpose
TBD - created by archiving change provider-data-practice-facts. Update Purpose after archive.
## Requirements
### Requirement: Bundled curated data-practice facts
The system SHALL bundle a hand-curated knowledge base of per-provider data-practice facts,
where each provider entry records: whether the provider trains on customer API data by
default (`yes`, `no`, or `opt-out`), the retention window for API inputs and outputs when
publicly documented, a link to the subprocessor list when one exists, and whether an
enterprise tier changes any of these answers. Every entry SHALL carry a top-level
last-reviewed date in ISO-8601 (`YYYY-MM-DD`) form, consistent with the other bundled
knowledge bases.

#### Scenario: A fully curated provider entry
- **WHEN** the data-practice knowledge base is loaded for a provider with all four facts curated
- **THEN** the entry exposes the training default, the retention window, the subprocessor link, and the enterprise-tier note alongside its last-reviewed date

#### Scenario: A partially curated provider entry
- **WHEN** the data-practice knowledge base is loaded for a provider where only some facts are publicly documented
- **THEN** the undocumented facts are recorded as explicitly unknown rather than omitted or guessed

### Requirement: Source citation per fact
Each data-practice fact SHALL carry a source citation consisting of a URL and a locator
note identifying where in the source the statement is made, together with the date the
fact was retrieved from that source.

#### Scenario: A fact renders with its citation
- **WHEN** a data-practice fact is surfaced anywhere by borderlint
- **THEN** it is presented with its source URL, locator note, and retrieval date

### Requirement: Human curation only
The data-practice knowledge base SHALL be populated exclusively by human curation via pull
request; the system SHALL NOT auto-fill any fact from upstream feeds, and the scheduled
coverage check SHALL NOT propose values for missing facts.

#### Scenario: Drift output proposes no facts
- **WHEN** the scheduled check reports a provider missing from the data-practice knowledge base
- **THEN** the gap record carries no training default, retention window, or subprocessor link

### Requirement: Explicit absence handling
borderlint SHALL state that data practices are not curated for a provider detected in a
scan but absent from the data-practice knowledge base, rather than rendering empty values,
and SHALL NOT fail the scan on that absence.

#### Scenario: An uncurated provider in a scan
- **WHEN** a scan detects a provider absent from the data-practice knowledge base
- **THEN** the scan exits normally and surfaces the provider as not curated for data practices

### Requirement: Advisory framing
All rendered data-practice facts SHALL be framed as advisory statements about providers'
documented practices as of their retrieval dates, with a visible disclaimer that they are
not legal advice; facts SHALL never influence verdicts, policy evaluation, or exit codes.

#### Scenario: Facts never change a verdict
- **WHEN** a scan produces findings for a provider whose curated facts are present
- **THEN** the verdicts and exit code are identical to a run without the data-practice knowledge base

### Requirement: Xiaomi MiMo curated facts
The bundled data-practice knowledge base SHALL carry a curated entry for `xiaomi_mimo` stating
the training default (`no`), the retention posture, and the storage-region note, each fact
carrying its source citation; undocumented facts (subprocessors) SHALL be recorded as null.

#### Scenario: Facts render with citations
- **WHEN** the evidence pack or KB website renders data practices for `xiaomi_mimo`
- **THEN** the training default cites the privacy policy statement that submitted content will
  not be used for model training, and the storage note cites the service agreement's EU +
  Singapore storage disclosure

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

### Requirement: Cited entries without stale unavailability notes
Every curated data-practice entry SHALL cite each non-null fact with a source URL, locator,
and retrieval date, and SHALL NOT retain explanatory notes claiming sources were unreachable
once facts have been curated; facts that remain undocumented SHALL stay null without notes
implying future availability.

#### Scenario: Citations complete, no stale unavailability claims
- **WHEN** any curated entry is loaded
- **THEN** every non-null fact has a complete citation, no note claims sources were unreachable, and remaining nulls carry no misleading explanation

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

### Requirement: Complete citations without stale notes
Each of the four new entries SHALL cite every non-null fact with a source URL, locator, and
retrieval date, and SHALL NOT claim sources were unreachable; undocumented facts SHALL remain
null.

#### Scenario: Citations complete across the four entries
- **WHEN** the four entries are loaded
- **THEN** every non-null fact has a complete citation and no entry claims unavailability

### Requirement: Curated facts for high-traffic inference hosts
The bundled data-practice knowledge base SHALL carry cited entries for the ten high-traffic
multi-model inference hosts `cerebras`, `cohere`, `deepinfra`, `fireworks_ai`, `groq`,
`mistral`, `openrouter`, `perplexity`, `sambanova`, and `together_ai`: each stating the
training default for customer API traffic, the retention posture, the subprocessor list where
one is published, and the enterprise/tier distinction where the provider's terms make one.
Where a provider's training commitment is tier-dependent (`cohere`, `mistral`), the entry
SHALL state the primary default and disclose the split in the tier fact, per the established
tier-split convention. Where the effective data practice depends on a downstream party —
partner models on `deepinfra`, routed model providers behind `openrouter` — the entry SHALL
record both the host's own commitment and the downstream dependence. Facts the cited
documents do not state SHALL remain null (notably `sambanova` retention), and a training
default inferred from a purpose-limited license rather than an explicit no-training sentence
SHALL quote the actual clause in its locator (`cerebras`, `sambanova`).

#### Scenario: Zero-retention-by-default hosts state their exceptions
- **WHEN** data practices render for `fireworks_ai`, `perplexity`, or `deepinfra`
- **THEN** the training default reads `no` and the retention fact records zero retention as
  the default, disclosing the documented exceptions — Fireworks' Response API `store=true`
  30-day retention, and DeepInfra's partner-model caveat for Google/Anthropic models

#### Scenario: Groq cites its contractual no-training clause
- **WHEN** data practices render for `groq`
- **THEN** the training default reads `no` citing the Services Agreement's Inputs/Outputs
  clause, and the retention fact notes the up-to-30-day reliability/abuse logs and the
  self-serve zero-retention setting available to all customers

#### Scenario: Tier-dependent training defaults disclose the split
- **WHEN** data practices render for `cohere` and `mistral`
- **THEN** the Cohere training default reads `opt-out` with the tier fact disclosing that
  trial keys train with no documented opt-out and ZDR requires enterprise approval, and the
  Mistral training default reads `opt-out` (free-tier Studio trains unless opted out) with
  the tier fact disclosing that the paid API is excluded from training by default

#### Scenario: Together records the stored-by-default posture and secondary use
- **WHEN** data practices render for `together_ai`
- **THEN** the training default reads `no` (opt-in only), and the retention fact records
  that prompts/responses are stored until the user deletes them with no fixed window, that
  stored content may be used for product improvements, and that self-serve ZDR exists

#### Scenario: OpenRouter records both layers of the routing relationship
- **WHEN** data practices render for `openrouter`
- **THEN** the training default reads `no` for OpenRouter itself with zero retention as its
  own default, and the entry discloses that downstream model providers may train unless the
  user restricts routing (provider-training opt-out or ZDR-only routing)

#### Scenario: Inference-from-license entries quote the actual clause
- **WHEN** data practices render for `cerebras` and `sambanova`
- **THEN** both training defaults read `no` with locators quoting the purpose-limited
  license clauses they rest on, SambaNova's retention fact is null (undocumented for the
  hosted API), and Cerebras' retention fact discloses that log retention carries no
  documented bounded window

### Requirement: Complete citations for the inference-host entries
Each of the ten new entries SHALL cite every non-null fact with a source URL, locator, and
retrieval date from the provider's own governing documents (terms of service, DPA, privacy
documentation, or official docs). Where a subprocessor list is published only as a
JS-rendered trust-center page, the citation SHALL reference the contract or document that
names the list URL as canonical, and SHALL NOT claim the source was unreachable.

#### Scenario: Citations complete across the ten entries
- **WHEN** the ten entries are loaded
- **THEN** every non-null fact has a complete citation keyed to a provider-authored document,
  no entry claims unavailability, and each entry key exists in the bundled provider
  knowledge base

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

