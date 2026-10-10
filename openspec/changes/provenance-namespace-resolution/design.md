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

## Risks and accepted trade-offs

### R1 — the final-segment fallback attributes provenance to internal names that merely start with a family prefix

Rule 3 of D2 tries an image reference's final segment on its own. Once the host is gone nothing else
distinguishes "a registry repo holding model weights" from "an internal service whose name happens to
begin with a family prefix", and every string literal in a scanned file faces `match_model()`
(`detect.py`). Verified on this branch:

| literal | resolves to |
|---|---|
| `registry.corp/ml/mistral-serving` | `eu` / Mistral AI |
| `docker.io/library/whisper-transcribe` | `us` / OpenAI |
| `internal.registry/ml/falcon-sandbox` | `ae` / TII |
| `docs.example.com/gpt-4-guide` | `us` / OpenAI — a docs URL, not a model at all |

The asymmetry is the part worth stating. For `deny_models` the error is **fail-closed**: an internal
`ghcr.io/acme/deepseek-config-migrator` trips `deny_models: ["deepseek"]`, which is noisy but never lets
banned weights through. For a provenance *allow-list* it can cut the other way — attributing an internal
tool to `us`/OpenAI can relax a verdict that the serving provider's bloc would have failed. This is the
same honesty bar the existing basename rule already sets (a `.gguf` basename is attributed from a
filename alone), so it is accepted rather than blocked — but as a stated trade-off, pinned by tests, not
as emergent behaviour.

Mitigations, in order of preference:

1. **The original literal is always kept as evidence** (D2), so the finding reads
   `registry.corp/ml/mistral-serving`, not `mistral` — a reviewer sees exactly what matched and can
   judge it without re-deriving the stripping.
2. **Scope the deny entry**, not the matcher: `deny_models: ["deepseek-r1"]` bans the family member
   without catching an internal `deepseek-config-migrator`. Deny entries are anchored prefixes, so this
   costs one string.
3. **Waive the finding** with a file-level `borderlint: allow <reason>` comment — available for the
   provenance finding; `model_denied` stays unwaivable inline by design, exactly like `denied_provider`.
4. Narrowing rule 3 itself (e.g. requiring the final segment to look like a tag/manifest rather than a
   service name) is left as a follow-up: every heuristic tried for it also weakens the evasion fix, and
   the four rows above are all attributable from the evidence string alone.

### R2 — a URL carrying its scheme resolves nothing (documented, deliberately not fixed here)

`https://huggingface.co/TheBloke/deepseek-coder-33B-AWQ` resolves to nothing: `"https:"` contains no dot,
so the host walk never starts and there is no segment to drop. Fixing it by stripping a leading
`scheme://` before the walk would be two lines — and would feed *every* documentation URL in a repo into
the R1 fallback above, turning `https://docs.example.com/gpt-4-guide` from a non-match into an OpenAI
claim. The docs therefore describe the form that works (`huggingface.co/TheBloke/…`, scheme-less) rather
than promising the browser paste; scheme handling belongs in its own change with its own false-positive
budget and its own near-miss pins.

## Residual limit (documented, not fixed)

An identifier whose family is genuinely absent from the map still resolves through tier-2 to the
serving provider's bloc, and no deny entry can match it. Detection of "this string looks like a model
id I do not know" is a separate capability; the docs now say so plainly rather than implying the deny
list is unconditional. R1 is its mirror image: the map over-reaching for a name it should not know.
Between them the honest statement is that prefix matching resolves *known families in known shapes*,
and both failure modes are visible in the evidence string.
