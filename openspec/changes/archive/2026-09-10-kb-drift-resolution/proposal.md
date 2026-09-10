# Proposal: kb-drift-resolution

## Why

The 2026-09-07 weekly freshness run (issue #39) reports four upstream providers and thirteen
model families the knowledge base cannot resolve — among them high-traffic releases (ByteDance
Seed, poolside Laguna, Thinking Machines Inkling) whose flows currently classify as `unknown`.
Until each item is assigned by hand or acknowledged with a reason, the review queue cannot
converge and real gaps drown in resolved noise.

## What Changes

- Add a bundled provider entry `scx_ai` (SCX.ai Holdings, ASX-listed Australian sovereign-AI
  inference platform): endpoint host `api.scx.ai`, jurisdiction `au`, sovereignty bloc `au`.
- Record drift aliases for litellm's rebranded DashScope routes — `qwencloud` (international)
  and `qwen_ai_platform` (mainland) → `alibaba_dashscope`; both configured hostnames
  (`dashscope-intl.aliyuncs.com`, `dashscope.aliyuncs.com`) are already bundled.
- Record a drift alias `bing_grounding` → `azure_foundry`: litellm's Grounding-with-Bing
  wrapper calls the customer's Foundry project endpoint (`*.services.ai.azure.com`), which the
  KB already covers; `bing_grounding/search` is filed as structural residue (a search tool,
  not a model).
- Add provenance patterns resolving the twelve remaining model families, with blocs confirmed
  by the maintainer 2026-09-08:
  - `cn` — ByteDance `Seed`, Baidu `CoBuddy`, StepFun `Step`
  - `us` — Microsoft `MAI`, Google `nano-banana`, Microsoft Research `multilingual-e5`,
    Thinking Machines Lab `Inkling`, poolside `Laguna`, PrismML `Ternary-Bonsai`,
    BigScience/Hugging Face `mt0`
  - `eu` — JetBrains `Mellum`
  - `sg` — MindAI `Macaron`
- Bump the review dates of the touched knowledge-base files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `jurisdiction-classification`: SCX.ai endpoints resolve to provider `scx_ai` with
  jurisdiction `au`.
- `model-provenance`: the twelve drift-run model families resolve to their developer
  organisations' blocs.

## Impact

- `borderlint/data/providers.json` (+1 entry), `sovereignty.json` (+1 mapping),
  `provenance.json` (+36 patterns — family stems, org prefixes, and hub-qualified route
  literals per design D3), `scripts/kb_drift_aliases.json` (+3 aliases, +1 residue entry).
- Detection tests for the new endpoint and pattern resolutions; KB website and evidence pack
  render the new provider from the bundled data with no code change.
- Freshness issue #39's actionable sections drop from 4 providers + 13 families to zero.

## Non-goals

- No data-practice curation: `scx_ai` joins the data-practice gap queue honestly, and the 93
  existing gaps remain the separate ongoing curation backlog.
- No SDK keys for `scx_ai` until official package coordinates are verified (the SDK-coverage
  check will surface the gap).
- No scanner-side handling of the alias names: aliases live in the dev-side suppression file
  only and never become provider entries.
