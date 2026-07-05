## Context

After the provider-context change, the family section's remainder is dominated by classes a
human has already judged unresolvable (pricing buckets, `fal_ai/`-style path ids, bare words),
but the judgment lives in conversation history, not in the machinery. The suppression file
already carries two judgment classes (aliases, ignores) with loud-fail validation — the natural
home for a third.

## Goals / Non-Goals

**Goals:** the issue separates "decide me" from "acknowledged inert"; every acknowledgment is a
recorded, reasoned entry; nothing is hidden — residue renders with counts.
**Non-Goals:** changing what counts as covered; touching the provider section.

## Decisions

### D1 — Residue is a reporting classification applied after matching
**Decision:** `residue` maps exact identifiers or id-prefixes (lowercase, matched against the
full upstream key; an entry ending in `/` or `-` reads naturally as a prefix, but all entries
match by prefix — exactness comes from writing the full key) to reasons. The 2026-07-05 seed is
a bulk acknowledgment: every currently uncovered id as an exact key (human review: nothing
actionable), plus prefixes only for classes that keep arriving in the same shape
(`fireworks-ai-`, `together-ai-` pricing buckets; `fal_ai/` path ids). Classification runs on the coverage check's *output*: uncovered ids matching a residue
prefix are grouped per entry and rendered as counts in a collapsed section; the rest stay in the
actionable family list.
**Rationale:** Running after matching means a residue entry can never mask a real covered id or
suppress a future pattern match — the failure mode of every other suppression design.
**Alternatives rejected:**
- *Stem-keyed residue.* Rejected: stems are derived from the shifting id population
  (`fireworks-ai-4.1b` stems to `fireworks`) and would collide with genuine families.
- *Rule-based junk detection (path-segment counts, word lists).* Rejected: clever heuristics
  rot silently; a curated list with reasons is auditable and matches the file's ethos.
- *Excluding residue ids from the report entirely.* Rejected: invisible acknowledgment is
  indistinguishable from coverage; counts keep the residue honest and reversible.

### D2 — Same file, same loud-fail discipline
**Decision:** The `residue` block lives in `kb_drift_aliases.json`; an entry with an empty
reason raises, failing the weekly job. A residue prefix that matches nothing is permitted
silently (ids come and go upstream; a dead entry is inert, not dangerous).
**Rationale:** One file for all drift judgments; the deterministic-diff requirement already
names the curated suppression list as an input, so purity wording is untouched.
**Alternatives rejected:**
- *A separate residue file.* Rejected: two files, one judgment domain; the loud-fail validation
  and the scanner-never-reads guarantee would need duplicating.
- *Warn on dead residue entries.* Rejected: ids come and go upstream; a dead entry is inert,
  and the weekly log is read by nobody.

### D3 — Summary line answers the only question that matters
**Decision:** The report opens with one line: "**Actionable:** N providers, M families ·
**acknowledged residue:** K ids across R classes." Sections follow as today; the residue
section uses a `<details>` block so the issue body stays short.
**Rationale:** The user's stated need is telling "task to do" from "lying around"; the summary
line is that answer, and GitHub renders `<details>` collapsed by default.
**Alternatives rejected:**
- *Encode the counts in the issue title.* Rejected: retitling on every run churns
  notifications and breaks the update-in-place lookup, which matches on the exact title.
- *Omit residue counts from the summary.* Rejected: invisible residue drifts toward
  unauditable; the count is the cheap honesty signal.

## Risks / Trade-offs

- **[Over-broad residue prefix]** e.g. `fal_ai/` acknowledges all future fal ids including a
  hypothetical patternable family. → Accepted for the three timeless classes only (buckets and
  fal paths share one shape); everything else is seeded as exact keys, so future variants —
  a new `command-*` model, a new `azure/o*` id — surface as actionable. The counts keep
  prefix growth visible; narrowing is a one-line PR.

## Migration Plan

1. Residue block + validation; classification + rendering + summary line.
2. Seed entries from the current issue body's structural classes.
3. Tests: classification after matching, count rendering, loud-fail, actionable unaffected.
4. Rollback: revert; the section merges back into the family list.

## Open Questions

None.
