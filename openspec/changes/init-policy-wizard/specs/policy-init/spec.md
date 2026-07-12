## ADDED Requirements

### Requirement: Init command availability
The CLI SHALL provide an `init` command that scaffolds a `residency.json` policy by interviewing the
operator and grounding proposals in a read-only inventory scan of the target path.

#### Scenario: Init scaffolds a policy
- **WHEN** the user runs `borderlint init` in a project
- **THEN** borderlint interviews for a home base and handled data classes, runs an inventory scan, and writes a `residency.json`

### Requirement: Home base interview
The `init` command SHALL prompt for a home base selected from the supported seats `hk`, `mo`, `CN-GBA`, `jp`, `kr`, `sg`, `au`, `uk`, `eu`, `my`, defaulting to `hk` on empty input, and SHALL validate the value against the recognised jurisdiction vocabulary.

#### Scenario: Home base accepted
- **WHEN** the operator enters `sg` as the home base
- **THEN** `sg` is recorded as the policy `home_location`

#### Scenario: Empty home base defaults
- **WHEN** the operator provides no input for the home base prompt
- **THEN** the home base defaults to `hk`

#### Scenario: Invalid home base rejected
- **WHEN** the operator enters a token outside the supported seat list (e.g. `zz` or `us`)
- **THEN** the prompt is repeated until a supported seat is entered (the wizard validates membership in the supported seats, not merely a two-letter format)

### Requirement: Data class interview
The `init` command SHALL prompt for which data classifications the operator handles, from `non-pii`, `employee-pii`, `customer-pii` (plus any user-typed extra), defaulting to all three when no selection is made.

#### Scenario: Selected classes recorded
- **WHEN** the operator selects `customer-pii` and `employee-pii`
- **THEN** the proposed policy covers only those two classifications

#### Scenario: Empty class selection defaults to all
- **WHEN** the operator provides no class selection
- **THEN** the proposed policy covers `non-pii`, `employee-pii`, and `customer-pii`

### Requirement: Inventory-grounded jurisdiction walk
After the inventory scan, the `init` command SHALL walk each observed jurisdiction and, for each handled classification, prompt to keep or drop that jurisdiction for that class, adding affirmed jurisdictions to the class allow-list.

#### Scenario: Observed jurisdiction kept
- **WHEN** the inventory finds a flow to `sg` and the operator answers yes for `customer-pii`
- **THEN** `sg` is added to the `customer-pii` allow-list

#### Scenario: Observed jurisdiction dropped
- **WHEN** the inventory finds a flow to `us` and the operator answers no for `employee-pii`
- **THEN** `us` is omitted from the `employee-pii` allow-list

#### Scenario: Home base pre-seeded
- **WHEN** the home base is `hk`
- **THEN** `hk` is present in every handled classification's allow-list without a prompt

### Requirement: Overwrite protection
The `init` command SHALL refuse to overwrite an existing output file unless `--force` is supplied, exiting non-zero and printing an error to stderr.

#### Scenario: Refuse to overwrite
- **WHEN** a `residency.json` already exists and `init` is run without `--force`
- **THEN** borderlint prints an error and exits with a non-zero status without modifying the file

#### Scenario: Force overwrites
- **WHEN** a `residency.json` already exists and `init` is run with `--force`
- **THEN** the existing file is overwritten with the proposed policy

### Requirement: Non-interactive mode
When both `--home` and `--classes` are supplied, the `init` command SHALL skip all prompts, seed the home base into every class allow-list, add every observed jurisdiction to every class allow-list, and write the file directly.

#### Scenario: Scripted init
- **WHEN** the user runs `borderlint init --home hk --classes customer-pii,non-pii`
- **THEN** a `residency.json` is written with no interactive prompts

### Requirement: Emitted policy shape
The `init` command SHALL write a policy containing `home_location`, a `classifications` map of handled classes to jurisdiction allow-lists, and `on_unknown` set to `warn`, so the file loads via the existing policy loader. The `init` command SHALL NOT emit a `fail_on` block, so the policy inherits the engine default (`residency`, `denied_provider`, `model_denied`) rather than downgrading a later-added `deny_models` match to a warning or silently opting the user into the sovereignty dimension.

#### Scenario: Written file is loadable
- **WHEN** `init` writes `residency.json`
- **THEN** the file is accepted by the existing `load_policy` loader without error

#### Scenario: fail_on is inherited, not emitted
- **WHEN** `init` writes `residency.json`
- **THEN** the file contains no `fail_on` key and inherits the engine default failure set
