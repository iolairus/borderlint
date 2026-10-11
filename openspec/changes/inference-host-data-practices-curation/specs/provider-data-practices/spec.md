# provider-data-practices Delta

## ADDED Requirements

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
