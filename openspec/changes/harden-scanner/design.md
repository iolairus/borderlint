## Context

Both fixes are local hardening of the existing scanner; neither changes output for normal inputs.

## Goals / Non-Goals

**Goals:** neutralise repo-local git config vectors; bound memory on a single file read.
**Non-Goals:** removing the git label; configurable thresholds; full git sandboxing.

## Decisions

- **Git: command-line `-c` overrides beat repo config.** `git -c core.fsmonitor=false -c
  core.hooksPath=/dev/null describe …` plus `GIT_OPTIONAL_LOCKS=0` in the env. Command-line `-c`
  takes precedence over the scanned repo's `.git/config`, so a malicious `core.fsmonitor` cannot
  fire. Alternative — drop the git call entirely — rejected: the version label is a useful nicety and
  already falls back to the manifest. Alternative — `safe.directory` / ownership checks — rejected:
  doesn't cover the same-user CI-checkout case.
- **Size cap before read, via `stat().st_size`.** Check size in `scan()` before `read_text`; skip
  over 5 MB. `stat` avoids reading the file to learn its size. 5 MB is far above any real source file
  and well below an OOM risk. Alternative — stream line-by-line — rejected: more code; the AST scan
  needs the whole file anyway, and a 5 MB+ source file is not a real detection target.

## Risks / Trade-offs

- [A legitimate >5 MB generated source is skipped] → acceptable; such files are not hand-written AI
  call sites, and the cap prevents a memory-exhaustion DoS. The threshold is a named constant.
- [Hardened `-c` flags differ across very old git] → `-c key=val` and these keys are long-supported;
  the call already degrades to `None` on any git error, so an unknown flag never fails the scan.

## Migration Plan

Additive hardening. No data migration, no output change for in-spec inputs.
