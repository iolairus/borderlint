## Why

Dogfooding the `retire` app produced an empty flow map — but by **missing** the model call, not by
resolving it to `local`. The call is `fetch(`${LLAMA_URL}/v1/chat/completions`)`: an OpenAI-compatible
request to a runtime-configured endpoint — the single most common LLM-access pattern (vLLM, llama.cpp,
Ollama, OpenRouter, Together, Groq, DeepSeek, …). borderlint sees no SDK import and no static host, so
it stays silent. Repoint that env var at a `us` host and borderlint **still** misses it — a silent
false negative exactly where a residency tool must not be silent.

## What Changes

- **Detect OpenAI-compatible calls by their request-path signature** (`/v1/chat/completions`,
  `/v1/completions`, `/v1/responses`, `/v1/embeddings`) in Python and JS/TS source, even when the host
  is supplied at runtime.
- **Resolve the host** when a static one is adjacent to the path: a loopback host → `local`, a known
  provider host → that provider's jurisdiction. A dynamic/variable host → `unknown`, so
  `on_unknown: fail` gates it.
- **Precision:** only the OpenAI-compatible path family — never a bare `/v1/` (generic REST APIs use it).

## Capabilities

### Modified Capabilities
- `flow-detection`: a new detector for OpenAI-compatible API calls keyed on the request path.

## Impact

- A `_scan_api_calls` detector reusing the existing host resolution and the `custom_endpoint` / `local`
  model. No new provider, no new dependency.

## Non-goals

- Resolving a runtime variable to its default literal (e.g. `LLAMA_URL ?? 'http://localhost:8080'`).
  v1 treats a dynamic host as `unknown` — so `retire` surfaces an honest "destination set at runtime"
  flow rather than `local`. Variable/default data-flow analysis is a follow-up.
- Non-OpenAI-compatible vendor paths (e.g. Anthropic `/v1/messages`) — SDK imports already cover the
  common cases; additive later.
