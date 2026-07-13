## ADDED Requirements

### Requirement: Shields.io endpoint badge format
The CLI SHALL produce a shields.io endpoint JSON badge when `--format badge` is requested, conforming to schema version 1 with fields: `schemaVersion`, `label`, `message`, and `color`.

#### Scenario: Badge output requested in policy mode
- **WHEN** the user runs a scan with `--format badge` and a policy
- **THEN** the CLI emits JSON with `schemaVersion` set to 1, `label` set to `"borderlint"`, and valid `message` and `color` fields

#### Scenario: Badge output requested in inventory mode
- **WHEN** the user runs a scan with `--format badge` without a policy
- **THEN** the CLI emits JSON with `schemaVersion` set to 1, `label` set to `"borderlint"`, and valid `message` and `color` fields

### Requirement: Badge color coding by policy result
The badge color SHALL be `"green"` when no violations exist (policy mode, clean), `"red"` when any failures exist (policy mode), `"yellow"` when only warnings exist (policy mode, no failures), and `"blue"` in inventory mode (no policy).

#### Scenario: Clean policy result yields green badge
- **WHEN** a scan with policy finds no violations and `--format badge` is requested
- **THEN** the badge color is `"green"`

#### Scenario: Policy violations yield red badge
- **WHEN** a scan with policy finds at least one failure and `--format badge` is requested
- **THEN** the badge color is `"red"`

#### Scenario: Policy warnings only yield yellow badge
- **WHEN** a scan with policy finds warnings but no failures and `--format badge` is requested
- **THEN** the badge color is `"yellow"`

#### Scenario: Inventory mode yields blue badge
- **WHEN** a scan without policy runs with `--format badge`
- **THEN** the badge color is `"blue"`

### Requirement: Badge message content
The badge message SHALL be `"clean"` when no violations exist (policy mode), `"{N} flagged"` when N violations exist (policy mode), and `"{N} flows"` when N flows are detected in inventory mode (including `"0 flows"` when zero flows are detected).

#### Scenario: Clean message in policy mode
- **WHEN** a scan with policy finds no violations and `--format badge` is requested
- **THEN** the badge message is `"clean"`

#### Scenario: Flagged count message in policy mode
- **WHEN** a scan with policy finds 2 violations and `--format badge` is requested
- **THEN** the badge message is `"2 flagged"`

#### Scenario: Flow count message in inventory mode
- **WHEN** a scan without policy detects 3 flows and `--format badge` is requested
- **THEN** the badge message is `"3 flows"`

### Requirement: Badge format is non-gating
The `--format badge` output SHALL exit with status 0 regardless of violations, consistent with other artifact-export formats (SBOM, evidence).

#### Scenario: Badge format exits zero on violations
- **WHEN** a scan with policy finds violations and `--format badge` is requested
- **THEN** the CLI exits with status 0

#### Scenario: Badge format exits zero when clean
- **WHEN** a scan with policy finds no violations and `--format badge` is requested
- **THEN** the CLI exits with status 0
