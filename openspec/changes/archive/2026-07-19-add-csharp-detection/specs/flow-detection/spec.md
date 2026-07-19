# flow-detection — delta for add-csharp-detection

## ADDED Requirements

### Requirement: Detect AI SDK usage in C#
The system SHALL detect `using` directives referencing known AI SDK namespaces in C# source
files — covering plain, `global`, `static`, and alias forms — and record each as a detection
identifying the provider. Namespace matching SHALL be case-sensitive and prefix-based on dot
boundaries, so a directive deeper in a known namespace resolves to that provider while an
unrelated namespace sharing a leading substring does not.

#### Scenario: Plain using directive
- **WHEN** a C# file contains `using OpenAI.Chat;` and `OpenAI` is a known SDK namespace prefix
- **THEN** a detection is recorded identifying that provider

#### Scenario: Global and static forms
- **WHEN** a C# file contains `global using Azure.AI.OpenAI;` or `using static Anthropic.SDK.Constants;`
- **THEN** a detection is recorded identifying the respective provider

#### Scenario: Alias form resolves the right-hand side
- **WHEN** a C# file contains `using Client = OpenAI.Chat.ChatClient;`
- **THEN** the detection resolves from the aliased namespace, not the alias name

#### Scenario: Aggregator using directive
- **WHEN** a C# file contains `using Microsoft.SemanticKernel;`
- **THEN** a detection is recorded for that aggregator with an `unknown` jurisdiction

#### Scenario: Dot-boundary matching
- **WHEN** a C# file contains `using OpenAIUtils.Helpers;` against the known prefix `OpenAI`
- **THEN** no detection is recorded for that provider

#### Scenario: Using declaration is not a directive
- **WHEN** a C# file contains a `using` declaration or statement (for example `using var client = new HttpClient();`)
- **THEN** no SDK detection is recorded from that line

### Requirement: C# sources receive full flow scanning
C# source files SHALL receive the same non-import scanning as other supported languages:
endpoint-reference literals, OpenAI-compatible API call paths, configuration-endpoint keys,
inline waiver annotations, and model-reference binding.

#### Scenario: Endpoint literal in a C# file
- **WHEN** a C# file contains a known provider endpoint host in a string literal
- **THEN** an endpoint-reference detection is recorded for that provider

#### Scenario: Waiver in a C# file
- **WHEN** a flagged line in a C# file carries an inline `// borderlint: allow <reason>` waiver
- **THEN** the finding is reported as waived with its justification

#### Scenario: OpenAI-compatible call path in a C# file
- **WHEN** a C# file references an OpenAI-compatible API path (for example `$"{baseUrl}/v1/chat/completions"`) against a runtime-configured host
- **THEN** an api-call detection is recorded with an `unknown` jurisdiction

#### Scenario: Model reference binds in a C# file
- **WHEN** a C# file contains a known model identifier alongside a provider detection
- **THEN** the flow's provenance resolves from that model reference

## MODIFIED Requirements

### Requirement: Detect OpenAI-compatible API calls
The system SHALL detect an OpenAI-compatible API call in any supported source language by its
request-path signature — `/v1/chat/completions`, `/v1/completions`, `/v1/responses`, or
`/v1/embeddings` — even when the host is supplied at runtime, and record a detection. The system SHALL
resolve the jurisdiction from a static host in the **same string literal** (a single quoted or
template-literal token on one source line) as the path: a loopback host as `local`, and a known
provider host to that provider's jurisdiction. When the host is dynamic (a variable or interpolation),
supplied outside that literal, or absent (a relative path), the system SHALL record the
`custom_endpoint` pseudo-provider with jurisdiction `unknown`. The system SHALL NOT flag a `/v1/` path
outside this signature, and SHALL NOT record a duplicate detection for a flow already detected on the
same line — at most one detection per provider and jurisdiction per line.

#### Scenario: Call to a runtime-configured endpoint is unknown
- **WHEN** source contains `fetch(`${LLAMA_URL}/v1/chat/completions`)` with a host supplied at runtime
- **THEN** a detection is recorded with the `custom_endpoint` provider and jurisdiction `unknown`

#### Scenario: A host outside the path's literal is unknown
- **WHEN** the host is concatenated from a separate variable, for example `base + "/v1/chat/completions"`
- **THEN** a detection is recorded with jurisdiction `unknown`

#### Scenario: Call to a static loopback endpoint is local
- **WHEN** source contains a call to `http://localhost:8080/v1/chat/completions`
- **THEN** a detection is recorded with jurisdiction `local`

#### Scenario: A static known-provider endpoint is identified once
- **WHEN** source contains a call to `https://api.openai.com/v1/chat/completions`
- **THEN** exactly one detection identifies OpenAI with jurisdiction `us`, not duplicated by the path-signature detector

#### Scenario: A non-AI v1 path is not flagged
- **WHEN** source contains a path such as `/v1/users` or `/api/v1/health`
- **THEN** no OpenAI-compatible call detection is recorded
