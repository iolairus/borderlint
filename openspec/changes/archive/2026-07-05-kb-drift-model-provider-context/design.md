## Context

`model_coverage_gap` sees bare keys; `upstream_models` (`scripts/kb_drift.py`) discards each
entry's `litellm_provider`. The suppression list (aliases/ignores) and the KB's
`provenance_defaults` already encode exactly the two provider-context facts the check lacks.

## Goals / Non-Goals

**Goals:** the family section lists only ids a curator can act on (pattern, passthrough, or a
conscious `unknown`).
**Non-Goals:** scanner changes; suppressing multi-model hosts.

## Decisions

### D1 — Pair each id with its upstream provider; two context rules
**Decision:** `upstream_models` returns `(key, litellm_provider)`; `model_coverage_gap` excludes
ids whose provider is in the ignore list, and counts as covered ids whose provider — direct id match (normalised like `coverage_gap`) or
alias-list target — is a **speech-category** provider with a first-party default
(`kb.default_provenance(pid) != "unknown"`).
**Rationale:** An ignored provider's "models" are API routes, not weights; a first-party
provider's house ids resolve via tier 2 in every real scan, so listing them asks a human to
curate what the scanner already answers.
**Alternatives rejected:**
- *A model-id ignore list.* Rejected: per-id suppression rots fast and duplicates what the
  provider-level judgment already states once.
- *Treat all covered providers' ids as covered.* Rejected: multi-model hosts (fireworks,
  together, fal) serve third-party weights; their uncovered ids are the check's real signal.
- *First-party coverage for all 29 defaulted providers.* Rejected: it silences the exact signal
  that drives pattern curation — a novel first-party family (the next `o1`) would never surface,
  yet bare model strings in code resolve only via patterns. Speech tiers are the observed junk
  class; the category bound keeps the fix that narrow.

## Risks / Trade-offs

- **[A first-party provider starts hosting third-party models]** Its ids would be silently
  "covered". → Same drift class as the default itself; the defaults are reviewed data
  (`provider_defaults`), and removing the default restores the ids to the report.

## Migration Plan

1. Return pairs from `upstream_models`; thread suppression + kb defaults into
   `model_coverage_gap`.
2. Tests per rule; live run to measure.
3. Rollback: revert — report-only behavior.

## Open Questions

None.
