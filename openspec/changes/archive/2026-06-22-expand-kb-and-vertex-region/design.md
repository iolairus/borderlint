## Context

The detection engine resolves any KB provider from an SDK import or endpoint host, so most adds are
pure data. Vertex AI is the exception: like AWS/Azure, its region lives in the host, needing a third
region resolver. All jurisdictions here were web-verified (see issue #18 review).

## Goals / Non-Goals

**Goals:** add the verified, in-scope providers; resolve Vertex region from the host; keep `unknown`
honest for region-selectable clouds.
**Non-Goals:** guessing a region the host doesn't carry; adding out-of-scope/alias drift entries.

## Decisions

- **`gcp` region scheme mirrors `aws`/`azure`.** `_GCP_RE` captures `<region>-aiplatform.googleapis.com`
  (e.g. `europe-west4`, `asia-east2`, `northamerica-northeast1`); `_GCP_MULTI_RE` handles
  `aiplatform.<us|eu>.rep.googleapis.com`; the global `aiplatform.googleapis.com` matches the KB
  endpoint but yields no region → falls back to the entry default `unknown`. Same pattern as Bedrock.
- **Move `@ai-sdk/google-vertex` from `google_gemini` to `vertex_ai`.** That package is Vertex, not
  the consumer Gemini API; leaving it on `google_gemini` would mis-resolve Vertex usage and duplicate
  the npm key. `google_gemini` keeps `@ai-sdk/google` (consumer).
- **MiniMax / Z.ai split endpoints.** `endpoint_jurisdictions` overrides per host: `api.minimaxi.com`
  → `cn`, `api.minimax.io` → `unknown` (intl DC undocumented; refuse to guess `sg`). `z.ai` added to
  `zhipu` as `cn` (Z.ai cloud API is subject to Chinese law per its own docs).
- **Region-selectable clouds → `unknown`.** `nebius`/`novita` pick region per deployment with no host
  signal; `nvidia_nim` is commonly self-hosted — default `unknown`, with the hosted
  `integrate.api.nvidia.com` overridden to `us`. Honest, and `on_unknown: fail` still governs them.
- **`ollama` → `local`.** Local-first inference server; consistent with treating loopback as `local`.

## Risks / Trade-offs

- [A jurisdiction is wrong] → KB data, one-line fix; all values web-verified with sources, lower-
  confidence ones (`nebius`, `novita`, `nvidia_nim`) deliberately set to `unknown` rather than guessed.
- [GCP region list drifts as Google adds regions] → unknown regions return `None` → entry default
  `unknown` (fails safe), same as the AWS/Azure maps; add new regions as needed.

## Migration Plan

Additive. New KB entries + one resolver + display names. No data migration; output format unchanged.
