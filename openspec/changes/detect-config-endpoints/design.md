## Context

borderlint matches endpoint flows by known host substrings. Parameterized / OpenAI-compatible setups
put the endpoint behind a config key or a `base_url` kwarg, often with a custom host, so they are
missed. This change detects those, anchored on the config key / kwarg rather than the URL.

## Goals / Non-Goals

**Goals:** detect config-declared and code-override AI endpoints; resolve known hosts, flag custom
hosts as `unknown`, treat loopback as `local`.

**Non-Goals:** runtime/env-only URLs; arbitrary-URL flagging; full YAML/JSON schema parsing.

## Decisions

- **Anchor on AI-endpoint key names / the `base_url` kwarg, not on URLs.** Alternative: flag every
  URL found. Rejected — noise; most URLs are not AI endpoints.
- **Custom / unrecognised host → `unknown` (a real detection), not dropped.** This is the whole point:
  surface OpenAI-compatible / self-hosted endpoints for assertion; the user pins them via the
  `--providers` override. Alternative: ignore unknown hosts. Rejected — that is exactly the miss.
- **Loopback → `local`, never a cross-border violation.** Local inference (Ollama, vLLM, llama.cpp)
  is not a transfer, so flagging it would be a false alarm.
- **Lightweight key/value regex over YAML/JSON/TOML, not a parser.** Alternative: stdlib `json` +
  `tomllib` + PyYAML. Rejected — PyYAML breaks the zero-dependency guarantee, and one uniform regex
  handles all three formats in the existing scanner style. Accept minor imprecision.

## Risks / Trade-offs

- Regex key/value parsing may miss multi-line/complex YAML or over-match → accept; a missed config
  value still can't pass a *known* host falsely (the host scan catches those); refine the key set over time.
- The new `local` jurisdiction must be wired into the policy as always-allowed, or local inference
  would surface as `unknown`.
