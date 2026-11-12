# sovereignty Delta

## ADDED Requirements

### Requirement: Observability sovereignty follows the demonstrated operator
Documented Langfuse Cloud and LangSmith SaaS endpoints SHALL resolve to advisory sovereignty `us`, independently of their physical residency. SDK-only detections and custom or runtime-resolved destinations SHALL retain sovereignty `unknown`; loopback SHALL retain the existing `local` behavior. The mapping SHALL record Langfuse's ClickHouse/Langfuse GmbH mixed contracting caveat and SHALL NOT adjudicate which statute applies to a particular flow.

#### Scenario: Langfuse hosted EU endpoint has US sovereignty
- **WHEN** a flow to `cloud.langfuse.com` resolves to residency `ie`
- **THEN** its sovereignty is `us`

#### Scenario: LangSmith regional SaaS retains US sovereignty
- **WHEN** flows resolve to LangSmith's Netherlands or Australia hosted endpoints
- **THEN** their sovereignty is `us` while their residencies remain `nl` and `au`

#### Scenario: SDK-only usage has no inferred operator
- **WHEN** only a Langfuse or LangSmith SDK import is detected
- **THEN** sovereignty is `unknown`

#### Scenario: Custom self-hosted destination has no inferred operator
- **WHEN** an explicit observability key declares an unmapped non-loopback host or runtime-resolved value
- **THEN** sovereignty is `unknown`
