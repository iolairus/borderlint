# Design: xiaomi-mimo-coverage

## Context

Xiaomi MiMo is a top-5 token-volume provider (OpenRouter weekly, Aug 2026) absent from the KB.
The provenance map already carries a bare `xiaomi/` org prefix (bloc `cn`), and a drift residue
entry acknowledges `novita/xiaomimimo/*` ids as "nothing actionable" — but there is no provider
entry, so endpoint references to `api.xiaomimimo.com` flow undetected and no data-practice facts
exist. The platform documents two distinct hosts with different data postures.

## Goals / Non-Goals

**Goals:**

- Endpoint detection for both documented hosts with honest per-host jurisdictions.
- Provenance resolution for bare and qualified MiMo model ids.
- Curated, cited data-practice facts from Xiaomi's primary sources.

**Non-Goals:**

- No new detection machinery; no JVM/.NET SDK keys until official coordinates are verified.
- No in-PRC service terms curation (this covers the international platform only).

## Decisions

### D1: Global host resolves `unknown`, Token Plan host resolves `cn`
The service agreement (§4.4) states international-platform data is stored on servers in **Europe
and Singapore**, so `api.xiaomimimo.com` cannot honestly resolve to a single country — it gets
`unknown` (region-dependent), matching how `vertex_ai` is handled. The Token Plan host is
explicitly named `token-plan-cn.xiaomimimo.com` and documented as CN-only → `cn`.
*Alternative rejected:* resolving the global host to `sg` — the docs name two regions, not one;
picking either would understate EU exposure.

### D2: Provider id `xiaomi_mimo`, not `xiaomi`
`xiaomi` alone collides conceptually with Xiaomi's non-AI open platform (`open.be.mi.com`);
the AI API platform brands itself "Xiaomi MiMo". The id matches the drift residue naming
(`novita/xiaomimimo/*`) and keeps future Xiaomi services unambiguous.
*Alternative rejected:* `mimo` — ambiguous with unrelated products.

### D3: Provenance via two patterns, not one
Add `mimo-` (bare ids like `mimo-v2.5-pro`, which the quickstart examples use) alongside the
existing `xiaomi/` org prefix, plus the literal `novita/xiaomimimo/` for the redistributor
path — `match_model` anchors at the literal's start, so a bare `xiaomimimo/` pattern would
never match the two-qualifier form (verified empirically). All resolve bloc `cn`, org Xiaomi;
once the patterns land, the drift coverage gap for the residue id closes and its residue entry
is retired.
*Alternative rejected:* relying on the bare `xiaomi/` prefix only — misses bare `mimo-*` ids;
a `passthrough_orgs` entry for `novita/` — passthrough strips only one org and is meant for
quantizer hubs, not inference redistributors.

### D4: SDK keys limited to Python/npm names verified from docs
The quickstart shows OpenAI/Anthropic SDK usage via `base_url` (no dedicated SDK package), so
the entry lists no `sdks`/`npm` packages — detection rides on endpoint hosts. This avoids
fabricating coordinates; the SDK-coverage drift check will report the gap if official packages
appear later.
*Alternative rejected:* listing `openai`/`anthropic` as sdks — they are generic clients, not
MiMo-specific packages; listing them would misattribute every OpenAI import.

### D5: Data-practices facts cite both primary documents
Training default `no`: privacy policy §3.1 states submitted content "will not be used for model
training or any other purposes". Storage: service agreement §4.4 (EU + Singapore servers).
Retention: privacy policy §6 (purpose-bound, deleted/anonymised after fulfilment or erasure).
Token Plan tier note: dedicated CN base URL + `tp-` keys. Subprocessors: null — the policy
names third parties (Waffo HK for payments, Google for search) but publishes no list page.
*Alternative rejected:* citing the in-PRC terms — out of scope per proposal.

## Risks / Trade-offs

- [`unknown` jurisdiction may feel vague] → rendered as region-dependent with the EU+SG note
  surfaced in data practices; operators see the real posture instead of a false certainty.
- [Host set may grow] → new hosts are additive JSON rows; drift check flags uncovered upstreams.
- [Residue retirement changes drift output] → covered by updating the residue reason to point
  at the new provider entry rather than deleting history.

## Migration Plan

Purely additive bundled-data change. Rollback removes the entries; no behavioural migration.

## Open Questions

- None blocking; JVM/.NET SDK coordinates deferred until officially published.
