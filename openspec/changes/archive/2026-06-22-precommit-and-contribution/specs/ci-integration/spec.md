## ADDED Requirements

### Requirement: Pre-commit hook

The project SHALL provide a pre-commit hook definition that runs `borderlint scan` and gates
the commit on the scan's exit code. The hook MUST wrap the existing CLI without introducing new
flags or per-file behaviour.

#### Scenario: Hook blocks a commit on a violation
- **WHEN** a repository configures the borderlint pre-commit hook and a developer commits
- **THEN** pre-commit runs `borderlint scan` and the commit is blocked because the scan exits non-zero

#### Scenario: Hook passes a clean commit
- **WHEN** the configured scan reports no failing flow
- **THEN** the scan exits zero and the commit proceeds

#### Scenario: Consumer supplies policy arguments
- **WHEN** the consumer's `.pre-commit-config.yaml` passes args such as `--policy` and `--classification`
- **THEN** the hook forwards them to `borderlint scan` unchanged

#### Scenario: Hook scans the path, not the staged file list
- **WHEN** the hook runs
- **THEN** it scans the configured path (the repository root by default), not pre-commit's per-file
  list, so directory-level detection and de-duplication behave as in a normal scan
