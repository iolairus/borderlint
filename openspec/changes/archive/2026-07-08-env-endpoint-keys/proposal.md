## Why

Deployment configuration on disk — `.env` files, compose files, settings modules — declares AI
endpoints under env-style keys the scanner does not recognise: `TELLMEWHY_LLM_SERVER_URL=http://localhost:8080`
sat unread in a scanned `.env` while three flows reported `unknown` residency. The key matcher
knows only bare exact keys (`base_url`, `api_base` …); prefixed env names defeat its word
boundaries, and common suffixes (`SERVER_URL`) are absent. Runtime values stay honestly
unresolvable; packaged configs should not.

## What Changes

- The config-endpoint scanner additionally matches **env-style keys**: underscore-segmented
  names where one segment is an AI stem from a curated list (`LLM`, `OPENAI`, `ANTHROPIC`,
  `GPT`, `CLAUDE`, `GEMINI`, `MISTRAL`, `DEEPSEEK`, `QWEN`, `OLLAMA`, `VLLM`, `INFERENCE`,
  `COMPLETION`/`COMPLETIONS`, `EMBEDDING`/`EMBEDDINGS`) and the final segment is `URL`,
  `ENDPOINT`, `BASE`, or `HOST`. Case-insensitive; matches `.env`, YAML, JSON, TOML, and
  settings-module assignments alike.
- Non-AI keys stay unflagged: `HOMEPAGE_URL`, `DATABASE_URL`, `CALLBACK_URL` carry no AI stem;
  `MODEL` is deliberately not a stem (3-D/data-model collisions). Value-side rules are pinned: environment-getter
  captures are skipped; scheme-bearing values accept compose service hostnames.
- Existing exact-key matching is unchanged; this is additive.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `flow-detection`: the config-endpoint requirement covers env-style keys.

## Impact

- `borderlint/detect.py` — a second key pattern + segment filter in `_scan_config_endpoints`.
- `tests/`, `README.md` (one line in the capability bullet).
- Real effect measured: TellMeWhy's `.env` resolves its LLM flow to `local`.

## Non-goals

- No runtime resolution (env vars read at runtime stay `unknown`).
- No cross-file binding of an env value to the code that reads it — the config flow is its own
  detection, as today.
- No bare `MODEL`/`API` stems; the curated stem list is data a future change can extend.
