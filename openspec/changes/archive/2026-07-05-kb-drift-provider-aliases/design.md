## Context

`coverage_gap` (`scripts/kb_drift.py`) diffs upstream `litellm_provider` names against the
bundled KB's ids/names/SDK aliases. litellm's names are routes, not providers: `bedrock`,
`bedrock_converse`, `azure`, `azure_ai`, `gemini`, `chatgpt`, `palm` all denote providers the
KB covers under different ids, and a dozen more entries are search/scraping tools with no model
weights. The only suppression channel today is the KB's `sdks` list, which drives real import
detection — using it for drift aliases would make `import bedrock` a detection.

## Goals / Non-Goals

**Goals:** the provider section lists only genuinely unreviewed providers; every suppression is
a recorded human judgment; aliases fail loudly when their target disappears.
**Non-Goals:** touching scanner data or behavior; auto-classifying upstream names.

## Decisions

### D1 — Dev-side JSON next to the script, not bundled KB data
**Decision:** `scripts/kb_drift_aliases.json` with `aliases: {upstream → provider_id}` and
`ignore: {upstream → reason}`. Read by `kb_drift.py` only.
**Rationale:** This is drift-tooling configuration, invisible to scans; `borderlint/data/`
ships in the wheel and is loaded by `load_kb` — the wrong blast radius for CI-only data.
**Alternatives rejected:**
- *Extend `sdks` on provider entries.* Rejected: `sdks` drives import detection; `bedrock`
  as an SDK alias would fabricate detections.
- *Constants in the script.* Rejected: curation is data work; a JSON diff in a PR reads better
  than a Python diff, matching how every other KB is curated.
- *A `drift` block inside `providers.json`.* Rejected: same file, two audiences; the scanner's
  KB should contain only what the scanner reads.

### D2 — Aliases are existence-validated; ignores carry reasons
**Decision:** Every alias target must be a provider id present in the bundled KB — a missing
target raises, failing the weekly job loudly. Every ignore entry is `name: reason` (e.g.
`"firecrawl": "web scraping API, no model weights"`); an empty reason raises.
**Rationale:** An alias to a renamed/removed provider would silently re-hide a real gap — the
exact silent-rot class the freshness machinery exists to prevent. Reasons make each ignore an
auditable judgment, mirroring the human-assignment rule.
**Alternatives rejected:**
- *Warn instead of fail on unknown targets.* Rejected: a warning in a weekly cron's log is
  read by nobody; loud failure is the only observed channel.

### D3 — Suppression applies to the provider section only
**Decision:** `coverage_gap(upstream, known, suppression)` takes the suppression list as an
explicit third input — loaded in `main()` and passed in, like the upstream fetch — keeping the
diff a pure function. The model-family, sovereignty, and staleness sections are untouched.
**Rationale:** The family section already has its own honest suppression channels (patterns,
passthroughs); a second mechanism would blur which one owns a given name.
**Alternatives rejected:**
- *Extend suppression to the family/sovereignty sections.* Rejected: patterns, passthroughs,
  and the sovereignty map are those sections' curation channels; a name suppressed in two
  places has no single owner and rots in both.
- *Load the file inside `coverage_gap`.* Rejected: file I/O inside the diff breaks the
  pure-function contract the deterministic-diff requirement enumerates.

## Risks / Trade-offs

- **[Stale ignores]** A tool on the ignore list later ships an LLM API (e.g. a search vendor
  adds models). → The reason string dates the judgment; the entry is one PR to reverse. The
  weekly issue's convergence makes a wrong ignore visible by absence, which humans do notice
  when a vendor makes news.

## Migration Plan

1. Add `kb_drift_aliases.json` (first pass: route aliases + non-model tools from issue #39).
2. Load + validate in `main()`; pass to `coverage_gap(upstream, known, suppression)`;
   update the New-providers preamble to point triagers at the alias/ignore channel.
3. Tests: suppression, unknown-target raise, empty-reason raise, unaliased names still surface.
4. Rollback: revert; the report re-widens, nothing else changes.

## Open Questions

None.
