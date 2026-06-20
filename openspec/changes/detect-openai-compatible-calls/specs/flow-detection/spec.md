## ADDED Requirements

### Requirement: Detect OpenAI-compatible API calls
The system SHALL detect an OpenAI-compatible API call in Python or JavaScript/TypeScript source by its
request-path signature — `/v1/chat/completions`, `/v1/completions`, `/v1/responses`, or
`/v1/embeddings` — even when the host is supplied at runtime, and record a detection. The system SHALL
resolve the jurisdiction from a static host in the **same string literal** (a single quoted or
template-literal token on one source line) as the path: a loopback host as `local`, and a known
provider host to that provider's jurisdiction. When the host is dynamic (a variable or interpolation),
supplied outside that literal, or absent (a relative path), the system SHALL record the
`custom_endpoint` pseudo-provider with jurisdiction `unknown`. The system SHALL NOT flag a `/v1/` path
outside this signature, and SHALL NOT record a duplicate detection for a flow already detected on the
same line — at most one detection per provider and jurisdiction per line.

#### Scenario: Call to a runtime-configured endpoint is unknown
- **WHEN** source contains `fetch(`${LLAMA_URL}/v1/chat/completions`)` with a host supplied at runtime
- **THEN** a detection is recorded with the `custom_endpoint` provider and jurisdiction `unknown`

#### Scenario: A host outside the path's literal is unknown
- **WHEN** the host is concatenated from a separate variable, for example `base + "/v1/chat/completions"`
- **THEN** a detection is recorded with jurisdiction `unknown`

#### Scenario: Call to a static loopback endpoint is local
- **WHEN** source contains a call to `http://localhost:8080/v1/chat/completions`
- **THEN** a detection is recorded with jurisdiction `local`

#### Scenario: A static known-provider endpoint is identified once
- **WHEN** source contains a call to `https://api.openai.com/v1/chat/completions`
- **THEN** exactly one detection identifies OpenAI with jurisdiction `us`, not duplicated by the path-signature detector

#### Scenario: A non-AI v1 path is not flagged
- **WHEN** source contains a path such as `/v1/users` or `/api/v1/health`
- **THEN** no OpenAI-compatible call detection is recorded
