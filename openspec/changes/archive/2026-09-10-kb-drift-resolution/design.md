# Design: kb-drift-resolution

## Context

The 2026-09-07 freshness run left four provider names and thirteen model families in the
actionable queue. Research established each item's operator and jurisdiction; the maintainer
confirmed every bloc assignment on 2026-09-08. Three of the four provider names turn out to be
routes onto infrastructure the KB already covers (Alibaba DashScope's two hosts, Azure AI
Foundry's project endpoints), so only one genuinely new provider exists: SCX.ai, an ASX-listed
Australian sovereign-AI inference platform (`api.scx.ai`). One "family" (`search`) is the
`bing_grounding/search` tool id, not a model.

## Goals / Non-Goals

**Goals:**

- Drain issue #39's provider and model-family sections to zero actionable items, each
  resolution a recorded human judgment.
- Endpoint detection and sovereignty for SCX.ai — the KB's first `au` provider.
- Provenance resolution for the twelve genuine model families.

**Non-Goals:**

- No data-practice curation (for `scx_ai` or the existing 93-provider gap queue).
- No scanner-side changes: aliases and residue live only in the dev-side suppression file.
- No SDK keys for `scx_ai` until official package coordinates are verified.

## Decisions

### D1: Qwen rebrand routes are aliases, not provider entries

litellm's `qwencloud` (international) and `qwen_ai_platform` (mainland) are rebranded routes
onto DashScope — their configured hostnames are `dashscope-intl.aliyuncs.com` and
`dashscope.aliyuncs.com`, both already bundled under `alibaba_dashscope`. Adding provider
entries would duplicate detection for the same hosts; aliases record the judgment where the
drift checker reads it. Alternative rejected: a rename to a `qwen_*` id — churn with no
detection gain, and the DashScope hosts remain the ground truth.

### D2: `bing_grounding` aliases to `azure_foundry`; its `search` id is residue

litellm's Grounding-with-Bing wrapper calls the customer's Foundry project endpoint
(`*.services.ai.azure.com`), which `azure_foundry` already covers — so flows resolve today and
the honest record is an alias, not an ignore. An ignore (the SERP-tool precedent) would erase
the fact that this traffic rides a covered endpoint. `bing_grounding/search` is a tool id, not
a model, and is filed as structural residue with that reason.

### D3: Pattern stems are the most specific literal that covers the family

Several family stems are dangerously generic (`seed`, `step`, `mt`, `nano`, `multilingual`,
`search`); a bare-stem pattern would swallow unrelated future ids. Each new pattern therefore
uses the most specific stem that covers the family's actual members — org-qualified where the
upstream ids carry the org (`thinkingmachines/`, `bytedance/seed-`, `mindai/macaron-`),
version-qualified basenames otherwise (`nano-banana`, `multilingual-e5`, `mt0-`). The
implementation step enumerates the current members by running `scripts/kb_drift.py` and picks
stems from the real id list, mirroring how the checker matches `/`-suffixes. Because the
scanner's `match_model` is anchored at position 0 (no suffix walk), each observed
hub-qualified route also gets its own full-literal pattern (`deepinfra/bytedance/`,
`novita/mindai/`, …) — the same treatment `novita/xiaomimimo/` received. Tests pin one
unrelated near-miss per generic stem to `unknown`.

### D4: Bloc assignments follow the operator's legal home, maintainer-confirmed

All twelve assignments were confirmed 2026-09-08: `cn` — ByteDance Seed, Baidu CoBuddy,
StepFun; `us` — Microsoft MAI, Google nano-banana, Microsoft Research multilingual-e5,
Thinking Machines Lab Inkling, poolside Laguna (legal HQ US; Paris/London are satellites),
PrismML Ternary-Bonsai, BigScience mt0 (via Hugging Face, Inc., the workshop's lead); `eu` —
JetBrains Mellum (Amsterdam HQ, Prague hub — `eu` either way); `sg` — MindAI Macaron
(Singapore-incorporated Pte. Ltd.).

### D5: `scx_ai` reuses the existing `au` sovereignty vocabulary

The sovereignty map already defines `au` (TOLA 2018 + Privacy Act 1988) from the
bloc-vocabulary-completion change, so the first Australian provider entry needs no vocabulary
work: `jurisdiction: au` in `providers.json`, `scx_ai: au` in `sovereignty.json`.

## Risks / Trade-offs

- [Generic stems over-match future ids] → most-specific-stem rule (D3) plus a pinned
  near-miss test per generic stem.
- [litellm renames routes again] → alias validation already fails loudly when a target id
  vanishes; a rename resurfaces as a new drift item rather than rotting silently.
- [MindAI's operational footprint may weigh China over Singapore] → the bloc records the
  legal home, as everywhere else in the map; revisit if the corporate structure changes.

## Open Questions

- (none — all blocs confirmed 2026-09-08)
