## Context

`_VERSION_SUFFIX` (`kb.py`) is `@\d[A-Za-z0-9.-]*$` — deliberately digit-led to exclude emails.
The prior change's review enumerated the residue this leaves: nine `@default`/`@latest` Vertex
ids (six claude, three mistral/codestral), documented then as expected residue. The user has
elected to clear them.

## Goals / Non-Goals

**Goals:** the two Vertex meta-pins resolve; zero widening beyond them.
**Non-Goals:** arbitrary letter-led suffixes.

## Decisions

### D1 — A closed token set, not a looser pattern
**Decision:** `_VERSION_SUFFIX` becomes `@(?:\d[A-Za-z0-9.-]*|default|latest)$`.
**Rationale:** `default` and `latest` are Vertex's documented meta-versions — an enumerable,
closed set. The email-exclusion argument survives intact because no domain is literally
`default` or `latest`.
**Alternatives rejected:**
- *Admit any `[a-z]+` suffix.* Rejected: reopens the email false-positive class the digit-led
  rule exists to kill (`gemini-team@google.com` → `@google.com` would strip).
- *Add versioned patterns to the map.* Rejected same as before: grammar, not data.

## Risks / Trade-offs

- **[A literal like `thing@latest` in non-model contexts]** Docker tags (`image@latest` is not
  valid Docker syntax — tags use `:`) and npm ranges (`pkg@latest`) — an npm string like
  `eslint@latest` would strip to `eslint`, which matches no model prefix; bounded by anchoring
  as ever.

## Migration Plan

1. One-line regex change; tests. Rollback: revert.

## Open Questions

None.
