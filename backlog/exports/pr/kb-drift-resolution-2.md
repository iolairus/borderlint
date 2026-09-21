# fix(kb): resolve Sep-21 drift — aihubmix aggregator, AWS Transcribe, TypeSafe, 27 model families

## Summary

The 2026-09-21 freshness run reported the largest drift wave yet: three uncovered upstream providers and thirty unresolved model families, driven by the aihubmix aggregator's rebadged catalog and a batch of new OpenRouter publishers. This change drains both sections to zero actionable items: three new provider entries, an aggregator passthrough with explicit rebadge patterns, provenance for twelve publisher and four fine-tuner families with maintainer-confirmed blocs, and four residue judgments — including a standing prefix entry for OpenRouter's deliberately-anonymous stealth releases.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/kb-drift-resolution-2/` |
| Spec deltas | MODIFIED `jurisdiction-classification` — Bundled east-west provider knowledge base (no-endpoint provider rule + aihubmix/Transcribe/TypeSafe scenarios); ADDED `model-provenance` — LongCat, Nex, Agnes, Jev, and companion model families resolve provenance |

## Changes

- **Providers** — `aihubmix` (OpenAI-compatible multi-model aggregator; operator undisclosed, so jurisdiction and sovereignty stay honestly `unknown`), `aws_transcribe` (`transcribe.<region>.amazonaws.com` under the aws region scheme — the endpoint test confirms eu-west-1 → `ie` with sovereignty `us`), `typesafe` (TypeSafe AI, SF; upstream hostname undocumented, so the entry carries an empty endpoint list rather than a guess — precedent: the `litellm` entry). Drift alias `transcribe` → `aws_transcribe`.
- **Aggregator handling** — `aihubmix/` joins the provenance passthroughs (a route prefix carries no provenance); its rebadged ids get explicit patterns: `coding-glm`/`cc-glm` → Zhipu, `coding-kimi` → Moonshot, `coding-xiaomi-mimo` → Xiaomi, `hy3`/`hy4` → Tencent, `agnes` → Agnes AI (Sapiens AI, Singapore), `command-a` → Cohere, `longcat` → Meituan.
- **Publisher patterns** — Nex AGI (Shanghai Innovation Institute) and Dots Studio (Xiaohongshu) `cn`; ByteDance's new `bytedance-seed` org `cn`; TypeSafe `jev`, Relace, Inference.net `schematron`, Perceptron, Arcee `trinity`, Writer `palmyra` (incl. the Bedrock `writer.` prefix), Reka `us`; Black Forest Labs `flux.` `eu`. All observed hub-qualified route literals included per the established discipline.
- **Fine-tune base-inheritance** — Sao10K `l3-`/`l3.` (Llama-3.x) → `us`; TheDrummer `cydonia`/`skyfall`/`unslopnemo` (Mistral bases) → `eu`; Anthracite `magnum` (Qwen2.5) → `cn`; AionLabs `aion-` → `cn` with `aion-rp` (Llama-3.1 base) → `us` via longest-prefix precedence.
- **Stem discipline, tested** — bare `whisper` and `sonar` patterns were tried and rejected during implementation (`whispering-pines` and `sonarqube-scan` matched; an existing curation test pins `sonar-scanner` as must-not-match), so those families resolve only via qualified forms, with bare literals falling to the tier-2 provider default. Eight near-miss tests pin this wave's generic stems (`l`, `cc`, `coding`, `hy`, `whisper`, `sonar`, `trinity`, `union`).
- **Residue** — `openrouter/stealth/` as a standing prefix (cloaked releases are unattributed by design; union-alpha stays covered post-reveal), `openrouter/unbiased/pareto` (composite router product — no single weight-provenance is honest), `azure_ai/model-router` and `transcribe/StartTranscriptionJob` (structural).

## Verification

- [x] `openspec validate kb-drift-resolution-2 --strict` passes
- [x] All tasks in tasks.md checked
- [x] Tests covering each acceptance scenario (195 passed; `scripts/kb_drift.py` reports 0 actionable providers and 0 model families)
