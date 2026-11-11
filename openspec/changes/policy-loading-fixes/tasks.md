# Tasks: policy-loading-fixes

## 1. Vocabulary sync

- [x] 1.1 Add `vn` to `_SOVEREIGNTY_BLOCS` in `borderlint/policy.py` (design D1)
- [x] 1.2 Add `vn` to the sovereignty vocabulary error strings in
  `borderlint/policy.py` (load_policy) and `borderlint/kb.py` (load_kb user-override
  message) (design D1)

## 2. Clean error handling

- [x] 2.1 Wrap the `load_policy(a.policy)` call in `borderlint/cli.py` in
  `except (ValueError, OSError)` → `error: …` on stderr + return 2, matching the
  `load_kb` pattern above it (design D3)
- [x] 2.2 Harden `_envelope`'s `git rev-parse HEAD` with `-c core.fsmonitor=false`,
  `-c core.hooksPath=/dev/null`, and `GIT_OPTIONAL_LOCKS=0`, plus a comment
  cross-referencing `report.py`'s `_git_tag` (design D4)
- [x] 2.3 Add a `_line_no(src, pos)` helper in `borderlint/detect.py` and replace the
  six duplicated line-counting expressions (design D5)

- [x] 2.4 Validate the policy's top-level JSON shape in `load_policy` (a non-object
  root such as `null` or `[]` now raises a clean ValueError instead of a
  TypeError/AttributeError — spec-review finding)

## 3. Tests

- [x] 3.1 Vocabulary-parity regression test: `policy._SOVEREIGNTY_BLOCS ==
  kb._SOVEREIGNTY_BLOCS` and `policy._PROVENANCE_BLOCS == kb._PROVENANCE_BLOCS`
  (design D1)
- [x] 3.2 Acceptance test: a policy whose sovereignty allow-list contains `vn` loads
  and a `vn`-sovereignty flow passes the sovereignty check
- [x] 3.3 CLI tests: missing policy file, malformed JSON policy, and invalid-token
  policy each exit 2 with an `error:` line and no `Traceback` in stderr
- [x] 3.4 Envelope test: the `git` invocation in `_envelope` carries the hardened
  flags (assert via a monkeypatched `subprocess.run`)
- [x] 3.5 Existing line-number assertions in the suite serve as the `_line_no`
  refactor's regression net — no new behavior tests needed

## 4. Verify

- [x] 4.1 Run the full test suite
- [x] 4.2 Re-run the two audited failure cases by hand (missing file, vn policy) and
  confirm clean exit 2 / clean load
- [x] 4.3 `openspec validate policy-loading-fixes --strict`

## 5. Release

- [ ] 5.1 After merge, cut **minor release 1.16.0** (new accepted policy input + new
  clean-error contract, plus hygiene) via the standard release flow
