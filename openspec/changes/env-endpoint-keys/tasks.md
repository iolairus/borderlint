## 1. Detection

- [ ] 1.1 Add the env-style key pattern + segment filter (curated stem frozenset; final segment URL/ENDPOINT/BASE/HOST) to `_scan_config_endpoints`; existing exact-key regex untouched (D1, D3, "Detect AI endpoints declared in configuration")
- [ ] 1.2 Value-side rules on the shared path: skip captures containing `(`/`)`; accept scheme-bearing single-label hosts through the custom-endpoint path (D2)

## 2. Tests

- [ ] 2.1 Positives: `TELLMEWHY_LLM_SERVER_URL=http://localhost:8080` → local; `OPENAI_BASE_URL=https://api.openai.com/v1` → a detection identifying OpenAI (not asserting exactly one — the text scanner also fires); lowercase yaml `llm_server_url:`; compose list form `- OLLAMA_BASE_URL=http://ollama:11434` → custom endpoint unknown
- [ ] 2.2 Negatives: `DATABASE_URL`, `HOMEPAGE_URL`, `EMAIL_URL` (AI substring), `MODEL_URL` (stem deliberately absent) not flagged; env-getter assignment not flagged; `.`/`./src` still skipped (no scheme)

## 3. Docs & validation

- [ ] 3.1 README capability bullet mentions env-style keys; full suite + `openspec validate env-endpoint-keys --strict`; TellMeWhy re-scan shows the `.env` flow as local
