## 1. Suppression data

- [ ] 1.1 Create `scripts/kb_drift_aliases.json`: `aliases` (upstream → covered provider id) and `ignore` (upstream → reason), first pass curated from issue #39 — route aliases (`bedrock`, `bedrock_converse`, `azure`, `azure_ai`, `azure_text`, `gemini`, `chatgpt`, `palm`, `codestral`, `cohere_chat`, `amazon_nova` …) and non-model tools (`firecrawl`, `duckduckgo`, `dataforseo`, `exa_ai`, `google_pse`, `linkup` …), each ignore with a reason (D1, D2)

## 2. Drift checker

- [ ] 2.1 Load the suppression file in `scripts/kb_drift.py`; validate alias targets against bundled provider ids (raise on missing) and ignore reasons non-empty (raise on empty) (D2, "Upstream provider aliases and out-of-scope names are suppressed")
- [ ] 2.2 `coverage_gap(upstream, known, suppression)` filters aliased/ignored names; loaded in `main()` and passed in; model-family, sovereignty, and staleness sections untouched (D3, "Deterministic coverage diff")
- [ ] 2.3 Update the New-providers section preamble in `render_report` to mention recording an alias or out-of-scope entry in `scripts/kb_drift_aliases.json`; one sentence in CONTRIBUTING.md's drift-check paragraph ("Scheduled coverage check")

## 3. Tests

- [ ] 3.1 Suppression: aliased and ignored names excluded; unlisted names still surface
- [ ] 3.2 Loud failures: alias to a missing provider id raises naming both; empty ignore reason raises
- [ ] 3.3 Live-data guard: every alias target in the shipped `kb_drift_aliases.json` exists in `providers.json`; scanner path never reads the file ("The scanner never reads the suppression list")

## 4. Validation

- [ ] 4.1 Full suite + `openspec validate kb-drift-provider-aliases --strict`; live `scripts/kb_drift.py` run confirms the provider section shrinks to the genuine queue
