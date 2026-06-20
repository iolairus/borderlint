## 1. OpenAI-compatible call detection

- [x] 1.1 Add a `_scan_api_calls(path, src, kb)` detector matching the signatures (`/v1/chat/completions`, `/v1/completions`, `/v1/responses`, `/v1/embeddings`) in Python and JS/TS source; run it from `scan()` for those files
- [x] 1.2 Resolve a static host in the same string literal as the path: loopback → `local`; a KB-known host → that provider + jurisdiction; otherwise (dynamic/interpolated host, host outside the literal, or relative path) → `custom_endpoint` with jurisdiction `unknown`
- [x] 1.3 Match only the four signatures, never a bare `/v1/...`; emit at most one detection per (provider, jurisdiction) per line — drop an api-call detection that duplicates a flow another scanner already recorded on that line (the existing dedup key includes `kind`, so a same-line/same-provider suppression is needed)

## 2. Tests

- [x] 2.1 Tests: `${VAR}/v1/chat/completions` → `custom_endpoint`/`unknown`; `base + "/v1/chat/completions"` → `unknown`; `localhost:8080/v1/chat/completions` → `local`; `api.openai.com/v1/chat/completions` → exactly one OpenAI/`us` detection (no duplicate); `api.deepseek.com/v1/chat/completions` → DeepSeek/`cn`; a generic `/v1/users` path → no detection; the `retire` pattern (`fetch(`${LLAMA_URL}/v1/chat/completions`)`) yields one `unknown` flow
