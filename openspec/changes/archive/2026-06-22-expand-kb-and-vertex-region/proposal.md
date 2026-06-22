## Why

The KB-drift review (issue #18) surfaced mainstream providers borderlint doesn't yet cover, several
of which change residency outcomes for east-west teams — Chinese (Volcengine, MiniMax, Z.ai),
Russian (GigaChat), Indian (Sarvam), and EU (Scaleway, OVHcloud) endpoints. Separately, **Google
Vertex AI** is a real gap: it's region-coded in the host (like Bedrock/Azure) but unresolved today.

## What Changes

- **Add researched providers** to the KB with verified jurisdictions: `volcengine`, `minimax`,
  `gigachat` (→ `ru`), `sarvam` (→ `in`), `scaleway`/`ovhcloud` (→ `fr`), `hyperbolic`, and the US
  platforms `groq`, `together_ai`, `perplexity`, `xai`, `sambanova`, `replicate`, `anyscale`,
  `meta_llama`. Extend the existing `zhipu` entry with the `z.ai` international host (→ `cn`).
- **Region-selectable providers → `unknown`** (honest, governed by `on_unknown`): `nebius`, `novita`,
  `nvidia_nim` (hosted host → `us`). Routers `openrouter`/`vercel_ai_gateway` → `unknown`; `ollama`
  → `local`.
- **MiniMax split endpoints:** `api.minimaxi.com` → `cn`; `api.minimax.io` (international, data
  location undocumented) → `unknown`.
- **Google Vertex AI region resolution (code):** a new `gcp` region scheme resolves
  `<region>-aiplatform.googleapis.com` → jurisdiction (e.g. `asia-east2` → `hk`, `europe-west4` →
  `nl`); the regionless global endpoint stays `unknown`.
- Extend the report's jurisdiction display-name map for the new codes (`ru`, `in`, `fr`, `nl`, …).

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `jurisdiction-classification`: resolve GCP (Vertex AI) region-coded endpoint hosts to a jurisdiction.

## Impact

- KB data: ~22 new entries + `zhipu`/`google_gemini` tweaks in `providers.json` (move
  `@ai-sdk/google-vertex` from `google_gemini` to the new `vertex_ai`).
- Code: `kb.py` gains a `gcp` resolver (`_GCP_RE`/`_GCP_REGION`); `report.py` gains display names.
- Docs: README provider list; CONTRIBUTING notes the `gcp` region scheme.

## Non-goals

- No per-call region inference where the host carries none (global Vertex endpoint, region-selectable
  clouds) — those stay `unknown` by design.
- Not adding out-of-scope drift entries (speech, image/video, search/scrape, infra) or providers
  already covered under a litellm alias.
