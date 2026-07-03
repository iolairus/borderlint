## Context

borderlint resolves each flow to a **jurisdiction** (residency: where the endpoint sits) and a
**sovereignty** bloc (who can compel disclosure from the serving provider). Neither axis says
whose **model weights** the flow runs. The divergent cases are real and current: Bedrock
`ap-east-1` serving DeepSeek-R1 is residency `hk` / sovereignty `us` / weights PRC-origin;
self-hosted Qwen via Ollama is residency and sovereignty `local` with the same `cn` weight
origin. Sector rules on model origin and regulator model-supply-chain questions (HKMA GenAI
guidance, OGCIO framework, CAC filings) make this a third axis a policy must express. It was
explicitly deferred in `sovereignty-dimension`; the orthogonal-dimension pattern shipped there
(opt-in policy block, bloc vocabulary, additive reporting) is the template this change reuses.

## Goals / Non-Goals

**Goals:**
- Model provenance as a distinct per-flow attribute: the bloc of the legal regime under which the
  model's developer operates, resolved from statically visible model references.
- Ship a bundled, maintainable model-provenance map with the same freshness discipline as the
  provider KB.
- Let a policy optionally constrain provenance per classification with the same ergonomics as
  sovereignty (`on_unknown`, `fail_on`, waivers).
- Keep the change non-breaking: reports gain a column; absent the policy block, behaviour is
  identical to today.

**Non-Goals:**
- Adjudicating export-control applicability (the map surfaces; the policy decides).
- Derivative-weights genealogy (fine-tunes/distillations inherit the base family's bloc).
- Runtime model resolution (variables/env → `unknown`).
- Training-data provenance.

## Decisions

### D1 — Provenance is a third attribute, never folded into sovereignty
**Decision:** Each flow carries `jurisdiction`, `sovereignty`, and `provenance` (new).
**Rationale:** The axes decouple in both directions — US-sovereign flows serving `cn`-provenance
weights (Bedrock/DeepSeek) and `local`-sovereign flows serving foreign weights (Ollama/Qwen).
**Alternatives rejected:**
- *Override sovereignty when weights are foreign.* Rejected: destroys the compelled-disclosure
  answer; a policy needs both facts independently.
- *A combined "risk score".* Rejected: borderlint surfaces facts, policies decide; scoring is
  adjudication.

### D2 — Reuse the sovereignty bloc vocabulary, minus `local`
**Decision:** Provenance blocs are `us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`, `ca`, `unknown`.
`local` is excluded: weights always have a developer. An in-house-trained model is expressed via
a user KB override mapping the model pattern to the org's home bloc.
**Rationale:** One vocabulary, one display map, one mental model across dimensions.
**Alternatives rejected:**
- *Per-org provenance (openai, deepseek, …).* Rejected: policies are written against legal
  regimes, not company names; the org is kept as evidence, the bloc is the policy unit.
- *Include `local` for in-house models.* Rejected: conflates "no external sovereign" (a serving
  property) with "we authored the weights" (an authorship property); the user-override route is
  honest and explicit.

### D3 — Two-tier resolution: model reference first, first-party provider default second
**Decision:** (1) A matched model reference resolves via the provenance map. (2) Absent a model
reference, a provider that serves **only its own models** (OpenAI, Anthropic, DeepSeek, Mistral,
Zhipu, …) resolves to that org's bloc via a provider-level default in the provenance map.
Multi-model hosts (Bedrock, Vertex, aggregators) have no default → `unknown`. Azure OpenAI
defaults to `us` (serves OpenAI models only).
**Rationale:** `import openai` with no model string is still certainly OpenAI weights; without
tier 2, most real flows would resolve `unknown` and the dimension would be noise.
**Alternatives rejected:**
- *Model-reference-only resolution.* Rejected: a sea of `unknown` for the majority case where the
  provider is a first-party developer.
- *Default all providers to their sovereignty bloc.* Rejected: wrong for exactly the flows this
  dimension exists for (Bedrock is `us`-sovereign but serves `cn`-provenance models).

### D4 — Model references matched by anchored ID patterns, bound per file
**Decision:** A new `model_reference` detection kind matches string literals against anchored
patterns from the provenance map: Bedrock model IDs (`anthropic.claude-*`, `deepseek.r1*`),
bare API model strings (`gpt-4*`, `claude-*`, `qwen*`, `glm-*`), aggregator-qualified IDs
(`deepseek/deepseek-r1`), and hub repo IDs (`Qwen/*`, `meta-llama/*`). A model reference binds
to a provider detection **in the same file**; otherwise it stands alone as its own finding.
Longest pattern wins.
**Rationale:** These ID shapes are distinctive enough to anchor on; same-file binding is the
simplest rule that is right for the dominant one-provider-per-module layout.
**Alternatives rejected:**
- *AST-proximity binding (same call/function).* Rejected: fragile across SDK styles and both
  languages for marginal precision gain.
- *No binding (standalone findings only).* Rejected: loses the per-flow provenance answer that
  the policy evaluates.
- *Substring matching.* Rejected: the v1.2.1 override fix removed exactly this class of
  false-positive footgun; patterns are anchored.

### D5 — Opt-in policy block, symmetric `on_unknown` gate
**Decision:** Policy gains an optional `provenance` block with per-classification allow-lists and
`on_unknown`; `fail_on` accepts `provenance`. `on_unknown: "fail"` gates on its own — no second
gate through `fail_on` (the v1.2.1 sovereignty correction, applied from day one). Waivers apply;
provider deny-list still cannot be waived.
**Rationale:** Identical ergonomics to sovereignty; zero new concepts for adopters.
**Alternatives rejected:**
- *A shared `dimensions` policy super-block.* Rejected: restructures existing policies for
  aesthetics; additive blocks are the established, non-breaking pattern.

### D6 — Aggregator-qualified IDs upgrade resolution
**Decision:** `deepseek/deepseek-r1` via OpenRouter/LiteLLM resolves provenance `cn` even while
residency and sovereignty stay `unknown`.
**Rationale:** The org prefix is statically present; provenance is the one axis aggregators
don't obscure. This makes the dimension *more* informative exactly where the other two are blind.

### D7 — Local model identifiers: pass-through orgs, GGUF basenames, pinned family stems
**Decision:** Three mechanisms make local-LLM usage (Ollama, llama.cpp, MLX) resolvable:
(1) a **pass-through org list** — quantizer/community-conversion hubs (`mlx-community/`,
`thebloke/`, `bartowski/`, `unsloth/`, …) are stripped and the remaining model name re-matched,
since the redistributor org carries no provenance while the family name in the repo does;
(2) literals ending `.gguf` match by **basename**, since file paths defeat start-anchoring;
(3) family prefixes are **pinned with digits/punctuation** (`llama3`, `phi4`, `gemma2`) rather
than bare stems, and a small stoplist rejects tool names (`llama_index`, `llama-cpp-python`)
that would otherwise match a family prefix. Families whose developer bloc is outside the
vocabulary (Falcon/TII, EXAONE/LG, Solar/Upstage) get **no entry** — absence resolves `unknown`
for bound flows without generating standalone noise rows; they join the vocabulary-completion
follow-up.
**Rationale:** Redistributor repos dominate real local-model strings; without pass-through, the
dimension is blind exactly where `local`/`local`/`<bloc>` matters most.
**Alternatives rejected:**
- *Map quantizer orgs to a bloc directly.* Rejected: `bartowski/` publishes conversions of every
  family; the org identifies packaging, never weights origin.
- *Bare family stems (`llama`, `phi`).* Rejected: collide with tooling and ordinary words
  (`llama_index`, `philadelphia`); digit/punctuation pinning plus a stoplist keeps anchoring
  honest.
- *Mapping out-of-vocabulary families to `unknown` entries.* Rejected: an entry that resolves
  `unknown` creates standalone `model_reference` rows that only add noise; absence gives the
  same verdict without the rows.

### D8 — Reporting: additive across all five formats
**Decision:** Text gains a provenance segment, JSON a `provenance` field, Mermaid appends the
bloc to node labels, SARIF includes it in the message, SBOM gains `provenances`. Default
`fail_on` excludes `provenance`.
**Rationale:** Same visibility-without-verdict posture as sovereignty.

## Risks / Trade-offs

- **[Model-ID churn]** New model families ship monthly; the map ages fast. → Mitigation: fold
  `provenance.json` into the existing kb-freshness machinery (`updated` date, scheduled coverage
  check, user-KB merge for immediate gaps).
- **[False-positive matches]** Model-like strings in unrelated contexts (a variable named
  `gpt`). → Mitigation: anchored patterns with ID punctuation (dots, slashes, version suffixes);
  invalid-token tests; `unknown` on no match, never a guess.
- **[Binding imprecision]** Same-file binding mis-attaches in multi-provider files. → Mitigation:
  evidence strings for both the provider and the model reference appear in the finding; advisory
  posture documented.
- **[First-party default drift]** A first-party provider starts hosting third-party models
  (as OpenAI/Anthropic partnerships evolve). → Mitigation: the default is per-provider data in
  `provenance.json`, reviewable on the same freshness cadence, removable without code change.

## Migration Plan

1. Add `provenance.json` (patterns + first-party provider defaults, `updated` date).
2. Extend `kb.py`: load/merge/validate the map; `resolve_provenance()`.
3. Extend `detect.py`: `model_reference` kind, same-file binding, `provenance` field on Detection.
4. Extend `policy.py`: optional `provenance` block, `provenance`/`provenance_unknown` reasons.
5. Extend `report.py`: render across all five formats.
6. No data migration; rollback is a code revert — old code ignores the new JSON file.

## Open Questions

- Should the Mermaid label carry both sovereignty and provenance, or become too noisy? Lean:
  append provenance only when it differs from sovereignty; to confirm during implementation
  against real diagrams.
- Whether `ollama pull`/model-file references in shell scripts and Dockerfiles are in scope for
  detection. Lean: defer to the IaC-scanning enhancement; Python/TS string literals only here.
