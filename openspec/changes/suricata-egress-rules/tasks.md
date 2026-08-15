## 1. Renderer

- [ ] 1.1 Add `suricata(findings, kb, policy, classification)` to `borderlint/report.py`: iterate KB endpoint hosts, select per host — jurisdiction outside `_allowed(classes[classification])`, region-scheme hosts always, every host without a policy — sort, assign sids from base 1900000
- [ ] 1.2 Rule template: `alert tls any any -> any any (msg:...; tls.sni; content:"<host>"; nocase; classtype:policy-violation; metadata:...; sid:N; rev:1;)` with provider name + jurisdiction + region-dependent marker in msg and provider id + jurisdiction in metadata
- [ ] 1.3 Generated-file header: source (KB date, policy digest or inventory mode), do-not-hand-edit note, alert→drop conversion note

## 2. CLI

- [ ] 2.1 Add `suricata` to the `--format` choices and renderer map
- [ ] 2.2 Add `suricata` to the non-gating export list (exit 0)

## 3. Tests

- [ ] 3.1 Unit tests: disallowed host present, allowed host absent, per-host split on a multi-jurisdiction provider (dashscope sg vs cn), uk→gb alias honoured, unknown-jurisdiction alerts, region-scheme always-alerts with marker, inventory mode covers all hosts, deterministic byte-identical output
- [ ] 3.2 End-to-end: `--format suricata` through `cli.main` exits 0 with violations present
- [ ] 3.3 Real-world validation: generated rulesets (policy + inventory modes) load clean via `suricata -T` in the official docker image; record the run in the PR

## 4. Docs

- [ ] 4.1 README: suricata format bullet (detection posture, alert vs drop, determinism caveat on sids across KB versions)
