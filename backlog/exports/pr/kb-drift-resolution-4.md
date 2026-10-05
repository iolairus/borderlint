# fix(kb): resolve Oct-05 drift — self-hosted decision runtimes, Qwen-adapter inheritance, Clef

## Summary

The 2026-10-05 freshness run reported three uncovered providers and seven model families — a wave with a new structural shape: all three providers are self-hosted typed-decision runtimes (litellm reaches each only at a deployer-supplied `api_base`; no vendor-operated endpoint exists), and every model in the wave is a fine-tune or adapter on a third-party base. This change drains both sections to zero with three `local`-jurisdiction provider entries, eight provenance patterns driven by the base-inheritance rule, and no residue.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/kb-drift-resolution-4/` |
| Spec deltas | MODIFIED `jurisdiction-classification` — Bundled east-west provider knowledge base (self-hosted-runtime rule + scenario); ADDED `model-provenance` — Nimble, Laya, Strands Decider, and Clef model families resolve provenance |

## Changes

- **Self-hosted runtime providers** — `bespoke` (Bespoke Labs, Mountain View — System One/Nimble), `laya` (Convai Innovations, Kerala, India — multilingual typed-decision engine), `strands_decider` (AWS's Strands Agents team — 2B decider). Each enters with an empty endpoint list and jurisdiction/sovereignty `local`, the ollama precedent: flows stay on the deployer's host, and recording vendor HQ would claim the vendor sees data that self-hosting keeps from it. The MODIFIED requirement makes this a standing rule. Bespoke's early-access hosted hostname is undocumented — never guessed.
- **Qwen-adapter inheritance** — Bespoke-Nimble-9B (a ~165 MiB LoRA on Qwen3.5-9B) and Strands Decider 2B (LoRA + pointer head on Qwen3.5-2B, published by AWS) both resolve bloc `cn` under the standing fine-tunes-inherit-base rule — the magnum/Ember precedent at its sharpest: whose weights, not whose brand. Org labels name base and tuner.
- **Laya checkpoints** — resolve `us` via their encoder bases: Answer.AI/LightOn ModernBERT (`english`, `typed-decisions`; assigned via the Answer.AI-led joint release, joint lineage in the label) and JHU mmBERT (`multilingual`). Convai, the Indian tuner, lives in the provider note — inheritance follows the base.
- **Clef** — Cloudflare's own decision line; one hub-qualified `cloudflare/clef` pattern covers all four litellm id forms via the checker's suffix walk, avoiding a risky bare 4-character stem. The `@cf/` literal-prefix charset limitation is pre-existing and uniform — recorded as a non-goal.
- **Nimbleway collision guard** — no bare `nimble` stem exists anywhere (design D5); Bespoke's model resolves only via qualified forms, with a near-miss test pinning the boundary.

## Verification

- [x] `openspec validate kb-drift-resolution-4 --strict` passes
- [x] All tasks in tasks.md checked
- [x] Tests covering each acceptance scenario (205 passed; `scripts/kb_drift.py` reports 0 actionable providers and 0 model families)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
