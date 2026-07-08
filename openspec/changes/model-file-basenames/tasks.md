## 1. Matcher

- [ ] 1.1 Extend the basename rule in `normalize_model` to (`.gguf`, `.onnx`, `.safetensors`); update the `.gguf`-specific comment and `match_model` docstring (D1, "Local model identifiers resolve provenance")

## 2. Tests

- [ ] 2.1 `models/clip-vit-b-32.onnx`→us, `weights/qwen2.5-vl-3b.safetensors`→cn; `dir/qwen2.5.zip` does not basename-match; gguf behavior unchanged

## 3. Validation

- [ ] 3.1 Full suite + `openspec validate model-file-basenames --strict`
