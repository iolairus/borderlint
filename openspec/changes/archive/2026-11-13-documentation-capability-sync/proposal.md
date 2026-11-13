# Proposal: documentation-capability-sync

## Why

The capability map still marks G2 as `next` even though `--explain` is implemented and tested.
A broader documentation review is needed after the A6/A7 and E5 releases: user-facing feature
summaries, integration instructions, and CI examples may describe older versions or omit shipped
behavior, making the released tool harder to understand and adopt.

## What Changes

- Correct G2 to shipped and reconcile the capability map with current specifications.
- Review README and other current user-facing documentation against the specifications, CLI
  help, and v1.19.0 package metadata; correct stale feature descriptions, commands, versions,
  installation guidance, and scope statements.
- Review contributor documentation, Claude Code/Cursor integrations, plugin documentation, and
  CI examples, including stale private-repository or pre-PyPI installation guidance.
- Preserve historical OpenSpec archives and backlog records as historical artifacts.
- Add or adjust regression checks only where existing tests assert documented behavior.

## Capabilities

### New Capabilities

- `documentation-accuracy`: current user-facing documentation and examples accurately describe
  shipped capabilities, installation paths, and integration behavior.

### Modified Capabilities

- `model-provenance`: correct the vocabulary description to state that provenance excludes both
  `vn` and `local`; this documents existing validation behavior without changing it.
- No runtime behavior changes.

## Impact

- Current documentation and examples, including `README.md`, `CAPABILITIES.md`,
  `CONTRIBUTING.md`, `integrations/`, and `examples/ci/` where review finds drift.
- Possible documentation-focused test updates.
- No scanner, policy, KB, report-schema, or CLI behavior changes.

## Non-goals

- No edits to archived OpenSpec proposals, backlog history, or release history.
- No new product capabilities or changes to deferred/next items beyond correcting their status.
- No regulatory or KB research and no provider-data curation.
- No edits inside managed agent-instruction blocks.
- No release version bump beyond documenting the already-released v1.19.0.
