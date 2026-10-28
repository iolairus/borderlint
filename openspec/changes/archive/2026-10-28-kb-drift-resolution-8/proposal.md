# Proposal: kb-drift-resolution-8

## Why

The 2026-10-26 weekly freshness refresh (issue #39) reports one uncovered upstream provider
and three unresolved model families; the wave grew during implementation (2026-10-27) with a
second Azure region namespace (`azure/us/`) and Baseten's new in-house decision-model line.
The structural twist: Azure's namespace has grown region segments (`azure/eu/o1`,
`azure/us/o1`), and the new provider is OpenCode's subscription gateway carrying thirty-one
models, of which exactly one id fails to resolve. Until each item is assigned by hand, these
flows classify as `unknown` and the review queue cannot converge.

## What Changes

- Add a bundled provider entry for `opencode_go`: OpenCode Go, the hosted inference
  subscription from Anomaly Innovations, Inc. (the SST team, San Francisco; Delaware
  governing law). Endpoint host `opencode.ai` (the single host serving
  `/inference/go/...`; no separate API host exists), jurisdiction `us`, sovereignty `us`,
  category `aggregator` — it is a multi-vendor subscription gateway. The note records the
  shared-site host caveat, the EU+US default processing regions, and that per-model
  retention/training terms vary by upstream vendor (the Go docs' privacy table is the
  authoritative source, and two catalog entries — the Muse Spark contributor tiers —
  train on prompts by default).
- Add provenance patterns for the four families:
  - `us` — qualified `azure/eu/o1`, `azure/eu/o3`, `azure/us/o1`, and `azure/us/o3` →
    OpenAI: the only bare-form ids in the new region-segmented `azure/<region>/`
    namespaces that fail to resolve. The versioned siblings (`azure/eu/o1-mini`,
    `azure/us/o4-mini-2025-04-16`, …) already resolve via the drift suffix walk against
    the existing dash-anchored `o1-`/`o3-`/`o4-` patterns; only the bare `o1`/`o3` forms
    needed qualified entries, and NO bare `o1`/`o3` stems are added (the dash anchor
    exists precisely to keep those short stems safe).
  - `us` — one hub-qualified `cloudflare/clairic` pattern (the wave-4 `clef` precedent;
    the `@cf/` form resolves through it via the suffix walk): Clairic is Cloudflare's
    own Workers AI extraction model, announced 2026-10-19, no base lineage disclosed —
    own model until lineage says otherwise.
  - `cn` — `step-5` (bare, version-anchored like the existing `step-3.`) and qualified
    `opencode_go/step-5` → StepFun: Step 5 Preview is StepFun's flagship agentic model
    (Shanghai entity confirmed via the vendor's own platform footer: Shanghai ICP filing
    and CAC generative-AI model filing), open weights under the StepFun Model License.
  - `cn` — Baseten's in-house decision models elephant-1 (9B) and mammoth-1 (27B),
    announced 2026-10-21: trained by Baseten's Base Labs as full fine-tunes of
    Qwen3.5-9B and Qwen3.5-27B respectively (HF cards state the base models explicitly;
    MIT license), so the fine-tunes-inherit-base rule assigns Alibaba's bloc with the
    organisation label naming base and tuner (the Bespoke Nimble / Drex precedent).
    Patterns: the two observed litellm forms under `baseten/decision-models/` and the
    two open-weights HF forms under `baselabs/`. NO bare `elephant`/`mammoth` stems —
    common English words with no dash anchor worth claiming.
- Bump the review dates of the touched knowledge-base files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `jurisdiction-classification`: one new hosted provider resolves with a documented
  endpoint host, jurisdiction `us`.
- `model-provenance`: the drift-run families resolve — four Azure region-namespace ids
  to OpenAI's bloc, Cloudflare's new own model, StepFun's Step-5 line, and Baseten's
  Qwen-derived decision models.

## Impact

- `borderlint/data/providers.json` (+1 entry), `sovereignty.json` (+1 `us` mapping),
  `provenance.json` (+11 patterns), tests.
- Issue #39's actionable sections drop from 1 provider + 4 families to zero. The
  data-practice gap queue grows 98 → 99 (OpenCode Go publishes a per-model privacy
  table worth curating later).

## Non-goals

- No data-practice curation: the gap queue stays the declared standing backlog.
- No scanner or checker changes: every item resolves via KB data.
- No structural fix for `azure/<region>/`: a passthrough-style treatment would need bare
  `o1`/`o3` stems to be safe against. Two regions (`eu`, `us`) surfaced within two days;
  a third region surfacing in a future wave is the trigger for revisiting this as a
  structural rule in a separate change.
- No patterns for `opencode_go`'s other catalog ids: all thirty remaining models resolve
  through existing family patterns via the suffix walk (`kimi-k3` → Moonshot, `glm-5.3`
  → Zhipu, `beam-free` → Reflection AI via `beam`, and so on). `hy3`/`hy4-preview`
  already resolve through the Hunyuan patterns.
- No region-prefix handling for the `azure/<region>/` segments themselves — they are not
  added to passthrough orgs (they carry no provenance, but stripping them would expose
  the bare `o1`/`o3` collision surface with no compensating benefit at this wave's
  size).
