# Design: kb-drift-resolution-8

## Research basis (all primary sources, 2026-10-26)

- **opencode_go** — OpenCode Go, the subscription inference offering from Anomaly
  Innovations, Inc. (the SST/OpenCode team; SF address, Delaware governing law per
  opencode.ai/legal/terms-of-service, eff. 2026-08-15). litellm's
  `litellm/llms/opencode/common_utils.py` defaults to `https://opencode.ai/inference/go/…`
  — a single host shared with the product site, path-scoped. Go is explicitly
  multi-vendor (OpenAI, Anthropic, Google, xAI, Zhipu, Moonshot, Meituan, StepFun,
  Xiaomi, MiniMax, Alibaba, DeepSeek, Meta). The docs/go privacy table records per-model
  terms: most 0-day/no-training, Claude Haiku 5.5 and the GPT Luna tiers 30-day vendor
  logs, Muse Spark contributor tiers train by default, DeepSeek under a monthly-renewed
  ZDR agreement.
- **azure/eu/o1, azure/eu/o3** — the Azure namespace in litellm's price map has grown a
  region segment (12 `azure/eu/o*` ids on 2026-10-26, joined by 12 `azure/us/o*` ids on
  2026-10-27 — ids priced from the Azure retail-prices API, Foundry Models, eastus). Per
  namespace, ten resolve via the drift suffix walk against the existing dash-anchored
  `o1-`/`o3-`/`o4-` patterns; only the two bare forms fail.
- **baseten/decision-models/** — Baseten's in-house decision-model line (announced
  2026-10-21): elephant-1 (9B) and mammoth-1 (27B), trained by Baseten's Base Labs as
  full fine-tunes of Qwen3.5-9B and Qwen3.5-27B (HF cards `baselabs/elephant-1` /
  `baselabs/mammoth-1` state the base models; MIT license; System One API at
  `inference.baseten.co/v1/systemone`).
- **clairic** — Cloudflare's own System One extraction model on Workers AI, announced
  2026-10-19 on the Cloudflare blog; mode `extraction`; no base-model lineage disclosed
  in any primary source; open-weights release intended.
- **step-5-preview** — StepFun's flagship agentic model (600B-A27B MoE, 1M context), open
  weights on Hugging Face (`stepfun-ai/Step-5-Preview`, StepFun Model License 1.0).
  Developer jurisdiction confirmed from the vendor's own platform footer: Shanghai
  registered entity, Shanghai ICP filing, CAC generative-AI filing — bloc `cn`.

## Decisions

- **D1 — `opencode_go` is an aggregator on a shared site host.** Category `aggregator`
  (multi-vendor subscription gateway, the inferenceapis shape). Endpoint `opencode.ai`
  only — the host is shared with the marketing site and docs, but every payload to it is
  Anomaly Innovations/us regardless, so jurisdiction classification is unaffected; the
  note carries the path-scoping and per-model-terms caveats. No tier-2 default
  (multi-vendor).
- **D2 — Four qualified patterns fix the Azure region namespaces; no structural change.**
  `azure/eu/o1`, `azure/eu/o3`, `azure/us/o1`, and `azure/us/o3` → OpenAI/us. The region
  segments are NOT added to passthrough orgs: stripping `azure/<region>/` would expose
  bare `o1`/`o3`, and the KB deliberately keeps those dash-anchored (`o1-`, `o3-`) — a
  bare `o1` prefix would claim any future `o1…` id sight unseen. Two regions surfaced
  within two days of each other, which the proposal's non-goals note as one short of the
  structural-rule trigger; a third region revisits this in a separate change.
- **D3 — Clairic follows the clef precedent exactly.** One hub-qualified pattern
  `cloudflare/clairic` → Cloudflare/us; the `@cf/cloudflare/clairic` form resolves
  through it via the suffix walk. No lineage statement exists, so the own-model
  assumption stands with the same "until lineage says otherwise" caveat; the org label
  stays plain `Cloudflare`.
- **D4 — Step-5 gets the version-anchored stem, matching `step-3.`.** Bare `step-5` and
  qualified `opencode_go/step-5` → StepFun/cn. The existing `step-3.` pattern shows the
  house convention for this family (version-anchored, never bare `step`, which would
  collide with generic words like `step-up-7b`). The price map was checked: the only
  `step*` ids are StepFun's. HF-org forms (`stepfun-ai/Step-5-Preview`) already resolve
  via the existing `stepfun-ai/` pattern.
- **D5 — Baseten's decision models inherit the Qwen bloc.** elephant-1 and mammoth-1 are
  full fine-tunes of Qwen3.5-9B/27B (HF cards state the bases), so the
  fine-tunes-inherit-base rule assigns `cn` with the org label naming base and tuner —
  `Alibaba (Base Labs post-train)` — the same call as Bespoke Nimble, Strands Decider,
  and Drex. Patterns are the four documented forms only: the two litellm
  `baseten/decision-models/baseten-{elephant,mammoth}` forms and the two HF
  `baselabs/{elephant,mammoth}` forms. NO bare `elephant`/`mammoth` stems — common
  English words with no anchor, and the family is two models old. The
  `baseten/decision-models/` namespace is not given a wildcard pattern: a future Baseten
  decision model on a non-Qwen base would be silently misassigned by one, so new entries
  surface in the drift report instead.

## Risks

- **The Muse Spark contributor tiers train on prompts** (D1): this is a data-practice
  fact, recorded in the provider note now and curable properly when the data-practice
  queue reaches `opencode_go`; provenance resolution is unaffected.
- **`azure/<region>/` may recur with other regions** (D2): accepted — each new variant
  surfaces in the weekly drift run, and three or more occurrences justify a structural
  rule as a separate change.
- **Clairic's undisclosed lineage** (D3): if Cloudflare later documents a third-party
  base, the bloc flips in a follow-up wave — same handling clef would get.
