## 1. GCP region resolver (code)

- [x] 1.1 Add `_GCP_RE`, `_GCP_MULTI_RE`, and `_GCP_REGION` (GCP region → ccTLD) to `kb.py`, and a
      `gcp` branch in `_region_jurisdiction` (regional + `<us|eu>.rep` multi-region; global → None).

## 2. KB data

- [x] 2.1 Add `vertex_ai` (endpoints `aiplatform.googleapis.com`, `region_scheme: gcp`, default
      `unknown`); move `@ai-sdk/google-vertex` from `google_gemini` to it.
- [x] 2.2 Add CN/east: `volcengine` (cn), `minimax` (cn; `endpoint_jurisdictions` → `api.minimax.io`:
      unknown); extend `zhipu` endpoints with `z.ai`.
- [x] 2.3 Add new-jurisdiction: `gigachat` (ru), `sarvam` (in), `scaleway` (fr), `ovhcloud` (fr).
- [x] 2.4 Add US: `groq`, `together_ai`, `perplexity`, `xai`, `sambanova`, `replicate`, `anyscale`,
      `meta_llama`, `hyperbolic` (all us).
- [x] 2.5 Add region-selectable/unknown: `nebius`, `novita`, `nvidia_nim` (endpoint
      `integrate.api.nvidia.com` → us, default unknown); routers `openrouter`/`vercel_ai_gateway`
      (aggregator, unknown); `ollama` → local.

## 3. Reporting

- [x] 3.1 Extend `report.JURIS` with display names for new codes (`ru`, `in`, `fr`, `nl`, `de`, `be`,
      `ch`, `it`, `es`, `fi`, `pl`, `jp`, `kr`, `tw`, `au`, `ca`, `br`, `il`, `id`, …).

## 4. Tests & docs

- [x] 4.1 Tests: Vertex `asia-east2`→hk, `europe-west4`→nl, global→unknown; a new provider resolves
      (e.g. `gigachat`→ru, `scaleway`→fr); `api.minimax.io`→unknown vs `api.minimaxi.com`→cn.
- [x] 4.2 README provider list updated; CONTRIBUTING notes `region_scheme: gcp`.
- [x] 4.3 `openspec validate expand-kb-and-vertex-region --strict` passes; full pytest green.
