## Why

A security pass flagged two hardening gaps for a tool that scans untrusted code in CI. (1) borderlint
runs `git` inside the scanned directory to label the Mermaid root node; git honours the repo-local
`.git/config`, a known command-execution surface when the scanned repo is attacker-controlled.
(2) Every matched file is read fully into memory with no size cap — a multi-GB file (relevant to the
planned supply-chain / container scan) can exhaust memory.

## What Changes

- **Harden the git call:** invoke `git describe` with `-c core.fsmonitor=false -c core.hooksPath=/dev/null`
  and `GIT_OPTIONAL_LOCKS=0`, neutralising repo-local config vectors. No output change — purely safer.
- **Cap file reads:** skip any file larger than a fixed threshold (5 MB) before reading it, so an
  oversized file is excluded rather than read into memory.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `flow-detection`: exclude oversized files from scanning (a new resilience/exclusion behaviour).

## Impact

- Code: `report._git_tag` (hardened invocation); `detect.scan` (size guard). No output/format change.
- The git hardening is internal — no requirement changes, hence no `cli-and-reporting` delta.
- Tests: oversized file is skipped; git label still resolves.

## Non-goals

- Not removing the git call (the version label is useful); only hardening it.
- No configurable size threshold — a fixed 5 MB constant suffices (no source file is that large).
- Not sandboxing arbitrary git config beyond the known-dangerous keys.
