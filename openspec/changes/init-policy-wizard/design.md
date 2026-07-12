## Context

borderlint is a stdlib-only Python CLI. Today a user must hand-write `residency.json` before
`borderlint scan -p residency.json` will gate anything. The policy shape is non-trivial: a
`classifications` map (data class → jurisdiction allow-list), a `home_location`, plus `on_unknown`
and `fail_on` blocks. New adopters have no starting point and no visibility into which jurisdictions
their code actually reaches. `cli.py` already defines `scan` and `diff` subparsers (lines 47–57) and
dispatches them in an `if`-ladder (lines 64–66). The detection engine (`scan()`) and evaluation core
(`load_policy()`/`evaluate()`) are stable and reusable as-is.

## Goals / Non-Goals

**Goals:**
- Add a third `init` subcommand that produces a usable `residency.json` with minimal friction.
- Interview for home base and handled data classes, then ground the proposal in a real inventory scan.
- Support non-interactive/scripted use via `--home` and `--classes`.
- Never silently clobber an existing policy file.

**Non-Goals:**
- No sovereignty/provenance block authoring beyond emitting safe defaults.
- No gating evaluation, SARIF, or SBOM output from `init`.
- No merge/migration of an existing policy; overwrite is refused unless `--force`.

## Decisions

**D1 — Thin CLI, logic in `borderlint/init.py`.**
`cli.py` gains only the `init` subparser and a `_run_init(a)` dispatcher that delegates to a new
`borderlint/init.py`. Keeps `cli.py` readable and the wizard unit-testable without argparse.
*Alternative considered:* inline everything in `cli.py`. Rejected — `cli.py` is already the dispatch
hub; piling interview logic there hurts testability and review.

**D2 — Reuse `scan()` in inventory mode for the observed jurisdictions.**
`init` calls `scan(path, kb)` (no policy) exactly as `scan` does, then collects the resolved
jurisdictions from the detections. This guarantees the wizard proposes only jurisdictions the code
actually reaches, and avoids duplicating detection logic.
*Alternative considered:* a separate lighter "jurisdiction lister". Rejected — it would drift from
the real scan and could miss wrapper/endpoint detections.

**D3 — Interview order: home → classes → per-jurisdiction walk.**
1. Home base: prompt with the supported seat list (`hk`, `mo`, `CN-GBA`, `jp`, `kr`, `sg`, `au`, `uk`,
   `eu`, `my`); default to `hk` on empty input. Validated against the same `_valid_home` vocabulary
   used by `policy.py`.
2. Data classes: prompt which of `non-pii`, `employee-pii`, `customer-pii` (plus any user-typed extra)
   the operator handles; default = all three.
3. Inventory walk: for each observed jurisdiction, for each handled class, prompt "keep `<jur>` for
   `<class>`? [y/N]". Affirmative adds the jurisdiction to that class's allow-list. The home base is
   pre-seeded into every class's allow-list (a home seat is always acceptable to itself).
*Alternative considered:* ask per-class allow-lists up front without an inventory. Rejected — users
don't know their egress surface; grounding in the scan is the whole point.

**D4 — Output shape matches `load_policy()` expectations.**
The written file uses the shorthand `{classification: [jurisdictions]}` map plus `home_location` and
`on_unknown: "warn"`. `fail_on` is deliberately **omitted** so the policy inherits the engine default
(`["residency","denied_provider","model_denied"]`); emitting it would either downgrade a later-added
`deny_models` match to a warning or silently opt every new user into the sovereignty dimension before
they have written a sovereignty block. The file still loads via `load_policy()` without special-casing.

**D5 — Overwrite guard via `--force`.**
Before writing, `init` checks `os.path.exists(out_path)`. If it exists and `--force` was not passed,
it prints an error to stderr and exits 2 (same code `scan`/`diff` use for bad input). `--force`
overwrites. Default output path is `./residency.json`; overridable with `-o/--output`.

**D6 — Non-interactive path.**
When both `--home` and `--classes` are supplied, skip all `input()` prompts: seed home into every
class, add every observed jurisdiction to every class's allow-list (scripted users get a permissive
starting point they can tighten), and write. If only one flag is given, that flag is honoured and
only the missing piece is prompted for (e.g. `borderlint init --home hk` uses `hk` and still asks
which classes to handle). A supplied `--home` is validated against the supported seats; an invalid
seat exits 2 rather than being silently written.

## Risks / Trade-offs

- [Risk] Inventory scan may find no AI flows (empty repo) → wizard has nothing to walk.
  → Mitigation: if no jurisdictions observed, seed only the home base into each class and inform the
  user the allow-list is minimal; they can re-run after adding integrations.
- [Risk] `input()` is hard to test. → Mitigation: inject the input source (default `builtins.input`)
  so tests monkeypatch it; file writes are asserted on disk/stringio.
- [Risk] Pre-seeding home into every class could over-permit. → Mitigation: home is the operator's
  own seat and is always acceptable to itself; this matches the deny-by-default model's intent.
- [Risk] Windows/non-TTY `input()` behaviour. → Mitigation: stdlib `input()` is cross-platform; no
  readline dependency introduced.

## Migration Plan

No migration: additive command only. Rollback = remove `init` subparser and `borderlint/init.py`.
Existing `scan`/`diff` behaviour is untouched.

## Open Questions

- Should `init` also emit a starter `sovereignty`/`provenance` block, or leave them for the user to
  add? (Current decision: emit only `classifications` + defaults; documented in Non-goals.)
- Should the default output path be configurable via `workflow.yaml`? (Out of scope for v1; `-o` flag
  covers it.)
