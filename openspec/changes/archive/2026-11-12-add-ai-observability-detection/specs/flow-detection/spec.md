# flow-detection Delta

## ADDED Requirements

### Requirement: Detect Langfuse and LangSmith observability flows
The scanner SHALL detect curated Langfuse and LangSmith SDK imports and documented hosted endpoint references, with provider category `observability` and default jurisdiction `unknown`. The Langfuse JS/TS package set SHALL comprise `@langfuse/tracing`, `@langfuse/otel`, `@langfuse/openai`, `@langfuse/langchain`, `@langfuse/vercel-ai-sdk`, and deprecated `langfuse`, `langfuse-core`, `langfuse-node`, `langfuse-langchain`, and `langfuse-vercel`; other Langfuse scope packages SHALL NOT match. The scanner SHALL recognise exactly `LANGFUSE_BASE_URL`, `LANGFUSE_HOST`, `LANGFUSE_BASEURL`, `LANGFUSE_OTEL_HOST`, `LANGSMITH_ENDPOINT`, and `LANGCHAIN_ENDPOINT` as explicit observability destination declarations, emitting kind `observability_endpoint`. Matching SHALL use these raw key spellings case-sensitively; camelCase and other case variants SHALL NOT match. Known hosts SHALL resolve through the provider KB, loopback to `local`, and unmapped or runtime-resolved destinations to `custom_endpoint`/`unknown`. Evidence and declaration-scoped duplicate suppression SHALL follow the existing agent-tool endpoint rules. No API key, tracing-enablement variable, generic OpenTelemetry declaration, arbitrary URL, or undocumented destination key SHALL independently create this detection kind. Findings SHALL represent potential or configured telemetry, never proof of transmission or payload contents.

#### Scenario: Python observability SDK import
- **WHEN** a Python file contains `import langfuse` or `import langsmith`
- **THEN** an `sdk_import` detection identifies the observability provider with jurisdiction, sovereignty, and provenance `unknown`

#### Scenario: Current and legacy Langfuse JS packages
- **WHEN** a TypeScript file imports `@langfuse/tracing`, `@langfuse/otel`, `@langfuse/openai`, `@langfuse/langchain`, `@langfuse/vercel-ai-sdk`, `langfuse`, `langfuse-core`, `langfuse-node`, `langfuse-langchain`, or `langfuse-vercel`
- **THEN** an `sdk_import` detection identifies Langfuse with default jurisdiction `unknown`

#### Scenario: Non-tracing Langfuse scope packages do not match
- **WHEN** a TypeScript file imports only `@langfuse/client`, `@langfuse/core`, `@langfuse/browser`, or an arbitrary future `@langfuse/*` package
- **THEN** no Langfuse SDK detection is produced

#### Scenario: LangSmith Java SDK import
- **WHEN** a Java file imports a class under `com.langchain.smith`
- **THEN** an `sdk_import` detection identifies LangSmith with default jurisdiction `unknown`

#### Scenario: Every explicit observability key is recognized
- **WHEN** a scanned file declares any of the six explicit observability destination keys with a static host value
- **THEN** it produces an `observability_endpoint` detection

#### Scenario: Observability key variants do not match
- **WHEN** a scanned file declares `langfuseBaseUrl`, `langsmith_endpoint`, `LANGFUSE_base_URL`, or another variant of an explicit key
- **THEN** no `observability_endpoint` detection is produced

#### Scenario: Known hosted destination resolves
- **WHEN** `LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com` is declared
- **THEN** one `observability_endpoint` detection resolves LangSmith and its curated residency and sovereignty without a generic duplicate

#### Scenario: Custom and runtime destinations remain honest
- **WHEN** an explicit key declares an unmapped host, loopback host, or runtime-templated value
- **THEN** the detection resolves respectively to `unknown`, `local`, or `unknown` with a runtime-resolved evidence marker

#### Scenario: Telemetry evidence is sanitized
- **WHEN** an explicit destination contains userinfo, a path, query, fragment, or trailing assignment
- **THEN** evidence contains only the declaration key and sanitized host

#### Scenario: Generic telemetry configuration is not vendor attribution
- **WHEN** a file contains only `OTEL_EXPORTER_OTLP_ENDPOINT`, `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, or an undocumented telemetry key
- **THEN** no `observability_endpoint` detection is produced

#### Scenario: Observability flows use existing policy behavior
- **WHEN** an observability destination is disallowed, unknown, local, or carries a justified waiver
- **THEN** existing residency, `on_unknown`, local-exemption, waiver, reporting, and exit-code behavior applies without a new option

## MODIFIED Requirements

### Requirement: Model references bind to same-file provider detections
A `model_reference` detection SHALL bind to an eligible provider detection in the same file when the
file's matched model references resolve to exactly one distinct provenance bloc, assigning that
bloc to the flow; when several same-bloc references bind, the first matched reference's
identifier SHALL be recorded as the flow's model identifier, representing its siblings. When a
file's model references resolve to more than one distinct bloc, binding would be ambiguous: no
binding SHALL occur and each reference SHALL stand alone. A `model_reference` with no eligible provider
detection in its file SHALL stand alone as its own finding. Binding SHALL NOT cross file
boundaries. Model references SHALL NOT bind to detections of kind `agent_tool_endpoint` or
`observability_endpoint`, nor to detections whose provider KB category is `observability`. Those
detections SHALL retain provenance `unknown`; when only ineligible detections occur in the file,
each reference SHALL stand alone.

#### Scenario: Model reference in the same file as a provider flow
- **WHEN** a file contains both a provider detection and a matching model reference
- **THEN** the provider flow carries the model reference's provenance and both evidences are traceable

#### Scenario: Ambiguous blocs do not bind
- **WHEN** a file contains a provider detection and model references resolving to two distinct blocs
- **THEN** the provider flow keeps its two-tier provenance and each reference is reported as its own standalone finding

#### Scenario: Standalone model reference
- **WHEN** a file contains a matching model reference but no provider detection
- **THEN** a standalone `model_reference` finding is reported with its resolved provenance

#### Scenario: Model reference does not bind to an agent tool
- **WHEN** a file contains an `agent_tool_endpoint` detection and a matching model reference but no other provider flow
- **THEN** the tool detection keeps provenance `unknown` and the model reference is reported standalone

#### Scenario: Model reference binds beside an agent tool
- **WHEN** a file contains an eligible model provider flow, an `agent_tool_endpoint` detection, and one matching model reference
- **THEN** the reference binds only to the eligible provider flow and not to the tool endpoint

#### Scenario: Model reference does not bind to an observability SDK
- **WHEN** a file contains a Langfuse or LangSmith SDK detection and a matching model reference but no eligible provider flow
- **THEN** the observability detection keeps provenance `unknown` and the model reference is reported standalone

#### Scenario: Model reference does not bind to an observability endpoint
- **WHEN** a file contains an `observability_endpoint` detection and a matching model reference but no eligible provider flow
- **THEN** the observability detection keeps provenance `unknown` and the model reference is reported standalone

#### Scenario: Model reference binds beside observability
- **WHEN** a file contains an eligible model provider flow, an observability detection, and one matching model reference
- **THEN** the reference binds only to the eligible provider flow and not to the observability detection
