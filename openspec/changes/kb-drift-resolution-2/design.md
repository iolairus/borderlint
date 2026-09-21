# Design: kb-drift-resolution-2

## Context

The 2026-09-21 run surfaced the largest drift wave yet: 3 providers, 30 families. Research
established every operator; the maintainer confirmed all blocs and judgment calls on
2026-09-21. Two structural sources drive the volume: aihubmix (an aggregator whose catalog
rebadges other vendors' models under its own ids) and a batch of new OpenRouter publishers,
including community fine-tuners whose models carry no org marker in the basename.

## Goals / Non-Goals

**Goals:**

- Drain the provider and model-family sections to zero actionable items, each resolution a
  recorded human judgment.
- Honest handling of three new provider shapes: an undisclosed-operator aggregator, an AWS
  regional speech service, and a provider with an undocumented API hostname.
- Provenance for rebadged, fine-tuned, and hub-qualified identifiers without over-matching.

**Non-Goals:**

- No data-practice curation; no SDK keys until verified; no per-request provenance for
  composite router products.

## Decisions

### D1: `aihubmix/` is a passthrough; its rebadges are explicit patterns

The aggregator's route prefix carries no provenance, so `aihubmix/` joins the passthrough
list — after the single strip the basename matches family patterns directly
(`aihubmix/agnes-2.5-flash` → `agnes-…`, `aihubmix/hy3` → `hy3`). The rebadge prefixes
`coding-`/`cc-` are NOT passthroughs: the normalizer strips only one prefix per literal, so a
`coding-` passthrough could never compose with the `aihubmix/` strip, and a bare generic
passthrough would silently swallow future unrelated ids. Instead each rebadge line gets an
explicit pattern (`coding-glm`, `coding-kimi`, `coding-xiaomi-mimo`, `cc-glm`) resolving to
the underlying developer (Zhipu, Moonshot, Xiaomi) — the `cc-glm-5.1` mapping is
undocumented upstream, but the `glm` token makes Zhipu the recorded inference. Precedent
note: openrouter uses hub-qualified patterns rather than a passthrough because its ids carry
an org segment; aihubmix ids are bare basenames, which is exactly the passthrough shape.

### D2: Three provider shapes, each recorded honestly

- `aihubmix`: aggregator entry with both documented hosts (`aihubmix.com`,
  `api.inferera.com`); jurisdiction and sovereignty `unknown` — the "US LLC" description is
  secondhand, the operator entity is undisclosed, and the KB records what is documented, not
  what is claimed about a provider by third parties.
- `aws_transcribe`: endpoint token `transcribe` under `region_scheme: aws`
  (`transcribe.<region>.amazonaws.com`), sovereignty `us` — the `aws_polly` mould.
- `typesafe`: no endpoint hosts at all. litellm reaches it only via proxy pass-through and
  no upstream hostname is documented; an entry with a guessed host would fabricate detection
  evidence. The entry still closes the drift provider gap, carries jurisdiction/sovereignty
  `us`, and documents the situation in its note; the endpoint is added when documented.

### D3: Stem discipline, tightened for the most generic wave yet

The established rule (most specific literal covering the real members) matters more this
round: stems like `l`, `cc`, `hy`, `coding`, `model`, `union`, `whisper`, `sonar`, `trinity`
are the most over-match-prone the checker has surfaced. Version- or org-qualify every
generic stem (`hy3`/`hy4` not `hy`; `l3-`/`l3.` not `l`; `coding-glm` not `coding-`). Bare
`whisper` and `sonar` were tried and rejected during implementation — they matched
`whispering-pines` and `sonarqube-scan` — and `sonar-` fell to the repo's own earlier pin that `sonar-scanner` (SonarQube tooling)
must stay unresolved — so whisper keeps `whisper-` plus the azure_ai form, sonar keeps only
`perplexity/`-qualified forms, and bare `sonar`/`whisper` literals in code resolve through
the tier-2 provider default instead. Hub-qualified route literals follow the `novita/xiaomimimo/`
precedent for every observed openrouter/together_ai/azure_ai/wandb form.

### D4: Fine-tunes inherit the base family's bloc — even across community orgs

Applying the provenance map's standing rule: Anthracite's `magnum-v4-72b` (Qwen2.5-72B
full-parameter tune) → `cn`; TheDrummer's `cydonia`/`skyfall`/`unslopnemo` (Mistral Small /
Nemo bases) → `eu`; Sao10K's `l3-`/`l3.`* (Llama-3.x merges) → `us` via Meta; AionLabs
splits — `aion-*` (DeepSeek/GLM derivatives) → `cn` with `aion-rp` (Llama-3.1 base) → `us`,
longest-prefix-wins ordering the exception above the family rule. Publisher nationality
(unknown for all four) is irrelevant under the rule: the weights' lineage carries the bloc.
Org labels name both lineage and tuner (e.g. "Mistral AI (TheDrummer tune)") so evidence
stays self-explanatory.

### D5: Deliberate-anonymity and composite products are residue, not guesses

`stealth/` becomes a prefix residue entry: OpenRouter's cloaked program is unattributed by
design, so every current and future `stealth/*` id is acknowledged with that reason and
re-attributed when revealed (union-alpha, since revealed as Pareto, stays covered either
way). `unbiased/pareto` is residue as a composite router product — it fans each request
across many frontier and open models, so no single weight-provenance would be honest.
`azure_ai/model-router` and `transcribe/StartTranscriptionJob` are structural (feature and
API operation, not models).

## Risks / Trade-offs

- [A future Sao10K/TheDrummer tune on a different base inherits the wrong bloc via a too-broad
  pattern] → patterns are family-scoped (`l3-`, `cydonia-`), never tuner-org-scoped; a new
  base family surfaces as fresh drift instead of resolving silently wrong.
- [`aihubmix/` passthrough hides future aihubmix-only ids] → it does not: after the strip,
  an unmatched basename is still uncovered and surfaces in the drift report.
- [`cc-glm` mapping is an inference, not documentation] → recorded as such in the pattern's
  org label context; if aihubmix documents a different base, the drift review corrects it.
- [Qualified-only whisper/sonar coverage misses bare literals in code] → accepted: bare
  exact `whisper`/`sonar` model strings resolve through the tier-2 provider default in
  provider context, and the alternative (bare patterns) demonstrably over-matched tool
  names (`whispering-pines`, `sonar-scanner`) — see D3.

## Open Questions

- (none — all blocs and judgment calls confirmed 2026-09-21)
