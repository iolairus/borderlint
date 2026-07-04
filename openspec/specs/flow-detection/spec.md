# flow-detection Specification

## Purpose
TBD - created by archiving change mvp-residency-scanner. Update Purpose after archive.
## Requirements
### Requirement: Detect AI provider SDK usage
The system SHALL detect usage of known AI provider SDKs in a scanned codebase and record each as a
detection identifying the provider.

#### Scenario: Python source imports a provider SDK
- **WHEN** a Python source file imports a known provider SDK (for example `openai`)
- **THEN** a detection is recorded identifying that provider, with the source file and line number

### Requirement: Detect AI provider endpoint references
The system SHALL detect references to known AI provider endpoint hosts in source files and in
configuration/text files, and record each as a detection identifying the provider.

#### Scenario: Endpoint host appears in a source string
- **WHEN** a scanned file contains a known provider endpoint host (for example `api.deepseek.com`)
- **THEN** a detection is recorded identifying that provider, with the file and line number

#### Scenario: Endpoint host appears in a configuration file
- **WHEN** a configuration or text file (for example `.env`) contains a known provider endpoint host
- **THEN** a detection is recorded identifying that provider

### Requirement: Exclude non-source locations
The system SHALL exclude version-control, dependency, and build directories from scanning so that
vendored or generated code does not produce detections.

#### Scenario: Match inside an excluded directory
- **WHEN** a provider endpoint host appears in an excluded directory (for example `node_modules`)
- **THEN** no detection is recorded for that location

### Requirement: Record traceable evidence
Each detection SHALL record the provider, the matched evidence, the file path, and the line number.

#### Scenario: Detection carries file and line
- **WHEN** any detection is produced
- **THEN** it includes the provider, the matched evidence, the file path, and the line number

### Requirement: Resilient scanning
The system SHALL continue scanning the remaining files when an individual file cannot be parsed.

#### Scenario: A file fails to parse
- **WHEN** a file cannot be parsed during a scan
- **THEN** the scan continues and other files are still scanned

### Requirement: De-duplicate detections
The system SHALL report at most one detection for the same provider, evidence, file, and line.

#### Scenario: Same flow detected more than once
- **WHEN** the same provider would be detected more than once at the same file and line
- **THEN** only one detection is reported for it

### Requirement: Detect AI SDK usage in TypeScript and JavaScript
The system SHALL detect imports of known AI SDK packages in TypeScript and JavaScript source files —
covering `import`, `require`, and dynamic `import()` forms — and record each as a detection
identifying the provider.

#### Scenario: ES module import
- **WHEN** a TypeScript or JavaScript file imports a known AI SDK package (for example `import OpenAI from "openai"`)
- **THEN** a detection is recorded identifying that provider

#### Scenario: CommonJS require
- **WHEN** a JavaScript file requires a known AI SDK package (for example `require("@anthropic-ai/sdk")`)
- **THEN** a detection is recorded identifying that provider

#### Scenario: Dynamic import
- **WHEN** a TypeScript or JavaScript file dynamically imports a known AI SDK package (for example `await import("openai")`)
- **THEN** a detection is recorded identifying that provider

### Requirement: Detect multi-provider aggregator usage
The system SHALL detect usage of known multi-provider aggregator or router libraries (for example
litellm, langchain) in any supported language and record each as a flow.

#### Scenario: Aggregator import in Python
- **WHEN** a Python file imports a known aggregator library (for example `import litellm`)
- **THEN** a detection is recorded for that aggregator

#### Scenario: Aggregator import in JavaScript
- **WHEN** a JavaScript file imports a known aggregator package (for example `@langchain/openai`)
- **THEN** a detection is recorded for that aggregator

### Requirement: Detect AI endpoints declared in configuration
The system SHALL detect endpoints referenced by known AI-endpoint configuration keys (for example
`base_url`, `api_base`, `azure_endpoint`, `openai_api_base`, `endpoint`) in YAML, JSON, and TOML
files, and record each as a detection.

#### Scenario: Custom endpoint in a YAML config
- **WHEN** a YAML file contains `base_url: https://llm.acme.cn/v1`
- **THEN** a detection is recorded for that endpoint

#### Scenario: Known provider endpoint via a config key
- **WHEN** a JSON file contains `"api_base": "https://api.deepseek.com"`
- **THEN** a detection is recorded identifying DeepSeek

#### Scenario: A non-AI key is not flagged
- **WHEN** a config file sets a non-AI URL under a non-AI key (for example `database_url: https://db.example.com`)
- **THEN** no detection is recorded for it

### Requirement: Detect AI client endpoint overrides in code
The system SHALL detect an AI client endpoint override supplied in Python or JavaScript/TypeScript
code (for example a `base_url` argument) and record the referenced endpoint.

#### Scenario: base_url override in Python
- **WHEN** Python code constructs a client with `base_url="https://llm.acme.cn"`
- **THEN** a detection is recorded for that endpoint

### Requirement: Inline waiver annotations
The system SHALL recognise an inline waiver annotation — a `borderlint: allow` comment with a
justification — on the flagged line or the line immediately above it, and associate its
justification with every flow detected on that line.

#### Scenario: Waiver on the flagged line
- **WHEN** a detected flow's line contains a `borderlint: allow <reason>` comment
- **THEN** that flow is associated with the waiver and its justification `<reason>`

#### Scenario: Waiver on the preceding line
- **WHEN** the line immediately above a detected flow contains a `borderlint: allow <reason>` comment
- **THEN** that flow is associated with the waiver and its justification `<reason>`

#### Scenario: One waiver covers every flow on the line
- **WHEN** a single line carries more than one detected flow and a `borderlint: allow <reason>` comment
- **THEN** every flow detected on that line is associated with the waiver

### Requirement: Detect OpenAI-compatible API calls
The system SHALL detect an OpenAI-compatible API call in Python or JavaScript/TypeScript source by its
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

### Requirement: Detect managed vector-database usage

borderlint SHALL detect managed vector-database (vector DBaaS) usage — via the provider's SDK
import or its managed endpoint host — and treat it as an AI data flow subject to the residency
policy. Each such provider MUST carry the category `vector_store`. Because a vector cluster's
region is chosen per deployment, the default jurisdiction for a vector-store provider SHALL be
`unknown`, refined to a specific jurisdiction only when its endpoint host resolves one.

#### Scenario: Vector-store SDK import is detected
- **WHEN** Python source imports a managed vector-database SDK (e.g. `import pinecone`)
- **THEN** a detection is recorded for that provider with category `vector_store` and
  jurisdiction `unknown`

#### Scenario: Vector-store endpoint is detected
- **WHEN** a source or config file references a managed vector-database host (e.g. a
  `*.pinecone.io` URL)
- **THEN** a detection is recorded for that provider with category `vector_store`

#### Scenario: A vector-store flow is governed by the policy
- **WHEN** a vector-store detection resolves to `unknown` and the policy sets `on_unknown: fail`
- **THEN** the flow fails the build, exactly as any other unknown-jurisdiction flow would

### Requirement: Exclude oversized files

borderlint SHALL skip any file whose size exceeds a fixed threshold (5 MB) before reading it, so a
very large file is excluded from scanning rather than read into memory. Skipping an oversized file
MUST NOT fail the scan.

#### Scenario: An oversized file is skipped
- **WHEN** a file with a scanned extension exceeds the size threshold
- **THEN** it is excluded from detection and the scan continues without error

#### Scenario: A normal-sized file is still scanned
- **WHEN** a file is at or under the threshold
- **THEN** it is scanned as usual

### Requirement: Detect model references
The system SHALL detect model references in scanned source as a `model_reference` detection
kind, by matching string literals against the anchored model-identifier patterns of the
provenance map. Detection SHALL cover the same languages and file kinds as provider detection.
Matching SHALL be anchored to model-identifier shapes; the system SHALL NOT flag arbitrary
substrings that merely resemble model names.

#### Scenario: A model identifier string literal is detected
- **WHEN** a scanned Python file contains the string literal `"claude-sonnet-4-6"` as a model argument
- **THEN** a `model_reference` detection is recorded with the file, line, and the matched identifier as evidence

#### Scenario: A resembling variable name is not flagged
- **WHEN** a scanned file contains a variable named `gpt` with no model-identifier string literal
- **THEN** no `model_reference` detection is recorded

### Requirement: Model references bind to same-file provider detections
A `model_reference` detection SHALL bind to a provider detection in the same file when the
file's matched model references resolve to exactly one distinct provenance bloc, assigning that
bloc to the flow; when several same-bloc references bind, the first matched reference's
identifier SHALL be recorded as the flow's model identifier, representing its siblings. When a
file's model references resolve to more than one distinct bloc, binding would be ambiguous: no
binding SHALL occur and each reference SHALL stand alone. A `model_reference` with no provider
detection in its file SHALL stand alone as its own finding. Binding SHALL NOT cross file
boundaries.

#### Scenario: Model reference in the same file as a provider flow
- **WHEN** a file contains both a provider detection and a matching model reference
- **THEN** the provider flow carries the model reference's provenance and both evidences are traceable

#### Scenario: Ambiguous blocs do not bind
- **WHEN** a file contains a provider detection and model references resolving to two distinct blocs
- **THEN** the provider flow keeps its two-tier provenance and each reference is reported as its own standalone finding

#### Scenario: Standalone model reference
- **WHEN** a file contains a matching model reference but no provider detection
- **THEN** a standalone `model_reference` finding is reported with its resolved provenance

### Requirement: Detections carry a provenance value
Each detection SHALL carry a provenance bloc, defaulting to `unknown`, populated during scanning
from the two-tier provenance resolution.

#### Scenario: A detection with no model reference on a first-party provider
- **WHEN** a provider that serves only its own models is detected with no bound model reference
- **THEN** the detection's provenance is the provider organisation's bloc
