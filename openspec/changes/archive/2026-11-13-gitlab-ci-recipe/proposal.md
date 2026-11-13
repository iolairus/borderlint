# Proposal: gitlab-ci-recipe

## Why

E5 remains incomplete because borderlint has GitHub Actions and Jenkins examples but no
ready-made GitLab CI recipe. GitLab users must translate the generic CLI instructions and
choose trigger rules themselves, which makes adoption slower and can accidentally create
duplicate branch and merge-request pipelines.

## What Changes

- Add `examples/ci/gitlab-ci.yml`, a copyable pipeline job that installs the released
  borderlint package from PyPI and runs the existing policy-gated scan against the repository
  root.
- Run the job for merge-request pipelines and pushes to the default branch, while excluding
  unrelated branch pipelines that would duplicate merge-request coverage.
- Preserve the CLI's exit status so violations fail the job without `allow_failure` or a
  swallowed exit code.
- Document the recipe in README and mark E5 shipped in `CAPABILITIES.md` once validated.
- Add a regression test for the recipe's installation, scan command, trigger rules, and
  fail-closed job behavior.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `ci-integration`: add a GitLab CI recipe alongside the existing pre-commit integration.

## Impact

- New documentation example: `examples/ci/gitlab-ci.yml`.
- Documentation updates: `README.md`, `CAPABILITIES.md`.
- Test update: `tests/test_borderlint.py`.
- No changes to the Python package, CLI arguments, scan behavior, or runtime dependencies.

## Non-goals

- No published GitLab CI/CD component or remote `include:` template.
- No GitLab-specific SARIF, artifact, badge, or report integration.
- No container image publication or GitLab Runner deployment.
- No changes to the existing GitHub Actions or Jenkins recipes.
- No new policy, classification, detection, or reporting behavior.
