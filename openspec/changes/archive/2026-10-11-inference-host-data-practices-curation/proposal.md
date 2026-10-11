# Proposal: inference-host-data-practices-curation

## Why

Ten high-traffic multi-model inference hosts are fully detectable in borderlint but have no
curated data-practice facts, so reviewers see "not curated" exactly where API inference
traffic concentrates. These are the providers a GBA reviewer most often finds between an
application and the model. Their governing documents are public (ToS, DPA, trust centers),
and all ten were researched from primary sources on 2026-10-10, making this the
highest-value curation batch remaining in the 102-entry gap queue.

## What Changes

- Add ten curated entries to `borderlint/data/data_practices.json`, each fact cited with
  URL + locator + retrieval date (2026-10-10), undocumented facts null:
  - `fireworks_ai` — training `no`; zero retention by default for inference (Response API
    with `store=true` retains 30 days); subprocessor list named in the DPA.
  - `together_ai` — training `no` (opt-in only); default stores prompts/responses until the
    user deletes them (no fixed window) with a documented "product improvements" secondary
    use; self-serve ZDR.
  - `groq` — training `no`; no retention by default, reliability/abuse logs up to 30 days;
    self-serve ZDR for all customers.
  - `cohere` — training `opt-out` (dashboard toggle for paying accounts; trial keys train
    with no documented opt-out); logged prompts deleted after 30 days; ZDR by enterprise
    approval.
  - `mistral` — training `opt-out` as primary default (free-tier Studio trains unless opted
    out); tier fact discloses the paid API is excluded from training by default; 30 rolling
    days abuse monitoring; request-based ZDR on paid stateless endpoints.
  - `perplexity` — training `no` for the API; zero retention is the API default (consumer
    app posture differs and is out of scope).
  - `deepinfra` — training `no` with a partner-model caveat (Google/Anthropic models on
    DeepInfra follow those companies' policies); contractual zero retention.
  - `openrouter` — training `no` and ZDR for OpenRouter the routing layer; downstream model
    providers may train unless the user restricts routing — the entry records both layers.
  - `cerebras` — training `no` (purpose-scoped license, no training right taken); inputs/
    outputs not retained; log retention has no documented bounded window.
  - `sambanova` — training `no` via a purpose-limited license (no explicit no-train
    sentence — locator quotes the actual clause); retention null (genuinely undocumented
    for the hosted API).
- KB website pages and the evidence-pack register render the entries automatically; the
  drift gap list shrinks 102 → 92.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `provider-data-practices`: adds ten entries under the shipped schema; no requirement text
  changes (cited-facts and no-stale-notes invariants apply).

## Impact

- `borderlint/data/data_practices.json`: ten new entries; drift gap list shrinks.
- No loader, renderer, CLI, detection, or evaluation changes. Advisory only — verdicts,
  policy evaluation, and exit codes are unaffected.

## Non-goals

- No consumer-app variants (Le Chat/Vibe, Perplexity Free/Pro/Max) — API/platform terms
  only, with tier splits disclosed in the tier fact where they exist.
- No schema changes (secondary-use nuances like Together's "product improvements" are
  recorded in fact text, not new fields).
- No re-curation of the 16 existing entries, and no curation of the remaining 92 gaps.
- No verification of JS-rendered trust-center list contents: where a list URL is confirmed
  only via the governing contract, the citation says so rather than claiming unavailability.
