## MODIFIED Requirements

### Requirement: Scan command
The CLI SHALL provide a `scan` command that takes a path to scan, an optional policy, an optional active classification, and an output format (human-readable, JSON, Mermaid, SARIF, SBOM, or evidence).

#### Scenario: Scan a path against a policy
- **WHEN** the user runs the scan command with a path, a policy, and a classification
- **THEN** the path is scanned and detected flows are evaluated against the policy for that classification

### Requirement: Init command
The CLI SHALL provide an `init` command, as a third subcommand alongside `scan` and `diff`, that scaffolds a `residency.json` policy. The command SHALL accept `--home <seat>`, `--classes <csv>`, `--output <path>` (default `./residency.json`), and `--force` options.

#### Scenario: Init subcommand is listed
- **WHEN** the user runs `borderlint --help`
- **THEN** `init` appears as an available subcommand alongside `scan` and `diff`

#### Scenario: Init accepts its options
- **WHEN** the user runs `borderlint init --home hk --classes customer-pii --output out.json --force`
- **THEN** the command parses without error and uses those values
