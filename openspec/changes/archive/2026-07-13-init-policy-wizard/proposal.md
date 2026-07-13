## Why

Adopting borderlint today requires hand-authoring a `residency.json` policy — a deny-by-default
allow-list keyed by data classification, plus optional sovereignty/provenance blocks. New users
have no scaffolding, no guidance on which jurisdictions their code actually touches, and no
safeguard against clobbering an existing policy. A guided `borderlint init` wizard lowers the
activation barrier: it interviews the operator for their home base and data classes, runs a
read-only inventory scan, then walks the observed jurisdictions to propose classifications —
writing a ready-to-use `residency.json`.

## What Changes

- Add a third `init` subparser beside `scan` and `diff` in `cli.py`, dispatched in the existing command ladder.
- Interactive interview via stdlib `input()`: home base (one of the supported seats: `hk`, `mo`, `CN-GBA`, `jp`, `kr`, `sg`, `au`, `uk`, `eu`, `my`), and which data classes the operator handles.
- Run a read-only inventory scan over the target path and walk each observed jurisdiction, prompting per-class keep/drop (e.g. "keep `sg` for `customer-pii`? y/n") to propose the allow-lists.
- Emit a `residency.json` (with `home_location`, `classifications`, and default `on_unknown`/`fail_on` blocks). Refuse to overwrite an existing file unless `--force` is passed.
- Non-interactive flags (`--home`, `--classes`) for scripted/CI use; when both are supplied the wizard skips prompts and writes directly.

## Capabilities

### New Capabilities
- `policy-init`: Interactive and non-interactive `borderlint init` wizard that interviews for home base and data classes, runs an inventory scan, proposes jurisdiction allow-lists per classification, and writes `residency.json` (refusing to overwrite without `--force`).

### Modified Capabilities
- `cli-and-reporting`: Add a requirement that the CLI provides an `init` command (third subcommand alongside `scan`/`diff`) with `--home`, `--classes`, and `--force` options.

## Impact

- `borderlint/cli.py`: new `init` subparser (around the `scan`/`diff` definitions at lines 47–57) and a dispatch branch in the `if`-ladder at lines 64–66; a new `_run_init(a)` handler.
- New module (e.g. `borderlint/init.py`) for the interview/inventory/proposal logic, keeping `cli.py` thin.
- `tests/test_borderlint.py`: monkeypatched `stdin` + written-file assertions, plus an overwrite-refusal case.
- No changes to the detection engine, knowledge base, or evaluation core; `init` reuses `scan()` in inventory mode and `load_policy()`/`evaluate()` shapes.
- Zero new runtime dependencies (stdlib `input()` only).

## Non-goals

- The wizard does not adjudicate cross-border arrangements or sovereignty/provenance blocks beyond emitting sensible defaults; it focuses on the `classifications` allow-lists.
- It does not run a gating evaluation or produce SARIF/SBOM — it only proposes and writes a policy file.
- It does not migrate or merge an existing policy; overwrite is refused unless `--force`.
