## ADDED Requirements

### Requirement: Detect OpenAI-compatible API calls
The system SHALL detect an OpenAI-compatible API call in Python or JavaScript/TypeScript source by its
request-path signature — `/v1/chat/completions`, `/v1/completions`, `/v1/responses`, or
`/v1/embeddings` — even when the host is supplied at runtime, and record a detection. The system SHALL
resolve the jurisdiction from a static host adjacent to the path in the same string: a loopback host as
`local`, and a known provider host to that provider's jurisdiction. The system SHALL record `unknown`
when the host is dynamic (a variable or interpolation) or otherwise unresolved. The system SHALL NOT
flag a non-OpenAI-compatible `/v1/` path.

#### Scenario: Call to a runtime-configured endpoint is unknown
- **WHEN** source contains `fetch(`${LLAMA_URL}/v1/chat/completions`)` with a runtime host
- **THEN** a detection is recorded with jurisdiction `unknown`

#### Scenario: Call to a static loopback endpoint is local
- **WHEN** source contains a call to `http://localhost:8080/v1/chat/completions`
- **THEN** a detection is recorded with jurisdiction `local`

#### Scenario: Call to a static known-provider endpoint resolves the provider
- **WHEN** source contains a call to `https://api.openai.com/v1/chat/completions`
- **THEN** a detection is recorded identifying OpenAI with jurisdiction `us`

#### Scenario: A non-AI v1 path is not flagged
- **WHEN** source contains a path such as `/v1/users` or `/api/v1/health`
- **THEN** no OpenAI-compatible call detection is recorded
