# residency-policy Specification

## Purpose
TBD - created by archiving change mvp-residency-scanner. Update Purpose after archive.
## Requirements
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

### Requirement: Local endpoints are not a residency violation
A flow whose jurisdiction is `local` SHALL NOT count as a residency (allow-list) violation,
regardless of the classification's allow-list, because local inference is not a cross-border
transfer. This exemption applies to the jurisdiction allow-list only; provider deny-lists and other
policy checks still apply.

#### Scenario: Local flow under a strict allow-list
- **WHEN** a flow resolves to `local` and the active classification's allow-list does not list `local`
- **THEN** the flow passes the residency check

### Requirement: Waived flows are not violations
A waiver with a non-empty justification SHALL change a finding that would otherwise be a residency
(allow-list) or unknown-jurisdiction failure into the `waived` state — a terminal state that is
reported but never contributes to the failure exit code, regardless of the `fail_on` set. A waiver
SHALL NOT override an explicit provider deny-list entry. A waiver with no justification SHALL be
ignored, and the flow SHALL be evaluated normally. Only a failing finding can be waived.

#### Scenario: Justified waiver on a residency failure
- **WHEN** a flow that would fail the allow-list carries a waiver with a justification
- **THEN** the finding is `waived` and does not contribute to the exit code

#### Scenario: Waiver does not override a provider deny-list
- **WHEN** a flow whose provider is on the policy deny-list carries a waiver
- **THEN** the finding remains a violation, because a waiver cannot clear an explicit deny

#### Scenario: Unjustified waiver is ignored
- **WHEN** a flow carries a waiver with no justification
- **THEN** the waiver is ignored and the flow is evaluated normally

### Requirement: Home location declaration
The system SHALL allow a policy to declare an optional `home_location` as a lowercase ccTLD/ISO-3166
country code or a recognised special token. A `home_location` that is not well-formed (neither a
two-letter lowercase code nor a recognised special token) SHALL produce a warning and SHALL NOT fail
the run, because the home location drives only informational context — regime tags and arrangement
references — and never the residency verdict.

#### Scenario: A well-formed home location is accepted
- **WHEN** a policy declares `home_location` `jp`
- **THEN** the value is accepted without warning and used to derive informational context

#### Scenario: A malformed home location warns but does not fail
- **WHEN** a policy declares `home_location` `United Kingdom`
- **THEN** borderlint emits a warning and the run's exit code is not changed on account of the home location

### Requirement: Optional sovereignty policy block
The system SHALL accept an optional `sovereignty` block in the policy. When the block is absent,
no sovereignty evaluation SHALL occur and no `sovereignty` finding reason SHALL be produced, so
that existing policies behave identically to before. When present, the block MAY declare
per-classification sovereignty allow-lists, an `on_unknown` setting (`warn` or `fail`, default
`warn`), and inclusion of `sovereignty` in `fail_on`.

#### Scenario: Absent sovereignty block leaves behaviour unchanged
- **WHEN** a policy has no `sovereignty` block
- **THEN** no flow is ever evaluated for sovereignty and no `sovereignty` reason is produced

#### Scenario: A classification declares a sovereignty allow-list
- **WHEN** the `sovereignty` block maps `customer-pii` to the allow-list `eu`, `uk`, `local`
- **THEN** flows for the `customer-pii` classification are evaluated against that sovereignty allow-list

### Requirement: Sovereignty deny-by-default evaluation
A flow whose sovereignty is not on the allow-list for the active classification's sovereignty block SHALL be reported as a `sovereignty` reason; a flow whose sovereignty is on the allow-list SHALL pass the sovereignty check. A flow with sovereignty `unknown` SHALL be treated according to the `on_unknown` setting. A flow with sovereignty `local` SHALL NOT count as a sovereignty violation regardless of the allow-list, mirroring the residency `local` exemption, because self-hosted inference has no external sovereign. Every sovereignty evaluation MUST respect the active classification's declared allow-list.

#### Scenario: Sovereignty outside the allow-list
- **WHEN** the `customer-pii` sovereignty allow-list is `eu`, `uk`, `local` and a flow resolves to sovereignty `us`
- **THEN** the flow is reported with a `sovereignty` reason

#### Scenario: Sovereignty within the allow-list
- **WHEN** the `customer-pii` sovereignty allow-list is `eu`, `uk`, `local` and a flow resolves to sovereignty `eu`
- **THEN** the flow passes the sovereignty check

#### Scenario: Local sovereignty is exempt
- **WHEN** a flow resolves to sovereignty `local` and the active sovereignty allow-list does not list `local`
- **THEN** the flow passes the sovereignty check

#### Scenario: Unknown sovereignty configured to warn
- **WHEN** `on_unknown` is `warn` and a flow resolves to sovereignty `unknown`
- **THEN** the flow is reported as a warning and does not fail the run on account of sovereignty

### Requirement: Sovereignty failure set
The `fail_on` set SHALL accept `sovereignty`. When `sovereignty` is in `fail_on` and a flow's
sovereignty reason is a `sovereignty` mismatch (not `unknown`-as-warn), the finding SHALL fail
the run. The default `fail_on` SHALL NOT include `sovereignty`, so that opting into the
sovereignty block without explicitly failing on it produces warnings only.

#### Scenario: Sovereignty failure when fail_on includes sovereignty
- **WHEN** `fail_on` includes `sovereignty` and a flow's sovereignty is outside the allow-list
- **THEN** the finding fails the run

#### Scenario: Sovereignty warns by default
- **WHEN** `fail_on` does not include `sovereignty` and a flow's sovereignty is outside the allow-list
- **THEN** the finding is a warning and does not fail the run

### Requirement: Waiver applies to sovereignty findings
A waiver with a non-empty justification SHALL downgrade a sovereignty failure to the `waived`
state, consistent with the residency waiver behaviour. A waiver SHALL NOT override an explicit
provider deny-list entry.

#### Scenario: Justified waiver on a sovereignty failure
- **WHEN** a flow that would fail the sovereignty allow-list carries a waiver with a justification
- **THEN** the finding is `waived` and does not contribute to the exit code

