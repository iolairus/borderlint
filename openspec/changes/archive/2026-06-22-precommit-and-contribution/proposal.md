## Why

borderlint ships a GitHub Action and a CLI, but two adoptability gaps remain from the agreed
P2 cut. There is no **pre-commit hook** (E4), so a bad flow is only caught in CI, not before
the commit lands. And there is no **documented contribution path** (F4), so the bundled
provider KB — the project's crown jewel — can only grow through maintainer edits. Both lower
the barrier to adoption and to community KB growth.

## What Changes

- Add a pre-commit hook definition (`.pre-commit-hooks.yaml`) that runs `borderlint scan` on
  commit and gates on its exit code (E4). The hook wraps the existing CLI; repo-specific
  `--policy` / `--classification` args are supplied by the consumer's `.pre-commit-config.yaml`.
- Add `CONTRIBUTING.md` documenting the provider-KB JSON schema (fields, required vs. optional,
  valid jurisdiction tokens) and the add-a-provider-via-PR workflow (F4).
- No change to detection, classification, policy, or output behaviour; no new runtime deps.

## Capabilities

### New Capabilities
- `ci-integration`: ready-made hooks that run borderlint in a developer/CI workflow — here, the
  pre-commit hook.

### Modified Capabilities
- `kb-freshness`: add a documented community contribution workflow (KB schema + add-a-provider
  PR path) alongside the existing drift check.

## Impact

- New files: `.pre-commit-hooks.yaml`, `CONTRIBUTING.md`.
- Docs: README pre-commit usage snippet; `CAPABILITIES.md` E4/F4 → shipped.
- No code under `borderlint/` changes — pre-commit invokes the existing `borderlint` entry point.

## Non-goals

- No pre-commit hook logic beyond wrapping the existing CLI (no new flags, no per-file mode).
- Not auto-merging community KB PRs — jurisdictions stay human-assigned, consistent with
  `kb-freshness`.
- No CycloneDX/SPDX export, GitLab recipe, or LLM enrichment (separate later items).
