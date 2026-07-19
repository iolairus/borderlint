# add-csharp-detection — tasks

## 1. Knowledge base

- [x] 1.1 Add `dotnet` namespace-prefix lists to providers.json for: openai, azure_openai, anthropic, aws_bedrock, sagemaker, vertex_ai, google_gemini, ollama — design decision 4
- [x] 1.2 Add aggregator entries `semantic_kernel` (`Microsoft.SemanticKernel`) and `microsoft_extensions_ai` (`Microsoft.Extensions.AI`) to providers.json + provider→`unknown` entries under `providers` in sovereignty.json — design decisions 4-5

## 2. Engine

- [x] 2.1 kb.py: build the `dotnet` match table from the optional key (same pattern as `jvm`); `match_dotnet()` with case-sensitive dot-boundary longest-prefix matching — spec: Detect AI SDK usage in C# (dot-boundary scenario)
- [x] 2.2 detect.py: `CS_EXT = {".cs", ".csx"}`, `_scan_cs()` regex over plain/global/static/alias `using` directives, dispatch branch mirroring JVM (`_scan_cs + _scan_text + _scan_api_calls + cfg`) — spec: both requirements

## 3. Tests

- [x] 3.1 C# fixture: `using OpenAI.Chat;` detected (us); dot-boundary negative (`OpenAIUtils`); `global using` and `using static` forms; alias form resolves the RHS — spec: Detect AI SDK usage in C#
- [x] 3.2 `using var client = …` declaration records no SDK detection; `Microsoft.SemanticKernel` resolves aggregator/unknown; `Amazon.Bedrock` and `Amazon.BedrockRuntime` each match only their own prefix — spec: using-declaration + aggregator scenarios, design risk 1
- [x] 3.3 Parity: endpoint literal in a `.cs` file detected; `// borderlint: allow` waiver honored on a flagged C# line; OpenAI-compatible call path against a runtime host (`$"{baseUrl}/v1/chat/completions"`) records `custom_endpoint`/`unknown` — spec: C# sources receive full flow scanning + MODIFIED Detect OpenAI-compatible API calls
- [x] 3.4 Full suite green

## 4. Real-world validation (before merge)

- [x] 4.1 Verify every KB namespace against its published NuGet package (openai-dotnet, Azure.AI.OpenAI, Anthropic.SDK, AWSSDK.Bedrock*, Google.Cloud.AIPlatform.V1, Mscc.GenerativeAI, OllamaSharp, Microsoft.SemanticKernel, Microsoft.Extensions.AI), AND explicitly confirm presence/absence of official Anthropic and Google GenAI .NET packages — if an official SDK exists, add its namespace alongside the community one — design decision 4
- [x] 4.2 Run the scanner against at least two real OSS C# codebases with direct provider integrations (e.g. an Azure OpenAI sample repo, a Semantic Kernel consumer); fix what the real code exposes before merge

## 5. Docs

- [x] 5.1 README: languages line + capabilities bullet gain C#; CAPABILITIES.md: add shipped row A9 to the §5.A language table; CONTRIBUTING.md: document the `dotnet` KB key and add it to the "At least one of `sdks`, `npm`, `jvm`, or `endpoints`" line — proposal Impact
