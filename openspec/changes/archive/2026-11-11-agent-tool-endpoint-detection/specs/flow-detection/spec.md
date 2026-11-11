# flow-detection Delta

## ADDED Requirements

### Requirement: Detect explicitly declared agent-tool endpoints
The scanner SHALL recognise curated configuration keys that explicitly declare an MCP or agent-tool endpoint in scanned source and configuration files, and SHALL record each declaration as an `agent_tool_endpoint` detection. The recognised forms SHALL include MCP-specific and agent-tool-specific snake_case, environment-style, and camelCase keys. The scanner SHALL NOT create this detection kind for arbitrary URLs or keys without explicit MCP/agent-tool context. Known hosts SHALL resolve through the provider KB, loopback hosts SHALL resolve to `local`, and unmapped or runtime-templated destinations SHALL resolve to `unknown`. Evidence SHALL identify the declaration key and only a sanitized host or runtime-resolved marker; it SHALL NOT retain URL userinfo, paths, query strings, fragments, headers, or complete assignment values. An explicit detection SHALL take precedence over a generic endpoint detection for the same declaration. These detections SHALL use the existing policy, waiver, reporting, and exit-code paths without a new CLI option.

#### Scenario: Unknown MCP destination in environment config
- **WHEN** a `.env` file contains `MCP_SERVER_URL=https://mcp.example.com/sse`
- **THEN** one `agent_tool_endpoint` detection identifies `custom_endpoint`, jurisdiction `unknown`, and sanitized host `mcp.example.com`

#### Scenario: Known MCP provider resolves without a duplicate
- **WHEN** a scanned config declares `MCP_SERVER_URL=https://mcp.sentry.dev/mcp`
- **THEN** one `agent_tool_endpoint` detection resolves Sentry's curated jurisdiction and sovereignty, and no generic endpoint detection is emitted for that declaration

#### Scenario: Camel-case agent-tool key resolves a custom host
- **WHEN** a TypeScript settings object contains `agentToolEndpoint: "https://tools.internal.example/mcp"`
- **THEN** an `agent_tool_endpoint` detection identifies the custom destination with jurisdiction `unknown`

#### Scenario: Loopback tool endpoint is local
- **WHEN** a declaration contains `mcp_endpoint: http://localhost:8931/sse`
- **THEN** the detection resolves to provider and jurisdiction `local`

#### Scenario: Runtime-templated destination remains visible
- **WHEN** a declaration contains `MCP_SERVER_URL=${MCP_GATEWAY_URL}/sse`
- **THEN** an `agent_tool_endpoint` detection resolves to `unknown` and uses a runtime-resolved evidence marker

#### Scenario: Sensitive URL components are excluded from evidence
- **WHEN** a declaration contains `https://user:secret@mcp.example.com/sse?token=secret#fragment`
- **THEN** its evidence contains the key and `mcp.example.com` but none of the userinfo, path, query, fragment, or secrets

#### Scenario: Arbitrary URL lacks tool context
- **WHEN** a scanned file contains `fetch("https://example.com/data")` or an ordinary `url` field with an unmapped host
- **THEN** no `agent_tool_endpoint` detection is produced

#### Scenario: Authentication URL is not a tool destination
- **WHEN** a scanned file declares `MCP_AUTH_URL=https://auth.example.com/authorize`
- **THEN** no `agent_tool_endpoint` detection is produced

#### Scenario: Disallowed tool destination fails residency
- **WHEN** an agent-tool endpoint resolves outside the active classification's allow-list
- **THEN** the finding fails with reason `residency` and the normal nonzero exit status

#### Scenario: Unknown handling and waivers retain existing semantics
- **WHEN** an agent-tool destination is unknown or carries a justified inline waiver
- **THEN** existing `on_unknown` and waiver behavior applies without a tool-specific override

#### Scenario: Tool findings use existing output contracts
- **WHEN** a scan with an `agent_tool_endpoint` detection renders as text, JSON, SARIF, SBOM, evidence, HTML, Mermaid, or badge output
- **THEN** the existing rendering path handles the finding without a new output schema or CLI option

## MODIFIED Requirements

### Requirement: Model references bind to same-file provider detections
A `model_reference` detection SHALL bind to a provider detection in the same file when the
file's matched model references resolve to exactly one distinct provenance bloc, assigning that
bloc to the flow; when several same-bloc references bind, the first matched reference's
identifier SHALL be recorded as the flow's model identifier, representing its siblings. When a
file's model references resolve to more than one distinct bloc, binding would be ambiguous: no
binding SHALL occur and each reference SHALL stand alone. A `model_reference` with no provider
detection in its file SHALL stand alone as its own finding. Binding SHALL NOT cross file
boundaries. Model references SHALL NOT bind to detections of kind `agent_tool_endpoint`; when
such a detection is the only provider detection in the file, each reference SHALL stand alone.

#### Scenario: Model reference in the same file as a provider flow
- **WHEN** a file contains both a provider detection and a matching model reference
- **THEN** the provider flow carries the model reference's provenance and both evidences are traceable

#### Scenario: Ambiguous blocs do not bind
- **WHEN** a file contains a provider detection and model references resolving to two distinct blocs
- **THEN** the provider flow keeps its two-tier provenance and each reference is reported as its own standalone finding

#### Scenario: Standalone model reference
- **WHEN** a file contains a matching model reference but no provider detection
- **THEN** a standalone `model_reference` finding is reported with its resolved provenance

#### Scenario: Model reference does not bind to an agent tool
- **WHEN** a file contains an `agent_tool_endpoint` detection and a matching model reference but no other provider flow
- **THEN** the tool detection keeps provenance `unknown` and the model reference is reported standalone

#### Scenario: Model reference binds beside an agent tool
- **WHEN** a file contains an eligible model provider flow, an `agent_tool_endpoint` detection, and one matching model reference
- **THEN** the reference binds only to the eligible provider flow and not to the tool endpoint
