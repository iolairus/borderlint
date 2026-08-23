# Tasks: faang-data-practices-curation

## 1. Entry curation

- [x] 1.1 Add the `meta_llama` entry: training_default reflecting Standard Services (content not used to train Meta Models, §5.1) with enterprise_tier disclosing the Discounted Services default-training split (§6.1); retention per §4.4; subprocessors self-citing object pointing at Meta's published subprocessor list (D1, D2)
- [x] 1.2 Add the `vertex_ai` entry: training_default citing the Service Specific Terms "Training restriction" (no training without prior permission); retention noting abuse-monitoring logging with exemption path, in-memory caching TTL, and per-feature retention conditions from the generative-AI ZDR page (D3)
- [x] 1.3 Add the `azure_foundry` entry: training_default (prompts/completions NOT used to train foundation models without permission) citing Foundry data-privacy documentation; Global/DataZone processing scope noted per D3; abuse-monitoring posture may reference the azure_openai citations' document family
- [x] 1.4 Add the `github_copilot` entry: training_default citing GitHub Generative AI Services Terms §3 (Inputs/Outputs not used to train without documented instruction); retention noting per-product documentation variance (§6); enterprise_tier noting the Copilot PST was deprecated 2026-03-05 in favour of these terms (D2)

## 2. Tests

- [x] 2.1 Extend data-practices tests: the four entries load with expected training defaults, every non-null fact carries a complete citation, no unavailability claims, and each key exists in providers.json

## 3. Validation

- [x] 3.1 Run full pytest suite and fix regressions
- [x] 3.2 Run `openspec validate faang-data-practices-curation --strict`
