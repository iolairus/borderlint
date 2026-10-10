# Proposal: provenance-namespace-resolution

## Why

`deny_models` is documented as the hardest statement in the provenance block, and the residency-policy
spec promises a denied family "cannot be dodged by a repository path or a version suffix". It can be
dodged by one specific and increasingly common path form: a **registry- or runtime-qualified model
identifier**. Anchored prefix matching sees the leading namespace segment, matches nothing, and the
reference therefore binds no model at all — so the flow falls through to tier-2 provenance and reports
the *serving provider's* bloc with full confidence.

Measured on 1.15.5, OpenAI flow, `deny_models: ["deepseek"]`:

| model reference | resolves to | deny fires |
|---|---|---|
| `deepseek-r1` | `cn` (DeepSeek) | yes |
| `ollama/deepseek-r1` | `us` (OpenAI default) | **no** |
| `vllm/deepseek-r1` | `us` | **no** |
| `mirror.internal/deepseek-r1` | `us` | **no** |
| `huggingface.co/TheBloke/deepseek-coder-33B-AWQ` | `us` | **no** |

The last row is the already-covered `TheBloke/…` identifier with only a host prefix added — copy-pasted
from a browser URL. The failure mode is doubly bad: provenance is reported as a *wrong* bloc rather than
`unknown`, so neither the deny, nor a provenance allow-list, nor `on_unknown` catches it.

## What Changes

- Extend model-identifier resolution with a **narrow namespace rule**: leading segments that carry no
  provenance of their own — host-like segments (containing a dot) and a curated set of local-runtime /
  launcher names (`ollama`, `vllm`, `lmstudio`, …) — are dropped to form additional match candidates,
  tried most-qualified first. An arbitrary organisation segment is still never dropped, so the existing
  negative guarantees (`solarwinds-agent`, bare `falcon`, `dir/qwen2.5.zip`) hold unchanged.
- Evaluate `deny_models` against the same candidate set, so a banned family matches whichever form of
  the identifier actually carries the family name.
- State the residual limit in the docs: an identifier whose family is absent from the map still resolves
  through tier-2 and cannot be denied.

## Non-goals

- No general basename matching for unqualified paths. `dir/qwen2.5.zip` deliberately resolves nothing,
  and dropping *any* leading segment would make `src/deepseek/client.py` resolve to `cn`.
- No change to tier-2 fallback semantics, provider KB content, jurisdictions, or sovereignty.
- No new policy keys; no output-format changes.
- Excluding the `--providers` input file from its own scan (a separate, unrelated reporting nit) is
  left as a follow-on change, per one-concern-per-change.
