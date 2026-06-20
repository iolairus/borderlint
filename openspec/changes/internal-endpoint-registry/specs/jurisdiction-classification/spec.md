## MODIFIED Requirements

### Requirement: User-supplied knowledge base
The system SHALL merge a user-supplied knowledge base with the bundled one: user entries add to the
bundled providers and, on a host, SDK, or package conflict, take precedence. The user-supplied
knowledge base does not replace the bundled one.

#### Scenario: Custom provider added alongside bundled
- **WHEN** the user supplies a knowledge base defining an additional provider
- **THEN** detections for that provider resolve using the supplied definition, and bundled providers still resolve

#### Scenario: User entry overrides a bundled host
- **WHEN** a user entry defines a host that also exists in the bundled knowledge base
- **THEN** the user entry's jurisdiction takes precedence

## ADDED Requirements

### Requirement: Endpoint-to-jurisdiction registry
The system SHALL accept a simple endpoints map (host to jurisdiction code) in a user-supplied file
and resolve those hosts to the given jurisdiction, merged additively with the bundled knowledge base.

#### Scenario: Internal regional endpoints resolve
- **WHEN** a user file maps `llm-cn.acme.com` to `cn` and `llm-hk.acme.com` to `hk`
- **THEN** a flow to `llm-cn.acme.com` resolves to `cn` and a flow to `llm-hk.acme.com` resolves to `hk`
