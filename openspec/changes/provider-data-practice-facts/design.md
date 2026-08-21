# Design: provider-data-practice-facts

## Context

borderlint bundles several hand-curated knowledge bases (`providers.json`, `sovereignty.json`,
`provenance.json`, `regimes.json`, …), each loaded by a small stdlib-JSON function in
`borderlint/kb.py` and each carrying a top-level last-reviewed date consumed by
`scripts/kb_drift.py`. The KB website (`scripts/kb_site.py`) renders provider pages from
these files, and the evidence pack (`borderlint/report.py`) renders per-flow governance
facts. Data-practice facts (training default, retention, subprocessors, enterprise delta)
are a new dimension over the same provider ids, with a different review cadence and a
citation-per-fact shape none of the existing KBs have.

## Goals / Non-Goals

**Goals:**

- A bundled, citable, review-dated data-practice KB keyed by existing provider ids.
- Reviewer-facing surfacing: evidence pack register + KB website provider pages.
- Staleness and curation-gap coverage in the scheduled drift check.
- Strictly advisory: zero influence on detection, verdicts, or exit codes.

**Non-Goals:**

- No auto-scraping or auto-fill of ToS content; no upstream feed ingestion for facts.
- No new CLI flags or JSON output fields (consumers can be added later without breakage).
- No legal analysis or regime-specific advice beyond the existing annex behaviour.
- No restructuring of `providers.json`.

## Decisions

### D1: Separate `data_practices.json`, not new fields on `providers.json`
Facts have their own cadence, schema (citations), and curation workflow. Mixing them into
provider entries would force residency re-reviews whenever a ToS fact changes and would
bloat the core resolution path.
*Alternative rejected:* extend `providers.json` entries — couples unrelated review cycles
and complicates the hot loader.

### D2: Per-fact citation objects `{url, locator, retrieved}`
The four facts typically live on different pages/sections of a provider's documentation;
a single per-entry source would be wrong as soon as one fact updates.
*Alternative rejected:* one source link per entry — loses precision reviewers need to
verify claims.

### D3: Retention stored as free text, not a structured duration
Real windows are conditional ("30 days unless legally required", "zero-retention for
enterprise"). Structured day-counts would encode false precision.
*Alternative rejected:* numeric retention days — cannot express conditions; would invite
wrong comparisons.

### D4: Standalone loader function following the existing pattern
A `load_data_practices()` function in `kb.py` mirroring `load_sovereignty()`/
`load_provenance()`: stdlib JSON, offline, returns a plain dict keyed by provider id.
Missing file is a packaging error (fail loud), consistent with other KBs.

### D5: Drift integration reuses the suppression list and report-item upsert
Two new sections in `scripts/kb_drift.py` — stale data-practices entries and providers
lacking coverage — flow through the existing open-item update logic (no duplicates across
runs) and honour `kb_drift_aliases.json` suppressions. Gap records carry no fact values,
per spec.

### D6: Seed curation covers flagship providers only
Initial entries for the highest-traffic providers (e.g. OpenAI, Anthropic, Google, Azure
OpenAI, AWS Bedrock); everything else surfaces honestly as "not curated". Curation depth
grows via PRs, matching the project's contribution model.

## Risks / Trade-offs

- [ToS facts silently go stale] → retrieval dates rendered everywhere + staleness section
  in the drift check on the standard review interval.
- [Readers mistake facts for legal advice] → mandatory disclaimer on every rendering
  surface, enforced by spec scenarios and tests.
- [Provider-id drift between the two KBs] → drift check reports mismatches; loader tests
  assert every data-practices key exists in `providers.json`.
- [Package size growth] → a few KB of JSON; negligible against existing bundled KBs.

## Migration Plan

Purely additive: new data file, new loader, new render sections. Rollback is removing the
file and the render call sites; scanners never depend on the KB, so no behavioural rollback
is needed. No data migration.

## Open Questions

- Exact seed provider list and per-provider citations (resolved during implementation by
  reading current public documentation; each fact needs URL + locator + retrieval date).
