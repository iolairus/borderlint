# fix(kb): resolve Sep-07 drift — SCX.ai provider, Qwen rebrand aliases, 12 model families

## Summary

The 2026-09-07 weekly freshness run (issue #39) reported four upstream providers and thirteen model families the knowledge base cannot resolve — among them high-traffic releases (ByteDance Seed, poolside Laguna, Thinking Machines Inkling) whose flows currently classify as `unknown`. This change drains both sections to zero actionable items: one genuinely new provider entry (`scx_ai`, the KB's first Australian provider), three drift aliases for routes onto already-covered infrastructure, provenance patterns for the twelve genuine model families with maintainer-confirmed blocs, and one structural-residue record.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/kb-drift-resolution/` |
| Spec deltas | MODIFIED `jurisdiction-classification` — Bundled east-west provider knowledge base (SCX.ai example + scenario); ADDED `model-provenance` — Seed, MAI, Laguna, Mellum, and Macaron model families resolve provenance |

## Changes

- **New provider `scx_ai`** — SCX.ai Holdings (ASX:SCX), Australian sovereign-AI inference platform: endpoint `api.scx.ai`, jurisdiction `au`, sovereignty bloc `au` (vocabulary already present from bloc-vocabulary-completion).
- **Drift aliases** — `qwencloud` and `qwen_ai_platform` → `alibaba_dashscope` (litellm's rebranded DashScope routes; both configured hostnames already bundled); `bing_grounding` → `azure_foundry` (Grounding-with-Bing rides the customer's Foundry project endpoint); `bing_grounding/search` filed as structural residue (tool id, not a model).
- **Provenance patterns (+36)** — family stems, org prefixes, and hub-qualified route literals (per the `novita/xiaomimimo/` precedent, since the scanner's matcher anchors at position 0): `cn` — ByteDance Seed, Baidu CoBuddy, StepFun Step; `us` — Microsoft MAI, Google nano-banana, Microsoft Research multilingual-e5, Thinking Machines Lab Inkling, poolside Laguna, PrismML Ternary-Bonsai, BigScience mt0; `eu` — JetBrains Mellum; `sg` — MindAI Macaron. Generic stems (`seed`, `step`, `mt`, `nano`, `multilingual`) are version- or org-qualified so unrelated identifiers stay `unknown`. Blocs confirmed by maintainer 2026-09-08.
- **Tests** — endpoint + sovereignty resolution for `scx_ai`; all thirteen family resolutions in the hub-qualified form litellm users write (including the `:free` OpenRouter variant); near-miss pins for every generic stem.

## Verification

- [x] `openspec validate kb-drift-resolution --strict` passes
- [x] All tasks in tasks.md checked
- [x] Tests covering each acceptance scenario (190 passed; `scripts/kb_drift.py` reports 0 actionable providers and 0 model families)
