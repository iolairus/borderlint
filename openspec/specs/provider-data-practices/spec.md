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

