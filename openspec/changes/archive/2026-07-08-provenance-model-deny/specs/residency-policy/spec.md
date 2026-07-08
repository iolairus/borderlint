## ADDED Requirements

### Requirement: Model deny-list evaluation
The system SHALL report a `model_denied` reason for a finding whose model identifier matches
an entry of the provenance block's `deny_models` list. `model_denied` SHALL be a default member
of the failure set, exactly as `denied_provider` is, so a denied model fails the run unless the
policy explicitly removes it from `fail_on`. Matching SHALL apply the same identifier
normalization as the provenance map — lowercasing, model-file
basenames, redistributor-org stripping, and version-pin stripping — so a denied family cannot
be dodged by a repository path or a version suffix. The deny SHALL apply to provider flows with
a bound model identifier and to standalone model-reference findings alike. A finding with no
model identifier SHALL NOT match any deny entry.

#### Scenario: A denied family fails regardless of the serving host
- **WHEN** `deny_models` contains `deepseek` and a Bedrock flow binds the model reference `deepseek.r1-v1:0`
- **THEN** the finding fails with a `model_denied` reason under the default failure set, even though the flow's bloc may be on the allow-list

#### Scenario: A redistributor path does not dodge the deny
- **WHEN** `deny_models` contains `deepseek` and a flow binds `TheBloke/deepseek-llm-7B-GGUF`
- **THEN** the finding fails with a `model_denied` reason

#### Scenario: A standalone model reference is denied
- **WHEN** `deny_models` contains `deepseek` and a file contains a matching standalone model reference with no provider detection
- **THEN** the standalone finding fails with a `model_denied` reason

#### Scenario: No bound model, no deny
- **WHEN** `deny_models` contains `gpt-` and a flow is detected with no model identifier
- **THEN** no `model_denied` reason is produced for that flow

## MODIFIED Requirements

### Requirement: Optional provenance policy block
The system SHALL accept an optional `provenance` block in the policy. When the block is absent,
no provenance evaluation SHALL occur and no `provenance`, `provenance_unknown`, or
`model_denied` finding reason SHALL be produced, so that existing policies behave identically to before. When present, the
block MAY declare per-classification provenance allow-lists, an `on_unknown` setting (`warn`
or `fail`, default `warn`), and a `deny_models` list of anchored model-identifier prefixes.
Deny entries SHALL be non-empty strings of at least three characters after lowercasing; an
invalid entry SHALL fail policy load with an error naming it. Provenance bloc tokens in the block SHALL be validated against the
provenance vocabulary at policy load time.

#### Scenario: Absent provenance block leaves behaviour unchanged
- **WHEN** a policy has no `provenance` block
- **THEN** no flow is ever evaluated for provenance and no provenance reason is produced

#### Scenario: Invalid provenance token in the policy is rejected
- **WHEN** a policy's `provenance` block lists the bloc `mars` for a classification
- **THEN** policy loading fails with an error naming the invalid token and the accepted vocabulary

#### Scenario: An invalid deny entry is rejected at load time
- **WHEN** a policy's `deny_models` contains an empty string or an entry shorter than three characters
- **THEN** policy loading fails with an error naming the entry

### Requirement: Waiver applies to provenance findings
A waiver with a non-empty justification SHALL downgrade a provenance failure to the `waived`
state, consistent with residency and sovereignty waiver behaviour. A waiver SHALL NOT override
an explicit provider deny-list entry or an explicit model deny-list entry.

#### Scenario: Justified waiver on a provenance failure
- **WHEN** a flow that would fail the provenance allow-list carries a waiver with a justification
- **THEN** the finding is `waived` and does not contribute to the exit code

#### Scenario: A waiver cannot override a model deny
- **WHEN** a flow matching a `deny_models` entry carries a waiver with a justification
- **THEN** the finding still fails with the `model_denied` reason
