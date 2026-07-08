## 1. Renderer

- [x] 1.1 `report.evidence(findings, kb, policy=None, envelope=None) -> str`: envelope block, seven-column inventory table (locations as per-flow sub-list), waiver register, arrangement references via the existing `_regimes`/`_arrangements`, summary counts; no-policy inventory framing (D1, "Evidence pack output format")

## 2. Regime annex

- [x] 2.1 `borderlint/data/evidence_regimes.json`: per-regime annex heading, citations, `static`/`org` field lists, keyed by the `regime_of` display string — "PDPO", "PIPL" (+ GBA SC reference hook), "Macao PDPA", "PDPA (SG)"; `updated` date, printed in the annex (D5, "Regime-aligned evidence annex")
- [x] 2.2 Annex rendering in `report.evidence`: static fields filled from findings, org fields as marked blanks, uncovered regimes state no annex available (D5)

## 3. CLI

- [x] 3.1 Envelope assembly in `cli.py`: tool version, three KB `updated` dates, UTC timestamp honouring `SOURCE_DATE_EPOCH`, `git rev-parse HEAD` on the scan root (stdlib subprocess, 2s timeout, `unavailable` on any failure), SHA-256 of the policy file, classification, home location (D2, D4, "Evidence audit envelope")
- [x] 3.2 Add `evidence` to the format choices; exit 0 like the SBOM (D3, "CI exit code")

## 4. Tests

- [x] 4.1 Inventory row carries axes + org + model; waiver register + summary; no-policy framing
- [x] 4.2 Envelope: commit + digest present in a repo, `unavailable` outside one; SOURCE_DATE_EPOCH determinism (two renders byte-identical); no network (scan-path guard test already sweeps imports)
- [x] 4.3 Exit code 0 with failing findings
- [x] 4.4 Annex per covered regime (hk, cn/CN-GBA, mo, sg): citations present, org fields blank-marked, static fields filled, data date printed; uncovered home location and `home_regime`-only policy → generic pack, no annex

## 5. Docs & validation

- [x] 5.1 README (Use section format list + a short evidence paragraph), CAPABILITIES P1-3 row
- [x] 5.2 Full suite + `openspec validate evidence-pack --strict`
