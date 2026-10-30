# Design: kb-drift-resolution-9

## Research basis (all primary sources, 2026-10-30)

- **bigmodel** — BigModel.cn is Zhipu AI's domestic open platform
  (docs.bigmodel.cn/cn/guide/start/introduction). The user agreement names the operator
  北京智谱华章科技股份有限公司 (Beijing Zhipu Huazhang Technology Co., Ltd.) with PRC
  governing law and courts at Zhipu's seat
  (docs.bigmodel.cn/cn/terms/user-agreement §一, §十四). API host
  `open.bigmodel.cn/api/paas/v4` (quick-start doc). The model catalog is GLM/CogView/
  CogVideoX/GLM-TTS/Embedding/CodeGeeX — all Zhipu — plus Vidu Q1/Vidu 2 (ShengShu
  Technology) in the video section, and §九 is an explicit third-party-products clause.
- **streamlake** — StreamLake is "an AI cloud service platform under Kuaishou"
  (streamlake.ai homepage). LLM inference is branded Vanchin (万擎): chat completions at
  `https://vanchin.streamlake.ai/api/gateway/v1/endpoints/chat/completions`
  (streamlake.ai document DOC/mj9z6fh8lxn87i86jrp); the CN-site video task API is
  `wanqing.streamlakeapi.com` (streamlake.com document WANQING/mu3inlewmkqm9kgaijp).
  The international ToS names STREAMLAKE PTE. LTD., incorporated in Singapore, with
  Singapore governing law and SIAC arbitration (§1.1, §11, §12). Parent Kuaishou
  Technology is headquartered in Beijing (HKEX filings). The platform advertises
  third-party models (e.g. DeepSeek) alongside its proprietary KAT-Coder line —
  multi-vendor.
- **kyma** — "Kyma API is a service of Affitor LLC, a Wyoming limited liability
  company" and "Kyma API is an aggregator… the actual computation happens on
  third-party AI infrastructure" (kymaapi.com/terms); "Kyma is operated from the
  United States" and DeepSeek-direct routes "are processed on infrastructure operated
  by DeepSeek in the People's Republic of China" (kymaapi.com/privacy). Governing law
  is Wyoming with exclusive forum in Wyoming state and federal courts (terms §15);
  the DMCA/mailing address is 2 Townsend St, San Francisco (terms §11, §17).
  OpenAI-compatible base `https://kymaapi.com/v1` (homepage quickstart). Unrelated to
  SAP's Kyma Kubernetes runtime.
- **aiand** — ai& Inc., registered office Queen's Tower A, 2-3-1 Minatomirai,
  Yokohama; governing law Japan, Tokyo District Court / JCAA Tokyo
  (aiand.com/legal/inference-terms-of-service §M.7, aiand.com/terms §14/§16).
  OpenAI- and Anthropic-compatible APIs at `https://api.aiand.com` (docs.aiand.com).
  Hosted Models are
  "created and licensed by a third party (the 'Model Provider')" (§A.2) — a
  multi-vendor host on its own Japan infrastructure; §C.2 commits that Customer Content
  is processed in Japan and not transferred outside Japan.
- **clf_ai_gateway** — CLF AI Gateway (clfaigateway.dev), "not affiliated with
  Cloudflare" (litellm provider docs); its data policy discloses that inference runs on
  Cloudflare Workers AI (`x-gw-provider: cloudflare-workers-ai` on every response).
  Terms governed by the laws of Vietnam (clfaigateway.dev/terms); payments are
  VN-first (VietQR/payOS) with Dodo Payments as merchant of record. Endpoint
  `https://api.clfaigateway.dev/v1`. Serves GLM, Kimi, DeepSeek, Qwen — multi-vendor.
- **zerogpu** — ZeroGPU, Inc. (zerogpu.ai), an "edge inference cloud" behind one
  OpenAI-compatible API (`https://api.zerogpu.ai/v1`); terms governed by the laws of
  the State of Texas, venue Travis County (zerogpu.ai/terms). NOT Hugging Face's
  ZeroGPU Spaces hardware tier — no relation (HF's own docs describe ZeroGPU as a
  Spaces hardware option, not an API provider). Serves OpenAI, Llama, Qwen, DeepSeek,
  GLM, LFM — multi-vendor.
- **refuseless** — refuseless.com hosts a fixed four-model lineup
  (`glm-5.3-abliterated`, `glm-5.3-flash-abliterated`, `deepseek-v4.1-flash-abliterated`,
  `deepseek-v4.1-flash-fast`) behind `https://api.refuseless.com/v1`
  (refuseless.com/docs). The ToS and privacy policy name no legal entity, no
  jurisdiction, and no governing-law clause — operator undisclosed. The `abl_` API-key
  prefix hints at the Catyonic OÜ (abliteration.org) operator but is unproven.
- **abliteration** — the HF org `abliteration` / abliteration.org, operated by Catyonic
  OÜ, Tallinn (stated on the HF org page), is a model catalog: it hosts zero models on
  HF (`api/models?author=abliteration` → `[]`) and its paid "API" is catalog metadata
  only. Not an inference provider.
- **eu_jev** — eu/jev (eu-jev.com) is "operated by Bevelites GmbH, Schleißheimer Str.
  188, 80797 München, Amtsgericht München, HRB 303590" with German governing law and
  Munich venue (eu-jev.com/terms §1, §12). It runs only its own model — "eu/jev runs
  its own model, so a Jev model ID returns HTTP 400" (eu-jev.com/docs) — and "the
  application, database and model execution are hosted in Germany" on a Hetzner
  server, "no proxy, CDN, or external model API sits in between", with a GDPR DPA and
  subprocessor list (eu-jev.com). The API is compatible with TypeSafe's Jev
  `/v1/systemone` format but the vendor states it is "not affiliated with TypeSafe AI"
  (eu-jev.com/terms). Endpoint `https://eu-jev.com` (`POST /v1/systemone`). Model
  lineage is undisclosed by the vendor; an aggregator labels it a Winnow-12B
  (Gemma-4-based) fine-tune, which is not primary-source confirmed.
- **soniox stt family** — Soniox Inc., 1045 Helm Lane, Foster City, CA; California
  governing law (soniox.com/policies/terms-of-service §35/§37). First-party-only: the
  ToS forbids reselling the services, and the catalog is exclusively Soniox's own
  speech models (soniox.com/docs/stt/models lists `stt-rt-v5`, `stt-async-v5`, plus v3/v4
  and preview aliases). The bare `stt-rt-preview` id in the upstream list is a legacy
  integration form; Soniox docs only ever use versioned names.
- **lfm** — LFM2.5-1.2B-Instruct is Liquid AI's own model: Liquid AI is "spun out of
  MIT CSAIL" (liquid.ai/company), and the HF card (LiquidAI/LFM2.5-1.2B-Instruct) states
  LFM2.5 "builds on the LFM2 architecture with extended pre-training" — own lineage, no
  other vendor's base.
- **baseten-joey** — Baseten's announcement "Decisions for a penny: introducing
  joey-1" (baseten.co/blog) states joey-1 is post-trained from Qwen3.5-2B by Base Labs,
  Baseten's in-house research lab (Baseten Labs, Inc., Delaware corp, California
  governing law per baseten.co/terms-and-conditions). Same inheritance shape as wave-8's
  elephant/mammoth.
- **motif** — Motif-3 is "built from the ground up by Motif Technologies… fully
  in-house, proprietary design" (HF card Motif-Technologies/Motif-3, MIT license), a
  ~314B-total / 13B-active MoE per the model card and the arXiv technical report
  (arxiv.org/abs/2608.09119). Motif Technologies' own site records its selection as a
  national team for Korea's sovereign AI foundation model program, Ministry of Science
  and ICT (motiftech.io/en/contact). Bloc `kr` — consistent with the KB's existing use
  of country-code blocs in provenance patterns.
- **kyma/sonar** — UNCONFIRMED. Kyma's own site and status page do not enumerate a
  `sonar` model; no primary source identifies the upstream. The Perplexity-Sonar
  hypothesis cannot be confirmed from Kyma's or Perplexity's materials.

## Decisions

- **D1 — `bigmodel` is an alias of `zhipu`, not a new provider.** Implementation
  surfaced the decisive fact: `open.bigmodel.cn` has been an endpoint on the existing
  `zhipu` entry since before this wave, so a separate `bigmodel` entry would duplicate
  the host (endpoint matching already resolved to `zhipu`) and split one entity's
  record across two ids. The route name is recorded in `kb_drift_aliases.json`
  (`aliases: bigmodel → zhipu`), and the `zhipu` note is enriched with the research:
  operator entity, domestic/international split, and the Vidu nuance. The Vidu section
  does not disturb the pre-existing tier-2 `cn` default — ShengShu is also cn-bloc, so
  the default stays honest for every currently served id. Catalog ids
  (`bigmodel/glm-5.3*`) resolve through the existing GLM patterns via the suffix walk.
- **D2 — StreamLake classifies `cn` with the Singapore entity on the record.** The
  operating entity is Singaporean, but parent, technology, and proprietary models are
  Kuaishou/Beijing — the offshore-entity shape the KB already records for Chinese
  vendors. Both documented hosts go on the entry; the note carries the STREAMLAKE
  PTE. LTD. / SIAC facts so the cn call is auditable.
- **D3 — The three small gateways get exactly their evidenced classifications.**
  `kyma` = aggregator/us (its own terms declare aggregation and US operation; the note
  preserves its DeepSeek-PRC routing disclosure, which is a per-model data-flow fact,
  not the provider's jurisdiction). `clf_ai_gateway` = aggregator/vn (Vietnam governing
  law; the note records the Cloudflare Workers AI compute dependency so execution
  location is not conflated with legal jurisdiction). `zerogpu` = us with an explicit
  not-Hugging-Face note — the name collision is a live misconfiguration risk.
- **D4 — `refuseless` follows the `aihubmix` precedent: undisclosed operator →
  `unknown`.** Endpoint host documented, so the entry carries it; jurisdiction and
  sovereignty stay `unknown`, and the note separates facts (cn-base weights lineup)
  from the unproven Catyonic OÜ hint. The served ids already resolve provenance through
  the existing anchored `glm-5.3` / DeepSeek patterns via the suffix walk, so no new
  patterns are needed for its catalog.
- **D5 — `aiand` is `jp`; first new jurisdiction code since `au`.** Multi-vendor host,
  so no tier-2 default; the Japan data-residency clause (ToS §C.2) is recorded in the
  note as the jurisdiction-relevant fact. `motif-3` underneath it gets bloc `kr` —
  provenance follows the model's developer, not the host.
- **D6 — `eu_jev` gets both a brand-stem pattern and the tier-2 default.** The vendor
  serves only its own model, so `eu-jeff` is a safe dash-anchored brand stem: model
  references resolve at the pattern tier (the drift coverage check only credits
  provider defaults for speech-category providers, so a default alone would leave the
  family flagged). The first-party-only tier-2 default `eu_jev → eu` additionally
  covers unbound flows at runtime. Both classify by operator (Bevelites GmbH,
  Germany); if base-model lineage is ever disclosed, the pattern is revisited.
- **D6b — `vn` joins the sovereignty vocabulary.** The bloc vocabulary is a fixed
  frozenset in `borderlint/kb.py` (`_SOVEREIGNTY_BLOCS`), so the new code is added
  there alongside a `sources` entry citing Vietnam's Law on Cybersecurity 2018 and
  Personal Data Protection Law 2025 (in force 2026-01-01) — the same shape as the
  existing jp/kr/sg entries. This is vocabulary data, not a framework change: no
  matching, policy, or report behaviour changes.
- **D7 — Soniox gets a provider default, not `stt` patterns.** A bare `stt` stem is
  generic speech-to-text shorthand and unclaimable; version-anchored `stt-rt-`/
  `stt-async-` stems would still be claiming another vendor's vocabulary. Soniox is
  first-party-only (ToS resale prohibition, exclusive own-model catalog), which is
  exactly the tier-2 default's contract — `soniox/stt-rt-preview` and the versioned
  siblings all resolve `us` through it.
- **D8 — `lfm2.` takes the dot anchor; `motif-3` and `baseten-joey` take version/
  namespace anchors.** `lfm2.` mirrors the `step-3.` convention (dot-anchored version
  stems) and covers LFM2.5 and future LFM2.x point releases without claiming a bare
  three-letter stem. `motif-3` is version-anchored like `step-5`; no bare `motif`
  (common English word). `baseten/decision-models/baseten-joey` stays inside the
  documented namespace — NO `baseten/decision-models/` wildcard, so a future Base Labs
  model on a non-Qwen base still surfaces in the drift report (the wave-8 guard).
- **D9 — Two families are honestly accepted as unknown residue.** `abliteration/` ids
  are placeholders on a non-provider namespace with undisclosed per-id lineage, and
  `kyma/sonar` has no primary-source-identifiable upstream. Both go to
  `scripts/kb_drift_aliases.json` residue with dated judgments — the Drex v1.0
  precedent: accept unknown rather than guess a bloc.

## Risks / follow-ups

- `bigmodel`'s Vidu section means a future wave may need `vidu` patterns if litellm
  prices those ids; they are not in the current drift output, so nothing is claimed now.
- If `refuseless` ever names its operator, the `unknown` classification should be
  revisited — the note says what evidence would change it.
- `clf_ai_gateway`'s compute transits Cloudflare (us) infrastructure; a future
  execution-location feature would model that separately from legal jurisdiction.
- If Kyma ever documents `sonar`'s upstream (or drops the id), the residue entry
  should be removed or replaced with a real pattern.
