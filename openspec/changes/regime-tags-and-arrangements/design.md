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
- **Selection rules are explicit and reference-only:**
  - **GBA Standard Contract** ⇐ a flow between `hk` and `CN-GBA` (the nine GBA cities) — **not** plain
    `cn`, which is outside the GBA zone (Beijing is the canonical not-covered case).
  - **PIPL cross-border** ⇐ a destination of `cn` (Mainland China, outside the GBA), or a `pipl` home
    sending outside Mainland/GBA.
  - **GDPR Chapter V** ⇐ a destination in the EU/EEA set: the `eu` token, or a member country code
    (`at be bg hr cy cz dk ee fi fr de gr hu ie it lv lt lu mt nl pl pt ro sk si es se is li no`).
  Over-surfacing a reference is harmless — it is labelled context, and the user decides applicability.
- **Regime tags are pinned to {PDPO, PIPL}** (the v1 home/destination regimes) and are informational
  only. GDPR stays a *reference link*, never a regime tag — keeping tags within the v1 regime focus
  and off the "global regime map" non-goal. Tags and references never feed the pass/fail decision —
  that stays purely the allow-list + deny-by-default.
- **Tag and arrangement are intentionally decoupled.** An `hk`->`CN-GBA` flow is tagged PIPL (the
  underlying regime of the GBA cities) yet surfaces the *GBA Standard Contract*, not the PIPL
  cross-border reference -- the tag names the law, the arrangement names the operative transfer route.
  Don't collapse them.

## Risks / Trade-offs

- Coarse selection may surface an arrangement that doesn't strictly apply → acceptable; it is labelled
  context, not a ruling, and over-surfacing beats omission for a sovereignty tool.
- Arrangement URLs drift → they live in the bundled data and ride the kb-freshness review loop.
