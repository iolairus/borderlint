# add-jvm-detection

## Why

Financial services across HK, Singapore, and the wider region — borderlint's primary audience — largely run on the JVM, and a residency linter that cannot read Java falls short exactly where the regulatory stakes are highest. The roadmap holds Java/Kotlin at P3 ("largest coverage gap by industry"); this change pulls it forward because JVM coverage is the adoption gate for that audience.

## What Changes

- **Java/Kotlin detection**: `.java`, `.kt`, and `.kts` sources are scanned for `import` statements (including `import static`) and matched against a new per-provider `jvm` knowledge-base key holding import-package prefixes.
- **Full scan parity**: JVM sources flow through the same per-file pipeline as JS/TS — endpoint literals, OpenAI-compatible call paths, config-endpoint keys, inline waivers, and model-reference binding all apply unchanged.
- **KB curation**: `jvm` package prefixes for the majors with official or de-facto JVM SDKs (OpenAI, Anthropic, Azure OpenAI, Google Gemini, Vertex AI, AWS Bedrock, SageMaker, Cohere, Ollama), plus two new aggregator entries — **LangChain4j** (`dev.langchain4j`) and **Spring AI** (`org.springframework.ai`) — modeled like litellm/langchain (`unknown` jurisdiction and sovereignty, runtime-routed).
- README/CAPABILITIES updated (languages line; new shipped row in the CAPABILITIES §5.A language coverage table).

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `flow-detection`: ADDED requirements for Java/Kotlin SDK-import detection and for JVM sources receiving the same endpoint/call-path/waiver scanning as other languages. (The existing aggregator requirement already covers "any supported language" — no modification needed.)

## Impact

- `borderlint/detect.py`: `JVM_EXT` + `_scan_jvm()` (regex over import statements, mirroring `_scan_js`), one new branch in the `scan()` suffix dispatch.
- `borderlint/kb.py`: build a `jvm` match table from the new optional per-provider key (same pattern as `npm`); `match_jvm()` with dot-segment-aware longest-prefix matching.
- `borderlint/data/providers.json` (+`sovereignty.json`): `jvm` keys on ~9 providers; two new aggregator entries.
- `tests/test_borderlint.py`: Java and Kotlin fixtures, aggregator resolution, endpoint-literal-in-Java case.
- `README.md` / `CAPABILITIES.md` / `CONTRIBUTING.md` (KB schema mention). Zero new dependencies.

## Non-goals

- **No build-file scanning** (`pom.xml`, `build.gradle`): a declared-but-unimported dependency is not a flow, and the house precedent is identical — Python/JS detection keys on imports, not `requirements.txt`/`package.json`. Roadmap candidate if demand appears.
- No Scala/Groovy/Clojure; no bytecode or classpath analysis.
- No JVM-specific model-reference syntax — the existing language-agnostic model binding applies as-is.
