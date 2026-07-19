# add-csharp-detection — design

## Context

Detection dispatches per file suffix in `scan()` (`detect.py:284-303`): JVM sources were added as a branch identical in shape to JS (`_scan_jvm + _scan_text + _scan_api_calls + cfg`). The KB carries per-language package keys (`sdks`, `npm`, `jvm`) built into match tables in `kb.py:202-217`; optional per-provider keys are the established extension mechanism, and `match_jvm()` already implements dot-boundary longest-prefix matching — the exact semantics .NET namespaces need. Aggregators are modeled as providers with `category: aggregator` and `unknown` jurisdiction/sovereignty (litellm, langchain, langchain4j, spring_ai).

## Goals / Non-Goals

**Goals:**
- C# `using`-directive detection resolved through the same KB, with full parity for the non-import scanners (endpoints, api calls, config keys, waivers, model binding).
- KB entries only for .NET SDKs that verifiably exist, curated conservatively and confirmed against the actual NuGet packages during real-world validation.

**Non-Goals:**
- Project-file scanning (`.csproj`/`packages.config`) — declared dependencies are not flows. VB.NET, F#, Razor. IL/assembly analysis.

## Decisions

1. **Regex scanner `_scan_cs()`, mirroring `_scan_jvm`**: one pattern over
   `^(global )?using (static )?(Alias = )?<Dotted.Namespace>;` lines covers the four import forms.
   For the alias form the right-hand side is captured (the alias name is irrelevant to provider
   resolution). `using` *statements/declarations* (`using var x = …`, `using (var x = …)`) fail the
   namespace capture or resolve to no provider — harmless by construction.
   *Alternative:* Roslyn or a C# parser dependency — rejected: zero-dependency constraint, and
   `using` directives are line-regular.
2. **New optional per-provider KB key `dotnet`** (list of namespace prefixes), built into a match
   table like `jvm`; `match_dotnet()` reuses the dot-boundary longest-prefix semantics of
   `match_jvm` (`OpenAI` matches `OpenAI.Chat`, not `OpenAIUtils`). Matching is case-sensitive —
   .NET namespaces are Pascal-cased and case-significant.
3. **Dispatch branch identical in shape to JVM**: `_scan_cs + _scan_text + _scan_api_calls + cfg`,
   so endpoint literals, OpenAI-compatible calls, config keys, waivers (C# comments are `//`,
   which `_waivers` already handles), and `_attach_models` all apply with no new code.
4. **Curation set (v1)**, official or de-facto SDK namespaces, verified against the published
   NuGet packages during implementation (2026-07-19):
   OpenAI (`OpenAI` — official openai-dotnet), Azure OpenAI (`Azure.AI.OpenAI`),
   Anthropic (`Anthropic` — official anthropic-sdk-csharp, NuGet `Anthropic` 12.x; the prefix also
   dot-boundary covers the community `Anthropic.SDK` namespace, so one prefix serves both),
   AWS Bedrock (`Amazon.BedrockRuntime`, `Amazon.Bedrock`), SageMaker (`Amazon.SageMakerRuntime`),
   Vertex AI (`Google.Cloud.AIPlatform`), Google Gemini (`Google.GenAI` — official
   googleapis/dotnet-genai — plus `Mscc.GenerativeAI`, the established community SDK),
   Ollama (`OllamaSharp`) — plus new aggregator entries **semantic_kernel**
   (`Microsoft.SemanticKernel`) and **microsoft_extensions_ai** (`Microsoft.Extensions.AI`),
   modeled on langchain4j/spring_ai (`unknown`/`unknown`, runtime-routed). Cohere and Mistral have
   no confident .NET namespace — left to the weekly KB drift process. Every namespace above is
   verified against the published NuGet package during task 4 before merge.
5. **Two aggregator ids rather than one** — Microsoft.Extensions.AI is the vendor-neutral
   abstraction layer Semantic Kernel itself builds on; different NuGet, different namespace,
   different signal. Folding them would misreport the provider name in findings (the langchain4j
   vs spring_ai precedent).

## Risks / Trade-offs

- [`Amazon.Bedrock` vs `Amazon.BedrockRuntime` are **sibling** namespaces, unlike the JVM case
  where `bedrockruntime` was a dot-child] → both prefixes listed explicitly; dot-boundary matching
  means neither implies the other. Tests pin this.
- [`using` declarations (`using var client = …`) syntactically resemble directives] → the capture
  lands on `var` or fails at the parenthesis; `var` matches no KB prefix. Test pins the negative.
- [Community SDK namespaces (Anthropic.SDK, Mscc.GenerativeAI, OllamaSharp) can churn] → the
  weekly KB drift check owns ongoing accuracy; v1 entries are verified at merge time.
- [Top-level `OpenAI` prefix is a single bare identifier] → dot-boundary matching still requires
  `OpenAI` or `OpenAI.<x>` exactly; `OpenAIUtils` cannot match.

## Open Questions

None.
