<!-- PR for /opsx change provider-data-practice-facts -->

## Summary

Privacy reviewers evaluating AI providers ask the same four questions first — does the provider
train on my API data by default, what is the retention window, where is the subprocessor list,
and does an enterprise tier change the answer — and today they dig each answer out of scattered
ToS pages. This change adds a bundled, hand-curated `data_practices.json` knowledge base answering
those questions for five flagship providers (OpenAI, Anthropic, Google Gemini, Azure OpenAI,
AWS Bedrock), where every fact carries a source URL + locator note + retrieval date verified
against primary documentation. The facts surface in two reviewer-facing places — a register in
the evidence pack and a section on KB-website provider pages — and the scheduled drift check now
flags stale entries and providers without coverage. Strictly advisory: verdicts, summary counts,
and exit codes are unchanged (tested); facts never influence detection or policy evaluation.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/provider-data-practice-facts/` |
| Spec deltas | ADDED `provider-data-practices` (5 requirements); ADDED `cli-and-reporting` (`Evidence pack data-practices register`); ADDED `kb-freshness` (`Data-practices staleness coverage`); ADDED `kb-website` (`Provider page data-practices section`) |

## Changes

- `borderlint/data/data_practices.json` (new): per-provider entries with `training_default`
  (`yes`/`no`/`opt-out`/null), free-text `retention`, self-citing `subprocessors` link,
  `enterprise_tier` note, per-entry ISO-8601 `reviewed` date, and per-fact citations.
  Undocumented facts are recorded as `null` (explicitly unknown) — Anthropic's retention window
  and Bedrock's training default are deliberately null because primary sources did not confirm them.
- `borderlint/kb.py`: `load_data_practices()` with loud validation (training vocabulary,
  ISO-8601 review date, complete `{url, locator, retrieved}` citations); exposed as
  `kb.data_practices`.
- `borderlint/report.py`: evidence pack gains an advisory "Data practices" register — curated
  facts with cited sources and retrieval dates; uncurated providers stay visible as "not curated".
- `scripts/kb_site.py`: provider pages gain a data-practices section with hyperlinked citations
  or an explicit "not curated yet" statement; disclaimer on every rendering.
- `scripts/kb_drift.py`: stale-entry and curation-gap sections joined to the summary head;
  gap records carry ids only, never fact values; new `data_practices_exempt` suppression key
  validated loudly (unknown id or empty reason raises).
- `CONTRIBUTING.md`: entry schema table and curation rules (cite primary sources, unknown means
  null, human curation only, 90-day review cadence).
- `tests/test_borderlint.py`: schema/citation tests, advisory-guarantee tests (verdicts identical
  with/without the KB), evidence-register scenarios, site page variants, drift staleness/gap/
  suppression cases including shipped-state assertions.

## Verification

- [x] `openspec validate provider-data-practice-facts --strict` passes
- [x] All tasks in tasks.md checked (15/15)
- [x] Tests covering each acceptance scenario (full suite: 174 passed)
- [x] Verification pass found and fixed one defect (locator prose leaked into citation hrefs);
      test tightened to assert the href is exactly the URL
