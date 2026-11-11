# cli-and-reporting Delta

## ADDED Requirements

### Requirement: Invalid input files fail with a clean error
The CLI SHALL reject an input file that is missing, unreadable, malformed, or contains
invalid values by printing a single `error: …` line to stderr and exiting with status 2 —
never an unhandled traceback. This applies to every user-supplied file the CLI loads:
the custom provider knowledge base (`--providers`), the residency policy (`--policy`),
and both SBOM documents in `diff` mode.

#### Scenario: A missing policy file fails cleanly
- **WHEN** `borderlint scan <path> --policy /nonexistent.json --classification x` is run
- **THEN** the CLI prints an `error:` line naming the problem and exits 2, with no
  traceback on stderr

#### Scenario: A malformed policy file fails cleanly
- **WHEN** the policy file is not valid JSON
- **THEN** the CLI prints an `error:` line and exits 2, with no traceback on stderr

#### Scenario: An invalid policy value fails cleanly
- **WHEN** the policy file is valid JSON but contains an invalid token (for example an
  unknown sovereignty bloc in a classification allow-list)
- **THEN** the CLI prints an `error:` line describing the invalid value and exits 2,
  with no traceback on stderr

### Requirement: Git invocations on scanned repos are config-neutralized
The CLI SHALL neutralize a scanned (potentially untrusted) repository's configuration on
every `git` subprocess it runs against that repository: `-c core.fsmonitor=false`,
`-c core.hooksPath=/dev/null`, and `GIT_OPTIONAL_LOCKS=0`. This covers both the tag
lookup for the Mermaid project label and the commit lookup for the evidence/HTML audit
envelope, so a scanned repo cannot influence or be mutated by the scan's own git calls.

#### Scenario: Evidence envelope uses the same hardened git posture as the tag lookup
- **WHEN** the CLI collects the audit envelope's `git rev-parse HEAD` for an
  `evidence` or `html` scan of a repository
- **THEN** the invocation carries `-c core.fsmonitor=false`,
  `-c core.hooksPath=/dev/null`, and `GIT_OPTIONAL_LOCKS=0`, matching the flags used
  for the Mermaid project-label tag lookup
