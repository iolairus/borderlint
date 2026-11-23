# Tasks: kb-drift-resolution-12

## 1. Providers and adjacent endpoint corrections

- [x] 1.1 Add Gnani and Gradium with the exact fields, SDK exemptions, residency qualifications,
      sovereignty, and no provider-level provenance default in design D1; add exact Prisma and
      Gradium model patterns under task 2 (spec: Wave-12 providers resolve documented destinations)
- [x] 1.2 Add ResetData/au and Vispark/in with documented hosts, empty dedicated SDK arrays, and
      sovereignty; add only Vispark's justified first-party provider default (design D1)
- [x] 1.3 Add Xiaomi SGP/AMS Token Plan hosts and endpoint jurisdictions; update its note for
      Individual/Team and regional service (spec: Wave-12 adjacent endpoint facts)
- [x] 1.4 Add `api.z.ai` → `sg`, correct the international legal-forum note, and retain provider
      sovereignty absent evidence of a different legal entity (design D1)
- [x] 1.5 Advance provider/sovereignty dates, add reasoned SDK exemptions, and update README's
      bundled-provider count from 138 to 142 (design D1)
- [x] 1.6 Make KB-site regime aggregation ignore jurisdictions whose regime reference is null, so
      Gradium's `eu` endpoint renders without inventing a regime name (spec: Provider pages tolerate
      jurisdictions without a single regime)

## 2. Provenance reconciliation

- [x] 2.1 Add bounded `ca.` passthrough and tests proving Amazon/Anthropic inheritance without
      Canadian attribution or incomplete-key matches (design D2)
- [x] 2.2 Add Jina's four base-ID patterns with distinct Qwen/EuroBERT lineage, Tiny Aya, and the
      exact North patterns and namespace companions (design D2)
- [x] 2.3 Add Respan Span, Vispark Vision, Baseten Bison/Groundhog, Ideogram, and Juggernaut Flux
      patterns with exact qualifications and inherited organisation labels (design D2)
- [x] 2.4 Add Sarvam-105B, Cartesia Sonic, Liquid d1, Adept Fuyu, Google Genie, and Zyphra Zamba2
      patterns; leave generic and future near-misses unresolved (design D2)
- [x] 2.5 Add Kev and Kokoro inherited provenance; add all five Tev1 forms as cn and remove the
      broad `together/` and `together_ai/together/` US patterns (design D2; modified MAI/Ember/Aya
      requirement)
- [x] 2.6 Add only exact `together_ai/prunaai/p-image-ideogram` undisclosed-lineage residue and
      advance `provenance.updated`; do not broaden existing Pruna residue (design D3)

## 3. Data-practice refresh

- [x] 3.1 Correct Alibaba DashScope retention, Anthropic subprocessors, and GitHub Copilot's
      commercial/individual tier and feature-specific retention scope (design D4)
- [x] 3.2 Rebuild AWS Bedrock training, retention, subprocessor, and enterprise facts; update tests
      that expect null training/subprocessors (design D4)
- [x] 3.3 Refresh Azure Foundry and Azure OpenAI URLs, stateful/human-review retention, and the
      pre/post-2026-11-01 Modified Abuse Monitoring limitation without announcing a completed
      sunset (design D4)
- [x] 3.4 Re-verify DeepSeek with no factual change; correct Google Gemini paid/unpaid retention,
      subprocessor, and Paid Service tier facts (design D4)
- [x] 3.5 Refresh Meta Standard/Contributor/Hosted Platform distinctions and Moonshot's enterprise
      ZDR exclusions while retaining their general defaults (design D4)
- [x] 3.6 Replace NVIDIA NIM generic privacy claims with hosted trial API training/retention/tier
      facts; correct OpenAI endpoint-specific retention and subprocessor locator (design D4)
- [x] 3.7 Correct Tencent TokenHub training/ZDR/30-day facts and rewrite Vertex AI's feature- and
      model-specific retention without a universal ZDR claim (design D4)
- [x] 3.8 Refresh Xiaomi international/Team facts and split Zhipu domestic BigModel from
      international Z.ai training/retention/subprocessor scope (design D4)
- [x] 3.9 Set all 16 `reviewed` and re-verified citation retrieval dates plus file `updated` to the
      implementation review date; preserve documented nulls and remove stale caveats (design D4)

## 4. Regulator profiles

- [x] 4.1 Replace HKMA's citation and notes, remove `CN-GBA` from non-PII, and update all affected
      init/profile assertions (spec: HKMA profile follows current superseding guidance)
- [x] 4.2 Retain MAS's 2024 citation/defaults and add the 2026 Guidelines' 2027/2028 transition
      dates without presenting them as effective (spec: MAS profile records guidance transition)
- [x] 4.3 Refresh HKMA/MAS citation retrieval, profile review, and document update dates (design D5)

## 5. Tests and verification

- [x] 5.1 Test all four providers, SDK/host detection, sovereignty, regional endpoint overrides,
      Xiaomi/Z.ai corrections, and the absence of invented SDKs/residency
- [x] 5.2 Parameterize direct `kb.match_model` checks for every one of the 41 attributable upstream
      ids and representative canonical/namespace variants; test organisation labels and blocs
- [x] 5.3 Test generic near-misses, future versions, exact residue behavior, Geo CA boundaries, and
      removal of broad Together US fallback
- [x] 5.4 Assert every refreshed non-null data-practice fact has current provider-authored citation
      evidence and that specifically unchanged/null fields remain unchanged
- [x] 5.5 Run the full pytest suite and JSON/load validation
- [x] 5.6 Re-run `scripts/kb_drift.py`: zero providers, model families, sovereignty gaps, stale KBs,
      SDK gaps, and stale data-practice entries; only 116 standing data-practice gaps and
      acknowledged residue remain
- [x] 5.7 Run `openspec validate kb-drift-resolution-12 --strict` and review the diff for guessed
      lineage/residency, stale claims, broad patterns, or out-of-scope backlog curation
