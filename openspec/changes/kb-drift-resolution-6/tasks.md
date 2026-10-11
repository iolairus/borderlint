# Tasks: kb-drift-resolution-6

## 1. Providers and sovereignty

- [x] 1.1 Add `microsoft_365_copilot` to `borderlint/data/providers.json`: endpoint
  `graph.microsoft.com`, jurisdiction `us`, note recording the Graph beta preview status,
  the Microsoft-chosen model, and the shared Graph surface caveat (design D1)
- [x] 1.2 Add `scaledown` to `borderlint/data/providers.json`: endpoint
  `api.scaledown.xyz`, jurisdiction `us`, note recording the `.xyz` API host vs `.ai`
  docs/marketing hosts and the DPA US-only processing commitment (design D2)
- [x] 1.3 Add `microsoft_365_copilot` → `us` and `scaledown` → `us` to
  `borderlint/data/sovereignty.json`
- [x] 1.4 Bump `updated` in `providers.json` and `sovereignty.json` to 2026-10-11

## 2. Provenance

- [x] 2.1 Add patterns `mai-code` and `github_copilot/mai-code` → Microsoft AI, bloc `us`
  (design D4)
- [x] 2.2 Add org-namespace pattern `scaledown/` → ScaleDown, bloc `us`; NO bare
  `classify`/`compress`/`decisions`/`extract`/`summarize` stems (design D3)
- [x] 2.3 Add qualified pattern `microsoft_365_copilot/chat` → Microsoft, bloc `us`; NO
  bare `chat` stem (design D6)
- [x] 2.4 Add patterns `microsoft-decision` and `azure_ai/microsoft-decision` → bloc
  `cn`, org `Alibaba (Microsoft Decision-1 post-training)` (design D5)
- [x] 2.5 Add tier-2 provider default `scaledown` → `us`; NO default for
  `microsoft_365_copilot` (design D6)
- [x] 2.6 Bump `updated` in `borderlint/data/provenance.json` to 2026-10-11

## 3. Tests

- [x] 3.1 Provider tests: `graph.microsoft.com` resolves `microsoft_365_copilot`/us;
  `api.scaledown.xyz` resolves `scaledown`/us
- [x] 3.2 Provenance tests: `github_copilot/mai-code-1.1-flash` and `mai-code-1-flash` →
  us (Microsoft AI); all five `scaledown/*` ids → us (ScaleDown);
  `microsoft_365_copilot/chat` → us (Microsoft)
- [x] 3.3 Inheritance test: `azure_ai/Microsoft-Decision-1` and `Microsoft-Decision-1` →
  cn with the org label naming base and tuner
- [x] 3.4 Near-miss tests: hypothetical `chat-with-pdfs`, `classification-9b`,
  `summarize-pro-2` stay provenance `unknown`
- [x] 3.5 Tier-2 tests: unbound `scaledown` flow defaults to `us`; unbound
  `microsoft_365_copilot` flow stays `unknown`

## 4. Verify

- [x] 4.1 Run the full test suite
- [x] 4.2 Run `scripts/kb_drift.py` and confirm the provider and model-family sections
  report zero actionable items (data-practice gaps grow to 94 as the two new providers
  join the standing backlog)
- [x] 4.3 `openspec validate kb-drift-resolution-6 --strict`
