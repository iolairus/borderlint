## Why

Vertex AI and Bedrock pin model versions with an `@` suffix (`claude-3-5-haiku@20241022`,
`mistral-large@2407`, `jamba-1.5-large@001`, `anthropic.claude-haiku-4-5@20251001`). The model
identifier charset excludes `@`, so these literals are invisible to the scanner — flows using
them lose their provenance — and the weekly freshness report carries the digit-led share of the
`claude`, `mistral`, `jamba`, and `codestral` families (~35 ids today) as permanently
unfixable. Letter-led pins (`@default`, `@latest`) are out of scope by design — the digit-led
rule is what excludes emails — and remain expected residue.

## What Changes

- A model identifier MAY carry one version suffix: `@` followed by a digit-led version token
  (`@20241022`, `@2407`, `@001`). The identifier is matched against the provenance map by its
  part before the `@`; the full literal is kept as evidence.
- The suffix must be digit-led — `gemini-team@google.com` stays invisible, because an email's
  domain starts with a letter. The core charset is unchanged; `@` never joins it.
- One data addition serving the same goal: a bare `codestral` pattern, because the map has only
  `codestral-` and the stripped base `codestral` (from `codestral@2405`) would fail without it.
- The drift check inherits the fix for free (it calls the same matcher), clearing the digit-led
  `@` residue from freshness issue #39; `@default`/`@latest` forms stay listed, deliberately.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `model-provenance`: new requirement — version-pinned model identifiers resolve by their base
  identifier.

## Impact

- `borderlint/kb.py` — `match_model` splits a digit-led `@` version suffix before validation
  and matching; `_MODEL_ID` itself is untouched.
- `borderlint/data/provenance.json` — one bare `codestral` pattern.
- `tests/` — versioned forms per platform, the email negative, evidence integrity.
- Freshness issue #39 sheds the digit-led `@` residue of those families on the next run.

## Non-goals

- No general charset loosening: `@` is accepted only as a single, digit-led version delimiter.
- No version-aware provenance (a version suffix never changes the resolved bloc).
- No npm-scope handling (`@anthropic-ai/sdk` is SDK detection's job, not a model reference).
