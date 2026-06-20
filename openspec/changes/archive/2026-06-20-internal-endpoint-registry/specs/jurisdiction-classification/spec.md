## MODIFIED Requirements

### Requirement: User-supplied knowledge base
The system SHALL merge a user-supplied knowledge base with the bundled one: user entries add to the
bundled providers and, on a host, SDK, or package conflict, take precedence. A user-supplied host
SHALL be resolved in preference to any bundled host. The user-supplied knowledge base does not
replace the bundled one.

#### Scenario: Custom provider added alongside bundled
- **WHEN** the user supplies a knowledge base defining an additional provider
- **THEN** detections for that provider resolve using the supplied definition, and bundled providers still resolve

#### Scenario: User entry overrides a bundled host
- **WHEN** a user entry defines a host that also exists in the bundled knowledge base
- **THEN** the user entry's jurisdiction takes precedence over the bundled host

#### Scenario: User overrides a bundled provider
- **WHEN** a user entry defines a provider whose id, SDK, or package name also exists in the bundled knowledge base
- **THEN** the user definition takes precedence for that provider

## ADDED Requirements

### Requirement: Endpoint-to-jurisdiction registry
The system SHALL accept a simple endpoints map (host to jurisdiction code) in a user-supplied file
and resolve those hosts to the given jurisdiction, merged additively with the bundled knowledge base.
Each mapped jurisdiction MUST be a recognised token — a ccTLD/ISO country code, or one of `CN-GBA`,
`GBA`, `local`, `unknown`; an unrecognised token SHALL be rejected with an error.

#### Scenario: Internal regional endpoints resolve
- **WHEN** a user file maps `llm-cn.acme.com` to `cn`, `llm-sg.acme.com` to `sg`, and `llm-hk.acme.com` to `hk`
- **THEN** a flow to each host resolves to its mapped jurisdiction (`cn`, `sg`, and `hk` respectively)

#### Scenario: Invalid jurisdiction token is rejected
- **WHEN** a user file maps a host to an unrecognised token (for example `overseas`)
- **THEN** the system rejects it with an error
