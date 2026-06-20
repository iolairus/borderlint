## ADDED Requirements

### Requirement: Unrecognised configured host resolves to unknown
The system SHALL resolve an endpoint detected via a configuration key or client override to an
unknown jurisdiction when its host is not in the knowledge base and is not a loopback host, so that
the policy governs it.

#### Scenario: Custom OpenAI-compatible host
- **WHEN** a configured endpoint host (for example `llm.acme.cn`) is not in the knowledge base
- **THEN** its jurisdiction is unknown

### Requirement: Loopback endpoints are local
A loopback or localhost endpoint SHALL resolve to the `local` jurisdiction.

#### Scenario: Local inference server
- **WHEN** a configured endpoint points at `http://localhost:8080` or `http://127.0.0.1`
- **THEN** its jurisdiction is `local` (a loopback host takes precedence over the unknown-host rule)

## MODIFIED Requirements

### Requirement: Jurisdiction codes and special tokens
The system SHALL express jurisdictions as lowercase ccTLD/ISO-3166 country codes, plus the special
tokens `CN-GBA` (the nine Mainland GBA cities), `GBA` (an alias for `hk` plus `CN-GBA`), and `local`
(a loopback / on-host inference endpoint, which is not a cross-border transfer).

#### Scenario: GBA alias expands
- **WHEN** the `GBA` token is evaluated
- **THEN** it is treated as the set containing `hk` and `CN-GBA`

#### Scenario: local is a recognised token
- **WHEN** a flow resolves to `local`
- **THEN** it is a valid jurisdiction value, distinct from a country code and from `unknown`
