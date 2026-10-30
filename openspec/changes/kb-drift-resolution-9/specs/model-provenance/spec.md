# model-provenance Delta

## ADDED Requirements

### Requirement: Wave-9 provider defaults and anchored patterns resolve the drift families
The bundled provenance map SHALL resolve the following drift-run families, all patterns
matched case-insensitively, anchored, longest-first per the existing matching rules:

- Tier-2 provider default `soniox` → bloc `us`: Soniox is a first-party-only provider
  (its ToS forbids reselling the service and its catalog is exclusively its own speech
  models), which is exactly the provider-default contract. The whole `stt` family —
  the legacy unversioned `stt-rt-preview` form and the versioned `stt-rt-v3…v5` /
  `stt-async-*` ids — resolves through it. NO bare `stt`, `stt-rt`, or `stt-async`
  stem SHALL be added: speech-to-text shorthand is generic vocabulary that no single
  vendor may claim.
- `eu-jeff` → bloc `eu`, organisation Bevelites (eu/jev): eu/jev serves only its own
  decision model, so the dash-anchored brand stem is safe to claim; model references
  (`eu-jeff-latest`, `eu-jeff-1.0.0`, and the `eu_jev/`-qualified forms via the suffix
  walk) resolve at the pattern tier. The vendor discloses no base-model lineage, so
  the classification is by operator (Bevelites GmbH, Germany) — if lineage is ever
  disclosed, the pattern SHALL be revisited. A tier-2 provider default `eu_jev` →
  `eu` SHALL also exist: the provider is first-party-only, so unbound flows on the
  provider resolve by operator too. (The drift coverage check only credits provider
  defaults for speech-category providers, so the pattern — not the default — is what
  covers the `eu_jev/eu-jeff-*` ids there.)
- `lfm2.` → bloc `us`, organisation Liquid AI: LFM2.5 is Liquid AI's own architecture
  (MIT CSAIL spin-out) with extended pre-training over LFM2 — dot-anchored per the
  `step-3.` convention, covering LFM2.5 and future LFM2.x point releases. NO bare
  `lfm` stem SHALL exist.
- `baseten/decision-models/baseten-joey` → bloc `cn`, organisation naming base and
  tuner (`Alibaba (Base Labs post-train)`): joey-1 is post-trained from Qwen3.5-2B
  (Baseten's own announcement), so the fine-tunes-inherit-base rule assigns Alibaba's
  bloc — the same org label as the wave-8 elephant/mammoth entries. NO
  `baseten/decision-models/` namespace wildcard SHALL exist: a future Base Labs model
  on a non-Qwen base must surface in the drift report rather than inherit silently.
- `motif-3` → bloc `kr`, organisation Motif Technologies: Motif-3 is a from-scratch
  314B MoE ("fully in-house, proprietary design" per the model card) from a Korean
  sovereign-AI national-team lab. Version-anchored; NO bare `motif` stem SHALL exist
  (common English word).
- The providers `streamlake`, `kyma`, `aiand`, `clf_ai_gateway`, `zerogpu`, and
  `refuseless` SHALL carry NO tier-2 provenance default: each is multi-vendor
  (or, for refuseless, multi-lineage), so their catalogs resolve model-by-model through
  the existing family patterns. (`bigmodel` is not a new provider: it aliases to the
  existing `zhipu` entry, whose pre-existing tier-2 `cn` default is unchanged — honest
  for the whole current catalog since the third-party Vidu models are also cn-bloc.)
- The families `abliteration/` (catalog placeholder ids on a non-provider namespace,
  per-id lineage undisclosed) and `kyma/sonar` (upstream model not identified in any
  primary source) SHALL remain provenance `unknown`, recorded as acknowledged residue
  in `scripts/kb_drift_aliases.json` with dated judgments — accept unknown rather than
  guess a bloc (the Drex v1.0 precedent).

#### Scenario: Soniox speech flows resolve through the provider default
- **WHEN** an unbound flow on provider `soniox` carries no model reference, and the
  drift coverage check evaluates the `soniox/stt-*` id set (e.g. `soniox/stt-rt-preview`,
  `soniox/stt-rt-v5`, `soniox/stt-async-v5`)
- **THEN** the unbound flow resolves to bloc `us` via the tier-2 provider default,
  every id in the set counts as covered (the first-party speech-provider rule), and
  no bare `stt` stem exists in the pattern map

#### Scenario: eu/jev model ids resolve via the brand stem; unbound flows via the default
- **WHEN** a model reference `eu-jeff-1.0.0` is detected, the drift coverage check
  evaluates the qualified forms `eu_jev/eu-jeff-1.0.0` and `eu_jev/eu-jeff-latest`,
  and separately an unbound flow on provider `eu_jev` carries no model reference
- **THEN** the reference resolves to bloc `eu` with organisation Bevelites (eu/jev)
  via the `eu-jeff` pattern, the qualified forms count as covered via the drift
  check's suffix walk against the same pattern, and the unbound flow resolves to bloc
  `eu` via the tier-2 provider default — both classifying by operator while the
  vendor's base-model lineage remains undisclosed

#### Scenario: LFM2.5 resolves via the dot-anchored stem
- **WHEN** a model reference `lfm2.5-7b-chat` is detected, and the drift coverage
  check evaluates the qualified form `zerogpu/LFM2.5-1.2B-Instruct`
- **THEN** the reference resolves to bloc `us` with organisation Liquid AI via the
  `lfm2.` anchor, and the qualified form counts as covered via the drift check's
  suffix walk against the same pattern

#### Scenario: Baseten's joey inherits the Qwen bloc
- **WHEN** a model reference `baseten/decision-models/baseten-joey-2b-latest` is
  detected
- **THEN** it resolves to bloc `cn` with the organisation label naming base and tuner
  (`Alibaba (Base Labs post-train)`), per the fine-tunes-inherit-base rule

#### Scenario: Motif-3 resolves to kr via the version anchor
- **WHEN** a model reference `motif-3` is detected, and the drift coverage check
  evaluates the qualified form `aiand/motif-technologies/motif-3`
- **THEN** the reference resolves to bloc `kr` with organisation Motif Technologies
  via the version-anchored `motif-3` pattern, and the qualified form counts as
  covered via the drift check's suffix walk against the same pattern

#### Scenario: Guarded stems stay unknown
- **WHEN** hypothetical references `stt-9-ultra`, `lfma-7b`, or
  `motif-blank-7b` are detected
- **THEN** none resolves through any pattern (no bare `stt`, `stt-rt`, `stt-async`,
  `lfm`, or `motif` stems exist) and each keeps provenance `unknown` — while a form
  like `lfm-turbo-7b` continues to resolve through the pre-existing dash-anchored
  `lfm-` pattern, exactly as before this wave

#### Scenario: Multi-vendor wave-9 providers carry no tier-2 default
- **WHEN** unbound flows on providers `streamlake`, `kyma`, `aiand`,
  `clf_ai_gateway`, `zerogpu`, or `refuseless` carry no model reference
- **THEN** each keeps provenance `unknown` (no tier-2 default on a multi-vendor or
  multi-lineage provider)

#### Scenario: Refuseless catalog ids resolve through existing base patterns
- **WHEN** the drift coverage check evaluates the `refuseless` catalog (e.g.
  `refuseless/glm-5.3-abliterated`, `refuseless/deepseek-v4.1-flash-abliterated`)
- **THEN** every id counts as covered via the suffix walk against the pre-existing
  anchored GLM and DeepSeek family patterns, which are unchanged

#### Scenario: Acknowledged residue stays unknown
- **WHEN** model references `abliteration/abliterated-model` and `kyma/sonar` are
  detected
- **THEN** both keep provenance `unknown`, and the drift report carries them only as
  acknowledged residue with dated judgments in `scripts/kb_drift_aliases.json`
