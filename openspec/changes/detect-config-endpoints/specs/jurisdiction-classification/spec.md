## ADDED Requirements

### Requirement: Unrecognised configured host resolves to unknown
The system SHALL resolve an endpoint detected via a configuration key or client override to an
unknown jurisdiction when its host is not in the knowledge base, so that the policy governs it.

#### Scenario: Custom OpenAI-compatible host
- **WHEN** a configured endpoint host (for example `llm.acme.cn`) is not in the knowledge base
- **THEN** its jurisdiction is unknown

### Requirement: Loopback endpoints are local
A loopback or localhost endpoint SHALL resolve to the `local` jurisdiction.

#### Scenario: Local inference server
- **WHEN** a configured endpoint points at `http://localhost:8080` or `http://127.0.0.1`
- **THEN** its jurisdiction is `local`
