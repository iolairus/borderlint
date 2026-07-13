# flow-detection — delta for add-jvm-detection

## ADDED Requirements

### Requirement: Detect AI SDK usage in Java and Kotlin
The system SHALL detect imports of known AI SDK packages in Java and Kotlin source files —
covering plain and static import forms — and record each as a detection identifying the
provider. Package matching SHALL be prefix-based on dot boundaries, so an import deeper in a
known package resolves to that provider while an unrelated package sharing a leading substring
does not.

#### Scenario: Java import
- **WHEN** a Java file imports a known AI SDK package (for example `import com.openai.client.OpenAIClient;`)
- **THEN** a detection is recorded identifying that provider

#### Scenario: Kotlin import
- **WHEN** a Kotlin file imports a known AI SDK package (for example `import com.anthropic.client.AnthropicClient`)
- **THEN** a detection is recorded identifying that provider

#### Scenario: JVM aggregator import
- **WHEN** a Java or Kotlin file imports a known aggregator library (for example `dev.langchain4j.model.chat.ChatLanguageModel`)
- **THEN** a detection is recorded for that aggregator with an `unknown` jurisdiction

#### Scenario: Dot-boundary matching
- **WHEN** a Java file imports a package whose leading characters merely resemble a known prefix (for example `com.openaiutils.Foo` against the prefix `com.openai`)
- **THEN** no detection is recorded for that provider

### Requirement: JVM sources receive full flow scanning
Java and Kotlin source files SHALL receive the same non-import scanning as other supported
languages: endpoint-reference literals, OpenAI-compatible API call paths, configuration-endpoint
keys, inline waiver annotations, and model-reference binding.

#### Scenario: Endpoint literal in a Java file
- **WHEN** a Java file contains a known provider endpoint host in a string literal
- **THEN** an endpoint-reference detection is recorded for that provider

#### Scenario: Waiver in a Java file
- **WHEN** a flagged line in a Java file carries an inline `// borderlint: allow <reason>` waiver
- **THEN** the finding is reported as waived with its justification

#### Scenario: OpenAI-compatible call path in a Kotlin file
- **WHEN** a Kotlin file references an OpenAI-compatible API path (for example `/v1/chat/completions`) against a runtime-configured host
- **THEN** an api-call detection is recorded with an `unknown` jurisdiction

#### Scenario: Model reference binds in a Java file
- **WHEN** a Java file contains a known model identifier alongside a provider detection
- **THEN** the flow's provenance resolves from that model reference
