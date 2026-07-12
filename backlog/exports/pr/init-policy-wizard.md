## Summary

Adopting borderlint today requires hand-authoring a `residency.json` policy — a deny-by-default
allow-list keyed by data classification, plus optional sovereignty/provenance blocks. New users
have no scaffolding, no visibility into which jurisdictions their code actually reaches, and no
safeguard against clobbering an existing policy. This change adds a third `init` subcommand that
interviews the operator for a home base and the data classes they handle, runs a read-only
inventory scan, then walks the observed jurisdictions to propose per-classification allow-lists —
writing a ready-to-use `residency.json`. It refuses to overwrite an existing file without
`--force`, and supports non-interactive `--home`/`--classes` flags for scripted/CI use.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/init-policy-wizard/` |
| Spec deltas | ADDED `policy-init` (7 requirements); ADDED `cli-and-reporting` (`Init command` requirement) |

## Changes

- `borderlint/cli.py`: added the `init` subparser (`--home`, `--classes`, `-o/--output`, `--force`) and a dispatch branch calling `run_init`.
- `borderlint/init.py` (new): the wizard — injectable `input_fn` for testability, home-base and data-class interviews, inventory scan via `scan()`, per-jurisdiction keep/drop walk with home pre-seeded, overwrite guard, and non-interactive path.
  - Home validation checks **membership in the supported seats** (not merely a two-letter format), so `zz`/`us` are rejected and `uk`→`gb` still works, in both interactive and `--home` paths.
  - A single supplied flag (`--home` or `--classes`) is honoured; only the missing piece is prompted.
  - Emitted policy **omits `fail_on`** so it inherits the engine default (`residency`, `denied_provider`, `model_denied`) — avoids downgrading `deny_models` matches to warnings or silently opting users into the sovereignty dimension.
- `tests/test_borderlint.py`: interactive write, overwrite-refusal (exit 2, file untouched), overwrite-with-force, non-interactive no-prompt, unsupported-seat rejection (interactive + non-interactive), and single-`--home`-flag honoring.
- `README.md`: documented `borderlint init` (interactive + scripted flags).

## Verification

- [x] `openspec validate init-policy-wizard --strict` passes
- [x] All tasks in tasks.md checked
- [x] Tests covering each acceptance scenario (full suite: 132 passed)
- [x] Addressed all 4 review findings (spec delta corrected to ADDED; seat validation; `fail_on` omitted; single-flag honoring)
