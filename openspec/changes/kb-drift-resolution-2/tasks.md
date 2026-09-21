# Tasks: kb-drift-resolution-2

## 1. Providers

- [x] 1.1 Add provider entries to `borderlint/data/providers.json` (surgical one-line edits):
  `aihubmix` (aggregator category, endpoints `aihubmix.com` + `api.inferera.com`,
  jurisdiction `unknown`, note on the undisclosed operator), `aws_transcribe` (speech,
  endpoint token `transcribe` with `region_scheme: aws`, in the `aws_polly` mould),
  `typesafe` (no endpoints, jurisdiction `us`, note that the upstream hostname is
  undocumented and litellm reaches it via proxy pass-through) — verify the loader accepts an
  empty endpoint list before committing to that shape
- [x] 1.2 Add sovereignty mappings: `aihubmix: unknown`, `aws_transcribe: us`,
  `typesafe: us`

## 2. Provenance

- [x] 2.1 Add `aihubmix/` to `passthrough_orgs` (aggregator route prefix carries no
  provenance)
- [x] 2.2 Add rebadge patterns: `coding-glm` + `cc-glm` → Zhipu AI cn, `coding-kimi` →
  Moonshot AI cn, `coding-xiaomi-mimo` + `xiaomi-mimo` → Xiaomi cn, `hy3`/`hy4` → Tencent
  cn, `agnes-` → Agnes AI (Sapiens AI) sg, `command-a` → Cohere ca, `longcat-` → Meituan cn
- [x] 2.3 Add publisher patterns (bare + hub-qualified forms per design D3, from the
  enumerated member list): Nex AGI cn, Dots Studio cn, Meituan cn, TypeSafe jev us, Relace
  us, Inference.net schematron us, Perceptron us, Arcee trinity us, Writer palmyra (incl.
  `writer.`) us, Perplexity sonar us, Reka us, bare `whisper` us, `flux.` eu
- [x] 2.4 Add fine-tune inheritance patterns: `l3-`/`l3.` (+ `openrouter/sao10k/l3`) → Meta
  us; `cydonia-`/`skyfall-`/`unslopnemo` (+ hub forms) → Mistral AI (TheDrummer tune) eu;
  `magnum-` (+ hub form) → Alibaba (Anthracite tune of Qwen2.5) cn; `aion-` → cn with
  `aion-rp` → us above it
- [x] 2.5 Bump the `updated` dates of the touched KB files

## 3. Drift suppression

- [x] 3.1 Add residue entries to `scripts/kb_drift_aliases.json`: `stealth/` (prefix —
  OpenRouter cloaked releases deliberately unattributed at launch, judged 2026-09-21),
  `unbiased/pareto` (composite router product, no single weight-provenance),
  `azure_ai/model-router` (routing feature, structural), `transcribe/starttranscriptionjob`
  (API operation, structural)

## 4. Tests

- [x] 4.1 Endpoint tests: `aihubmix.com` → `aihubmix` jurisdiction `unknown`;
  `transcribe.eu-west-1.amazonaws.com` → `aws_transcribe` region-resolved with sovereignty
  `us`; `typesafe` entry loads with empty endpoints and jurisdiction `us`
- [x] 4.2 Provenance tests: one resolution per confirmed group, in the hub-qualified forms
  litellm users write (aihubmix rebadges via the passthrough, magnum/cydonia inheritance,
  aion vs aion-rp precedence, agnes sg, sonar/whisper bare forms)
- [x] 4.3 Near-miss tests: one unrelated id per generic stem (`l`, `cc`, `coding`, `hy`,
  `whisper`, `sonar`, `trinity`, `union`) stays provenance `unknown`

## 5. Verify

- [x] 5.1 Run the full test suite
- [x] 5.2 Run `scripts/kb_drift.py` and confirm the provider and model-family sections
  report zero actionable items
- [x] 5.3 `openspec validate kb-drift-resolution-2 --strict`
