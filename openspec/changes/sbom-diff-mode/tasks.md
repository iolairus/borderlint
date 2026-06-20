## 1. Diff command

- [ ] 1.1 Add a `diff <baseline> <current>` subcommand that loads two SBOM JSON files and rejects (exit 2) any input that is not a `borderlint.ai-dataflow-sbom/1` document (parse error or wrong/missing schema)
- [ ] 1.2 Compute added/removed flows at (provider, jurisdiction) granularity from the SBOM components in a pure `report.diff_flows(old, new)` helper — KB- and policy-independent (names taken from the SBOMs)
- [ ] 1.3 Render text + JSON (`--format text|json`); exit non-zero iff a non-`local` flow was added, else 0

## 2. Tests

- [ ] 2.1 Tests: an added non-`local` flow → reported added + exit non-zero; a removed flow with no additions → exit 0; an added `local`-only flow → exit 0; a non-SBOM input → exit 2; baseline/current order matters (added vs removed are not symmetric)
