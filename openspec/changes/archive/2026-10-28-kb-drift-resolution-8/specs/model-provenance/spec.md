# model-provenance Delta

## ADDED Requirements

### Requirement: Azure region-namespace o-series, Clairic, Step-5, and Baseten decision models resolve provenance
The bundled provenance map SHALL resolve the following drift-run families, all patterns
matched case-insensitively, anchored, longest-first per the existing matching rules:

- The qualified `azure/eu/o1`, `azure/eu/o3`, `azure/us/o1`, and `azure/us/o3` forms →
  bloc `us`, organisation OpenAI: the Azure namespace has grown region segments, and
  only the bare forms fail to resolve (versioned siblings already match the
  dash-anchored `o1-`/`o3-`/`o4-` patterns via the suffix walk). NO bare `o1` or `o3`
  stem SHALL be added — the dash anchor is what keeps those short stems safe, and the
  region segments SHALL NOT be added to the passthrough orgs (stripping them would
  expose exactly that bare-stem surface).
- The hub-qualified `cloudflare/clairic` form → bloc `us`, organisation Cloudflare (the
  wave-4 `clef` precedent: the `@cf/cloudflare/clairic` form is covered through it via
  the suffix walk). Clairic is Cloudflare's own Workers AI extraction model with no
  disclosed base lineage — own model until lineage says otherwise.
- `step-5` (version-anchored, matching the existing `step-3.` convention) and the
  qualified `opencode_go/step-5` form → bloc `cn`, organisation StepFun (Shanghai
  entity, CAC-filed; Step 5 Preview is open weights under the StepFun Model License).
  NO bare `step` stem SHALL exist.
- The four documented Baseten decision-model forms —
  `baseten/decision-models/baseten-elephant`, `baseten/decision-models/baseten-mammoth`,
  and the HF-org forms `baselabs/elephant`, `baselabs/mammoth` → bloc `cn`, organisation
  naming base and tuner (`Alibaba (Base Labs post-train)`): elephant-1 and mammoth-1 are
  Base Labs full fine-tunes of Qwen3.5-9B and Qwen3.5-27B respectively (stated on the HF
  cards), so the fine-tunes-inherit-base rule assigns Alibaba's bloc. NO bare
  `elephant`/`mammoth` stems and NO `baseten/decision-models/` namespace wildcard SHALL
  exist — a future Baseten decision model on a non-Qwen base must surface in the drift
  report rather than inherit silently.

The `opencode_go` provider SHALL carry NO tier-2 provenance default: it is a
multi-vendor subscription gateway, and its catalog resolves model-by-model through the
existing family patterns.

#### Scenario: Azure region-namespace bare forms resolve qualified
- **WHEN** model references `azure/eu/o1`, `azure/eu/o3`, `azure/us/o1`, and
  `azure/us/o3` are detected
- **THEN** all four resolve to bloc `us` with organisation OpenAI

#### Scenario: Azure region-namespace versioned forms stay covered
- **WHEN** the drift coverage check evaluates the `azure/eu/o*` and `azure/us/o*` id
  sets (e.g. `azure/eu/o1-mini`, `azure/us/o4-mini-2025-04-16`)
- **THEN** every id counts as covered — the bare forms via the new qualified patterns,
  the versioned forms via the suffix walk against the pre-existing dash-anchored
  `o1-`/`o3-`/`o4-` patterns, which are unchanged

#### Scenario: Baseten decision models inherit the Qwen bloc
- **WHEN** model references `baseten/decision-models/baseten-elephant-9b-latest`,
  `baseten/decision-models/baseten-mammoth-27b-latest`, `baselabs/elephant-1`, and
  `baselabs/mammoth-1` are detected
- **THEN** each resolves to bloc `cn` with the organisation label naming base and tuner
  (`Alibaba (Base Labs post-train)`), per the fine-tunes-inherit-base rule, and no bare
  `elephant` or `mammoth` stem exists

#### Scenario: Clairic resolves qualified; the hub form is covered by the suffix walk
- **WHEN** a model reference `cloudflare/clairic` is detected, and the drift coverage
  check evaluates `cloudflare/@cf/cloudflare/clairic`
- **THEN** the reference resolves to bloc `us` with organisation Cloudflare, and the hub
  form counts as covered via the suffix walk against the same pattern (the wave-4 `clef`
  precedent)

#### Scenario: Step-5 resolves bare and qualified
- **WHEN** model references `step-5-preview` and `opencode_go/step-5-preview` are
  detected
- **THEN** both resolve to bloc `cn` with organisation StepFun

#### Scenario: Short stems stay guarded
- **WHEN** hypothetical references `o1-preview-clone`, `step-up-7b`, or `o3unknown` are
  detected
- **THEN** none resolves through any new pattern (no bare `o1`, `o3`, or `step` stems
  exist); `o1-preview-clone` still resolves through the pre-existing dash-anchored
  `o1-` pattern exactly as before, and `step-up-7b` keeps provenance `unknown`

#### Scenario: OpenCode Go catalog is covered model-by-model; unbound flows stay unknown
- **WHEN** the drift coverage check evaluates the `opencode_go` catalog (e.g.
  `opencode_go/kimi-k3`, `opencode_go/beam-free`), and separately an unbound flow on
  provider `opencode_go` carries no model reference
- **THEN** every catalog id except the newly-patterned `step-5-preview` counts as covered
  via the suffix walk against the existing family patterns (Moonshot, Reflection AI, and
  so on), and the unbound flow keeps provenance `unknown` (no tier-2 default on a
  multi-vendor gateway)
