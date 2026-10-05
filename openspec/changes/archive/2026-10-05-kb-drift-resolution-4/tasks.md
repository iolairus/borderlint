# Tasks: kb-drift-resolution-4

## 1. Providers

- [x] 1.1 Add provider entries to `borderlint/data/providers.json` (surgical one-line
  edits): `bespoke`, `laya`, `strands_decider` — each with empty SDK/npm/endpoint lists,
  jurisdiction `local`, and a note naming the vendor (Bespoke Labs, Mountain View; Convai
  Innovations, Kerala; Strands Agents/AWS) and the self-hosted `api_base` mechanics
- [x] 1.2 Add sovereignty mappings: `bespoke: local`, `laya: local`,
  `strands_decider: local`

## 2. Provenance

- [x] 2.1 Add patterns (8): `bespoke/nimble`, `bespoke-nimble`,
  `bespokelabs/bespoke-nimble` → Alibaba (Bespoke Nimble LoRA) cn; `strands-decider` →
  Alibaba (AWS Strands Decider tune) cn; `laya/english` + `laya/typed-decisions` →
  Answer.AI/LightOn ModernBERT (Laya tune) us; `laya/multilingual` → JHU mmBERT (Laya
  tune) us; `cloudflare/clef` → Cloudflare us. NO bare `nimble` stem (Nimbleway collision,
  design D5)
- [x] 2.2 Bump the `updated` dates of the touched KB files

## 3. Tests

- [x] 3.1 Entry tests: `bespoke`, `laya`, `strands_decider` load with empty endpoints,
  jurisdiction `local`, sovereignty `local`
- [x] 3.2 Provenance tests: the two Qwen-adapter inheritance cases, the qualified Nimble
  route forms, the three Laya checkpoints, and clef in both observed forms (bare
  `cloudflare/clef` and via the checker's suffix walk on
  `cloudflare/@cf/cloudflare/clef-flash`)
- [x] 3.3 Near-miss tests: `nimble-search-1` and `clefable-2b` stay provenance `unknown`

## 4. Verify

- [x] 4.1 Run the full test suite
- [x] 4.2 Run `scripts/kb_drift.py` and confirm the provider and model-family sections
  report zero actionable items
- [x] 4.3 `openspec validate kb-drift-resolution-4 --strict`
