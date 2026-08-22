<!-- PR for /opsx change cn-data-practices-curation -->

## Summary

Three of the top-10 token-volume providers — DeepSeek (#1/#5/#9), Tencent Hunyuan (#2) and
Zhipu GLM (#6) — had data-practices entries whose every fact was `null` because primary sources
couldn't be reached during the earlier curation pass. Fresh research (2026-08-22) located their
governing documents, and this change curates the entries under the existing schema:

- **deepseek** — training default **opt-out**: the privacy policy states personal data is
  processed "to train and improve our technology, such as our machine learning models" with a
  policy-level opt-out right; the Open Platform ToS defers personal-data handling to it with
  no API-specific carve-out. PRC processing/storage; no fixed retention window; no documented
  ZDR tier. (cdn.deepseek.com policy URLs.)
- **tencent_hunyuan** — retention cites the TokenHub Privacy Policy Module verbatim:
  diagnostic/usage data explicitly **including "output information"** generally retained up to
  30 days, longer for billing. `training_default` stays null — no explicit statement about
  customer inference inputs exists; the note carries the scope caveat.
- **zhipu** — training default **no** for identifiable content ("no unauthorised use or
  disclosure beyond executing your service requests") with the anonymisation-training carve-out
  quoted in the locator; China-only storage; buffer-period deletion including backups;
  subprocessors recorded as a self-citing object pointing at the platform's third-party SDK
  table.

All stale "sources unreachable" notes are gone; every non-null fact carries url + locator +
retrieval date 2026-08-22. Strictly advisory — verdicts and exit codes unchanged.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/cn-data-practices-curation/` |
| Spec deltas | ADDED `provider-data-practices` (`Curated facts for the top CN token-volume providers`; `Cited entries without stale unavailability notes`) |

## Changes

- `borderlint/data/data_practices.json`: the three entries filled per above; unreachable-source
  notes removed (tencent_hunyuan keeps a scope-caveat note).
- `tests/test_borderlint.py`: `test_data_practices_cn_entries_curated` asserts expected training
  defaults (opt-out/null/no), complete citations, the zhipu carve-out disclosure, the zhipu
  subprocessors self-citing object, and absence of stale unreachable-notes; stale deepseek-null
  assertions removed from the uncurated-provider test.

## Verification

- [x] `openspec validate cn-data-practices-curation --strict` passes
- [x] All tasks in tasks.md checked (8/8)
- [x] Tests covering each acceptance scenario (full suite: 186 passed)
- [x] Review pass probed every scenario live: KB website pages render the new facts (training
  row present/absent exactly as curated); evidence pack shows the deepseek register block with
  the opt-out fact, full citation chain, and PRC retention text; loader validation passes on all
  citations; no stale unreachable-notes anywhere
