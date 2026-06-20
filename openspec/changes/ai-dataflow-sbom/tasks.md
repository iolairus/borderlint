## 1. SBOM export

- [x] 1.1 Add `sbom` to the `--format` choices and a `report.sbom(findings, kb, policy)` renderer
- [x] 1.2 Emit the envelope (schema id `borderlint.ai-dataflow-sbom/1`, borderlint version, KB `updated` date) + components — one per provider with id, name, sorted jurisdiction(s), and call sites (`file`, `line`, `kind`, `evidence`, `jurisdiction`); totally ordered (providers by id; sites by file, line, kind, evidence; jurisdictions sorted); serialize with `json.dumps(sort_keys=True)`, no timestamp, and no severity/level/verdict field
- [x] 1.3 `--format sbom` does not gate CI — exit 0 even when a supplied policy would fail (carve-out in the CI exit-code path)

## 2. Tests

- [x] 2.1 Tests: the envelope carries schema id + version + KB date; components list every flow with sorted jurisdiction(s) + sites; no `severity`/`level`/verdict field appears anywhere; a failing policy still emits all flows and exits 0; `--format sbom` without a policy exits 0; the same scan twice is byte-identical
