## Context

`_scan_config_endpoints` runs on every scanned file and matches `_ENDPOINT_KEY` — a closed list
of exact keys (`base_?url|api_base|openai_api_base|azure_endpoint|api_endpoint|inference_endpoint`)
behind `\b` boundaries. Underscore is a word character, so `OPENAI_BASE_URL` never matches even
though `base_url` is in the list; `SERVER_URL`-style suffixes are absent entirely. The
host-shape value guard (from the tsconfig fix) already rejects non-host values.

## Goals / Non-Goals

**Goals:** packaged configs resolve; zero regression on the existing exact keys; non-AI URL
keys stay silent.
**Non-Goals:** runtime env resolution; cross-file env-to-code binding.

## Decisions

### D1 — Segment matching, not a looser regex
**Decision:** A second pattern captures underscore-segmented key tokens; a filter accepts a key
when (a) some segment equals an AI stem from a curated frozenset and (b) the final segment is
`URL`, `ENDPOINT`, `BASE`, or `HOST`. Comparison is case-insensitive on whole segments.
**Rationale:** Substring matching would let `EMAIL_URL` match stem `AI`; segment equality makes
`TELLMEWHY_LLM_SERVER_URL` match on `LLM` while `EMAIL_URL` has no qualifying segment.
**Alternatives rejected:**
- *Any `*_URL` key.* Rejected: `HOMEPAGE_URL`, `WEBHOOK_URL`, `DATABASE_URL` — a false-positive
  factory; the existing non-AI-key scenario forbids it.
- *`MODEL` and bare `API` as stems.* Rejected: `MODEL_URL` collides with 3-D/data models and
  `API_URL` with every REST service; the curated list can grow by data-shaped follow-ups when
  evidence appears.
- *Loosen `\b` in the existing regex.* Rejected: entangles the two match classes; a separate
  pattern keeps the exact-key behaviour provably unchanged.

### D2 — Value-side rules pinned where the review broke them
**Decision:** Captures containing code-call punctuation (`(`/`)`) are skipped — the
environment-getter idiom `os.environ.get(...)` is runtime resolution, and the packaged `.env`
is the declaration this change reads. A value bearing an explicit scheme (`://`) is accepted
with a single-label host (compose service names like `ollama`) and resolves through the
existing custom-endpoint path to `unknown`; the tsconfig hole stays closed because `"."` and
`"./src"` carry no scheme.
**Rationale:** The review executed both idioms against the shipped guard: the getter produced
`os.environ.get(` as evidence and the compose form was silently dropped. Both rules are one
predicate each on the shared value path, so the exact-key matcher inherits the same hygiene.
**Alternatives rejected:**
- *Parse the getter's default argument.* Rejected: string-level capture of one Python idiom's
  second argument is a parser in a regex's clothing; the `.env` file already states the value.
- *Keep requiring a dotted host.* Rejected: compose files are the stated motivation and their
  canonical value shape is a dotless service name behind a scheme.

### D3 — Same downstream pipeline, no new detection kind
**Decision:** Env-style matches flow through the existing `config_endpoint` handling: host-shape
guard, loopback → `local`, KB match → provider, else custom-endpoint `unknown`.
**Rationale:** The key is just another spelling of the same declaration; a new kind would fork
reporting for zero information gain.

## Risks / Trade-offs

- **[Stem list rot]** New AI runtimes bring new key spellings. → The list is a frozenset next
  to the existing key regex; extending it is a one-line, test-backed change, and the miss mode
  is the status quo (unknown), never a false positive.

## Migration Plan

1. Second pattern + segment filter; tests; README line. Rollback: revert.

## Open Questions

None.
