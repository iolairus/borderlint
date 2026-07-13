# add-jvm-detection — tasks

## 1. Knowledge base

- [x] 1.1 Add `jvm` prefix lists to providers.json for: openai, anthropic, azure_openai, google_gemini, vertex_ai, aws_bedrock, sagemaker, cohere, ollama — design decision 4
- [x] 1.2 Add aggregator entries `langchain4j` (`dev.langchain4j`) and `spring_ai` (`org.springframework.ai`) to providers.json + `unknown` blocs in sovereignty.json — design decisions 4-5

## 2. Engine

- [x] 2.1 kb.py: build the `jvm` match table from the optional key (same pattern as `npm`); `match_jvm()` with dot-boundary longest-prefix matching — spec: Detect AI SDK usage in Java and Kotlin (dot-boundary scenario)
- [x] 2.2 detect.py: `JVM_EXT = {".java", ".kt", ".kts"}`, `_scan_jvm()` regex over plain/static imports, dispatch branch mirroring JS (`_scan_jvm + _scan_text + _scan_api_calls + cfg`) — spec: both requirements

## 3. Tests

- [x] 3.1 Java fixture: `com.openai` import detected (us); dot-boundary negative (`com.openaiutils`); `import static` form — spec: Detect AI SDK usage in Java and Kotlin
- [x] 3.2 Kotlin fixture: `com.anthropic` import (no semicolon) detected; langchain4j import resolves aggregator/unknown — spec: Java/Kotlin + aggregator scenarios
- [x] 3.3 Parity: endpoint literal in a `.java` file detected; `// borderlint: allow` waiver honored on a flagged Java line — spec: JVM sources receive full flow scanning
- [x] 3.4 Full suite green

## 4. Docs

- [x] 4.1 README: languages line + capabilities bullet gain Java/Kotlin; CAPABILITIES.md: add a shipped Java/Kotlin row to the §5.A language table; CONTRIBUTING.md: document the `jvm` KB key — proposal Impact
