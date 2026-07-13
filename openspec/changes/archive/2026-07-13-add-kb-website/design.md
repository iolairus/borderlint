# add-kb-website — design

## Context

The KB lives in six date-stamped JSON files under `borderlint/data/`. `scripts/` already holds
stdlib-only dev tooling (`kb_drift.py`), and CI has three workflows (ci, release, kb-refresh) but
no Pages deployment. There is no site tooling of any kind in the repo. The audience is
non-developer practitioners arriving from search engines, so pages must be fast, readable, and
individually addressable; there is no need for interactivity.

## Goals / Non-Goals

**Goals:**
- One command turns the bundled KB into a complete static site; CI publishes it on KB change and release.
- Pages good enough for long-tail search: unique titles/descriptions, one subject per URL, honest about unknowns.

**Non-Goals:**
- JavaScript, search, analytics, custom domains, hand-authored content, per-model pages.

## Decisions

1. **Plain stdlib generator (`scripts/kb_site.py`) emitting HTML strings**, mirroring the house
   pattern from the `--format html` renderer (escape everything, one shared inline CSS block).
   *Alternatives:* mkdocs/Jekyll/Sphinx — rejected: a dependency and a theme to maintain for what
   is a projection of six JSON files; Jekyll additionally drags in Ruby on CI.
2. **Output to `site/` (gitignored), built fresh in CI.** *Alternative:* committing rendered HTML
   to `docs/` for classic Pages — rejected: generated artifacts in git drift from their source and
   bloat diffs; the Pages-actions path deploys from a build artifact instead.
3. **Model pages at developer-organisation grain**: `provenance.json` patterns grouped by `org`
   (all 211 patterns carry `org` and `bloc`), one page per organisation listing its patterns and
   bloc(s); slug normalised from the org name, deterministic suffix on collision. Chosen because
   the slug is unambiguous and it matches how practitioners ask the question ("whose models?").
   *Alternatives:* one page per pattern (~211) — rejected: thin near-duplicate pages hurt search
   and readers alike; grouping by (org, bloc) or pattern prefix — rejected: prefix-derived slugs
   are ambiguous when a group holds several prefixes.
4. **URLs are stable slugs**: `providers/<provider-id>.html` (ids already exist and don't change)
   and `models/<org-slug>.html` (normalised from the organisation name, deterministic); no date or
   hash in URLs so links keep working.
5. **Regime/arrangement references resolved per provider jurisdiction** by reusing the mappings in
   `regimes.json` / `arrangements.json` directly. All page *content* comes from the KB JSON; the
   generator imports only display-name constants (`JURIS`, `SOVEREIGNTY`) from `borderlint.report`
   rather than duplicating ~50 label strings that would drift. Regimes render as names only
   (the KB stores no regime URLs); arrangements carry a `url` and render as hyperlinks.
   `evidence_regimes.json` is not used — it holds filing expectations, not page content.
6. **Workflow uses the standard Pages pair** (`actions/upload-pages-artifact` +
   `actions/deploy-pages`) with triggers: push to `main` filtered on `borderlint/data/**` and
   `scripts/kb_site.py`, `release: published`, `workflow_dispatch`. *Alternative:* deploying on
   every push — rejected: pointless rebuilds and a noisy deployment history.

## Risks / Trade-offs

- [Pages must be enabled once in repo settings] → task includes enabling via `gh api`; workflow
  fails loudly with a clear message if not enabled.
- [Org-name slugs can collide after normalisation] → slugs normalised (lowercase, `-`),
  collisions suffixed deterministically; smoke test asserts uniqueness.
- [Search indexing takes weeks-months to compound] → acceptable: the site costs nothing to keep
  publishing; value accrues.

## Open Questions

None.
