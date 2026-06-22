## Why

A residency tool must catch where data comes to **rest**, not only where requests go. Managed
vector databases (Pinecone, Weaviate Cloud, Qdrant Cloud, Zilliz/Milvus) store embeddings of your
data in a cloud region — a cross-border storage flow borderlint currently ignores (A5). Separately,
the latest KB review surfaced mainstream inference providers we do not yet cover.

## What Changes

- **Detect managed vector databases (A5):** add their SDKs/endpoints to the KB so borderlint flags
  them and resolves their jurisdiction like any provider. Because a vector cluster's region is
  chosen per-deployment, the default jurisdiction is `unknown` (refined when the endpoint host is
  seen), consistent with how Azure/Bedrock are handled.
- **Provider `category`:** add an optional KB field (`inference` default | `vector_store`) so reports
  distinguish a data-at-rest sink from an inference API. Surfaced in text, JSON, and SBOM output.
- **Expand inference coverage:** add `cerebras`, `fireworks_ai`, `deepinfra`, `fal_ai`, `baseten`,
  `friendliai` (→ `us`), and `databricks` (→ `unknown`, workspace-region dependent).
- No change to policy evaluation — a vector-store flow gates on residency exactly like any flow.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `flow-detection`: detect managed vector-database (data-sink) usage and carry a provider category.
- `cli-and-reporting`: distinguish a provider's category (inference vs. vector store) in output.

## Impact

- KB data: new entries in `borderlint/data/providers.json` (4 vector stores + 7 inference providers),
  optional `category` field.
- Code: `kb.category()`; report renderers surface the category. No change to `detect.py`/`policy.py`.
- Docs: `CONTRIBUTING.md` schema gains `category`; `CAPABILITIES.md` A5 → ✅; README notes vector stores.

## Non-goals

- No per-region resolution of a vector cluster from its host (region is runtime/config — `unknown`).
- Not detecting self-hosted/embedded stores (e.g. local Chroma); only managed DBaaS endpoints/SDKs.
- No new policy semantics or a separate "storage" failure type — residency is residency.
