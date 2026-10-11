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
`tencent_hunyuan`, and `zhipu` replacing their previously all-null entries: DeepSeek with
training default `opt-out` (policy-level right, no documented API carve-out), PRC residency,
and purpose-bound retention with no fixed window; Tencent Hunyuan with a 30-day
diagnostic/usage retention scope quoted verbatim (including output information) and training
default null where documents are silent; Zhipu with training default `no` for identifiable
content plus its anonymisation training carve-out quoted in the locator, China-only storage,
and its named third-party SDK table as subprocessors.

#### Scenario: DeepSeek entry carries the policy-level opt-out posture
- **WHEN** the evidence pack or KB website renders data practices for `deepseek`
- **THEN** the training default reads opt-out with a citation noting no self-serve API opt-out is documented, and the retention fact cites PRC processing and storage

#### Scenario: Tencent Hunyuan retention quotes its actual scope
- **WHEN** data practices render for `tencent_hunyuan`
- **THEN** the retention fact cites the 30-day diagnostic/usage window verbatim including output information, and training_default is null

#### Scenario: Zhipu entry discloses the anonymisation carve-out
- **WHEN** data practices render for `zhipu`
- **THEN** the training default reads no with the anonymisation-training carve-out quoted in its locator, and the subprocessors link cites the platform's third-party SDK table

### Requirement: Cited entries without stale unavailability notes
Every curated data-practice entry SHALL cite each non-null fact with a source URL, locator,
and retrieval date, and SHALL NOT retain explanatory notes claiming sources were unreachable
once facts have been curated; facts that remain undocumented SHALL stay null without notes
implying future availability.

#### Scenario: Citations complete, no stale unavailability claims
- **WHEN** any curated entry is loaded
- **THEN** every non-null fact has a complete citation, no note claims sources were unreachable, and remaining nulls carry no misleading explanation

### Requirement: Curated facts for FAANG first-party AI platforms
The bundled data-practice knowledge base SHALL carry cited entries for `meta_llama`,
`vertex_ai`, `azure_foundry`, and `github_copilot`: each stating the training default for
customer API/platform traffic, the retention posture, and the enterprise/tier distinction where
the platform's terms make one, every non-null fact citing its platform-specific document — Meta
Model API terms, Google Cloud Service Specific Terms "Training restriction" and its generative-AI
zero-data-retention documentation, Microsoft Foundry data-privacy documentation, and GitHub
Generative AI Services Terms respectively. Where a platform's training commitment is tier- or
service-dependent (e.g. Meta's Standard vs Discounted services), the entry SHALL state the
primary default and disclose the split in the tier fact's locator. Facts the cited documents do
not state SHALL remain null with a scope caveat where the omission could mislead.

#### Scenario: Meta Llama entry discloses its service-tier split
- **WHEN** data practices render for `meta_llama`
- **THEN** the training default reflects the Standard Services commitment (content not used to train Meta Models) and the tier fact discloses that Discounted Services may train on content by default

#### Scenario: Vertex entry cites the training restriction and retention paths
- **WHEN** data practices render for `vertex_ai`
- **THEN** the training default cites Google Cloud's training restriction (no training without prior permission), and retention notes the abuse-monitoring logging exemption path and per-feature retention conditions

#### Scenario: Azure Foundry mirrors its sibling posture
- **WHEN** data practices render for `azure_foundry`
- **THEN** the entry states customer data is not used to train foundation models, citing Microsoft Foundry's data-privacy documentation

#### Scenario: GitHub Copilot cites the current generative-AI terms
- **WHEN** data practices render for `github_copilot`
- **THEN** the training default cites the GitHub Generative AI Services Terms (Inputs/Outputs not used to train without documented instruction), and retention notes that per-product retention varies by documented feature

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

