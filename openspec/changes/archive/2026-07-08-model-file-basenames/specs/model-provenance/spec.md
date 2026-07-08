## MODIFIED Requirements

### Requirement: Local model identifiers resolve provenance
The system SHALL resolve provenance for the identifier forms used by local LLM tooling:
(1) a redistributor-qualified identifier — a quantizer or community-conversion org (GGUF/MLX
hubs) followed by a model name — SHALL resolve by disregarding the redistributor org and
matching the remaining model name against the family prefixes, because the redistributor carries
no provenance; (2) a model-file reference ending in a model-file
extension (`.gguf`, `.onnx`, `.safetensors`) SHALL match by its file basename, ignoring
directory components; (3) bare local-runtime model names (e.g. Ollama tags) SHALL be
covered by the family prefixes. Tool-name prefixes that merely resemble a model family SHALL NOT
match.

#### Scenario: An MLX community identifier resolves by its model name
- **WHEN** a flow carries the model reference `mlx-community/Qwen2.5-7B-Instruct-4bit`
- **THEN** its provenance resolves to `cn`

#### Scenario: A GGUF file path resolves by its basename
- **WHEN** a flow carries the model reference `models/qwen2.5-7b-instruct-q4_k_m.gguf`
- **THEN** its provenance resolves to `cn`

#### Scenario: A bare local-runtime tag resolves
- **WHEN** a flow carries the model reference `llama3.2`
- **THEN** its provenance resolves to `us`

#### Scenario: A tool name resembling a model family is not matched
- **WHEN** a scanned file contains the string literal `llama_index` or `llama-cpp-python`
- **THEN** no model reference is detected

#### Scenario: An ONNX file path resolves by its basename
- **WHEN** a flow carries the model reference `models/clip-vit-b-32.onnx`
- **THEN** its provenance resolves to `us`

#### Scenario: A safetensors path resolves by its basename
- **WHEN** a flow carries the model reference `weights/qwen2.5-vl-3b.safetensors`
- **THEN** its provenance resolves to `cn`

#### Scenario: An unlisted extension gets no basename treatment
- **WHEN** a flow carries the model reference `dir/qwen2.5.zip`
- **THEN** no basename matching occurs and the whole path faces anchored matching, resolving nothing
