## Why

Vertex pins models with `@default` and `@latest` as well as digit-led versions
(`vertex_ai/claude-fable-5@default`, `vertex_ai/mistral-large@latest`). The version-pin rule is
digit-led only, so nine real upstream ids stay invisible to the scanner and sit permanently in
the freshness report — the meta-pin share of the `@` residue after `versioned-model-identifiers`
shipped. (Two digit-led ids, `text-unicorn@001` and `imagegeneration@006`, remain map-coverage
gaps for legacy Google families — out of scope here.)

## What Changes

- The literal tokens `default` and `latest` become valid version pins alongside digit-led
  tokens: a closed two-word set, so the email exclusion argument is untouched (`@google.com` is
  neither digit-led nor a listed token).
- No other letter-led suffix is admitted.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `model-provenance`: the version-pin requirement admits the two literal tokens.

## Impact

- `borderlint/kb.py` — the version-suffix pattern gains the two alternatives.
- `tests/` — both tokens resolve; other letter-led suffixes still rejected.
- Freshness issue #39 sheds the nine meta-pin `@` ids.

## Non-goals

- No general letter-led suffixes; no version-aware provenance.
