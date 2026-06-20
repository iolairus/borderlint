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

