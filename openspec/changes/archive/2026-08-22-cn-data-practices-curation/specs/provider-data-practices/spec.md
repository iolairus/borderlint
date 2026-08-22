# provider-data-practices Delta

## ADDED Requirements

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
