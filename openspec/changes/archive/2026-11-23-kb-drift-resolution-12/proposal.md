# Proposal: kb-drift-resolution-12

## Why

The live 2026-11-23 drift run reports four uncovered providers, 22 model families (42 ids), a
stale regulator-profile KB, and 16 stale data-practice entries. Source review found that this is
not a date-only wave: HKMA's cited 2019 AI principles were superseded in October 2026, 15 stale
data-practice entries contain outdated or incomplete facts, and Tev1's existing broad Together
mapping contradicts its disclosed Qwen base.

## What Changes

- Add **Gnani**, **Gradium**, **ResetData**, and **Vispark** with source-backed endpoints, SDKs,
  residency, sovereignty, and category. Gnani/Gradium default residency remains `unknown`;
  Gradium's enrolled EU/US hosts receive endpoint overrides. ResetData resolves to `au`; Vispark
  to `in`. Only Vispark receives a first-party provenance default.
- Reconcile all 42 actionable model ids. Add anchored mappings for 41, including Jina's mixed
  Qwen/EuroBERT lineage, Tiny Aya, Bedrock Geo CA passthrough, Respan Span, Baseten Bison and
  Groundhog, Cohere North, Sarvam-105B, Cartesia Sonic, Google Genie, and Qwen-derived Kev/Tev1.
  Acknowledge only `together_ai/prunaai/p-image-ideogram` as exact undisclosed-lineage residue.
  Remove the obsolete broad `together/` and `together_ai/together/` US patterns.
- Refresh all 16 stale data-practice entries. DeepSeek alone is date-only; correct the other 15
  using current provider-authored terms and documentation, preserving explicit nulls and tier or
  feature limits. Add Xiaomi's Singapore/Europe Token Plan hosts and correct Z.ai's documented
  Singapore processing and legal note without inferring a new sovereignty bloc.
- Replace HKMA's superseded citation, remove the unsupported `CN-GBA` non-PII seed, and correct
  its rationale. Retain MAS's current 2024 citation and Singapore-only seeds while recording the
  issued 2026 Guidelines and their future effective dates.
- Advance touched KB dates, update the bundled provider count from 138 to 142, and add regression
  tests for exact anchors, near-misses, endpoint overrides, refreshed facts, and profile defaults.

## Capabilities

### New Capabilities
- (none)

### Modified Capabilities
- `jurisdiction-classification`: four new providers and two adjacent endpoint corrections.
- `model-provenance`: wave-12 provenance, Geo CA passthrough, Tev1 correction, exact residue.
- `provider-data-practices`: current cited facts for all 16 stale entries.
- `regulator-profiles`: current HKMA/MAS guidance and conservative seeds.
- `kb-website`: providers with EU endpoints render without inventing an EU regime name.

## Impact

Provider, sovereignty, provenance, data-practice, regulator-profile, drift-alias, README, and test
files. Provider/model/stale-KB/stale-data sections should converge to zero; the standing
data-practice backlog becomes 116 with the four new providers.

## Non-goals

- No curation of the existing 112-entry data-practice backlog or fabrication of facts for the four
  new providers.
- No broad provider/org provenance patterns, guessed residency, or inferred lineage.
- No reconsideration of acknowledged Sarvam residue/defaults outside the actionable wave.
- No new regulator profiles, runtime fetching, legal determinations, or release in this change.
