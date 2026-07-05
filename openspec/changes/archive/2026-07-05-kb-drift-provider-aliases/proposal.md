## Why

The freshness issue's new-provider section lists ~56 upstream names, and most are standing
noise: litellm route aliases of providers we already cover (`bedrock`, `azure`, `gemini`,
`chatgpt`, `palm`, `cohere_chat` …) and non-model tools litellm wraps (`firecrawl`,
`duckduckgo`, `dataforseo`, `google_pse`). They cannot be silenced honestly today — adding fake
provider entries would pollute scanner detection — so the section never converges and real new
providers drown in it.

## What Changes

- A dev-side alias file consumed only by the drift checker, with two lists:
  **aliases** (upstream name → covered provider id) and **ignores** (upstream names that are
  not AI model providers, each with a reason).
- The provider gap excludes aliased and ignored names. An alias pointing at a provider id that
  does not exist in the bundled KB fails the check loudly — aliases cannot rot silently.
- The file ships outside the package (`scripts/`), so the scanner and wheel are untouched.
- First curation pass: the current route aliases and search/scraping tools from issue #39.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kb-freshness`: the scheduled check gains alias/ignore suppression for the provider section
  (new requirement), and the existing scheduled-check and deterministic-diff requirements are
  reworded to admit the suppression list as an input.

## Impact

- `scripts/kb_drift_aliases.json` (new, dev-only), `scripts/kb_drift.py` (filter + validation),
  `tests/` (suppression, unknown-target failure, reason presence).
- Freshness issue #39's provider section shrinks from ~56 names to the genuine review queue.

## Non-goals

- No changes to scanner detection: aliases never become provider entries, SDK names, or
  endpoints.
- No auto-classification of upstream names — every alias and ignore is a human judgment,
  recorded with the entry.
- No suppression in the model-family section (patterns and passthroughs already govern it).
