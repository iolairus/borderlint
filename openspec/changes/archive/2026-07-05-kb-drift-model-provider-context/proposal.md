## Why

The model-coverage check judges every upstream key by prefix matching alone, so it nags about
ids that are not provenance gaps: "models" of ignored non-model providers (`apiserpent/search`)
and house models of first-party providers the scanner already resolves via tier-2 defaults
(`deepgram/base`, `gigachat/Embeddings`). ~50 ids of permanent, unactionable residue.

## What Changes

- The check receives each upstream model id with its upstream provider name.
- Ids whose provider is marked out-of-scope in the suppression list are excluded — they are not
  models.
- Ids whose provider resolves (directly, or through the alias list) to a bundled
  **speech-category** provider with a first-party provenance default count as covered — real
  scans resolve those flows via tier 2, and speech tiers (`deepgram/base`) are not weights
  families a pattern should chase. Inference providers' ids keep surfacing: a novel first-party
  family name (the next `o1`) must still reach pattern curation, because bare model strings in
  code resolve only via patterns.
- Multi-model hosts and unknown providers are unaffected; their ids still face prefix matching.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kb-freshness`: the model-coverage requirement gains provider-context rules; the scheduled-
  check and suppression-list requirements are reworded to track them.

## Impact

- `scripts/kb_drift.py` — `upstream_models` returns (id, provider) pairs; `model_coverage_gap`
  gains a suppression parameter (the KB is already a parameter).
- `tests/` — one case per rule; multi-model hosts unaffected.
- Freshness issue #39 sheds the speech-tier and search-route ids.

## Non-goals

- No change to scanner resolution; this is report-input hygiene only.
- No suppression of multi-model hosts' ids — their gaps are real.
