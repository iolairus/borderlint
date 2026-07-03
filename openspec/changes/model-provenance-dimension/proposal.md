## Why

borderlint models **residency** (where the bytes rest) and **sovereignty** (who can compel
disclosure from the serving provider) — but neither says **whose model weights** a flow runs. A
flow to AWS Bedrock `ap-east-1` serving DeepSeek-R1 is residency `hk`, sovereignty `us`, yet the
weights are PRC-origin; a self-hosted Qwen via Ollama is residency and sovereignty `local` with
the same `cn` provenance. Regulator expectations (HKMA GenAI guidance, OGCIO framework, CAC
filings) and sector rules on model origin make this a third governance axis a policy must be able
to express. This was explicitly deferred in `sovereignty-dimension`'s non-goals; this change
un-defers it.

## What Changes

- Introduce a **provenance** attribute on each detected flow: the bloc of the legal regime under
  which the model's developer operates, derived from **model references** found statically in
  code (model ID strings, Bedrock model IDs, aggregator-qualified IDs, hub repo IDs).
- Add a bundled **model provenance map**: model-ID pattern → developer org → bloc, reusing the
  sovereignty bloc vocabulary (`us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`, `ca`, `unknown`).
- Add a **`model_reference` detection kind**. A model reference binds to a provider detection in
  the same file; otherwise it stands alone. Flows with no model reference carry provenance
  `unknown`.
- Extend the policy schema with an optional **`provenance` block** mirroring `sovereignty`:
  per-classification allow-lists, `on_unknown`, inclusion in `fail_on`. Opt-in and non-breaking;
  `on_unknown: "fail"` gates on its own (symmetric with residency and sovereignty).
- Surface provenance in all report formats (text column, JSON field, Mermaid label, SARIF
  message, SBOM `provenances`), never replacing residency or sovereignty.

## Capabilities

### New Capabilities
- `model-provenance`: model whose weights a flow runs — map model references to the developer's
  bloc, orthogonal to residency and sovereignty; evaluate against an optional per-classification
  provenance allow-list.

### Modified Capabilities
- `flow-detection`: new `model_reference` detection kind; same-file binding of model references
  to provider detections; detections carry a provenance value.
- `residency-policy`: policy schema gains an optional `provenance` block; evaluation produces
  `provenance` / `provenance_unknown` reasons; `fail_on` accepts `provenance`.
- `cli-and-reporting`: all report formats surface the provenance bloc per flow; no new required
  CLI flags (policy-driven).

## Non-goals

- **Not adjudicating export-control applicability.** The map surfaces weight origin; the policy
  decides. No opinion on whether a control regime legally applies.
- **Not derivative-weights genealogy.** Fine-tunes and distillations inherit the base family's
  bloc; lineage tracing (Qwen-distilled-into-Llama) is out of scope.
- **Not runtime model resolution.** Model IDs passed through variables or environment resolve to
  `unknown` — a first-class, policy-governable answer.
- **Not training-data provenance.** Weights origin only; dataset origin is a different problem.
- **No breaking changes.** Absent the policy block, behaviour is identical to today.

## Impact

- `borderlint/data/`: new `provenance.json` (model-ID pattern → bloc, with `updated` date per
  kb-freshness convention).
- `borderlint/detect.py`, `borderlint/kb.py`, `borderlint/policy.py`, `borderlint/report.py`:
  detect, resolve, evaluate, and render the new dimension.
- `tests/test_borderlint.py`: resolution, binding, evaluation, `fail_on`, waiver, and reporting
  cases.
- `examples/residency.json`, `CAPABILITIES.md`, `README.md`: annotated example and docs.
