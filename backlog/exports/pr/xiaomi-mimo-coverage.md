<!-- PR for /opsx change xiaomi-mimo-coverage -->

## Summary

Xiaomi MiMo ranks #3 by token volume on OpenRouter's weekly leaderboard (MiMo-V2.5, Aug 2026),
yet borderlint could not detect it: no provider entry, no endpoint mapping, no provenance
pattern beyond a bare org prefix, and no curated data-practice facts. This change adds the
`xiaomi_mimo` provider with both documented hosts — `api.xiaomimimo.com` resolves
region-dependent (`unknown`; the international platform stores data in EU + Singapore data
centres per service agreement §4.4) while `token-plan-cn.xiaomimimo.com` resolves `cn` — plus
provenance patterns so bare (`mimo-v2.5-pro`), org-qualified (`xiaomi/mimo-…`) and
redistributor-qualified (`novita/xiaomimimo/…`) model ids all resolve to bloc `cn`, and a fully
cited data-practices entry (training default **no**: "Xiaomi will not use the content you
provide for model training or any other purposes", privacy policy §3.1). The drift residue
entry for the Novita path retires now that the patterns cover it.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/xiaomi-mimo-coverage/` |
| Spec deltas | MODIFIED `jurisdiction-classification` (`Bundled east-west provider knowledge base`); ADDED `model-provenance` (`MiMo model identifiers resolve provenance`); ADDED `provider-data-practices` (`Xiaomi MiMo curated facts`) |

## Changes

- `borderlint/data/providers.json`: `xiaomi_mimo` entry — both hosts via
  `endpoint_jurisdictions`, note documenting the EU+SG storage posture and the Token Plan's
  dedicated CN host; no SDK keys (usage rides generic OpenAI/Anthropic SDKs against these hosts).
- `borderlint/data/provenance.json`: `mimo-` and literal `novita/xiaomimimo/` patterns →
  bloc `cn`, org Xiaomi (start-anchored matching requires the literal qualifier form).
- `borderlint/data/sovereignty.json`: `xiaomi_mimo: cn` (caught by the live sovereignty-gaps
  audit test — every bundled provider needs a bloc).
- `scripts/kb_drift_aliases.json`: retired the covered residue entry.
- `borderlint/data/data_practices.json`: curated entry with citations to the MiMo privacy
  policy (§3.1 training commitment, §6 retention) and service agreement (§1.1 storage-region
  selection, §4.4 EU+SG storage); subprocessors null (no published list).
- `tests/test_borderlint.py`: endpoint detection for both hosts with distinct jurisdictions;
  provenance resolution across all three id forms + drift-gap-closed assertion; data-practices
  schema/citation completeness including the actual policy quote.

## Verification

- [x] `openspec validate xiaomi-mimo-coverage --strict` passes
- [x] All tasks in tasks.md checked (10/10)
- [x] Tests covering each acceptance scenario (full suite: 185 passed)
- [x] Review pass probed every scenario live against the bundled KB, plus four seams beyond
  unit tests: KB website page renders with the cited data-practices section; evidence pack
  shows the inventory row, DP register entry, and training fact; drift gap for the residue id
  is closed; sovereignty gaps remain empty across all bundled providers
