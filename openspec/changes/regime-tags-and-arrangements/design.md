## Context

The report already surfaces one hardcoded arrangement (the GBA Standard Contract) for flagged
flows. This change generalises that to a bundled list and adds regime tags, so a flagged flow comes
with regulatory context — all reference-only, consistent with "the tool never adjudicates."

## Goals / Non-Goals

**Goals:** tag flagged flows with the implicated regime(s); surface matching arrangement reference(s)
from a bundled list, selected by jurisdictions + home regime.

**Non-Goals:** enforcing/adjudicating arrangements; a complete global regime map; changing severity
or exit codes.

## Decisions

- **Bundled `arrangements.json`, selected heuristically.** Alternative: hardcode each arrangement in
  report code. Rejected — the list is curatable data, like the provider KB.
- **Selection rules are coarse and reference-only.** GBA ⇐ a flow between `hk` and `cn`/`CN-GBA`;
  PIPL cross-border ⇐ a `pipl` home sending outside Mainland/GBA, or a destination in `cn`/`CN-GBA`;
  GDPR ⇐ a destination in the EU/EEA. Over-surfacing a reference is harmless (it is context); the
  user decides applicability.
- **Regime tags are informational, derived from (home regime, destination).** They never feed the
  pass/fail decision — that stays purely the allow-list + deny-by-default.

## Risks / Trade-offs

- Coarse selection may surface an arrangement that doesn't strictly apply → acceptable; it is labelled
  context, not a ruling, and over-surfacing beats omission for a sovereignty tool.
- Arrangement URLs drift → they live in the bundled data and ride the kb-freshness review loop.
