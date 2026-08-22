# Tasks: cn-data-practices-curation

## 1. Entry curation

- [x] 1.1 Fill the `deepseek` entry in `borderlint/data/data_practices.json`: training_default `opt-out`, PRC residency + purpose-bound retention (no fixed window), enterprise_tier note on absent ZDR; citations to cdn.deepseek.com privacy policy and Open Platform ToS; remove the unreachable-source note (D1)
- [x] 1.2 Fill the `tencent_hunyuan` entry: retention quoting the TokenHub Privacy Policy Module 30-day diagnostic/usage scope verbatim (incl. output information, longer for billing); training_default stays null; subprocessors stay null; replace the note with a scope caveat (D2)
- [x] 1.3 Fill the `zhipu` entry: training_default `no` citing UA §三.9(1) with the anonymisation carve-out from Privacy Policy §二.7(4)/§四.10 quoted in the locator; China-only storage; buffer-period deletion; subprocessors object citing the third-party SDK table (D3, D4)

## 2. Tests

- [x] 2.1 Extend data-practices tests: the three entries load with expected training defaults (opt-out/null/no), every non-null fact cited, no "unreachable" notes remain
- [x] 2.2 Verify zhipu subprocessors is a self-citing object with url/locator/retrieved and renders as a link on the KB website page

## 3. Validation

- [x] 3.1 Run full pytest suite and fix regressions
- [x] 3.2 Run `openspec validate cn-data-practices-curation --strict`
