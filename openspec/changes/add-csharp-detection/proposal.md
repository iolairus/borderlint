# add-csharp-detection

## Why

The .NET estate is the other half of the enterprise story the JVM change told: banks, insurers, and government shops across borderlint's home markets run large C# codebases, and Microsoft's AI push (Semantic Kernel, Microsoft.Extensions.AI, Azure OpenAI) is landing AI flows in exactly those codebases. borderlint currently reads Python, JS/TS, and Java/Kotlin; C# is the largest remaining coverage gap by industry.

## What Changes

- **C# detection**: `.cs` and `.csx` sources are scanned for `using` directives (plain, `global`, `static`, and alias forms) and matched against a new per-provider `dotnet` knowledge-base key holding namespace prefixes.
- **Full scan parity**: C# sources flow through the same per-file pipeline as JS/TS and JVM — endpoint literals, OpenAI-compatible call paths, config-endpoint keys, inline waivers (`// borderlint: allow`), and model-reference binding all apply unchanged.
- **KB curation**: `dotnet` namespace prefixes for providers with official or de-facto .NET SDKs (OpenAI, Azure OpenAI, Anthropic, AWS Bedrock, SageMaker, Vertex AI, Google Gemini, Ollama), plus two new aggregator entries — **Semantic Kernel** (`Microsoft.SemanticKernel`) and **Microsoft.Extensions.AI** (`Microsoft.Extensions.AI`) — modeled like langchain4j/spring_ai (`unknown` jurisdiction and sovereignty, runtime-routed). A **Hugging Face** aggregator entry (previously absent from the KB entirely) covers `huggingface_hub`, `@huggingface/inference`, the de-facto .NET client, and the router/api-inference endpoints.
- README/CAPABILITIES updated (languages line; new shipped row A9 in the CAPABILITIES §5.A table).

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `flow-detection`: ADDED requirements for C# SDK-usage detection and for C# sources receiving the same endpoint/call-path/waiver scanning as other languages. MODIFIED the "Detect OpenAI-compatible API calls" requirement to say "any supported source language" instead of "Python or JavaScript/TypeScript" — the wording had already drifted behind the JVM change. (The existing aggregator requirement already covers "any supported language" — no modification needed.)

## Impact

- `borderlint/detect.py`: `CS_EXT` + `_scan_cs()` (regex over `using` directives, mirroring `_scan_jvm`), one new branch in the `scan()` suffix dispatch.
- `borderlint/kb.py`: build a `dotnet` match table from the new optional per-provider key (same pattern as `jvm`); `match_dotnet()` with dot-segment-aware longest-prefix matching.
- `borderlint/data/providers.json` (+`sovereignty.json`): `dotnet` keys on ~8 providers; two new aggregator entries.
- `tests/test_borderlint.py`: C# fixtures covering the `using` forms, aggregator resolution, endpoint-literal and waiver parity.
- `README.md` / `CAPABILITIES.md` / `CONTRIBUTING.md` (KB schema mention). Zero new dependencies.

## Non-goals

- **No project-file scanning** (`.csproj`, `packages.config`, `Directory.Packages.props`): a declared-but-unused dependency is not a flow — the house precedent across Python/JS/JVM is to key on imports.
- No VB.NET or F# (`open` directives differ syntactically; roadmap candidates if demand appears).
- No Razor/`.cshtml` scanning — C# embedded in markup is out of scope for the regex scanner.
- No C#-specific model-reference syntax — the existing language-agnostic model binding applies as-is.
