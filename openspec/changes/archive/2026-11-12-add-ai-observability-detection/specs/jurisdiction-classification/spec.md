# jurisdiction-classification Delta

## ADDED Requirements

### Requirement: Observability destination jurisdiction resolution
Documented Langfuse and LangSmith hosted endpoints SHALL resolve to the exact country of their primary trace/application-data hosting region, independently of sovereignty. SDK-only detections and destinations without curated host evidence SHALL resolve to `unknown`. The bundled mappings SHALL be:

- `cloud.langfuse.com` → `ie`; `us.cloud.langfuse.com` → `us`; `hipaa.cloud.langfuse.com` → `us`; `jp.cloud.langfuse.com` → `jp`.
- `api.smith.langchain.com` → `us`; `eu.api.smith.langchain.com` → `nl`; `apac.api.smith.langchain.com` → `au`; `aws.api.smith.langchain.com` → `us`; `azure.api.smith.langchain.com` → `us`.
- `us-central1.p.api.smith.langchain.com` → `us`; `europe-west4.p.api.smith.langchain.com` → `nl`; `australia-southeast1.p.api.smith.langchain.com` → `au`.

These values SHALL describe primary trace/application-data residency and SHALL NOT assert the location of every backup, authentication, billing, support, or subprocessed copy.

#### Scenario: Langfuse EU cloud resolves to Ireland
- **WHEN** a flow references `cloud.langfuse.com`
- **THEN** its residency is `ie`, not the broader sovereignty token `eu`

#### Scenario: Langfuse US and Japan regions resolve independently
- **WHEN** flows reference `us.cloud.langfuse.com`, `hipaa.cloud.langfuse.com`, and `jp.cloud.langfuse.com`
- **THEN** their residencies are respectively `us`, `us`, and `jp`

#### Scenario: LangSmith EU and APAC resolve to exact countries
- **WHEN** flows reference `eu.api.smith.langchain.com` and `apac.api.smith.langchain.com`
- **THEN** their residencies are respectively `nl` and `au`

#### Scenario: LangSmith US infrastructure variants resolve to US
- **WHEN** flows reference the default, AWS, or Azure LangSmith SaaS host
- **THEN** each resolves to residency `us`

#### Scenario: Private Service Connect hosts retain their regional mapping
- **WHEN** flows reference the three documented LangSmith Private Service Connect hosts
- **THEN** they resolve respectively to `us`, `nl`, and `au` rather than falling back to a shorter host mapping

#### Scenario: SDK or custom deployment has no inferred country
- **WHEN** only an observability SDK import or unmapped custom destination is present
- **THEN** residency is `unknown`
