# Proposal: kb-drift-resolution-4

## Why

The 2026-10-05 freshness run reports three uncovered upstream providers and seven unresolved
model families — a wave with a new shape: all three providers are self-hosted decision-model
runtimes (litellm reaches each via the deployer's own `api_base`; none operates a hosted
endpoint), and every model in the wave is a fine-tune or adapter on a third-party base.
Until each item is assigned by hand, these flows classify as `unknown` and the review queue
cannot converge.

## What Changes

- Add three bundled provider entries for self-hosted decision-model runtimes, each with an
  empty endpoint list and jurisdiction and sovereignty `local` (the ollama precedent: flows
  stay on the deployer's host; vendor identity lives in the note, and an endpoint is added
  only if one is ever documented):
  - `bespoke` — Bespoke Labs (Mountain View) System One / Nimble runtime
  - `laya` — Convai Innovations (Kerala, India) Laya decision engine
  - `strands_decider` — the Strands Agents (AWS) Decider runtime
- Add provenance patterns for the seven families, blocs confirmed by the maintainer
  2026-10-05 under the fine-tunes-inherit-base rule:
  - `cn` — Bespoke-Nimble-9B (LoRA on Qwen3.5-9B) and Strands Decider 2B (LoRA + pointer
    head on Qwen3.5-2B, AWS-published) — both inherit Alibaba's bloc, org labels naming
    base and tuner
  - `us` — the three Laya checkpoints (ModernBERT-large bases for `english` and
    `typed-decisions`, assigned via the Answer.AI-led joint release; JHU mmBERT for
    `multilingual`) and Cloudflare's `clef` line (own models until lineage says otherwise;
    one hub-qualified `cloudflare/clef` pattern covers all four observed id forms)
- No bare `nimble` pattern under any circumstances: the name collides with the existing
  `nimble` provider (Nimbleway, `il`); Bespoke's model resolves only via qualified forms
  (`bespoke/nimble`, `bespoke-nimble`, `bespokelabs/bespoke-nimble`).
- Bump the review dates of the touched knowledge-base files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `jurisdiction-classification`: self-hosted runtime providers resolve to `local` with
  empty endpoint lists.
- `model-provenance`: the drift-run model families resolve to their base families' blocs,
  including the two Qwen-adapter inheritance calls.

## Impact

- `borderlint/data/providers.json` (+3 entries), `sovereignty.json` (+3 `local` mappings),
  `provenance.json` (+8 patterns), tests.
- No drift-suppression changes: every item resolves via entries or patterns; nothing is
  residue this wave.
- Issue #39's actionable sections drop from 3 providers + 7 families to zero.

## Non-goals

- No data-practice curation: the three runtimes join the gap queue honestly (self-hosted
  vendors still publish terms worth curating later).
- No scanner-side handling of Workers AI's `@cf/` literal prefix: the `@` fails the
  model-id charset gate for all `@cf/` ids equally — a pre-existing limitation, out of
  scope; clef coverage rides the `cloudflare/clef` suffix form.
- No speculative endpoint for Bespoke's early-access hosted offering (hostname
  undocumented — never guessed).
