# Proposal: kb-drift-resolution-9

## Why

The 2026-10-30 weekly freshness run reports nine uncovered upstream providers and seven
unresolved model families (issue #39's rendered body is stale at 2026-10-26; the local
drift run is the live figure). The wave is diverse: a domestic-China Zhipu surface, a
Kuaishou MaaS fronted by a Singapore entity, three small gateways (US, Vietnam,
operator-undisclosed), a Japan-resident open-weight host, an EU first-party decision
API, a US edge-inference cloud, and one Hugging Face catalog org that is not an
inference provider at all. Until each item is assigned by hand, these flows classify as
`unknown` and the review queue cannot converge.

## What Changes

- Alias `bigmodel` → `zhipu` and enrich the existing `zhipu` entry's note: BigModel.cn
  (智谱开放平台) is Zhipu AI's domestic-China open platform, and its host
  `open.bigmodel.cn` has been on the `zhipu` entry since before this wave — a separate
  provider entry would duplicate the endpoint and split one entity's record. The note
  now records the operator entity (Beijing Zhipu Huazhang, PRC governing law), the
  domestic/international split (api.z.ai), and that the catalog's Vidu section
  (ShengShu, also cn-bloc) makes it not strictly first-party while the pre-existing
  tier-2 `cn` default stays honest for every currently served id.
- Add seven bundled provider entries:
  - `streamlake` — StreamLake (Kuaishou), the "Vanchin" (万擎) MaaS. Endpoints
    `vanchin.streamlake.ai` (LLM gateway) and `wanqing.streamlakeapi.com` (video task
    API). The international service is operated by STREAMLAKE PTE. LTD. (Singapore
    governing law, SIAC arbitration), but parent, technology, and proprietary models
    are Kuaishou/Beijing — jurisdiction and sovereignty `cn` per the offshore-entity
    precedent (the `xiaomi_mimo` note shape), with the Singapore entity recorded in the
    note. Multi-vendor MaaS → NO tier-2 default.
  - `kyma` — Kyma API, an explicit multi-vendor aggregator run by Affitor LLC (Wyoming
    LLC, Wyoming governing law, "operated from the United States"). Endpoint
    `kymaapi.com`; jurisdiction and sovereignty `us`; category `aggregator`. Not SAP
    Kyma. The note records the provider's own disclosure that DeepSeek-direct routes are
    processed in the PRC.
  - `aiand` — ai& Inc. (Yokohama, Japan; Japanese governing law, Tokyo venue), a
    multi-vendor host serving third-party open weights from its own Japan-based
    infrastructure with contractual Japan data residency (Inference API ToS §C.2: no
    transfer of Customer Content outside Japan). Endpoint `api.aiand.com`; jurisdiction
    and sovereignty `jp`. NO tier-2 default (multi-vendor host).
  - `clf_ai_gateway` — CLF AI Gateway, an independent OpenAI-compatible reseller
    gateway, explicitly not affiliated with Cloudflare, whose inference upstream is
    Cloudflare Workers AI (its data policy discloses the `x-gw-provider:
    cloudflare-workers-ai` header). Terms governed by the laws of Vietnam; VN-first
    payments. Endpoint `api.clfaigateway.dev`; jurisdiction and sovereignty `vn`;
    category `aggregator`.
  - `zerogpu` — ZeroGPU, Inc., a US edge-inference cloud (Texas governing law, Travis
    County venue). Endpoint `api.zerogpu.ai`; jurisdiction and sovereignty `us`. The
    note records that it is NOT Hugging Face's ZeroGPU Spaces hardware tier — same
    name, unrelated product. Multi-vendor → NO tier-2 default.
  - `refuseless` — Refuseless, a hosted API serving a fixed four-model lineup of
    refusal-removed ("abliterated") GLM and DeepSeek weights. Endpoint
    `api.refuseless.com`; jurisdiction and sovereignty `unknown` — the ToS and privacy
    policy name no legal entity, no jurisdiction, and no governing law (the `aihubmix`
    precedent: undisclosed operator). The note records that the served weights derive
    from cn-base models and that the `abl_` API-key prefix hinting at Catyonic OÜ is
    unproven and not a KB fact.
  - `eu_jev` — eu/jev, a first-party "decisions" API operated by Bevelites GmbH
    (Munich; German governing law), serving only its own model (`eu-jeff-latest` /
    `eu-jeff-1.0.0`) with application, database, and model execution hosted in Germany.
    Endpoint `eu-jev.com`; jurisdiction and sovereignty `eu`. First-party-only →
    dash-anchored `eu-jeff` brand-stem pattern (bloc `eu`, classifying by operator
    while lineage is undisclosed) plus a tier-2 provenance default `eu` for unbound
    flows.
- Record `abliteration` in `scripts/kb_drift_aliases.json` (`ignore`): the abliteration
  HF org / abliteration.org is a model-catalog site operated by Catyonic OÜ (Tallinn)
  that hosts zero models and serves no inference — not a provider.
- Add provenance patterns and defaults for the resolvable families:
  - Tier-2 default `soniox` → `us`: Soniox is a first-party-only provider (its ToS
    forbids reselling the service; it serves only its own speech models), so the whole
    `stt` family (`stt-rt-preview`, `stt-rt-v3…v5`, `stt-async-*`) resolves through the
    provider default — the house rule for first-party-only providers. NO bare `stt`
    stem (generic speech-to-text shorthand, unclaimable).
  - `lfm2.` → Liquid AI, bloc `us`: LFM2.5 is Liquid AI's own architecture (MIT CSAIL
    spin-out, Cambridge MA), extended pre-training of LFM2 — dot-anchored per the
    `step-3.` convention; NO bare `lfm` stem.
  - `baseten/decision-models/baseten-joey` → `Alibaba (Base Labs post-train)`, bloc
    `cn`: joey-1 is post-trained from Qwen3.5-2B (Baseten's own announcement blog), so
    the fine-tunes-inherit-base rule applies — same org label as the wave-8
    elephant/mammoth entries.
  - `motif-3` → Motif Technologies, bloc `kr`: Motif-3 is a from-scratch 314B MoE
    ("fully in-house, proprietary design" per the HF card; Korea sovereign-AI national
    team member per the vendor site). Version-anchored; NO bare `motif` stem.
- Record two families as acknowledged residue in `scripts/kb_drift_aliases.json`:
  - `abliteration/` — catalog/placeholder ids (e.g. `abliteration/abliterated-model`)
    on a namespace that is not an inference provider; per-id lineage undisclosed.
  - `kyma/sonar` — a gateway id whose upstream model no primary source identifies
    (Kyma's own pages do not enumerate it; the Perplexity-Sonar hypothesis is not
    confirmable). Accept unknown rather than guess a bloc (the Drex v1.0 precedent).
- Bump the review dates of the touched knowledge-base files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `jurisdiction-classification`: seven new hosted providers resolve with documented
  endpoint hosts and jurisdictions (cn, us, jp, vn, us, unknown, eu), and the
  `bigmodel` route resolves to the existing `zhipu` entry (cn) via alias.
- `model-provenance`: the drift-run families resolve — the Soniox `stt` family via the
  first-party provider default, Liquid AI's LFM2.5 line, Baseten's third Qwen-derived
  decision model, and Motif-3; two families are honestly accepted as unknown residue.

## Impact

- `borderlint/data/providers.json` (+7 entries, `zhipu` note enriched),
  `sovereignty.json` (+7 mappings, +1 `vn` source citation),
  `provenance.json` (+4 patterns, +2 provider defaults),
  `borderlint/kb.py` (+1 sovereignty vocabulary token `vn`),
  `borderlint/report.py` (+1 sovereignty display name),
  `scripts/kb_drift_aliases.json` (+1 alias, +1 ignore, +2 residue reasons), tests.
- Issue #39's actionable sections drop from 9 providers + 7 families to zero. The
  data-practice gap queue grows 99 → 106 (seven new providers join the standing
  backlog), residue grows by the newly acknowledged ids.

## Non-goals

- No data-practice curation: the gap queue stays the declared standing backlog.
- No scanner or checker changes: every item resolves via KB data.
- No per-model provenance for `refuseless`'s lineup beyond what existing patterns
  already cover (`glm-5.3-abliterated` and friends resolve through the pre-existing
  anchored GLM/DeepSeek family patterns via the suffix walk).
- No new provider entry or provenance patterns for `bigmodel`: it aliases to `zhipu`
  (same company; its host was already on that entry), and its catalog ids resolve
  through the existing GLM-family patterns.
- No sovereignty-framework change: `jp` was already in the sovereignty vocabulary, and
  `vn` joins it as vocabulary data (one token in `borderlint/kb.py`'s
  `_SOVEREIGNTY_BLOCS` plus a `sources` citation in `sovereignty.json`) — no matching,
  policy, or report behaviour changes.
- No lineage claim for `eu-jeff`: the vendor names no base model, and the
  aggregator-reported Winnow-12B (Gemma-4-based) link is not primary-source confirmed —
  the tier-2 provider default classifies by operator (eu), and any future lineage
  disclosure revisits the pattern level.
