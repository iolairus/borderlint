## 1. Implement badge renderer

- [x] 1.1 Add `badge(findings, kb, policy)` function in `borderlint/report.py` that returns a shields.io endpoint JSON string with `schemaVersion`, `label`, `message`, and `color` fields
- [x] 1.2 Implement color logic: green for clean (policy mode, no failures), red for violations (policy mode), blue for inventory mode (no policy)
- [x] 1.3 Implement message logic: `"clean"` for clean, `"{N} flagged"` for N violations, `"{N} flows"` for N flows in inventory mode

## 2. Wire badge format into CLI

- [x] 2.1 Add `"badge"` to `--format` choices in `borderlint/cli.py` scan subparser
- [x] 2.2 Add `"badge"` to the renderers dict in `cli.py` pointing to `report.badge`
- [x] 2.3 Add `"badge"` to the non-gating format check (alongside `"sbom"` and `"evidence"`) so it exits 0 regardless of violations

## 3. Tests

- [x] 3.1 Add unit test for badge output in policy mode (clean): verify JSON keys, message `"clean"`, color `"green"`
- [x] 3.2 Add unit test for badge output in policy mode (violations): verify message `"{N} flagged"`, color `"red"`
- [x] 3.3 Add unit test for badge output in inventory mode: verify message `"{N} flows"`, color `"blue"`
- [x] 3.4 Add unit test for badge exit code: verify exit 0 on violations (non-gating)

## 4. Documentation

- [x] 4.1 Add README section explaining `--format badge` usage and shields.io endpoint schema
- [x] 4.2 Add GitHub Actions example step showing how to publish badge to Pages/gist for `img.shields.io/endpoint?url=…`
