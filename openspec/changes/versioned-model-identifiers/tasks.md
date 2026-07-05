## 1. Matcher

- [ ] 1.1 In `borderlint/kb.py` `match_model`: strip one trailing `@<digit-led version>` (regex `@\d[A-Za-z0-9.-]*$`) before the `_MODEL_ID` gate; match the base, return the original literal as evidence (D1, D2, "Version-pinned model identifiers resolve provenance")

## 2. Data

- [ ] 2.1 Add bare `codestral` pattern (org Mistral, bloc eu) to `borderlint/data/provenance.json` — the stripped base of `codestral@2405` has no prefix today (review F3)

## 3. Tests

- [ ] 3.1 Versioned forms resolve: `claude-3-5-haiku@20241022`→us, `anthropic.claude-haiku-4-5@20251001`→us, `mistral-large@2407`→eu, `mistral-large@2411-001`→eu (hyphenated version), `jamba-1.5-large@001`→il, `codestral@2405`→eu; evidence keeps the suffix
- [ ] 3.2 Negatives: `gemini-team@google.com` and `a@b@1` do not match; version never changes the bloc (`mistral-large` == `mistral-large@2407`)
- [ ] 3.3 Drift interaction: `model_coverage_gap` on a `vertex_ai/claude-3-5-haiku@20241022` fixture reports nothing

## 4. Validation

- [ ] 4.1 Full suite + `openspec validate versioned-model-identifiers --strict`; live `scripts/kb_drift.py` run confirms the digit-led `@` ids leave the report and the expected residue is exactly the letter-led pins (`@default`, `@latest`)
