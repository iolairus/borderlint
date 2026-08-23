# Proposal: faang-data-practices-curation

## Why

Four first-party FAANG AI platforms are fully detectable in borderlint — `meta_llama`,
`vertex_ai`, `azure_foundry`, `github_copilot` (all sovereignty `us`) — but have no curated
data-practice facts, so reviewers see "not curated" exactly where enterprise traffic concentrates.
Their governing documents are the same doc families already cited for sibling entries
(`azure_openai`, Google Gemini terms), making this the highest-value, lowest-risk curation batch.
It also completes data-practices coverage for every FAANG first-party platform in the KB.

## What Changes

- Add four curated entries to `borderlint/data/data_practices.json`:
  - `meta_llama` — Llama API terms: prompts/outputs not used to train Meta's models; retention
    per policy; no published subprocessor list.
  - `vertex_ai` — Google Cloud terms + Vertex data-governance docs: paid/Vertex traffic not used
    to train; region-scoped processing per the endpoint's rep location.
  - `azure_foundry` — Microsoft Foundry product terms: customer data not used to train base
    models; abuse-monitoring posture mirrors the cited Azure OpenAI entry.
  - `github_copilot` — GitHub Copilot terms: prompts/suggestions not retained by default
    (business tier), public-code-match and retention settings documented.
- Each fact carries url + locator + retrieval date from primary sources; undocumented facts stay
  null. KB website pages and the evidence-pack register render the entries automatically.

## Capabilities

### New Capabilities
- (none)

### Modified Capabilities
- `provider-data-practices`: no requirement text changes — this change adds four entries under
  the shipped schema (cited-facts and no-stale-notes invariants apply).

## Impact

- `borderlint/data/data_practices.json`: four new entries; KB website and evidence-pack
  rendering automatic; drift gap list shrinks accordingly.
- No loader, renderer, CLI, detection, or evaluation changes. Advisory only.

## Non-goals

- No re-curation of existing complete entries.
- No consumer-app variants (ChatGPT, Claude.ai equivalents) — API/platform terms only.
- No changes to loaders or renderers.
