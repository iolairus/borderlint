## ADDED Requirements

### Requirement: GitLab CI recipe

The project SHALL provide a ready-made GitLab CI recipe that installs the released borderlint
package from PyPI and runs the existing CLI against the repository root with a caller-selected
policy and classification. The recipe MUST preserve the scan's exit status and MUST NOT require
GitHub-specific services or credentials.

#### Scenario: Merge request is checked
- **GIVEN** a consuming repository uses the recipe with its policy and classification
- **WHEN** GitLab creates a merge-request pipeline
- **THEN** the job installs borderlint from PyPI and scans the repository root with those inputs

#### Scenario: Policy violation fails the job
- **GIVEN** the configured scan detects a policy violation
- **WHEN** borderlint exits non-zero
- **THEN** the GitLab job fails without an allow-failure setting or a swallowed command status

#### Scenario: Clean scan passes the job
- **GIVEN** the configured scan detects no failing flow
- **WHEN** borderlint exits zero
- **THEN** the GitLab job succeeds

### Requirement: GitLab pipeline trigger scope

The GitLab CI recipe SHALL run its borderlint job for merge-request pipelines and pushes to the
repository's default branch. It MUST NOT add a general topic-branch rule that duplicates
merge-request pipeline coverage.

#### Scenario: Default-branch push is checked
- **WHEN** a pipeline runs for a push to the default branch
- **THEN** the recipe includes the borderlint job

#### Scenario: Unrelated topic-branch push is skipped
- **GIVEN** a push is neither a merge-request event nor a push to the default branch
- **WHEN** GitLab evaluates the recipe rules
- **THEN** the borderlint job is not added for that branch push

### Requirement: GitLab recipe discovery

The project documentation SHALL identify the GitLab CI recipe and explain where consumers must
substitute their policy path and data classification. The E5 capability status MUST be updated
when the recipe and its validation are complete.

#### Scenario: Consumer finds a copyable example
- **WHEN** a GitLab user reads the CI documentation
- **THEN** they can locate the complete recipe and identify the policy and classification values
  to replace for their repository
