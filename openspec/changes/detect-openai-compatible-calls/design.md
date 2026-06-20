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
- **"Same string literal" is the resolution boundary.** A static host resolves the jurisdiction only
  when it sits in the *same quoted or template-literal token on one line* as the path — so
  `'http://localhost:8080/v1/chat/completions'` and `` `${VAR}/v1/chat/completions` `` are in-scope (the
  second has no static host → `unknown`), but `base + "/v1/chat/completions"` (host in a different
  token) is dynamic → `unknown`. Reuse the existing resolver: loopback → `local`;
  `kb.match_endpoint(host)` → that provider + jurisdiction; otherwise `custom_endpoint` / `unknown`.
- **De-dup needs a same-line/same-provider pass — the existing key won't collapse it.** `match_endpoint`
  is a substring match, so a static `https://api.openai.com/v1/...` is *already* emitted as an
  `endpoint_reference` by `_scan_py` / `_scan_text`. The dedup key is `(provider_id, kind, evidence,
  file, line)`, so a new `api_call` detection of the same line would NOT collapse. So `scan()` drops an
  api-call detection when another scanner already recorded the same `(provider_id, jurisdiction, file,
  line)` — yielding one detection per flow per line. (The collision exists for both languages:
  `_scan_text` runs on JS/TS as well as config and also substring-matches endpoints, so a static known
  host in a `.ts` string literal is likewise double-produced — the suppression pass applies uniformly.)

## Risks / Trade-offs

- A literal signature in a comment/docstring, or a *non-AI* internal endpoint literally named
  `/v1/embeddings`, both flag — resolving to `custom_endpoint` / `unknown`, never a wrong provider
  attribution. Accepted: conservative for a deny-by-default tool, and a waiver clears it. The signature
  is deliberately the OpenAI-compatible suffix family, not a bare `/v1/`, to keep this rare.
- `retire` surfaces `unknown` rather than `local` until variable-default resolution lands → correct and
  conservative for a sovereignty tool; documented as a non-goal.
