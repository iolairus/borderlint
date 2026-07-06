## Why

The freshness issue mixes two different things: items awaiting a human decision (a new provider,
a patternable family) and ids that are structurally unresolvable — litellm pricing buckets,
aggregator path-style ids, bare-word ids whose patterns would collide. A triager cannot tell
"task to do" from "known inert residue" without re-deriving the analysis each time, so the
issue reads as ~110 items when the actionable count is a fraction of that.

## What Changes

- The suppression file gains a third block: **residue** — curated id-prefixes with a stated
  reason, classifying uncovered model identifiers as acknowledged structural residue.
- The report's family section shows **actionable** families only; acknowledged residue renders
  in a separate collapsed section as per-class counts (reason + id count), not id lists.
- A leading summary line states the actionable counts, so the issue answers "anything to do?"
  in one line.
- Residue classification applies only to ids the coverage check already failed to resolve — it
  can never mask a covered id, and an id that later gains a pattern simply leaves the residue
  count. Residue entries without a reason fail the check loudly, like ignores.
- Residue entries are exact identifiers or id-prefixes. First curation pass, per the human
  review of 2026-07-05 ("nothing in the current list is actionable"): the full current
  uncovered set bulk-acknowledged as exact ids, plus prefixes for the timeless structural
  classes (litellm pricing buckets, `fal_ai/` path ids) that keep arriving in the same shape.
  New upstream ids match neither and surface as actionable.
- The seven surfacing providers move to the ignore list with reasons recording the same review
  ("reviewed 2026-07-05, not actionable; revisit on new information").

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kb-freshness`: new requirements for acknowledged structural residue and the actionable
  summary line; the scheduled-check, model-coverage, and suppression-list requirements updated
  to track them.

## Impact

- `scripts/kb_drift_aliases.json` (residue block), `scripts/kb_drift.py` (classification +
  rendering + summary line), tests.
- Issue #39 becomes a one-line answer to "is there anything to do?".

## Non-goals

- No change to coverage semantics — residue is a reporting classification, never a matching rule.
- No auto-close-on-empty (separate, currently moot).
- No residue mechanism for the provider section: every listed provider is a pending human
  decision by definition.
