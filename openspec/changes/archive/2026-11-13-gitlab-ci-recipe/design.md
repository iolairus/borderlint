# Design: gitlab-ci-recipe

## Context

E5's remaining gap is documentation and validation, not scanner functionality. The released
PyPI package already supplies the `borderlint` console command and returns non-zero for policy
violations. The repository has no GitLab pipeline example, while `examples/ci/` already holds
GitHub Actions and Jenkins examples.

## Decisions

- **D1 — Provide a standalone, copyable `gitlab-ci.yml` example.** Use a supported Python
  image, install `borderlint` from PyPI with `python -m pip`, and invoke
  `borderlint scan . --policy residency.json --classification customer-pii` directly as the job
  script. A published GitLab CI/CD component was rejected because it introduces component
  versioning and release machinery for one small job. A project-owned container image was
  rejected because borderlint has no runtime dependencies and needs no new image supply chain.
- **D2 — Use `rules` for merge requests and the default branch.** Include merge-request events
  and branch pipelines where `CI_COMMIT_BRANCH` equals `CI_DEFAULT_BRANCH`; do not add a general
  branch rule. This provides pre-merge and post-merge coverage without duplicate topic-branch
  pipelines. Legacy `only`/`except` syntax was rejected in favor of current GitLab `rules`.
- **D3 — Fail through the ordinary command exit status.** Keep the scan as the final, direct
  `script` command, with no `allow_failure: true`, `|| true`, or shell wrapper that could hide a
  violation. Policy mode is the default example because inventory mode does not gate violations.
- **D4 — Keep validation repository-local and dependency-free.** Add textual regression checks
  for the PyPI installation, exact scan invocation, trigger expressions, and absence of job
  bypasses, consistent with the existing pre-commit definition test. Do not add a YAML parser
  solely for this documentation example. A live GitLab Runner is not assumed to be available;
  this limitation must be reported rather than represented as an end-to-end GitLab test.

## Risks / Trade-offs

- [The recipe installs the latest release rather than a pinned version] → this matches the
  README's generic installation guidance and avoids stale version numbers; consumers can pin the
  package when reproducibility requires it.
- [The example assumes `residency.json` and `customer-pii`] → these are the established README
  conventions; comments tell consumers to adjust both for their repository.
- [Static checks cannot prove GitLab Runner behavior] → use standard GitLab syntax and state
  clearly that no hosted GitLab execution was performed.

## Migration Plan

Additive documentation and test changes only. Consumers opt in by copying the example; existing
pipelines and CLI behavior are unaffected. Revert by removing the example and documentation
references.
