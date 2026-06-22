## Context

borderlint's detection engine already resolves any provider in the KB from an SDK import or an
endpoint host. Vector DBaaS fits that model with no engine change — it needs KB entries plus a way
to distinguish a storage sink from an inference call in reports. The inference-provider additions
are pure KB data surfaced by the last drift review.

## Goals / Non-Goals

**Goals:**
- Flag managed vector DBaaS (Pinecone, Weaviate Cloud, Qdrant Cloud, Zilliz/Milvus) and govern it.
- Make a vector store visibly distinct from an inference API in text/JSON/SBOM output.
- Add the surfaced inference providers with honest jurisdictions.

**Non-Goals:**
- Per-cluster region resolution; self-hosted/embedded store detection; new policy semantics.

## Decisions

- **`category` resolved at report time, not stored on `Detection`.** `KB.category(pid)` reads the
  field from the provider entry (default `inference`); `detect.py` and the `Detection` dataclass are
  untouched. Alternative — add `category` to every `Detection` — rejected: needless churn through the
  scanners when the KB already owns provider metadata.
- **Vector-store default jurisdiction `unknown`.** The cluster region is chosen at deployment and is
  not reliably in the host; `unknown` is the honest answer and lets `on_unknown` govern it — same
  pattern as Azure/Bedrock. Endpoint resolution can still refine it if a host carries a region.
- **SDK import flags the dependency even if self-hosted.** A `qdrant_client`/`pymilvus` import
  resolves to `unknown`; a loopback endpoint is separately detected as `local`. Consistent with how
  borderlint treats region-in-endpoint providers — surfaced, not hidden.
- **Jurisdictions for new inference providers** (confidence in commit/PR): `cerebras`, `fireworks_ai`,
  `deepinfra`, `baseten` → `us` (single US-served API); `fal_ai`, `friendliai` → `us` (serverless
  endpoint US-served; lower confidence); `databricks` → `unknown` (model serving region = workspace
  cloud region). Jurisdictions are human-assigned and easily corrected later.

## Risks / Trade-offs

- [A self-hosted vector store SDK import resolves to `unknown` and may warn/fail] → expected; pair
  with a loopback endpoint (→ `local`) or an inline waiver, same as any unknown flow.
- [A new inference provider's jurisdiction is wrong] → it's KB data, one-line fix; confidence noted
  so a maintainer can correct without re-deriving.

## Migration Plan

Additive. New KB entries + a `category` method + report formatting. No data migration; existing
SBOMs without `category` still diff (the field is additive and absent-tolerant).
