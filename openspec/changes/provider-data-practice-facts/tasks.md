# Tasks: provider-data-practice-facts

## 1. Knowledge base data and loader

- [ ] 1.1 Create `borderlint/data/data_practices.json` with the entry schema from design D1–D3: per-provider `training_default` (`yes`|`no`|`opt-out`), `retention`, `subprocessors` link, `enterprise_tier` note, per-fact citation objects `{url, locator, retrieved}`, top-level ISO-8601 last-reviewed date (D1, D2, D3)
- [ ] 1.2 Add `load_data_practices()` to `borderlint/kb.py` following the existing stdlib-JSON loader pattern; fail loud on missing file (D4)
- [ ] 1.3 Add tests: schema shape, every key exists in `providers.json`, last-reviewed date parses as ISO-8601, citations carry url/locator/retrieved

## 2. Advisory guarantees

- [ ] 2.1 Add test proving verdicts, summary counts, and exit codes are identical with and without the data-practices KB present for the same tree and policy
- [ ] 2.2 Add test that an uncurated detected provider does not fail a scan and is surfaced as not curated

## 3. Evidence pack register

- [ ] 3.1 Extend the evidence renderer in `borderlint/report.py` with a data-practices register: curated providers with facts + citations + retrieval dates, uncurated providers marked not curated, advisory disclaimer on the register
- [ ] 3.2 Add tests covering the three register scenarios (curated listed with citations, uncurated visible, verdicts untouched)

## 4. KB website section

- [ ] 4.1 Extend `scripts/kb_site.py` provider pages with the data-practices section: facts, hyperlinked citations with retrieval dates, disclaimer; "not curated" statement for providers without entries
- [ ] 4.2 Add generator tests for both page variants (curated / uncurated)

## 5. Freshness coverage

- [ ] 5.1 Extend `scripts/kb_drift.py` with stale-entry and missing-provider sections reusing the suppression list and open-item upsert; gap records carry no fact values (D5)
- [ ] 5.2 Add drift tests: stale entry reported, unsuppressed gap reported with no fact values, suppressed provider excluded

## 6. Seed curation and docs

- [ ] 6.1 Curate seed entries for flagship providers (OpenAI, Anthropic, Google, Azure OpenAI, AWS Bedrock), each fact sourced with URL + locator + retrieval date read from current public documentation (D6)
- [ ] 6.2 Document the new KB in CONTRIBUTING.md (schema, human-curation rule, review cadence)

## 7. Validation

- [ ] 7.1 Run full pytest suite and fix regressions
- [ ] 7.2 Run `openspec validate provider-data-practice-facts --strict`
