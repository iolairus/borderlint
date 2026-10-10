# Tasks: kb-drift-resolution-5

## 1. Provenance

- [x] 1.1 Add `in.` to `passthrough_orgs` in `borderlint/data/provenance.json` (Bedrock
  India-Geo inference-profile prefix, design D1), keeping the list's existing order
  convention
- [x] 1.2 Add the qualified pattern `azure/whisper` → OpenAI, bloc `us`, mirroring the
  `azure_ai/whisper` entry; NO bare `whisper` stem (design D2)
- [x] 1.3 Bump the `updated` date of `borderlint/data/provenance.json`

## 2. Drift aliases

- [x] 2.1 Add residue entry `azure/model-router` to `scripts/kb_drift_aliases.json` —
  "Azure Foundry model-routing feature, not a model (structural)"; same reason as the
  existing `azure_ai/model-router` key, new variant under the `azure` namespace (design D3)

## 3. 90-day legal review of evidence_regimes.json

- [x] 3.1 Verify the PDPO summary against its sources (Cap. 486 s.33 operation status,
  PCPD cross-border guidance/RMCCs, PCPD AI framework) and correct if inaccurate
- [x] 3.2 Verify the PIPL summary against its sources (Arts. 38–40 transfer routes and the
  2024 Provisions exemptions, Arts. 55–56 PIA, GBA Standard Contract variants) and correct
  if inaccurate
- [x] 3.3 Verify the Macao PDPA summary (Law 8/2005 Arts. 19–20, GBA Standard Contract
  Mainland–Macao variant) and the PDPA (SG) summary (s.26, PDPC guidelines, Model AI
  Governance Framework) against their sources and correct if inaccurate
- [x] 3.4 Bump `updated` in `borderlint/data/evidence_regimes.json` to the review date,
  recording any in-window legal changes found (or that none were found)

## 4. Tests

- [x] 4.1 Provenance tests: `in.moonshotai.kimi-k3` resolves `cn` (Moonshot AI) via the
  `in.` passthrough; `azure/whisper` resolves `us` (OpenAI)
- [x] 4.2 Near-miss tests: `whispering-pines` and `in.inhouse-7b` stay provenance
  `unknown` (no bare `whisper` stem; stripped region prefix matches no family pattern)

## 5. Verify

- [x] 5.1 Run the full test suite
- [x] 5.2 Run `scripts/kb_drift.py` and confirm the model-family and stale-KB sections
  report zero actionable items (data-practice gaps remain the standing backlog)
- [x] 5.3 `openspec validate kb-drift-resolution-5 --strict`
