# Tasks: kb-drift-resolution-3

## 1. Providers

- [x] 1.1 Add provider entries to `borderlint/data/providers.json` (surgical one-line
  edits): `prism` (Prism Inference, endpoint `api.prisminference.com`, jurisdiction `us`,
  note on the open-weight serving platform) and `sail` (Sail Research, endpoint
  `api.sailresearch.com`, jurisdiction `us`, note on the org-qualified open-weight catalog)
- [x] 1.2 Add sovereignty mappings: `prism: us`, `sail: us`

## 2. Provenance

- [x] 2.1 Add `prism/` and `sail/` to `passthrough_orgs` (host route prefixes carry no
  provenance)
- [x] 2.2 Add patterns: `zai-org/` → Zhipu AI cn; `mai-cyber` + `mai-image` (+ `azure_ai/`
  hub forms) → Microsoft AI us; `fw-gpt-oss` → OpenAI us; `deep-research` (+
  `gemini/deep-research`) → Google us; `virtual-try-on` (+ `vertex_ai/virtual-try-on`) →
  Google us; `together/` (+ `together_ai/together/`) → Together AI us; `c4ai-` → Cohere ca;
  `ember-` + `openrouter/fireworks/ember` → Moonshot AI (Fireworks Ember post-train) cn;
  `apodex/`/`apodex-` (+ hub form) → Apodex us (follow-on drift, design D6)
- [x] 2.3 Bump the `updated` dates of the touched provider/provenance/sovereignty files

## 3. Drift suppression

- [x] 3.1 Add prefix residue entry `fireworks_ai/accounts/fireworks/routers/` to
  `scripts/kb_drift_aliases.json` (Fireworks routing endpoints, not models — structural,
  judged 2026-10-02), and extend the Pareto composite judgment to versioned releases
  (`openrouter/unbiased/pareto-` prefix, design D6)

## 4. Stale-KB review

- [x] 4.1 Bump `updated` on `borderlint/data/arrangements.json` and
  `borderlint/data/regimes.json` to the review date — summaries unchanged per the completed
  90-day review recorded in design D5 (verify no other edits slip into these files)

## 5. Tests

- [x] 5.1 Endpoint test: `api.prisminference.com` → `prism` and `api.sailresearch.com` →
  `sail`, both jurisdiction `us`, sovereignty `us`
- [x] 5.2 Provenance tests: passthrough resolutions (`prism/deepseek-v4-flash` → cn
  DeepSeek, `sail/zai-org/GLM-5.3` → cn Zhipu, `sail/openai/gpt-oss-120b` → us OpenAI),
  the Ember inheritance (`openrouter/fireworks/ember-1` → cn), and one per remaining group
  (MAI lines, fw-gpt-oss, c4ai, deep-research, virtual-try-on, together/Tev1)
- [x] 5.3 Near-miss tests: `deepfake-detector-2`, `virtual-assistant-1`, `embering-7b`,
  `maize-1` stay provenance `unknown`

## 6. Verify

- [x] 6.1 Run the full test suite
- [x] 6.2 Run `scripts/kb_drift.py` and confirm providers, model families, and stale-KB
  sections all report zero actionable items
- [x] 6.3 `openspec validate kb-drift-resolution-3 --strict`
