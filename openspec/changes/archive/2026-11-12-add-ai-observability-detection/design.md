# Design: add-ai-observability-detection

## Context

Borderlint detects inference providers and agent tools but not the observability sinks that can receive the same prompts and outputs. A6 will start with Langfuse and LangSmith. Both support cloud and customer-operated deployments, so package identity and physical destination must remain separate facts.

## Research basis

### Langfuse

- Current Python uses package/import `langfuse`. Current JS tracing uses `@langfuse/tracing` and `@langfuse/otel`; integrations include `@langfuse/openai`, `@langfuse/langchain`, and `@langfuse/vercel-ai-sdk`. Sources: https://langfuse.com/docs/observability/sdk/overview and https://langfuse.com/docs/observability/get-started
- The official JS repository marks unscoped `langfuse`, `langfuse-core`, `langfuse-node`, and `langfuse-langchain` as deprecated v3 packages; the migration guide says `langfuse-vercel` was replaced by `@langfuse/otel`. Sources: https://github.com/langfuse/langfuse-js/blob/main/README.md and https://langfuse.com/docs/observability/sdk/upgrade-path/js-v3-to-v4
- `cloud.langfuse.com` primarily uses AWS eu-west-1 (Ireland); `us.cloud.langfuse.com` and `hipaa.cloud.langfuse.com` use us-west-2 (US); `jp.cloud.langfuse.com` uses ap-northeast-1 (Japan). Source: https://langfuse.com/security/data-regions
- Postgres backups have secondary regions; ClickHouse tracing data and S3 media are not cross-region replicated. The DPA permits some processing outside the selected region. The residency value therefore denotes the primary trace-hosting country, not every copy or processing event. Sources: https://langfuse.com/security/data-regions and https://langfuse.com/dpa
- Cloud and self-hosted SDKs share configuration through `LANGFUSE_BASE_URL`, `base_url`/`baseUrl`, and direct OTLP examples using `LANGFUSE_HOST`; the LiteLLM integration documents `LANGFUSE_OTEL_HOST`. Sources: https://langfuse.com/docs/observability/sdk/overview, https://langfuse.com/docs/observability/get-started, and https://langfuse.com/integrations/gateways/litellm
- Legacy JS configuration used `LANGFUSE_BASEURL`; self-hosting can be local, on-premises, arbitrary cloud, or air-gapped. Sources: https://langfuse.com/docs/observability/sdk/upgrade-path/js-v3-to-v4 and https://langfuse.com/docs/self-hosting
- Langfuse was acquired by ClickHouse in January 2026. The Cloud Addendum defines Langfuse Cloud as ClickHouse's SaaS; general terms name ClickHouse, Inc., with Langfuse GmbH for pay-as-you-go customers. Sources: https://langfuse.com/press, https://clickhouse.com/legal/langfuse-cloud-addendum, https://langfuse.com/terms, and https://langfuse.com/imprint
- Other languages use OpenTelemetry or the public API rather than dedicated native Langfuse SDKs. Source: https://langfuse.com/docs/observability/sdk/overview

### LangSmith

- Python and JS/TS use package `langsmith`; official Java imports are under `com.langchain.smith`. Sources: https://docs.langchain.com/langsmith/create-account-api-key and https://github.com/langchain-ai/langsmith-java
- `LANGSMITH_ENDPOINT` and constructor configuration can select cloud or self-hosted deployments; legacy `LANGCHAIN_ENDPOINT` remains supported. Sources: https://docs.langchain.com/langsmith/create-account-api-key and https://docs.langchain.com/langsmith/profile-configuration
- `api.smith.langchain.com` uses GCP us-central1 (US); `eu.api.smith.langchain.com` uses europe-west4 (Netherlands); `apac.api.smith.langchain.com` uses australia-southeast1 (Australia); `aws.api.smith.langchain.com` uses us-east-2 (US); `azure.api.smith.langchain.com` uses centralus (US). Sources: https://docs.langchain.com/langsmith/create-account-api-key and https://docs.langchain.com/langsmith/cloud
- Private Service Connect hosts `us-central1.p.api.smith.langchain.com`, `europe-west4.p.api.smith.langchain.com`, and `australia-southeast1.p.api.smith.langchain.com` map respectively to the same US, Netherlands, and Australia locations. Source: https://docs.langchain.com/langsmith/cloud
- Authentication/authorization storage has separate documented locations, and billing information is stored in the US. Residency here means primary trace/application-data location, not all associated data. Source: https://docs.langchain.com/langsmith/cloud
- Self-hosted endpoints are deployer-supplied; non-air-gapped self-hosting can have separate billing/operational egress, which is not conflated with the trace destination. Sources: https://docs.langchain.com/langsmith/self-host-usage and https://docs.langchain.com/langsmith/self-host-egress
- LangSmith terms identify LangChain Inc., a Delaware corporation. This supports advisory `us` sovereignty for LangChain-operated SaaS, not customer-operated deployments. Source: https://www.langchain.com/terms-of-service
- No official LangSmith .NET SDK is documented in the vendor's SDK reference; unofficial namespaces will not be invented. Source: https://docs.langchain.com/langsmith/reference

## Goals / Non-Goals

**Goals:**
- Detect the two curated observability products without claiming observed transmission.
- Resolve exact primary hosting countries and hosted-operator sovereignty independently.
- Preserve sanitized evidence and existing policy/report behavior.

**Non-Goals:**
- Generic OpenTelemetry routing, additional vendors, payload analysis, or runtime discovery.
- Data-practice curation, new policy/output schemas, or unrelated detector fixes.

## Decisions

- **Exact-country residency.** Use `ie` for Langfuse Ireland and `nl` for LangSmith Netherlands, not `eu`; use `au` for Sydney. `eu` remains a sovereignty bloc, not a substitute for physical country evidence.
- **Hosted Langfuse sovereignty is `us`.** Apply it only after a documented hosted host resolves, following the parent/operator precedent. Record the Langfuse GmbH contracting caveat. SDK-only and custom destinations remain `unknown`.
- **SDK-only means unknown.** Do not infer a cloud default region or operator from an import, API key, or tracing flag. No provenance default is added.
- **Explicit package inventory.** Cover the researched current/deprecated tracing packages and LangSmith Java. Reject blanket `@langfuse/*` matching because client/browser/core packages are outside the tracing slice and future scope packages would match automatically.
- **Exact destination-key inventory.** Recognize only the six agreed keys as `observability_endpoint`, using raw case-sensitive key matching; do not broaden generic AI environment stems or apply A7's camelCase/case normalization to this key set. Constructor-only custom destinations without vendor context remain outside this slice.
- **Reuse A7 declaration mechanics carefully.** Parameterize the curated declaration scanner by key set and kind, retaining sanitized evidence, occurrence spans, IDN handling, and A7 regression behavior. Known hosts use the KB; loopback is `local`; unknown/runtime values are `unknown`.
- **One model-eligibility rule.** Exclude `agent_tool_endpoint`, `observability_endpoint`, and providers categorized `observability` from model binding and tier-2 defaults. Other eligible flows in the same file still bind normally.
- **Small reporting addition.** Add `(observability)` to text and expose the existing category field in JSON/SBOM. No category-specific policy or verdict logic.

## Alternatives Considered

- **EU residency/sovereignty for regional cloud endpoints.** Rejected: exact physical residency is `ie`/`nl`, and the confirmed Langfuse hosted operator decision is `us` sovereignty.
- **Infer hosted defaults from SDKs.** Rejected: environment/constructor overrides and self-hosting make that unsound.
- **Match the whole Langfuse npm scope or generic OTel.** Rejected: both attribute packages/destinations without sufficient tracing/vendor evidence.
- **Reuse `config_endpoint` for telemetry declarations.** Rejected: a distinct kind supports honest provenance exclusion and clear output semantics.
- **Curate retention/training practices now.** Rejected: the existing uncurated state is valid and independent research should not enlarge A6.

## Risks / Trade-offs

- [Risk] New findings can warn or fail previously clean scans → Mitigation: intended A6 coverage; existing `on_unknown` and waivers apply, with release notes.
- [Risk] Corporate structure and regional inventory drift → Mitigation: dated primary-source notes and existing KB review/drift posture.
- [Risk] Primary trace country is mistaken for all processing → Mitigation: provider notes and documentation state the authentication/billing/backup caveats.
- [Risk] Sharing A7 declaration logic regresses agent tools → Mitigation: retain the complete A7 test matrix unchanged.
- [Risk] Static imports imply tracing that is disabled → Mitigation: describe potential/configured telemetry only, never observed exfiltration.

## Real-world validation (gate before merge)

Validate SDK and destination fixtures from official Langfuse/LangSmith examples and at least two public repositories per vendor where available. Cover current and legacy packages, every explicit key, hosted/custom/loopback/runtime values, disabled-tracing negatives, and generic OTel negatives. Record sanitized sources and results in the PR.
