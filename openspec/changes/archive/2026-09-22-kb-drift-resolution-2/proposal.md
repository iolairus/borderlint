# Proposal: kb-drift-resolution-2

## Why

The 2026-09-21 freshness run reports three uncovered upstream providers and thirty unresolved
model families — the largest drift wave since the checker shipped, driven by the aihubmix
aggregator's rebadged catalog and a batch of new OpenRouter publishers. Until each item is
assigned by hand or acknowledged with a reason, these flows classify as `unknown` and the
review queue cannot converge.

## What Changes

- Add three bundled provider entries:
  - `aihubmix` — OpenAI-compatible multi-model aggregator (endpoints `aihubmix.com`,
    `api.inferera.com`); operator undisclosed, so jurisdiction and sovereignty are honestly
    `unknown` (the openrouter treatment).
  - `aws_transcribe` — AWS Transcribe speech service, endpoint `transcribe` under the aws
    region scheme (`transcribe.<region>.amazonaws.com`), sovereignty `us`, in the
    `aws_polly` mould.
  - `typesafe` — TypeSafe AI (San Francisco), jurisdiction and sovereignty `us`, with no
    endpoint hosts: the upstream API hostname is undocumented (litellm proxies it) and the
    KB never guesses.
- Add `aihubmix/` as a provenance passthrough (an aggregator route prefix carries no
  provenance) and explicit patterns for its rebadged ids: `coding-glm`/`cc-glm` → Zhipu,
  `coding-kimi` → Moonshot, `coding-xiaomi-mimo` → Xiaomi, `hy3`/`hy4` → Tencent Hunyuan,
  `agnes` → Agnes AI, `command-a` → Cohere, `longcat` → Meituan.
- Add provenance patterns for the remaining families, blocs confirmed by the maintainer
  2026-09-21:
  - `cn` — Nex AGI (Shanghai Innovation Institute), Dots Studio (Xiaohongshu/RedNote),
    Meituan LongCat, Tencent Hunyuan hy3/hy4, ByteDance's new `bytedance-seed` publisher org
    (the wave's `seed` family), Anthracite `magnum` (Qwen2.5 fine-tune — inherits the base
    bloc), AionLabs `aion-*` (DeepSeek/GLM derivatives)
  - `us` — TypeSafe `jev`, Relace, Inference.net `schematron` (Llama-3.2 tunes), Perceptron,
    Arcee `trinity`, Writer `palmyra` (incl. the Bedrock `writer.` prefix), Perplexity
    `sonar` and the OpenAI `whisper` family via qualified forms only (bare stems over-match
    tool names — see design D3), Sao10K's `l3-`/`l3.` Llama-3.x fine-tunes (inherit Meta's
    bloc), and the one AionLabs exception `aion-rp` (Llama-3.1 base)
  - `eu` — Black Forest Labs `flux.`, TheDrummer's `cydonia`/`skyfall`/`unslopnemo`
    (all Mistral bases — inherit the base bloc)
  - `sg` — Agnes AI (Sapiens AI, Singapore)
- Record the drift alias `transcribe` → `aws_transcribe` (the checker's normalizer does not
  equate the two ids) and four residue judgments: `openrouter/stealth/` as a prefix entry
  (OpenRouter's cloaked releases are deliberately unattributed at launch; re-attribute on
  reveal), `openrouter/unbiased/pareto` (composite router product — no single
  weight-provenance is honest), `azure_ai/model-router` (routing feature) and
  `transcribe/StartTranscriptionJob` (API operation) as structural.
- Bump the review dates of the touched knowledge-base files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `jurisdiction-classification`: the three new providers resolve with their documented
  jurisdictions (aihubmix `unknown`, AWS Transcribe region-resolved, TypeSafe `us`).
- `model-provenance`: the drift-wave model families resolve to their developer
  organisations' blocs, including fine-tune base-inheritance and the aggregator passthrough.

## Impact

- `borderlint/data/providers.json` (+3 entries), `sovereignty.json` (+3 mappings),
  `provenance.json` (+1 passthrough, +62 patterns — family stems, org prefixes, and
  hub-qualified route literals per the established D3 discipline),
  `scripts/kb_drift_aliases.json` (+1 alias, +4 residue entries).
- Detection tests for the new endpoints and pattern resolutions; KB website and evidence
  pack render the new providers from bundled data with no code change.
- Issue #39's actionable sections drop from 3 providers + 30 families to zero.

## Non-goals

- No data-practice curation: the three new providers join the gap queue honestly.
- No SDK keys for the new providers until official package coordinates are verified.
- No per-request provenance for composite/router products (pareto): the residue records the
  judgment; anything finer is future work if such products proliferate.
