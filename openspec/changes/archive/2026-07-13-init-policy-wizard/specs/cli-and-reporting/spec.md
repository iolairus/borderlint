## ADDED Requirements

### Requirement: Init command
The CLI SHALL provide an `init` command, as a third subcommand alongside `scan` and `diff`, that scaffolds a `residency.json` policy. The command SHALL accept `--home <seat>`, `--classes <csv>`, `--output <path>` (default `./residency.json`), and `--force` options.

#### Scenario: Init subcommand is listed
- **WHEN** the user runs `borderlint --help`
- **THEN** `init` appears as an available subcommand alongside `scan` and `diff`

#### Scenario: Init accepts its options
- **WHEN** the user runs `borderlint init --home hk --classes customer-pii --output out.json --force`
- **THEN** the command parses without error and uses those values
