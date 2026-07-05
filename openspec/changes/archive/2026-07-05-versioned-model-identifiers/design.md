## Context

`_MODEL_ID` (`kb.py:117`, `^[A-Za-z0-9._/:-]{3,100}$`) gates every candidate literal before
prefix matching; `@` is not in the charset, so Vertex/Bedrock version-pinned ids fail the gate
outright. The freshness report shows the fallout: `claude` 18, `mistral` 8, `jamba` 4,
`codestral` 4. The digit-led pins resolve once the suffix strips (codestral needs one bare
pattern the map lacks); the letter-led pins (`@default`, `@latest`) stay invisible by the same
rule that excludes emails — expected residue, not a defect.

## Goals / Non-Goals

**Goals:** version-pinned ids resolve to the same bloc as their base identifier; zero new
false-positive surface.
**Non-Goals:** general `@` support in identifiers; version-aware resolution.

## Decisions

### D1 — Split the suffix, don't loosen the charset
**Decision:** `match_model` strips one trailing `@<version>` where `<version>` matches
`\d[A-Za-z0-9.-]*`, then validates and matches the remainder exactly as today. The original
literal (suffix included) is returned as evidence.
**Rationale:** The version is metadata about *which* weights snapshot, never *whose* weights —
provenance is a property of the base identifier.
**Alternatives rejected:**
- *Add `@` to `_MODEL_ID`.* Rejected: every email address in a scanned string literal becomes a
  candidate, and `gemini-team@google.com` starts with a live prefix — a guaranteed
  false-positive class. The digit-led rule kills emails structurally (domains start with a
  letter).
- *Add versioned patterns to the map (`claude-3-5-haiku@20241022`).* Rejected: unbounded data
  churn for what is one grammar rule; every new snapshot date would be a KB gap.

### D2 — One suffix, at the end, nothing else changes
**Decision:** Exactly one `@` is recognised, only in trailing position; multi-`@` literals and
`@`-elsewhere literals stay invisible, as today.
**Rationale:** The observed grammar (Vertex, Bedrock) has exactly one version pin; anything
else is not a model identifier shape we know, and unknown shapes stay unmatched by design.

## Risks / Trade-offs

- **[Digit-led version that is really something else]** A literal like `thing@2fast` would be
  split and `thing` matched. → Bounded by anchoring: `thing` must still start with a known map
  prefix; the pre-@ part faces exactly the same gate as any bare literal.
- **[Versioned `.gguf` paths]** `dir/model@2407.gguf` strips the suffix before the basename
  rule and then fails anchoring, where the unversioned path would match by basename. No
  regression (today it fails the charset gate outright) and not an observed real-world form;
  accepted, documented here.

## Migration Plan

1. Suffix split in `match_model` (one regex + slice before the existing gate).
2. Tests: Vertex and Bedrock versioned forms resolve; email negative; evidence carries the
   full literal.
3. Rollback: revert — data untouched.

## Open Questions

None.
