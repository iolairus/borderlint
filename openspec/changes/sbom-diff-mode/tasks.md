## 1. Diff command

- [x] 1.1 Add a `diff <baseline> <current>` subcommand that loads two SBOM JSON files and exits 2 on any input that is not a `borderlint.ai-dataflow-sbom/1` document (parse error or wrong/missing schema)
- [x] 1.2 Compute added/removed flows in a pure `report.diff_flows(old, new)` helper — a flow is `(component id, j)` for each `j` in the component's `jurisdictions`; provider id is identity (name is display only); KB- and policy-independent
- [x] 1.3 Render added/removed flows in text + JSON (`--format text|json`); exit 1 iff a non-`local` flow (including `unknown`) was added, else 0

## 2. Tests

- [x] 2.1 Tests: an added non-`local` flow → reported added + exit 1; an added `unknown`-only flow → exit 1; an added `local`-only flow → exit 0; a removed flow with no additions → exit 0; swapping the inputs inverts added/removed; a non-SBOM input → exit 2
