## 1. KB data

- [x] 1.1 Add 4 managed vector-store entries to `providers.json` with `"category": "vector_store"`,
      jurisdiction `unknown`: pinecone, weaviate, qdrant, zilliz_milvus (SDKs + npm + endpoints).
- [x] 1.2 Add 7 inference providers: cerebras, fireworks_ai, deepinfra, fal_ai, baseten, friendliai
      (→ `us`), databricks (→ `unknown`), with SDKs/npm/endpoints.

## 2. Category surfacing

- [x] 2.1 Add `KB.category(pid)` (default `inference`) in `kb.py`.
- [x] 2.2 `report.text`: annotate vector-store providers (e.g. `(vector store)`).
- [x] 2.3 `report.as_json` and `report.sbom`: include a `category` field per finding/component.

## 3. Tests

- [x] 3.1 Vector-store SDK import → detected, category `vector_store`, jurisdiction `unknown`.
- [x] 3.2 A new inference provider resolves (e.g. `cerebras` → `us`).
- [x] 3.3 Text shows `(vector store)`; JSON/SBOM carry `category`; verdict unchanged.

## 4. Docs & validation

- [x] 4.1 `CONTRIBUTING.md`: document the `category` field; CAPABILITIES A5 → ✅; README notes vector stores.
- [x] 4.2 `openspec validate vector-stores-and-providers --strict` passes; full pytest green.
