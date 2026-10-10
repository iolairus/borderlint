# residency-policy Delta

## MODIFIED Requirements

### Requirement: Model deny-list evaluation
The system SHALL report a `model_denied` reason for a finding whose model identifier matches
an entry of the provenance block's `deny_models` list. `model_denied` SHALL be a default member
of the failure set, exactly as `denied_provider` is, so a denied model fails the run unless the
policy explicitly removes it from `fail_on`. Matching SHALL apply the same identifier
normalization as the provenance map — lowercasing, model-file
basenames, redistributor-org stripping, and version-pin stripping — so a denied family cannot
be dodged by a repository path or a version suffix. Matching SHALL additionally test every
candidate form the provenance map would try for that identifier, including forms with a host-like
or curated local-runtime namespace segment disregarded, so a denied family cannot be dodged by
pulling it through a registry, a mirror, or a runtime launcher. The deny SHALL apply to provider
flows with a bound model identifier and to standalone model-reference findings alike. A finding with
no model identifier SHALL NOT match any deny entry. Because the candidate set is deliberately wider than
the map's primary form, an internal image name whose final segment begins with a denied family prefix is
denied too; that over-reach is fail-closed, is recorded in the design (Risks, R1), and is scoped by
narrowing the `deny_models` entry rather than by weakening the matcher.

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

#### Scenario: A runtime namespace does not dodge the deny
- **WHEN** `deny_models` contains `deepseek` and a flow binds `ollama/deepseek-r1`
- **THEN** the finding fails with a `model_denied` reason and its provenance resolves to `cn` rather than to the serving provider's bloc

#### Scenario: A registry or mirror host does not dodge the deny
- **WHEN** `deny_models` contains `deepseek` and a flow binds `mirror.internal/deepseek-r1`, or binds
  `huggingface.co/TheBloke/deepseek-coder-33B-AWQ`
- **THEN** each finding fails with a `model_denied` reason

#### Scenario: An internal tool name under a denied family is denied, fail-closed
- **WHEN** `deny_models` contains `deepseek` and a flow binds the internal image
  `ghcr.io/acme/deepseek-config-migrator`
- **THEN** the finding fails with a `model_denied` reason whose evidence is the full original literal,
  and scoping the entry to `deepseek-r1` exempts it without exempting the family
