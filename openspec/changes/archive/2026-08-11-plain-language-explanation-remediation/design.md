## Context

borderlint currently emits terse reason codes. Users must map `residency`, `sovereignty`, `unknown` etc. to actionable guidance. The CLI is deterministic, zero-deps, and must remain so.

## Goals / Non-Goals

**Goals:**
- Add `--explain` flag to `scan` that produces plain-language explanations and remediation hints per finding.
- Keep explanations deterministic, template-driven, no LLM.
- Preserve exit codes and gating semantics.

**Non-Goals:**
- No LLM enrichment, no auto-fix, no policy generation.
- No change to SARIF/evidence formats; mermaid, sbom, html, and badge outputs are unchanged in v1 (`--explain` affects text and json only).

## Decisions

- **Template-driven explanations**: Map reason codes to human text via `report.explain_reason()` using KB names and policy context. Rejected LLM generation to keep zero deps.
- **Flag-gated output**: `--explain` toggles explanation fields in text/json. Rejected always-on to avoid noise.
- **No new data model**: Reuse `Finding` and `Detection`; add optional `explanation` string computed at render time.

## Risks / Trade-offs

- [Risk] Explanation text may drift from policy semantics] → Mitigation: unit tests for each reason code template.
- [Risk] Localization not supported] → Mitigation: English only for v1, matches repo language.
