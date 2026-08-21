# Proposal: provider-data-practice-facts

## Why

Privacy reviewers evaluating AI providers ask the same four questions first — does the
provider train on my API data by default, what is the retention window, where is the
subprocessor list, and does an enterprise tier change the answer — and today they dig each
answer out of scattered ToS pages. borderlint already earns trust by hand-curating
residency and sovereignty facts; these data-practice facts are the adjacent set with the
same curation-is-the-value property. Surfacing them in the evidence pack means a reviewer
gets the answers next to the flow inventory they are already filing.

## What Changes

- Add a bundled, hand-curated knowledge base of per-provider data-practice facts covering
  the four canonical questions, each fact carrying a source citation (URL + locator note)
  and a retrieval date, with each entry carrying its own last-reviewed date.
- Expose the facts through the KB loader (offline, stdlib JSON, no schema break to
  existing entries).
- Render a data-practices section on each provider page of the KB website: facts, citations
  as hyperlinks, as-of dates, and an advisory disclaimer. Providers without curated facts
  state that explicitly.
- Extend the evidence pack with a per-provider data-practices register (citations and
  as-of dates included; uncurated providers rendered as explicitly not curated).
- Cover the new knowledge base in the scheduled freshness/staleness check so facts are
  re-reviewed on the standard interval.
- Facts are advisory statements about documented practices — never legal advice and never
  auto-filled from upstream feeds.

## Non-goals

- No auto-scraping or auto-fill of ToS content; facts enter only via human-curated PRs.
- No new CLI flags or JSON output fields; surfacing is limited to the evidence format and
  the KB website.
- No legal analysis beyond advisory statements about documented practices.
- No restructuring of the existing `providers.json` knowledge base.

## Capabilities

### New Capabilities
- `provider-data-practices`: bundled per-provider data-practice facts (training default,
  retention, subprocessors, enterprise-tier delta) with citations, review dates, human
  curation, and explicit absence handling.

### Modified Capabilities
- `kb-website`: provider pages gain a data-practices section with citations and disclaimer.
- `cli-and-reporting`: the evidence pack gains a data-practices register for providers in
  the flow inventory.
- `kb-freshness`: the staleness check explicitly covers the data-practices knowledge base.

## Impact

- New bundled data file (`borderlint/data/data_practices.json`) — shipped package grows,
  no new runtime dependencies.
- `borderlint/kb.py` loader; `borderlint/report.py` evidence renderer; `scripts/kb_site.py`
  generator; `scripts/kb_drift.py` staleness inputs; `tests/test_borderlint.py`.
- No CLI surface change: the facts appear only in the `evidence` format and the KB website.
- No detection or policy-evaluation behaviour changes.
