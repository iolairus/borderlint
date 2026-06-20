## Context

`_scan_config_endpoints` only fires behind a config key (`base_url:`, `api_base`, …) and `_scan_js`
only matches imports. A raw `fetch(`${VAR}/v1/chat/completions`)` with a runtime host hits neither —
the gap dogfooding `retire` exposed. The signal that *is* present is the OpenAI-compatible request path.

## Goals / Non-Goals

**Goals:** detect OpenAI-compatible calls by path signature in PY + JS/TS; resolve a static host, else
`unknown`.

**Non-Goals:** runtime variable/default resolution; non-OpenAI-compatible vendor paths.

## Decisions

- **Signature = the OpenAI-compatible suffixes, not a bare `/v1/`.** Alternative: match any `/v1/`.
  Rejected — every REST API uses `/v1/`; the `chat/completions` | `completions` | `responses` |
  `embeddings` family is the OpenAI-compatible tell. A path like `/v1/users` MUST NOT flag.
- **Dynamic host → `unknown`, not `local`.** A base_url-configurable client can point anywhere at
  runtime; `unknown` is the honest verdict and `on_unknown: fail` gates it. Resolving the `?? localhost`
  default would need variable/default data-flow analysis — deferred. So `retire` reads as one `unknown`
  flow ("destination set at runtime; pin it"), which is more correct than a guessed `local`.
- **Reuse host resolution + `custom_endpoint` / `local`.** When a static `http(s)://host` precedes the
  path in the same string: loopback → `local`; `kb.match_endpoint(host)` → that provider + jurisdiction;
  otherwise `custom_endpoint` / `unknown`. No new provider id. `# ponytail: one regex + existing resolver`.
- **De-dup against existing detections on the same line** so a static known endpoint already caught by a
  config-key or import scan is not double-reported.

## Risks / Trade-offs

- A literal `/v1/chat/completions` in a comment or doc string would flag → acceptable; it is still an
  OpenAI-compatible reference worth surfacing, and waivers cover false positives.
- `retire` surfaces `unknown` rather than `local` until variable-default resolution lands → correct and
  conservative for a sovereignty tool; documented as a non-goal.
