# Design: provenance-namespace-resolution

## Context

Two constraints shape the fix. First, zero runtime dependencies and a deterministic core. Second,
anchored matching is itself the false-positive defence in a tool whose output gates CI — the spec
already declines basename matching for unqualified paths for exactly this reason. Any loosening must
therefore be *typed*, not general.

`normalize_model()` is the single normalization shared by prefix matching and `deny_models`
evaluation (decision D2 of the provenance change). That sharing is what makes the deny list hard to
dodge, so it must survive this change intact — one normalization story, used by both call sites.

## Decision D1 — named runtimes go in data, arbitrary registries go in code

Two distinct shapes are failing, and they belong in different places:

- **Named local runtimes** (`ollama/`, `vllm/`, `lmstudio/`) are a closed, curated vocabulary. They go
  into `provenance.json` → `passthrough_orgs`, which already exists precisely for "a leading segment
  that carries no provenance" and is applied before matching. Zero code change: `ollama/deepseek-r1`
  strips to `deepseek-r1` and resolves, and because the deny list shares `normalize_model()` it is
  fixed by the same edit.
- **Arbitrary registries and mirrors** (`huggingface.co/`, `mirror.internal/`, `ghcr.io/acme/`) are an
  open vocabulary that cannot be curated. These are recognised *structurally*: a leading segment that
  contains a dot is a host, not an organisation or a family name.

Rejected: putting registry prefixes in the pattern map — every registry would need an entry per family
(n x m growth across 350 patterns), and the map is curated for *developers*, not routes. Rejected:
adding each runtime as a `deepseek`-style pattern — same n x m problem, and it would attribute
provenance to a runtime instead of to the model's developer.

## Decision D2 — candidate list, most-qualified first, existing form unchanged

`normalize_model()` keeps its exact contract (a single best-effort normalized string): policy deny,
the tests and the SBOM all depend on it. A new `KB.model_candidates(literal)` returns the ordered forms
to try:

1. today's normalized form, first — so every currently-resolving identifier resolves identically;
2. each successive form with one leading **host-like** segment removed (containing a dot), re-applying
   passthrough-org stripping at each step, so `huggingface.co/TheBloke/x` reaches `x`;
3. once at least one host-like segment has been dropped — the literal is then demonstrably an image
   reference — the final segment alone, which covers `docker.io/library/llama3:8b`.

`match_model()` iterates the candidates against `_prov_prefixes`, preserving longest-prefix-wins within
each candidate, and returns on the first hit while keeping the original literal as evidence. Deny
evaluation consumes the same list, so a banned family matches whichever form carries its name.

Rejected: general basename matching — it would resolve `src/deepseek/client.py` to `cn` and break the
specified `dir/qwen2.5.zip` scenario. Rejected: stripping *any* leading segment — `solarwinds-agent`
and bare `falcon` are specified non-matches, and an unknown org may legitimately own a family name.
Rejected: making an unresolvable literal yield `unknown` provenance instead of the tier-2 provider
default — defensible, but it changes the documented two-tier contract and would flood existing clean
repos with warnings; recorded as a follow-up question instead.

## Residual limit (documented, not fixed)

An identifier whose family is genuinely absent from the map still resolves through tier-2 to the
serving provider's bloc, and no deny entry can match it. Detection of "this string looks like a model
id I do not know" is a separate capability; the docs now say so plainly rather than implying the deny
list is unconditional.
