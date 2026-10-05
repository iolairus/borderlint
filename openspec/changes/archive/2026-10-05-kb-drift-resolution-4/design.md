# Design: kb-drift-resolution-4

## Context

The 2026-10-05 wave is three self-hosted decision-model runtimes (bespoke, laya,
strands_decider — all `api_base`-driven in litellm, none with a vendor-operated endpoint)
plus Cloudflare's clef line. litellm added the three via its unified `/v1/decisions` work,
marking an emerging "typed-decision model" category (Jev, Nimble, Laya, Strands Decider,
Clef, Perplexity Decisions). Research established every operator and base lineage; the
maintainer confirmed all calls on 2026-10-05.

## Goals / Non-Goals

**Goals:**

- Drain the provider and model-family sections to zero, each resolution a recorded human
  judgment.
- A correct KB shape for self-hosted runtimes: the flow stays on the deployer's host, so
  `local` is the honest jurisdiction and sovereignty — vendor HQ would misstate where data
  goes.
- Consistent base-inheritance for the wave's fine-tunes, including two more pointed calls.

**Non-Goals:**

- No `@cf/` charset-gate change; no speculative endpoints; no data-practice curation.

## Decisions

### D1: Self-hosted runtimes get `local`/`local` entries with empty endpoints

None of the three vendors operates an endpoint litellm can reach — the deployer supplies
`api_base`. The ollama/lemonade precedent applies: jurisdiction and sovereignty `local`
("the operator's own jurisdiction governs"), empty endpoint list under the no-guessed-
hostname rule, vendor identity and the self-hosted mechanics in the note. Bespoke's
early-access hosted offering has no documented hostname; if one appears, it enters as
ordinary drift. Alternative rejected: vendor-HQ jurisdictions (us/in/us) would claim the
vendor can see the data, which is exactly what self-hosting prevents.

### D2: Both Qwen adapters inherit Alibaba's bloc

Bespoke-Nimble-9B is a ~165 MiB LoRA on Qwen3.5-9B (requires the base checkpoint to run);
Strands Decider 2B is a LoRA + pointer head on Qwen3.5-2B, published by AWS's Strands
Agents team. The standing rule — fine-tunes and distillations inherit the base family's
bloc — applies regardless of tuner identity, as it did for magnum (Anthracite→Qwen) and
Ember (Fireworks→Kimi). Both resolve `cn` with org labels naming base and tuner:
"Alibaba (Bespoke Nimble LoRA)" and "Alibaba (AWS Strands Decider tune)". The AWS case is
the rule's sharpest outcome so far and is exactly what the provenance dimension measures:
whose weights, not whose brand.

### D3: Laya's encoder bases resolve `us`; ModernBERT assigned via the Answer.AI-led release

`laya/multilingual` rides JHU's mmBERT (`us`, clear). `laya/english` and
`laya/typed-decisions` ride ModernBERT-large — a joint Answer.AI (US) + LightOn (FR)
release; the maintainer assigned `us` via the Answer.AI-led release, with the joint lineage
named in the org labels ("Answer.AI/LightOn ModernBERT (Laya tune)"). Convai Innovations
(the Indian tuner) appears in the provider note, not the bloc — inheritance follows the
base, as everywhere else. Three per-model patterns keep the labels precise; an org-level
`laya/` pattern would blur the two base lineages.

### D4: Clef is Cloudflare's own line; one hub-qualified pattern covers all forms

litellm carries four clef ids (`cloudflare/@cf/cloudflare/clef(-flash)` and
`cloudflare/clef(-flash)`); the checker's suffix walk reduces every one to a
`cloudflare/clef` prefix, so a single pattern (org Cloudflare, bloc `us`) covers the
family without a risky bare 4-character `clef` stem. Base lineage is undisclosed
(moderate confidence it is Cloudflare's own work); a disclosure is ordinary drift-review
material. Scanner-side, Workers AI literals beginning `@cf/` fail the model-id charset
gate — a pre-existing, uniform limitation recorded as a non-goal.

### D5: The Nimbleway collision forbids any bare `nimble` stem

The existing provider `nimble` is Nimbleway (`il`). Bespoke's model therefore resolves
only via qualified forms — `bespoke/nimble` (covers `nimble-latest` by prefix),
`bespoke-nimble` (bare literal form, covers the HF basename), and
`bespokelabs/bespoke-nimble` — and a near-miss test pins a bare `nimble`-prefixed id to
`unknown`.

## Risks / Trade-offs

- [`local` entries under-warn if a vendor later launches a hosted service] → the hosted
  hostname would be new drift (endpoint detection is host-driven); the entry's note says
  endpoints are added when documented.
- [ModernBERT `us` flattens a genuinely joint US/FR lineage] → the org label names both
  orgs; a policy that distinguishes `us` from `eu` for encoder bases this small is unlikely
  to hinge on it, and the label gives reviewers the full picture.
- [Clef lineage undisclosed] → org-level assignment to Cloudflare is the same treatment
  every undisclosed-lineage first-party line gets; drift review corrects on disclosure.

## Open Questions

- (none — all calls confirmed 2026-10-05)
