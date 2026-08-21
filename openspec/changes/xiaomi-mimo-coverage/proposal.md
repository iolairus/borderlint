# Proposal: xiaomi-mimo-coverage

## Why

Xiaomi MiMo ranks #3 by token volume on OpenRouter's weekly leaderboard (MiMo-V2.5, Aug 2026),
yet borderlint's knowledge base cannot detect it: no provider entry, no endpoint mapping, no
provenance pattern beyond a bare org prefix, and no curated data-practice facts. Developers
routing to `api.xiaomimimo.com` flow undetected — a blind spot exactly where traffic is.

## What Changes

- Add a bundled provider entry `xiaomi_mimo`: endpoint hosts (`api.xiaomimimo.com`,
  `token-plan-cn.xiaomimimo.com`) with region-aware endpoint jurisdictions (global platform
  serves from EU/Singapore data centres; the Token Plan host is explicitly CN), plus Python/npm
  SDK names.
- Add provenance patterns for `mimo-`/`mimo/` model ids resolving to bloc `cn` (Xiaomi
  Technology), extending the existing bare `xiaomi/` prefix.
- Curate a data-practices entry: training default `no` (privacy policy states content "will
  not be used for model training or any other purposes"), retention per policy, storage
  regions EU + Singapore (service agreement §4.4), Token Plan tier note.
- Record the drift residue entry for `novita/xiaomimimo/*` as covered (alias target now
  exists in the KB).
- KB website and evidence pack render the new provider automatically from the bundled data.

## Capabilities

### New Capabilities
- (none)

### Modified Capabilities
- `jurisdiction-classification`: Xiaomi MiMo endpoints resolve to documented jurisdictions
  (`unknown`/region-dependent for the global host, `cn` for the Token Plan host).
- `model-provenance`: MiMo model ids resolve to provenance bloc `cn`.
- `provider-data-practices`: curated facts for `xiaomi_mimo` with citations.

## Impact

- `borderlint/data/providers.json` (+1 entry), `provenance.json` (+2 patterns),
  `data_practices.json` (+1 entry), `scripts/kb_drift_aliases.json` (residue note update).
- Detection tests for endpoint + model-reference resolution; site/evidence render via
  existing generators with no code change.
- Shipped package grows by a few KB of JSON; no CLI or evaluation changes.

## Non-goals

- No new detection machinery — the entry uses the existing SDK/endpoint resolution rules.
- No JVM/.NET SDK keys until official coordinates are verified (the SDK-coverage drift check
  will surface the gap honestly).
- No claim about in-PRC service terms: this entry covers the international platform
  (mimo.mi.com / xiaomimimo.com); the PRC-specific terms are a separate curation if needed.
