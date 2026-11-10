# Design: kb-drift-resolution-10

## Research basis (all primary sources, 2026-11-10)

- **empiriolabs** — EmpirioLabs.ai LLC, "a New Mexico limited liability company"
  (empiriolabs.ai/terms-of-service §1; governing law New Mexico, §16); GitHub org footer
  Seattle, WA (github.com/EmpirioLabs-ai). OpenAI-compatible endpoint
  `https://api.empiriolabs.ai/v1` (docs.litellm.ai/docs/providers/empiriolabs and every
  model page). Multi-vendor: ToS §1/§3 state the service "connects users to various AI
  models from multiple sources… not owned by the model developers"; each catalog page
  discloses the upstream author (Perplexity ids labeled "Author: Perplexity,
  Proprietary Endpoint"; step/stepaudio "Author: StepFun"; seed "ByteDance";
  skylark-embedding-vision "Author: ByteDance, region Malaysia, alias
  byteplus/doubao-embedding-vision"; fugu "Author: Sakana AI"). Only `aplomb-1` is
  labeled first-party ("Author: EmpirioLabs, Native Inference").
- **hostinger_router** — Hostinger AI Router (hostinger.com/support "What is Hostinger
  AI Router"; docs.litellm.ai/docs/providers/hostinger_router; keys prefixed
  `sk-hstgr-`). Endpoint `https://router.hostinger.com/v1`, serving `/chat/completions`,
  `/responses`, `/messages`, and `/embeddings` — OpenAI- and Anthropic-compatible
  (litellm docs; Hostinger support article), billed in Hostinger AI credits.
  Contracting entities per
  the Universal ToS §2/§18: HOSTINGER INTERNATIONAL LIMITED (Cyprus) for most
  countries, plus UK/Indonesia/Singapore/Luxembourg entities; payments via HOSTINGER,
  UAB (Kaunas, Lithuania); governing law and courts: Luxembourg (§22). Multi-vendor
  gateway reselling OpenAI/Anthropic/Google/xAI models; upstream inference locations
  not disclosed.
- **wally** — Wally, hosted inference by RunAnywhere, Inc. (Delaware C-corp, principal
  place of business Redwood City, CA — SEC Form D, sec.gov EDGAR 2092245; YC W26).
  Fixed catalog of open-weight models (DeepSeek, GLM) behind
  `https://inference.runanywhere.ai/v1` (runanywhere.ai/legal/terms §2;
  docs.litellm.ai/docs/providers/wally). Zero data retention for prompt/completion
  bodies by default (runanywhere.ai/legal/privacy).
- **seed-2-*** — ByteDance Seed 2.0 family (Pro/Code/Lite/Mini) and 2.1 (Pro/Turbo):
  official launch post seed.bytedance.com/en/blog/seed-2-0-official-launch; proprietary,
  closed weights. Beijing, cn.
- **step-3-5-flash / step-3-7-flash** — StepFun (Shanghai, cn): Step 3.5 Flash released
  2026-01-29, 196B sparse MoE, open weights stepfun-ai/Step-3.5-Flash (Apache-2.0);
  Step 3.7 Flash is a vision-language MoE built on Step 3.5 Flash. The dash ids are
  reseller normalizations of the dotted upstream names.
- **stepaudio-2-5-chat / stepaudio-3-chat** — StepFun Step-Audio chat models (family:
  github.com/stepfun-ai/Step-Audio2, arXiv 2507.16632); chat variants are proprietary,
  API-only. cn.
- **tongyi-embedding-vision-flash / -plus** — Alibaba Cloud Model Studio multimodal
  embedding models (alibabacloud.com/help/en/model-studio/tongyi-embedding-vision-flash;
  the 2026-03-06 snapshot is Qwen3-based per help.aliyun.com). Proprietary, API-only.
  cn.
- **skylark-embedding-vision** — ByteDance Skylark (云雀) multimodal embedding served on
  Volcengine ModelArk / BytePlus (docs.byteplus.com/en/docs/ModelArk/2310403).
  Proprietary, API-only. cn.
- **fugu-*** — Sakana AI (Tokyo, jp): Fugu is a learned multi-agent orchestration
  model coordinating a pool of frontier LLMs (arXiv 2606.21228); fugu-ultra-v2 listed
  on OpenRouter; proprietary, API-only. `fugu-max` is likely a reseller-side tier name
  (not found in Sakana's own sources) — same family either way.
- **aplomb-1** — EmpirioLabs' first in-house model (empiriolabs.ai/blog/introducing-
  aplomb-1): a fine-tune of Qwen3.5-4B (5.3B params, 1M context, Qwen3-Omni audio
  encoder, custom decision head), open weights under the custom EmpirioLabs Model
  License (HF org empiriolabsai). Inherits the Qwen bloc per the fine-tune rule.
- **jina-reranker-m0 / jina-reranker-v3.5** — Jina AI GmbH, Berlin (jina.ai/legal; HRB
  218021). m0: multilingual multimodal reranker, Qwen2-VL-2B-Instruct base + LoRA
  (huggingface.co/jinaai/jina-reranker-m0). v3.5: 0.6B listwise reranker, Qwen3-0.6B
  base (huggingface.co/jinaai/jina-reranker-v3.5). Both CC BY-NC 4.0. The Qwen bases
  are documented on the cards, so the fine-tunes-inherit-base rule assigns cn with the
  org naming base and tuner.
- **grok4.6** — xAI (us): Grok 4.6 released 2026-08-12; the official API id is the
  dashed `grok-4.6` (docs.oracle.com generative-ai release notes serve it as
  `xai.grok-4.6`); `grok4.6` is the undashed provider-alias form. Proprietary.
- **Ripple-65B-Preview** — Ricursive Intelligence (Palo Alto; co-founders Anna Goldie
  and Azalia Mirhoseini): 64.8B dense model pretrained from scratch on 12T tokens,
  Apache-2.0 open weights (HF org ricursiveAI). us.
- **rnj-1-instruct** — Essential AI (San Francisco; co-founded by Ashish Vaswani and
  Niki Parmar): 8B dense model trained from scratch, Apache-2.0 open weights
  (gigazine.net 2025-12-08 report quoting Vaswani). us.
- **glimpse-1.0** — Elorian AI (Palo Alto; founded 2025 by Andrew Dai, Yinfei Yang,
  Seth Neel): post-trained from an UNNAMED open-weights base; research preview, no
  weights released. Base lineage undisclosed in every located source → residue.

## Decisions

- **D1 — `empiriolabs` is an aggregator with author-disclosed catalog pages.** Category
  `aggregator` (its own ToS declares multi-source resale), jurisdiction us. No tier-2
  default: 22 of 23 ids are third-party. The note records that per-model author
  disclosure exists on the vendor's own pages — which is what makes the pattern-level
  attributions below honest rather than guessed.
- **D2 — Hostinger is `eu` via its contracting entities, not Lithuanian-specific.** The
  KB codes jurisdictions, and the Router's contracting entities are all EU/UK/SG/ID
  with Luxembourg governing law; `eu` is the honest bloc. The Kaunas group HQ is
  recorded in the note.
- **D3 — Wally is a us host of cn-origin weights — two different axes.** Provider
  jurisdiction/sovereignty is `us` (Delaware corp, Redwood City); the served models
  keep their own provenance (DeepSeek/GLM patterns already cover the catalog). No
  tier-2 default.
- **D4 — Dash-normalization anchors sit beside the dot anchors.** `seed-2-` and
  `step-3-` mirror `seed-2.`/`step-3.` for reseller-normalized dash ids
  (`seed-2-0-code`, `step-3-5-flash`). Both remain version-anchored; no bare `seed` or
  `step` stem is touched.
- **D5 — Reseller namespaces get qualified patterns; family names get anchored
  stems.** `empiriolabs/perplexity-` is qualified (no bare `perplexity-` stem —
  Perplexity's own naming space is not claimable by a reseller prefix elsewhere).
  `fugu-`, `stepaudio-`, `tongyi-embedding-vision`, `skylark-embedding`, `aplomb-1`,
  `ripple-65b`, `rnj-1`, `grok4.` are all anchored forms of distinctive names;
  `skylark` and `ripple` deliberately keep their qualifiers (common English words).
- **D6 — Two Jina rerankers inherit the Qwen bloc; the rest of the Jina line does
  not move.** m0 and v3.5 document Qwen bases on their HF cards, so the
  fine-tunes-inherit-base rule applies with the org naming base and tuner (`Alibaba
  (Jina AI post-train)`). The patterns are exact version-anchored stems so the
  jina-bert-based v1/v2/v3 line (own lineage, eu via the `jina_ai` default) is not
  swept in. The `jina_ai` tier-2 default is unchanged.
- **D7 — Aplomb-1 inherits the Qwen bloc despite being the vendor's first-party
  model.** First-party hosting does not change provenance: the base is Qwen3.5-4B
  (blog-stated), so `aplomb-1` → `Alibaba (EmpirioLabs post-train)`, cn.
- **D8 — Glimpse-1.0 is residue.** Developer confirmed (Elorian AI, Palo Alto), but
  the base model is unnamed in every located source. Per the Drex v1.0 precedent the
  id is accepted as unknown residue with a dated judgment rather than guessing the
  developer's bloc onto an undisclosed base.

## Risks / follow-ups

- `empiriolabs`'s catalog will keep growing; each new family surfaces in drift as
  usual. The qualified `empiriolabs/perplexity-` pattern means future perplexity-* ids
  there inherit honestly (author disclosed).
- If Sakana publishes `fugu-max` as a real tier (or not), the `fugu-` stem covers both
  cases — org unchanged.
- If Elorian discloses Glimpse's base, replace the residue entry with a pattern
  (and the bloc follows the base).
- Hostinger may publish upstream inference locations later; the note says what evidence
  would refine the entry.
