## 1. OpenAI-compatible call detection

- [ ] 1.1 Add a `_scan_api_calls(path, src, kb)` detector matching the OpenAI-compatible request-path signatures (`/v1/chat/completions`, `/v1/completions`, `/v1/responses`, `/v1/embeddings`) in Python and JS/TS source; run it from `scan()` for those files
- [ ] 1.2 Resolve the host adjacent to the path in the same string: loopback → `local`; a KB-known host → that provider + jurisdiction; a static unknown host → `custom_endpoint`; a dynamic/variable host → `custom_endpoint` with jurisdiction `unknown`
- [ ] 1.3 Match only the OpenAI-compatible signatures, never a bare `/v1/...` (no false positives on generic REST APIs); de-duplicate against an endpoint already detected on the same line

## 2. Tests

- [ ] 2.1 Tests: `${VAR}/v1/chat/completions` → `unknown`; `localhost:8080/v1/chat/completions` → `local`; `api.openai.com/v1/chat/completions` → OpenAI/`us`; `api.deepseek.com/v1/chat/completions` → DeepSeek/`cn`; a generic `/v1/users` path → no detection; the `retire` pattern (`fetch(`${LLAMA_URL}/v1/chat/completions`)`) yields one `unknown` flow
