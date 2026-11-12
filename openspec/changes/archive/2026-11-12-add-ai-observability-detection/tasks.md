# Tasks: add-ai-observability-detection

## 1. Knowledge base — jurisdiction and sovereignty requirements

- [x] 1.1 Add Langfuse with category `observability`, default residency `unknown`, Python `langfuse`, JS packages `@langfuse/tracing`, `@langfuse/otel`, `@langfuse/openai`, `@langfuse/langchain`, `@langfuse/vercel-ai-sdk`, plus deprecated `langfuse`, `langfuse-core`, `langfuse-node`, `langfuse-langchain`, and `langfuse-vercel`; all four documented cloud hosts, exact `ie`/`us`/`jp` mappings, and primary-source notes including backup/processing caveats.
- [x] 1.2 Add LangSmith with category `observability`, default residency `unknown`, Python/JS `langsmith`, JVM `com.langchain.smith`, all eight documented public/private hosted hosts, exact `us`/`nl`/`au` mappings, and authentication/billing caveats.
- [x] 1.3 Set both provider sovereignty defaults to `unknown` and hosted-jurisdiction overrides to `us`; record Langfuse's ClickHouse/Langfuse GmbH nuance and LangChain's US operator source. Add no provenance defaults.
- [x] 1.4 Add reasoned SDK drift exemptions for unavailable JVM/.NET packages, retaining LangSmith's verified JVM key, and update KB review dates.

## 2. Detection — observability flow and provenance requirements

- [x] 2.1 Reuse the A7 declaration scanner through a small shared helper parameterized by key set and detection kind; add exactly the six observability keys with raw case-sensitive matching while preserving A7's key normalization and behavior.
- [x] 2.2 Resolve known, custom, loopback, and runtime destinations with sanitized evidence and occurrence-scoped duplicate suppression.
- [x] 2.3 Introduce one model-eligibility predicate for agent-tool endpoints, observability endpoints, and observability-category detections; use it for both model binding and tier-2 defaults.

## 3. Reporting — observability category requirement

- [x] 3.1 Add `(observability)` to text output while preserving existing JSON/SBOM category fields and all other category rendering.
- [x] 3.2 Update the provider category vocabulary in `CONTRIBUTING.md` and Detection kind documentation where applicable.

## 4. Tests — every acceptance scenario

- [x] 4.1 Test every SDK package named in task 1.1 and all 12 hosted host mappings, including longest-host/private-connectivity precedence and SDK-only unknown residency/sovereignty/provenance; reject `@langfuse/client`, `@langfuse/core`, `@langfuse/browser`, and arbitrary future scope packages.
- [x] 4.2 Test all six explicit keys, custom/loopback/runtime branches, comments, sanitization, declaration-scoped deduplication, and generic-OTel/API-key/tracing-flag negatives; reject camelCase and mixed-case observability key variants.
- [x] 4.3 Test observability-only and mixed OpenAI model-reference binding, plus unchanged A7 model-binding behavior.
- [x] 4.4 Test allowed, disallowed, unknown-warn/fail, local, and justified-waiver CLI behavior and exit codes.
- [x] 4.5 Exercise text, JSON, SARIF, SBOM, evidence, HTML, Mermaid, and badge outputs; assert text/JSON/SBOM category and unchanged schemas.
- [x] 4.6 Run drift/SDK coverage checks and the complete A7 regression matrix.

## 5. Validation and documentation — A6 closure

- [x] 5.1 Perform the design's official-example and public-repository validation; record sanitized sources, results, and rejected telemetry keys in the PR.
- [x] 5.2 Document supported SDKs, explicit keys, exact-country hosted mappings, hosted-US sovereignty, SDK/custom unknown behavior, caveats, and static-analysis limits in README.
- [x] 5.3 Mark A6 shipped in `CAPABILITIES.md` with the Langfuse + LangSmith scope.

## 6. Verification — full change acceptance

- [x] 6.1 Run `openspec validate add-ai-observability-detection --strict`, the full pytest suite, and KB drift checks.
- [x] 6.2 Run representative CLI scans and build/smoke-test the wheel with the new bundled KB data.
