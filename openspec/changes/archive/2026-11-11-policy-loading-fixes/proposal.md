# Proposal: policy-loading-fixes

## Why

Two repo audits (2026-11-11, ponytail-audit run twice) found two live defects in
policy loading, both verified by running the CLI, plus two small hygiene items:

1. **The sovereignty vocabulary is split-brain.** `kb.py`'s `_SOVEREIGNTY_BLOCS`
   gained `vn` in wave 9 (clf_ai_gateway resolves to it), but the deliberate duplicate
   in `policy.py` did not — so a policy whose sovereignty allow-list contains `vn` is
   rejected with `invalid sovereignty bloc 'vn'`, even though the scanner itself can
   now emit that bloc. The spec has the same drift: the `Sovereignty bloc vocabulary`
   requirement still lists the pre-vn vocabulary, so spec, policy module, and KB
   disagree three ways. The error strings in `policy.py` and `kb.py` also predate
   `vn`, so even the guidance text is wrong.
2. **Bad policy files crash the CLI with a traceback.** `cli.py` wraps `load_kb` and
   `evaluate` in clean `error: …` + exit 2 handling, but `load_policy` between them is
   unwrapped: a missing file, malformed JSON, or an invalid bloc escapes as an
   unhandled exception (exit 1 with a stack trace), breaking the tool's own
   error-reporting contract in CI.
3. **The evidence envelope's `git` call is unhardened.** `report.py`'s `_git_tag`
   deliberately neutralizes a scanned repo's git config (`core.fsmonitor=false`,
   `core.hooksPath=/dev/null`, `GIT_OPTIONAL_LOCKS=0`) as an execution-vector guard;
   `cli.py`'s `_envelope` calls plain `git rev-parse HEAD` on the same untrusted repo.
   rev-parse runs no hooks, so the real risk is minimal — but the two call sites
   disagree about the same threat, and the careful one explains why.
4. **The line-counting idiom is duplicated six times** in `detect.py`
   (`src.count("\n", 0, m.start()) + 1` at lines 113, 126, 142, 177, 283, 335) — six
   copies to read and keep in sync.

## What Changes

- Sync the vocabulary: add `vn` to `policy.py`'s `_SOVEREIGNTY_BLOCS` and to the
  user-facing vocabulary strings in `policy.py` (`load_policy` sovereignty error) and
  `kb.py` (`load_kb` user-override sovereignty error). Update the sovereignty spec's
  vocabulary requirement to include `vn` (it should have changed in wave 9).
- Add a regression guard that fails the test suite if the two module-level bloc
  vocabularies ever differ again (sovereignty and provenance both — the provenance
  pair happens to be in sync today and should be pinned too).
- Wrap the `load_policy` call in `cli.py` in the same
  `except (ValueError, OSError)` → `error: …` + exit 2 pattern already used for
  `load_kb`, covering missing files, unreadable files, malformed JSON, and invalid
  tokens. Spec the clean-error contract for invalid input files.
- Harden `_envelope`'s `git rev-parse HEAD` with the same neutralizing flags
  `_git_tag` uses (`-c core.fsmonitor=false -c core.hooksPath=/dev/null` and
  `GIT_OPTIONAL_LOCKS=0`), so both git invocations on a scanned repo share one
  posture.
- Replace the six line-counting copies with one `_line_no(src, pos)` helper in
  `detect.py`. Pure refactor: no behavior change, covered by the existing
  line-number assertions in the test suite.

## Release

Ships as **minor release 1.16.0**: the policy layer gains new accepted input (the
`vn` bloc) and a new clean-error contract for invalid input files, on top of two
hygiene cleanups — more than a patch, nothing breaking.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `sovereignty`: the bloc vocabulary requirement gains `vn`, and policy allow-lists
  accept the full vocabulary the scanner can emit.
- `cli-and-reporting`: invalid policy input fails with a clean error and exit 2
  instead of a traceback, and both git invocations on a scanned repo run with
  neutralized repo config.

## Impact

- `borderlint/policy.py` (+1 token, error-string fix), `borderlint/kb.py`
  (error-string fix), `borderlint/cli.py` (+3 lines of error handling, +4 hardened
  git flags), `borderlint/detect.py` (+1 helper, −6 duplicated expressions), tests
  (+4). Net roughly −10 lines in `detect.py`.
- No data-file changes; no detection or evaluation behavior changes beyond accepting
  the already-shipped `vn` bloc.

## Non-goals

- No restructuring to eliminate the deliberate vocabulary duplication (the comment in
  `policy.py` documents why it exists: avoiding a circular import). The regression
  test makes the duplication safe instead of removing it.
- No change to exit-code semantics for scan results (violations still exit 1, exports
  still exit 0); this change only covers input-file errors, which already used exit 2
  on the `load_kb` path.
- No shared git-helper module for the two call sites: `_envelope` lives in `cli.py`
  and `_git_tag` in `report.py`, and importing one into the other is more coupling
  than two identical flag lists are worth. A comment cross-references them.
- No performance work on the line-counting helper: it stays the same O(file) scan per
  match; the goal is one idiom, not a faster one.
