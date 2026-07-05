## Context

Identical shape to `bloc-vocabulary-completion` (archived 2026-07-04), one bloc instead of five.
The vocabulary lives in five copies (kb.py ×2, policy.py ×2, report.py display map) plus four
hardcoded error-message lists; the sources block documents each bloc's compelled-disclosure
regime; the Apertus family is org-anchored on the hub (`swiss-ai/…`) with a distinctive stem.

## Goals / Non-Goals

**Goals:** `ch` valid everywhere a bloc is accepted; Apertus resolves.
**Non-Goals:** Swiss providers; further blocs (the drift check surfaces the next candidate).

## Decisions

### D1 — Same recipe as the five-bloc completion
**Decision:** `ch` joins both frozensets, both mirrors, the display map ("Switzerland" — the
JURIS label for the same code), the error messages, and the sources block (revised FADP, in
force 2023, plus the BÜPF interception framework). Patterns: `apertus` (distinctive stem, no
collision surface) and `swiss-ai/` (org).
**Rationale:** The invariant from the completion change holds: one vocabulary, one display map;
a bloc valid in one dimension but not the other breaks the shared rendering.
**Alternatives rejected:**
- *Map Apertus to `eu`.* Rejected: Switzerland is not EU/EEA; the sovereignty map's value is
  honesty about legal regimes, and this would be the first deliberately wrong entry.
- *Wait for more Swiss families.* Rejected by the human decision in the issue #39 triage; a
  bloc costs one token per copy and the family is live upstream now.

## Risks / Trade-offs

- **[`apertus` collision]** Latin word, rare in code; no known tool or package namespace;
  anchored matching bounds the residue risk.
- **[litellm-qualified literals]** A code literal in the full upstream form
  (`publicai/swiss-ai/apertus-…`) stays `unknown` at detect time — `publicai/` is neither a
  passthrough nor a pattern — consistent with every provider-qualified litellm id. The drift
  check's any-depth suffix matching still clears the report entry.

## Migration Plan

1. Vocabulary copies + error messages; data entries; docs; tests. Rollback: revert.

## Open Questions

None.
