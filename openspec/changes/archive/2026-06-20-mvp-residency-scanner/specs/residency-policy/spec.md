## ADDED Requirements

### Requirement: Classification-keyed policy
The system SHALL accept a policy that maps each data classification to an allow-list of acceptable
jurisdiction codes.

#### Scenario: Policy defines a classification allow-list
- **WHEN** a policy maps `customer-pii` to the allow-list `hk`, `CN-GBA`, `sg`
- **THEN** those jurisdictions are the acceptable set for the `customer-pii` classification

### Requirement: Per-run classification selection
The system SHALL accept exactly one active data classification per run, declaring the data class
flowing through the scanned path, and SHALL evaluate flows against that classification's allow-list.

#### Scenario: Run declares a classification
- **WHEN** a run declares the classification `customer-pii`
- **THEN** detected flows are evaluated against the `customer-pii` allow-list

### Requirement: Deny-by-default evaluation
A flow whose resolved jurisdiction is not on the allow-list for the active classification SHALL be
reported as a violation; a flow whose jurisdiction is on the allow-list SHALL pass.

#### Scenario: Jurisdiction outside the agreed locations
- **WHEN** the `customer-pii` allow-list is `hk`, `CN-GBA`, `sg` and a flow resolves to `my`
- **THEN** the flow is reported as a violation

#### Scenario: Jurisdiction within the agreed locations
- **WHEN** the `customer-pii` allow-list is `hk`, `CN-GBA`, `sg` and a flow resolves to `sg`
- **THEN** the flow passes

### Requirement: GBA alias in policy
When an allow-list contains `GBA`, the system SHALL treat both `hk` and `CN-GBA` as acceptable.

#### Scenario: GBA token permits a GBA flow
- **WHEN** an allow-list contains `GBA` and a flow resolves to `CN-GBA`
- **THEN** the flow passes

### Requirement: Unknown jurisdiction handling
The policy SHALL configure whether a flow with an unknown jurisdiction is treated as a warning or
as a violation.

#### Scenario: Unknown configured to fail
- **WHEN** the policy treats unknown jurisdictions as violations and a flow resolves to unknown
- **THEN** the flow is reported as a violation

#### Scenario: Unknown configured to warn
- **WHEN** the policy treats unknown jurisdictions as warnings and a flow resolves to unknown
- **THEN** the flow is reported as a warning and does not fail the run

### Requirement: Built-in and extensible classifications
The system SHALL support the classifications `non-pii`, `employee-pii`, and `customer-pii`, and
SHALL allow additional user-defined classifications in the policy.

#### Scenario: User-defined classification
- **WHEN** a policy defines an additional classification and a run selects it
- **THEN** flows are evaluated against that classification's allow-list

### Requirement: Provider allow and deny lists
The system SHALL allow a policy to deny-list or allow-list specific providers independent of
jurisdiction. A denied provider SHALL be a violation; when an allow-list is set, a provider not on
it SHALL be a violation.

#### Scenario: Denied provider
- **WHEN** a policy denies the provider `deepseek` and a flow uses `deepseek`
- **THEN** the flow is reported as a violation regardless of its jurisdiction

### Requirement: Configurable failure set
The system SHALL allow a policy to configure which finding types fail the run (the failure set),
defaulting to residency violations and denied-provider violations.

#### Scenario: Failure set omits a finding type
- **WHEN** a policy's failure set omits unknown-jurisdiction findings and a flow resolves to unknown
- **THEN** the run does not fail on that finding

### Requirement: Declare home regime
The system SHALL allow a policy to declare the entity's home regime (`pdpo` for Hong Kong or `pipl`
for GBA/Mainland), which determines which cross-border arrangement references are surfaced.

#### Scenario: Home regime declared
- **WHEN** a policy declares the home regime `pdpo`
- **THEN** arrangement references surfaced for flagged flows are those relevant to a PDPO home regime
