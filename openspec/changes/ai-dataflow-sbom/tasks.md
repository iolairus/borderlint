## 1. SBOM export

- [ ] 1.1 Add `sbom` to the `--format` choices and a `report.sbom(findings, kb, policy)` renderer
- [ ] 1.2 Emit a deterministic, severity-free JSON document: envelope (schema id `borderlint.ai-dataflow-sbom/1`, borderlint version, KB `updated` date) + components — one per provider with name, sorted jurisdiction(s), and call sites (`file`, `line`, `kind`, `evidence`, `jurisdiction`) sorted by file then line
- [ ] 1.3 `--format sbom` does not gate CI — exit 0 even when a supplied policy would fail

## 2. Tests

- [ ] 2.1 Tests: the SBOM lists every detected flow with its jurisdiction(s) and sites; a failing policy still emits all flows with no severity and exits 0; the same scan produces byte-identical output (deterministic, no timestamp)
