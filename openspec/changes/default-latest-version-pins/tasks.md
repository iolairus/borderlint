## 1. Matcher

- [ ] 1.1 Extend `_VERSION_SUFFIX` in `borderlint/kb.py` to `@(?:\d[A-Za-z0-9.-]*|default|latest)$` (D1, "Version-pinned model identifiers resolve provenance")

## 2. Tests

- [ ] 2.1 `mistral-large@latest`→eu and `claude-fable-5@default`→us resolve; `gemini-team@google.com` and `model@stable` still rejected; flip the existing `codestral@latest is None` assertion in tests/test_borderlint.py (now resolves eu)

## 3. Validation

- [ ] 3.1 Full suite + `openspec validate default-latest-version-pins --strict`; live drift run confirms the meta-pin (`@default`/`@latest`) residue is gone
