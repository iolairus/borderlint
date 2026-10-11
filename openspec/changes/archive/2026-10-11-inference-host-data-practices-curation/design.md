# Design: inference-host-data-practices-curation

## Context

Ten high-traffic inference hosts sit in the data-practice gap queue. All ten were
researched from primary sources (provider ToS, DPA, privacy documentation, official docs)
on 2026-10-10 — that retrieval date lands on every citation. The batch follows the
CN/FAANG curation precedent: entries under the shipped schema, no loader or renderer
changes, advisory only.

## Goals / Non-Goals

**Goals:**

- Ten cited entries that let a reviewer answer "does this host train on my API traffic, and
  how long does it keep it" without leaving the report.
- Honest treatment of the three hard shapes in this batch: tier-dependent training
  defaults, downstream-party dependence (router/partner models), and genuinely undocumented
  facts.

**Non-Goals:**

- Consumer-app terms; schema changes; re-curation of existing entries; the remaining 92
  gaps.

## Decisions

### D1: API/platform terms only; consumer splits disclosed, not curated

Several providers run consumer apps with different defaults (Perplexity's app trains by
default; Mistral's Le Chat/Vibe differs from the paid API). borderlint detects API usage,
so entries cover the API/platform surface, and a consumer divergence is noted only where it
could mislead a reviewer who conflates the two. This extends the FAANG non-goal into a
standing scoping rule for the batch.

### D2: Tier-dependent training defaults state the conservative primary

`cohere` (trial keys train, paying accounts get an opt-out toggle) and `mistral`
(free-tier Studio trains unless opted out; paid API excluded) both split by tier. The
primary default records the *less* protective tier (`opt-out`) because a detected API key
proves nothing about its tier; the enterprise_tier fact discloses the more protective
posture. Same convention as Meta's Standard/Discounted split in the FAANG batch.

### D3: Downstream-party dependence is recorded in fact text, not the schema

`openrouter` is a router: its own posture is no-training + ZDR, but the effective outcome
depends on the downstream provider unless the user restricts routing. `deepinfra` is a host
with a partner-model carve-out (Google/Anthropic models follow their own policies). Both
entries record the host's commitment as the fact value and the dependence in the fact text.
A schema field for "downstream dependence" was rejected: one field cannot carry the
routing-control semantics, and the advisory framing already demands reading the text.

### D4: JS-rendered trust centers are cited through their naming contract

Several subprocessor lists (Cerebras, Perplexity, SambaNova, Fireworks, Together, Mistral)
are Vanta/SafeBase JS apps whose contents are not machine-readable. The subprocessor fact
cites the provider's DPA/terms clause that names the list URL as canonical (a readable,
provider-authored source), never a note claiming the page was unreachable — the base spec's
no-stale-unavailability-notes requirement applies. List contents are browser-verifiable by
the reviewer; what the KB asserts is the list's canonical location.

### D5: Inferred `no` is allowed when the license is purpose-limited — with the clause quoted

`cerebras` and `sambanova` never say "we do not train" verbatim; the `no` rests on a
license scoped to service provision ("and for no other purposes"). That is a real legal
signal, weaker than an explicit commitment. The entry records `no` with the actual clause
quoted in the locator, so the reviewer sees the basis rather than a bare label. SambaNova's
retention stays null: nothing documents it for the hosted API, and the sovereign/on-prem
ZDR marketing does not transfer to the hosted service.

## Risks / Trade-offs

- [Terms change after the retrieval date] → every citation carries `retrieved:
  2026-10-10`; the entries are explicitly "as of" statements, and the drift checker's
  staleness clock (`updated` bump in this change) restarts the review interval.
- [Together's "product improvements" secondary use reads harsher than its `no` training
  default] → recorded verbatim in the retention fact; the training_default field answers
  only the training question, per the schema.
- [Enterprise tiers may offer undocumented-better terms] → entries record the public
  baseline; enterprise_tier notes where private paper can supersede.

## Open Questions

- (none — research complete; ambiguous facts are nulls by design, not open questions)
