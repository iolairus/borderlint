# Tasks: kb-drift-resolution

## 1. Enumerate

- [x] 1.1 Run `scripts/kb_drift.py` locally to enumerate the current members of each of the
  twelve model families and fix the exact pattern stems per design D3 (most specific literal
  that covers the members; org-qualified where the upstream ids carry the org)

## 2. Knowledge-base data

- [x] 2.1 Add provider entry `scx_ai` to `borderlint/data/providers.json` — name "SCX.ai",
  endpoint `api.scx.ai`, jurisdiction `au`, empty SDK/npm lists (surgical one-line edit,
  matching the file's hand formatting)
- [x] 2.2 Add `scx_ai: au` to the provider map in `borderlint/data/sovereignty.json`
- [x] 2.3 Add the provenance patterns from 1.1 to `borderlint/data/provenance.json` with the
  confirmed blocs — cn: ByteDance Seed, Baidu CoBuddy, StepFun Step; us: Microsoft MAI,
  Google nano-banana, Microsoft Research multilingual-e5, Thinking Machines Lab Inkling,
  poolside Laguna, PrismML Ternary-Bonsai, BigScience mt0; eu: JetBrains Mellum; sg: MindAI
  Macaron
- [x] 2.4 Bump the `updated` dates of the touched KB files

## 3. Drift suppression

- [x] 3.1 Add aliases to `scripts/kb_drift_aliases.json`: `qwencloud` → `alibaba_dashscope`,
  `qwen_ai_platform` → `alibaba_dashscope`, `bing_grounding` → `azure_foundry`, each judgment
  dated
- [x] 3.2 Add residue entry `bing_grounding/search` (search tool, not a model; provider
  aliased to `azure_foundry`)

## 4. Tests

- [x] 4.1 Endpoint test: `api.scx.ai` resolves to provider `scx_ai`, jurisdiction `au`,
  sovereignty `au`
- [x] 4.2 Provenance tests: one resolution per bloc group (`deepinfra/ByteDance/Seed-1.8` →
  cn, `deepinfra/thinkingmachines/Inkling` → us, `wandb/JetBrains/Mellum2-12B-A2.5B-Instruct`
  → eu, `novita/mindai/macaron-v1-tall` → sg)
- [x] 4.3 Near-miss tests: one unrelated id per generic stem (`seed`, `step`, `mt`, `nano`,
  `multilingual`) stays provenance `unknown`

## 5. Verify

- [x] 5.1 Run the full test suite
- [x] 5.2 Run `scripts/kb_drift.py` and confirm the provider and model-family sections report
  zero actionable items
- [x] 5.3 `openspec validate kb-drift-resolution --strict`
