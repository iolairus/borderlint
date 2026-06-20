## ADDED Requirements

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
