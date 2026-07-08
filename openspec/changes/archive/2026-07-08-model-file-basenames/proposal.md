## Why

Only `.gguf` paths match by basename, so an ONNX or safetensors path whose basename names its
family — `models/clip-vit-b-32.onnx`, `weights/qwen2.5-vl-3b.safetensors` — is invisible to
provenance while the identical GGUF path resolves: the llama.cpp ecosystem got the treatment
while the ONNX and HF-native formats did not, for no principled reason. (memorybox's
`clip_text_encoder.onnx` needs this rule *and* a pattern — the rule is the reusable half.)

## What Changes

- The basename rule extends from `.gguf` to a curated model-file extension set: `.gguf`,
  `.onnx`, `.safetensors`. Directory components are ignored; the basename faces the same
  anchored prefix matching as any identifier.
- Nothing else changes: no new patterns, no charset changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `model-provenance`: the local-model-identifiers requirement covers the extension set.

## Impact

- `borderlint/kb.py` — one tuple in `normalize_model`.
- `tests/` — onnx and safetensors basenames resolve; a path with an unlisted extension does not.
- `deny_models` inherits the coverage automatically (it reuses the same normalization) — the
  residency-policy spec already words it generically; no delta needed there.

## Non-goals

- No `.pt`/`.bin` (pickle-era names are too generic to anchor honestly); the set can grow by
  evidence.
