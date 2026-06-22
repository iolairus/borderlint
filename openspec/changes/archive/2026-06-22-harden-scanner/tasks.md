## 1. Git hardening (#1)

- [x] 1.1 In `report._git_tag`, run git with `-c core.fsmonitor=false -c core.hooksPath=/dev/null`
      and `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`; behaviour/output unchanged.

## 2. File-size cap (#2)

- [x] 2.1 In `detect.scan`, define `MAX_FILE_BYTES = 5 * 1024 * 1024` and skip any file whose
      `stat().st_size` exceeds it, before `read_text`.

## 3. Tests & validation

- [x] 3.1 An oversized file (> cap) is skipped; a normal file is still scanned.
- [x] 3.2 `_git_tag` still resolves a tag on a normal repo (existing test stays green).
- [x] 3.3 `openspec validate harden-scanner --strict` passes; full pytest green.
