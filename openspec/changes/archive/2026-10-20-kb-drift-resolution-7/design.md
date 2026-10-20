# Design: kb-drift-resolution-7

## Research basis (all primary sources, 2026-10-20)

- **coralbricks** — `litellm/llms/openai_like/providers.json` registers base URL
  `https://inference.coralbricks.ai/v1`. CoralBricks (San Francisco; Afore-backed)
  serves Z.ai GLM-5.3 and DeepSeek V4.1 Flash FP4 variants (coralbricks.ai, /trust).
- **inferenceapis** — same litellm config registers `https://api.inferenceapis.com/v1`.
  A one-person gateway (Taylor Hawkes) over Together AI + DeepInfra; all infrastructure
  US (inferenceapis.com/about, /terms, /trust). Legal entity/state not stated anywhere —
  jurisdiction `us` rests on the named US operator and all-US processing, and the note
  records the gap.
- **nace** — `litellm/llms/nace/decisions/transformation.py` defaults to
  `https://console.nace.ai` (`POST /v1/systemone`); the vendor's HF model cards document
  `https://drex.nace.ai` as the same API. Nace.AI, Inc., Delaware corp, Palo Alto;
  California governing law; US processing (console.nace.ai/terms, /privacy).
- **openinfer** — litellm `constants.py` lists `https://api.openinfer.ai/v1` as an
  openai-compatible provider (no dedicated handler). OpenInfer, Inc., San Mateo, CA
  (openinfer.io/terms, /privacy). Serves third-party open weights under its `@oi/`
  namespace. NB: a different `openinfer-project` (open-infer.org) exists — not the
  litellm target; the KB records only the `api.openinfer.ai` entity.
- **semantic** — Google's Ranking API (Vertex AI Agent Builder / Discovery Engine):
  `semantic-ranker-default/fast-00N`, Google-developed (cloud.google.com
  /generative-ai-app-builder/docs/ranking).
- **sam** — `meta/sam-3.1` on the Meta Model API: SAM 3.1, Meta's Segment Anything line
  (github.com/facebookresearch/sam3, release notes 2026-03-27).
- **happyhorse / wan** — Alibaba video families on DashScope (alibabacloud.com Model
  Studio docs are the canonical API reference; Wan-AI / Wan-Video are Alibaba Tongyi's
  publishing orgs). HappyHorse is closed/API-only; no primary source ties it to a Wan
  (or any) base — lineage undisclosed, org label plain `Alibaba`. Wan2.2 builds on
  Wan2.1 per the Wan2.2 README; 2.7/3.0 continue the vendor series.
- **beam** — Reflection AI's first open-weight model: 501B-A23B MoE, pretrained from
  scratch on 23.8T tokens, Apache-2.0 (reflection.ai/blog/introducing-beam,
  /beam-is-available; HF org `reflection`). Launch partners Baseten, Together AI,
  Nebius — the three observed litellm namespaces.
- **drex** — Nace's decision models (github.com/nace-ai/drex-decision-models README +
  HF cards): v1.5 post-trains Xiaomi MiMo-V2.6-Distill-Qwen-9B; v2.0 (= current
  `drex-latest`) uses a Qwen3.6-35B-A3B backbone; v1.0 lineage undisclosed in every
  primary source.

## Decisions

- **D1 — Four providers, all `us`/`us`, documented hosts only.** coralbricks
  `inference.coralbricks.ai`; inferenceapis `api.inferenceapis.com`; nace both
  `console.nace.ai` (litellm default) and `drex.nace.ai` (vendor-documented same
  service); openinfer `api.openinfer.ai`. Each note carries its caveat: CoralBricks'
  SCC-based outside-US processing, Inference APIs' unestablished legal entity, Nace's
  dual hostnames, OpenInfer's customer-selected regions and the open-infer.org
  disambiguation.
- **D2 — `inferenceapis` is category `aggregator`.** It owns no models and resells
  Together AI / DeepInfra capacity behind one key — the aiml/aihubmix shape. The other
  three are plain multi-model inference hosts.
- **D3 — No tier-2 defaults anywhere in this wave.** coralbricks/openinfer/inferenceapis
  are multi-vendor; Nace serves only its own models but its lineage is mixed (v1.5/v2.0
  cn-inherited, v1.0 undisclosed), so a default would guess on v1.0.
- **D4 — Collision guards: qualified `meta/sam`, anchored `wan2.`/`wan3.`.** A bare
  `sam` prefix-matches `sambanova` and any `sam*` id; a bare `wan` prefix-matches every
  `wandb/<org>/<model>` id (wandb is not a passthrough org). HappyHorse and Beam are
  collision-free stems in the current price map (verified), so bare `happyhorse` and
  `beam` follow the `chirp` precedent.
- **D5 — Drex resolves version by version; v1.0 is honest residue.** v1.5 and v2.0
  inherit Alibaba's bloc (Qwen-lineage bases; the Bespoke Nimble / Strands Decider
  precedent) with org label `Alibaba (Nace Drex post-train)`. v1.0's lineage is
  undisclosed — recorded in `kb_drift_aliases.json` residue as accept-unknown rather
  than guessed. `drex-latest` currently targets v2.0 and is assigned `cn` with a
  moving-alias caveat: versioned patterns make any future `drex-v3.0` surface in the
  drift report, but `-latest` will silently track whatever Nace retargets — re-review
  on the next Drex release.
- **D6 — Beam gets bare + HF-org + the three host-qualified forms.** All three hosting
  namespaces (`baseten/`, `together_ai/`, `nebius/`) are observed in the price map, and
  the HF org form `reflection/Beam-1.0-*` is the primary distribution of an Apache-2.0
  open-weight model — all plausible code literals, so all are patterns.
- **D7 — No qualified `dashscope/` patterns.** Namespaced DashScope ids were never given
  qualified patterns (`dashscope/qwen-turbo` resolves via the tier-2
  `alibaba_dashscope` default, which is the same `cn` bloc); the bare stems cover the
  drift suffix walk and un-namespaced literals. Adding a one-off qualified form here
  would break the convention without changing any outcome.

## Risks

- **`drex-latest` is a moving alias** (D5): mitigated by versioned patterns surfacing
  new releases and by the design note; accepted residual risk.
- **Bare `beam`/`happyhorse` could collide with future unrelated ids** (D4): accepted
  house-style risk, same as `chirp`; the weekly drift run is the tripwire — a colliding
  family would surface as misassigned and be corrected.
- **Inference APIs is a one-person operation** (D1/D2): jurisdiction `us` rests on the
  operator's identity and all-US infrastructure rather than a corporate seat; the note
  records the entity gap so a future re-review can downgrade to `unknown` if facts
  change.
- **Nace dual hostnames** (D1): both recorded; if the vendor retires one, endpoint
  matching still lands on the other.
