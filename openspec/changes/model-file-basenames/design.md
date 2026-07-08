## Context

`normalize_model` (`kb.py`) basenames only `low.endswith(".gguf")` before prefix matching; the
design that shipped it (D7, model-provenance-dimension) reasoned "file paths defeat
start-anchoring" — true of every model-file format, not just GGUF.

## Goals / Non-Goals

**Goals:** ONNX and safetensors paths resolve like GGUF ones.
**Non-Goals:** generic checkpoint extensions (`.pt`, `.bin`); archive formats.

## Decisions

### D1 — A curated extension tuple, same basename rule
**Decision:** `endswith((".gguf", ".onnx", ".safetensors"))` → basename; everything downstream
unchanged.
**Rationale:** All three are unambiguous model-artifact extensions; the basename still faces
anchored prefix matching, so a `random.onnx` resolves nothing.
**Alternatives rejected:**
- *`.pt`/`.pth`/`.bin`.* Rejected: generic serialization names (`model.bin`, `best.pt`) carry
  no family signal and invite noise for zero resolution gain.
- *Basename every slash-containing literal.* Rejected: destroys org-prefix matching
  (`Qwen/Qwen2.5` must match on the org, not the basename).

## Risks / Trade-offs

- **[Versioned model-file paths]** `dir/qwen2.5@2407.onnx` — the version-pin strip runs first
  and swallows the extension, skipping the basename step; identical to the documented GGUF
  behaviour, inherited knowingly.
- **[Sharded checkpoints]** `model-00001-of-00004.safetensors` basenames carry no family and
  resolve nothing — same honest `unknown` as today.

## Migration Plan

1. Extend the tuple; tests. Rollback: revert.

## Open Questions

None.
