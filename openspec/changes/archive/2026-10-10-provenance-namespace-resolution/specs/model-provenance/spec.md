# model-provenance Delta

## MODIFIED Requirements

### Requirement: Local model identifiers resolve provenance
The system SHALL resolve provenance for the identifier forms used by local LLM tooling:
(1) a redistributor-qualified identifier — a quantizer or community-conversion org (GGUF/MLX
hubs) followed by a model name — SHALL resolve by disregarding the redistributor org and
matching the remaining model name against the family prefixes, because the redistributor carries
no provenance; (2) a model-file reference ending in a model-file
extension (`.gguf`, `.onnx`, `.safetensors`) SHALL match by its file basename, ignoring
directory components; (3) bare local-runtime model names (e.g. Ollama tags) SHALL be
covered by the family prefixes; (4) a leading namespace segment that carries no provenance of its
own SHALL likewise be disregarded, namely a **host-like** segment (one containing a dot — a registry
or mirror host) and a curated local-runtime launcher name (`ollama/`, `vllm/`, `lmstudio/`), because
such a segment names where the weights were pulled from, not who developed them. Candidate forms SHALL
be tried most-qualified first, so an identifier that already resolves continues to resolve unchanged.
Once at least one host-like segment has been disregarded the reference is demonstrably an image or
registry path, and the final segment alone SHALL also be tried. An arbitrary leading segment that is
neither host-like nor a curated launcher name SHALL NOT be disregarded. Tool-name prefixes that merely
resemble a model family SHALL NOT match.

Two consequences of that fallback are accepted and recorded in the change's design (Risks, R1/R2) rather
than hidden: an internal reference whose final segment merely *begins* with a family prefix acquires that
family's provenance, and a URL that carries its scheme resolves nothing at all.

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

#### Scenario: A runtime-qualified identifier resolves by its model name
- **WHEN** flows carry the model references `ollama/deepseek-r1`, `vllm/deepseek-r1` and
  `lmstudio/qwen2.5-7b-instruct`
- **THEN** all three resolve to bloc `cn` with developer organisations DeepSeek, DeepSeek and Alibaba
  respectively

#### Scenario: A registry-host-qualified identifier resolves by its model name
- **WHEN** flows carry the model references `mirror.internal/deepseek-r1` and
  `huggingface.co/TheBloke/deepseek-coder-33B-AWQ`
- **THEN** both resolve to bloc `cn` with organisation DeepSeek, the second reaching the family name
  only after the host segment and then the redistributor org are disregarded

#### Scenario: A multi-segment image reference resolves by its final segment
- **WHEN** a flow carries the model reference `docker.io/library/llama3:8b`
- **THEN** its provenance resolves to `us` with organisation Meta

#### Scenario: An unqualified path segment is not disregarded
- **WHEN** a scanned file contains the string literal `src/deepseek/client.py`
- **THEN** no model reference is detected, because `src` is neither host-like nor a curated launcher name

#### Scenario: A near-miss internal image name stays unmatched
- **WHEN** flows carry the model references `docker.io/library/sonarqube`,
  `registry.corp/ml/internal-router` and `gcr.io/my-project/deploy-tool`
- **THEN** none of them resolves to a bloc, pinning the boundary of the final-segment fallback: dropping
  the host must still leave a segment that starts with a known family prefix

#### Scenario: An internal name beginning with a family prefix acquires that provenance (accepted)
- **WHEN** a flow carries the model reference `registry.corp/ml/mistral-serving`
- **THEN** it resolves to `eu` with organisation Mistral AI, and the finding's evidence is the original
  literal rather than the stripped form, so the attribution is auditable (design R1)

#### Scenario: A URL carrying its scheme resolves nothing (documented limit)
- **WHEN** a scanned file contains the string literal `https://huggingface.co/TheBloke/deepseek-coder-33B-AWQ`
- **THEN** no model reference is detected, because `https:` is not host-like so no segment is ever
  disregarded; the scheme-less `huggingface.co/…` form is the one that resolves (design R2)
