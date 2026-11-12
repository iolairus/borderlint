# Proposal: add-ai-observability-detection

## Why

A6 remains uncovered: Langfuse and LangSmith can receive prompts, outputs, and traces, but their SDKs and telemetry destinations do not currently produce findings. These flows can bypass residency and sovereignty review even when the traced inference provider is already detected.

## What Changes

- Add Langfuse and LangSmith as `observability` providers with curated Python, JS/TS, and LangSmith JVM SDK coverage. Include current Langfuse tracing/integrations and explicit deprecated SDK packages, not the entire npm scope.
- Detect documented hosted endpoints with exact-country residency: Ireland (`ie`), Netherlands (`nl`), United States (`us`), Japan (`jp`), and Australia (`au`). Include Langfuse HIPAA and LangSmith Azure/private-connectivity hosts.
- Detect exactly six explicit destination keys: `LANGFUSE_BASE_URL`, `LANGFUSE_HOST`, `LANGFUSE_BASEURL`, `LANGFUSE_OTEL_HOST`, `LANGSMITH_ENDPOINT`, and legacy `LANGCHAIN_ENDPOINT`, using a new `observability_endpoint` kind.
- SDK-only, custom, and runtime-resolved destinations default to `unknown`; loopback resolves to `local`. Documented Langfuse Cloud and LangSmith SaaS endpoints use `us` sovereignty, while their physical residency remains independent.
- Reuse A7-style evidence sanitization and occurrence-scoped duplicate suppression. Add no CLI flag, policy block, runtime dependency, or network access.
- Exclude observability findings from model-reference binding and first-party provenance defaults.
- Surface `(observability)` in text and retain the category in JSON/SBOM without changing verdicts.
- Update README, contribution guidance, and mark A6 shipped after implementation.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `flow-detection`: observability SDKs and explicit telemetry destinations become traceable; model binding excludes non-model sinks.
- `jurisdiction-classification`: documented observability hosts resolve to exact physical countries.
- `sovereignty`: hosted Langfuse/LangSmith endpoints and self-hosted/SDK-only uses resolve independently.
- `cli-and-reporting`: reports expose the observability category.

## Impact

- Provider and sovereignty KB data, SDK drift exemptions, detector, reporting, tests, and documentation.
- Existing inference, MCP, and agent-tool behavior remains unchanged.

## Non-goals

- No other observability vendors, generic OTLP attribution, arbitrary telemetry URLs, or tracing-flag/API-key detection.
- No payload inspection, proof of transmission, tracing-enablement analysis, call-graph attribution, or transitive egress claims.
- No provenance defaults, data-practice curation, Go scanning, or unofficial SDK namespaces.
- No unrelated host-matcher, Suricata, generic config-deduplication, or A7 behavior changes.
