# suricata-egress-rules Specification

## Purpose
Compiling the provider KB and residency policy into a Suricata TLS-SNI alert ruleset for network-level detection of disallowed AI egress.
## Requirements


### Requirement: Suricata ruleset from KB and policy
The system SHALL provide a `suricata` output format that emits a Suricata ruleset derived from the provider KB and the residency policy, independent of scan findings. Rule selection SHALL be per endpoint host, using each host's resolvable jurisdiction — the per-host jurisdiction recorded in the KB endpoint table (an `endpoint_jurisdictions` override where present, else the provider default). With a policy and classification, a host SHALL produce an `alert` rule when its resolvable jurisdiction is not in the allowed set — the policy's allow-list for the active classification after alias expansion (`uk` → `gb`, `GBA` → `hk` + `CN-GBA`); a host whose jurisdiction is in the allowed set SHALL produce no rule. A host whose resolvable jurisdiction is `unknown` therefore alerts unless the policy allows `unknown`. Hosts of a provider with a region scheme SHALL always produce an alert rule regardless of policy (a static host pattern cannot express a per-region allow-list). Without a policy, every KB endpoint host SHALL produce an alert rule.

#### Scenario: A disallowed host becomes an alert rule
- **WHEN** the policy allows only `hk` for the classification and the KB maps `api.deepseek.com` to jurisdiction `cn`
- **THEN** the ruleset contains an alert rule matching TLS SNI `api.deepseek.com`

#### Scenario: An allowed host produces no rule
- **WHEN** the policy allows `us` and a host's resolvable jurisdiction is `us`
- **THEN** no rule matches that host

#### Scenario: A multi-jurisdiction provider is selected per host
- **WHEN** the policy allows `sg` and a provider has one host resolving to `sg` and another to `cn`
- **THEN** the `cn` host appears as an alert rule and the `sg` host does not

#### Scenario: Policy aliases are honoured
- **WHEN** the policy allows `uk` and a host's resolvable jurisdiction is `gb`
- **THEN** no rule matches that host

#### Scenario: Unknown jurisdiction alerts
- **WHEN** a host's resolvable jurisdiction is `unknown` and the policy does not allow `unknown`
- **THEN** the host appears as an alert rule

#### Scenario: Region-scheme hosts always alert
- **WHEN** a provider carries a region scheme (e.g. AWS Bedrock, Huawei ModelArts) and the policy allows that provider's default jurisdiction
- **THEN** the provider's hosts still appear as alert rules, marked region-dependent

#### Scenario: Inventory mode covers every endpoint
- **WHEN** the format is `suricata` and no policy is supplied
- **THEN** every KB endpoint host appears as an alert rule

### Requirement: Rule content and metadata
Each rule SHALL match on TLS SNI, carry `classtype:policy-violation`, state the provider name and resolvable jurisdiction in `msg`, and carry the provider id and jurisdiction as Suricata `metadata` key-value pairs. Region-scheme providers SHALL be marked region-dependent in `msg`. Rules SHALL be alert-posture; the file header SHALL document conversion to `drop` and state that the file is generated wholesale and not to be hand-edited.

#### Scenario: Rule carries provider context
- **WHEN** a rule is emitted for a DeepSeek host
- **THEN** its `msg` names DeepSeek and jurisdiction `cn`, its `metadata` carries the provider id and jurisdiction, and its match is on TLS SNI

#### Scenario: A region-scheme provider is marked
- **WHEN** a rule is emitted for a region-scheme provider (e.g. AWS Bedrock)
- **THEN** its `msg` marks the flow as region-dependent

### Requirement: Deterministic output
The ruleset SHALL be deterministic: hosts totally ordered, sids assigned from a fixed base (1900000) by that order, no timestamps — two runs over the same KB and policy SHALL produce byte-identical output.

#### Scenario: Two runs are byte-identical
- **WHEN** the same KB and policy render the `suricata` format twice
- **THEN** the outputs are byte-identical
