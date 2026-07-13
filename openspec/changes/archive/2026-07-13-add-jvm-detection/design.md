# add-jvm-detection — design

## Context

Detection dispatches per file suffix in `scan()` (`detect.py:267-288`): Python via AST, JS/TS via
regex import matching plus text/api-call/config scanners, plain text via the text scanners. The KB
already carries per-language package keys (`sdks` for Python, `npm` for JS) built into match
tables in `kb.py:202-215`; optional per-provider keys are the established extension mechanism.
Aggregators are modeled as providers with `category: aggregator` and `unknown`
jurisdiction/sovereignty (litellm, langchain, llama_index).

## Goals / Non-Goals

**Goals:**
- Java/Kotlin import detection resolved through the same KB, with full parity for the non-import
  scanners (endpoints, api calls, config keys, waivers, model binding).
- KB entries for the JVM SDKs that actually exist, curated conservatively (wrong jurisdiction
  facts are worse than missing ones).

**Non-Goals:**
- Build-file scanning (`pom.xml`/`build.gradle`) — a declared dependency is not a flow; imports
  are the signal, matching the Python/JS precedent exactly. Scala/Groovy. Bytecode analysis.

## Decisions

1. **Regex import scanner `_scan_jvm()`, mirroring `_scan_js`**: one pattern over
   `import (static )?<dotted.path>` lines covers both Java (trailing `;`) and Kotlin (none).
   *Alternative:* a Java parser dependency — rejected: zero-dependency constraint, and imports
   are line-regular in both languages.
2. **New optional per-provider KB key `jvm`** (list of import-package prefixes), built into a
   match table like the existing per-language tables; `match_jvm()` does longest-prefix matching
   **on dot boundaries** — the exact semantics `match_sdk` already implements (`kb.py:314-318`,
   `module == s or module.startswith(s + ".")`), NOT `match_npm`'s slash-boundary variant.
   (`com.openai` matches `com.openai.client.X`, not `com.openaiutils.X`.)
   *Alternative:* maven `group:artifact` coordinates — rejected with build-file scanning; import
   prefixes are what source files contain.
3. **Dispatch branch identical in shape to JS**: `_scan_jvm + _scan_text + _scan_api_calls + cfg`,
   so endpoint literals, OpenAI-compatible calls, config keys, waivers (`_waivers` is
   comment-syntax-agnostic), and `_attach_models` all apply with no new code.
4. **Curation set (v1)**: official or de-facto SDK packages, only where confident — OpenAI (`com.openai`),
   Anthropic (`com.anthropic`), Azure OpenAI (`com.azure.ai.openai`), Google Gemini
   (`com.google.genai`), Vertex AI (`com.google.cloud.vertexai`, `com.google.cloud.aiplatform`),
   AWS Bedrock (`software.amazon.awssdk.services.bedrockruntime`, `…services.bedrock`),
   SageMaker (`…services.sagemakerruntime`), Cohere (`com.cohere`), Ollama (`io.github.ollama4j`)
   — plus new aggregator entries **langchain4j** (`dev.langchain4j`) and **spring_ai**
   (`org.springframework.ai`) modeled on litellm/langchain (`unknown`/`unknown`, runtime-routed).
   The weekly KB drift process grows the set from here.
5. **Two new provider ids rather than folding LangChain4j into `langchain`** — different project,
   different maintainers; folding would misreport the provider name in findings.

## Risks / Trade-offs

- [Import prefix too broad (e.g. `software.amazon.awssdk.services.bedrock` also prefixes
  `bedrockruntime`)] → intended here (both are Bedrock); dot-boundary matching prevents the
  harmful cross-provider case; tests pin both directions.
- [Kotlin aliased imports (`import x.y as z`)] → the path before `as` is what's matched; alias is
  irrelevant to provider resolution.
- [JVM shops using only build-tool BOMs then wildcard imports (`import com.openai.*`)] → the
  wildcard line still carries the prefix; matched.

## Open Questions

None.
