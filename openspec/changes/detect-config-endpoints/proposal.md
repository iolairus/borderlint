## Why

Many apps select their model through configuration, not a hard-coded SDK: a `base_url` / `api_base`
in a YAML/JSON config (or passed in code) pointing at any OpenAI-compatible endpoint — a hosted
provider, a self-hosted vLLM, a corporate gateway, or localhost. Today borderlint resolves a config
value only when its host is a *known* provider; a custom OpenAI-compatible host is invisible, even
though it is a real AI data flow to an unknown jurisdiction. This change closes that gap.

## What Changes

- Detect AI-endpoint **config keys** (`base_url`, `api_base`, `azure_endpoint`, `openai_api_base`,
  `endpoint`) in **YAML / JSON / TOML** files and record the referenced endpoint.
- Detect an AI client **endpoint override in code** (`base_url=` / `baseURL:`) in Python and JS/TS.
- An endpoint detected this way whose host is **not in the knowledge base** resolves to **`unknown`**
  (a flagged flow), so deny-by-default + `on_unknown: fail` governs it and the user can pin it with a
  `--providers` override.
- A **loopback/localhost** endpoint resolves to **`local`** — local inference, not a cross-border flow.

## Capabilities

### Modified Capabilities
- `flow-detection`: detect AI-endpoint config keys (YAML/JSON/TOML) and code `base_url` overrides.
- `jurisdiction-classification`: unrecognised anchored hosts → `unknown`; loopback → `local`.
- `residency-policy`: a `local` endpoint is not a residency (allow-list) violation.

## Impact

- `borderlint/detect.py` (config-key + `base_url` regex scanners), `borderlint/kb.py` (host
  resolution returning `unknown` / `local` for anchored detections), `borderlint/policy.py`
  (`local` always allowed). No new dependencies — regex, no YAML parser.

## Non-goals

- Pure runtime / env-supplied URLs with no literal in the repo (out of static reach).
- Flagging arbitrary URLs — detection is **anchored on known AI-endpoint keys/kwargs**, not every URL.
- Full YAML/JSON schema parsing or per-model config graphs.
