# Tasks: gitlab-ci-recipe

## 1. GitLab recipe

- [x] 1.1 Add `examples/ci/gitlab-ci.yml` with a supported Python image, PyPI installation, and
      the direct policy-gated `borderlint scan .` command (design D1, D3; spec: GitLab CI recipe)
- [x] 1.2 Configure merge-request and default-branch `rules` without a general topic-branch rule;
      do not add `allow_failure` or an exit-code bypass (design D2, D3; specs: GitLab CI recipe,
      GitLab pipeline trigger scope)

## 2. Documentation and status

- [x] 2.1 Add a README GitLab CI snippet or link that identifies `residency.json` and
      `customer-pii` as consumer-selected values (spec: GitLab recipe discovery)
- [x] 2.2 Change E5 to shipped in `CAPABILITIES.md`, retaining the note that GitHub Actions,
      Jenkins, and GitLab recipes are available (spec: GitLab recipe discovery)

## 3. Validation

- [x] 3.1 Add a dependency-free regression test for the recipe's installation, scan command,
      trigger rules, and lack of failure bypasses (design D4)
- [x] 3.2 Run the full pytest suite and the recipe's scan command locally against a known clean
      and violating fixture to verify exit-code behavior (design D3, D4)
- [x] 3.3 Run `openspec validate gitlab-ci-recipe --strict`; record that hosted GitLab Runner
      execution was not performed if no GitLab test project is available (design D4)
