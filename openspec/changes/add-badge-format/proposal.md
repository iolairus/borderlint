## Why

CI dashboards and PR descriptions benefit from a visual residency status badge. A shields.io endpoint format lets teams embed a live badge (`img.shields.io/endpoint?url=…`) that turns green/red based on the policy evaluation result, making compliance visibility immediate without parsing logs.

## What Changes

- Add `--format badge` to `borderlint scan` that emits a shields.io endpoint JSON payload.
- `report.badge(findings, kb, policy)` produces `{"schemaVersion":1,"label":"borderlint","message":"…","color":"…"}`.
- Policy mode: message shows violation count (e.g., `"2 flagged"`), color red on failures, green when clean.
- Inventory mode (no policy): message shows flow count (e.g., `"3 flows"`), color blue.
- Docs: README section + GitHub Actions example publishing the badge to Pages/gist.

## Capabilities

### New Capabilities
- `badge-output`: Shields.io endpoint JSON format for CI/CD badge consumption, including color coding by policy result and consumption patterns (Pages, gist, img.shields.io).

### Modified Capabilities
- `cli-and-reporting`: Add `badge` to the `--format` choices and renderers dictionary.

## Impact

- `borderlint/report.py`: New `badge()` function.
- `borderlint/cli.py`: Add `"badge"` to format choices and renderers dict.
- `README.md`: New section explaining badge usage and CI example.
- `tests/`: Badge unit tests following SARIF test pattern (json.loads + key asserts).
- No new dependencies; output is pure JSON built from existing findings.

## Non-goals

- Not a web server or HTTP endpoint — the badge JSON is stdout output that the user pipelines to a gist/Pages.
- Not a general-purpose status API; scoped to shields.io endpoint schema v1.
