# Design: policy-loading-fixes

## Audit basis (verified by execution, 2026-11-11)

- `borderlint/policy.py:13-14` — `_SOVEREIGNTY_BLOCS` lacks `vn`;
  `borderlint/kb.py:144-145` has it. Empirical: `kb._SOVEREIGNTY_BLOCS -
  policy._SOVEREIGNTY_BLOCS == {'vn'}`; a policy with sovereignty allow-list `["vn"]`
  is rejected by `load_policy`. The provenance pair is in sync today.
- Error strings: `policy.py:71` and `kb.py:300` both print the pre-vn vocabulary.
- Spec drift: `openspec/specs/sovereignty/spec.md`'s `Sovereignty bloc vocabulary`
  requirement lists the pre-vn vocabulary — wave 9 updated code and data but not this
  requirement.
- `borderlint/cli.py:93` — `policy = load_policy(a.policy)` is unwrapped. Empirical:
  a missing policy path exits 1 with a `FileNotFoundError` traceback; an invalid bloc
  exits 1 with a `ValueError` traceback. The `load_kb` call ten lines earlier shows
  the house pattern: `except (ValueError, OSError) → print(error) → return 2`
  (JSONDecodeError is a ValueError, so one clause covers malformed JSON).

## Decisions

- **D1 — Sync the token, pin it with a test, keep the duplication.** `vn` joins
  `policy.py`'s frozenset and both error strings. The duplicated vocabularies stay
  (the circular-import reason is real), but a test asserting
  `policy._SOVEREIGNTY_BLOCS == kb._SOVEREIGNTY_BLOCS` and
  `policy._PROVENANCE_BLOCS == kb._PROVENANCE_BLOCS` fails the suite the next time
  one side moves without the other. Cheaper and more honest than a shared module
  that inverts the dependency.
- **D2 — The spec's vocabulary requirement catches up to wave 9.** The `vn` token
  was shipped in v1.15.12 without a spec update; this change amends the requirement
  text and adds a scenario locking the acceptance direction: policy allow-lists
  accept every vocabulary bloc, demonstrated with `vn`.
- **D3 — Reuse the existing error pattern for `load_policy`; no new exit codes.**
  Exit 2 with `error: …` on stderr is already the contract for bad input files
  (`load_kb`, `diff`). Wrapping `load_policy` in the identical
  `except (ValueError, OSError)` clause covers missing, unreadable, malformed, and
  invalid-token files with three lines. Scan-result exit codes are untouched.
- **D4 — The envelope's git call adopts `_git_tag`'s flags verbatim.** Add
  `-c core.fsmonitor=false -c core.hooksPath=/dev/null` and `GIT_OPTIONAL_LOCKS=0`
  to the `git rev-parse HEAD` subprocess call in `cli.py`'s `_envelope`, with a
  one-line comment cross-referencing `report.py`'s `_git_tag` (which documents the
  untrusted-repo rationale). No shared helper: the two call sites live in different
  modules, and a shared import is more coupling than two identical flag lists.
  rev-parse runs no hooks, so this is consistency hardening, not a live exploit fix.
- **D5 — One `_line_no(src, pos)` helper in `detect.py`.** Replace the six
  `src.count("\n", 0, m.start()) + 1` copies. Same algorithm, same result — the
  existing line-number assertions in the test suite are the regression net; no new
  behavior to spec.

## Risks / follow-ups

- None structural. The error-string and frozenset are the only two places the
  sovereignty vocabulary is spelled out by hand outside the spec; the regression
  test covers both modules, and the existing
  `test_bloc_vocabulary_sources_and_display` already covers sources/display names.
