# Design: cn-data-practices-curation

## Context

The `provider-data-practices` capability shipped with three flagship CN providers deliberately
null ("sources unreachable"). Fresh research (2026-08-22) located their primary sources. This
change is pure curation under the existing schema: no new requirements, only filled entries.

## Goals / Non-Goals

**Goals:**

- Replace all-null entries for deepseek, tencent_hunyuan, zhipu with cited facts.
- Keep the KB's honesty contract: quote scope precisely, keep nulls where documents are
  silent, mark caveats in locators rather than generalising.

**Non-Goals:**

- No schema, loader, or renderer changes.
- No re-review of already-complete entries.

## Decisions

### D1: DeepSeek training_default = `opt-out`
The privacy policy states data is processed "to train and improve our technology" and
describes an opt-out right; the Open Platform ToS defers personal-data handling to that policy
with no API carve-out. `opt-out` is the honest vocabulary fit — training happens unless the
user acts. The locator notes explicitly that no self-serve API opt-out mechanism is documented.
*Alternative rejected:* `"yes"` — overstates certainty about whether API traffic is treated as
personal-data processing; `opt-out` preserves the documented right without guessing.

### D2: Tencent retention scoped exactly as written
The 30-day window covers Configuration/Diagnostic & Usage Data "including output information";
whether raw input prompts fall inside it is not explicit. The entry quotes that scope verbatim;
training_default stays null.
*Alternative rejected:* generalising to "inputs and outputs retained 30 days" — would encode a
claim the document does not make.

### D3: Zhipu training_default = `no`, carve-out quoted in locator
The User Agreement commits to no unauthorised use beyond executing service requests; the
Privacy Policy separately reserves anonymised-data model training without consent. Encoding
`no` with the carve-out quoted gives reviewers the real picture; dropping to null would hide a
genuine identifiable-content commitment.
*Alternative rejected:* staying null — discards verified facts; encoding the carve-out as the
headline fact — inverts the reviewer-facing emphasis.

### D4: Subprocessors stay null for deepseek/tencent_hunyuan
Neither publishes a subprocessor list page. Zhipu's named third-party SDK table is recorded in
the `subprocessors` slot using its self-citing `{url, locator, retrieved}` form (the schema's
existing shape — no new mechanism); the locator notes these SDKs cover the platform's
account/payment/analytics surface.
*Alternative rejected:* listing the SDK names as prose in another field — the schema has the
right slot.

## Risks / Trade-offs

- [DeepSeek quotes came via search-snippet corroboration + archive confirmation] → retrieval
  date marked 2026-08-22; drift staleness check forces re-verification within 90 days.
- [CN providers change docs frequently] → per-entry `reviewed` dates + citations make drift
  visible; this is the designed remediation path.

## Migration Plan

Purely additive curation into an existing bundled file. Rollback restores prior entries from
git history; no behavioural migration.

## Open Questions

- None blocking.
