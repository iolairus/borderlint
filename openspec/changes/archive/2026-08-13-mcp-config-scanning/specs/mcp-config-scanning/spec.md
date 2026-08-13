## ADDED Requirements

### Requirement: MCP configuration files are scanned
The scanner SHALL recognise MCP configuration files by name — `.mcp.json`, `claude_desktop_config.json`, `.cursor/mcp.json`, and `.vscode/mcp.json` — and parse their server block structurally (`mcpServers`, or VS Code's top-level `servers`), producing one detection per configured server with kind `mcp_server`. A recognised file SHALL be claimed by the structural parser: a provider URL inside it SHALL NOT additionally surface as an `endpoint_reference` or `config_endpoint` detection. A recognised file that is not valid JSON SHALL fall back to the existing line scanning; valid JSON with no server block SHALL produce no `mcp_server` detections. Neither case SHALL fail the scan.

#### Scenario: A project MCP config yields one detection per server
- **WHEN** a scanned tree contains a `.mcp.json` with two entries under `mcpServers`
- **THEN** the scan produces two detections of kind `mcp_server`, each carrying the config file path and the server entry's line

#### Scenario: A VS Code MCP config parses its servers key
- **WHEN** a scanned tree contains a `.vscode/mcp.json` with entries under top-level `servers`
- **THEN** each entry produces an `mcp_server` detection exactly as an `mcpServers` entry would

#### Scenario: The structural parser claims the file
- **WHEN** a server entry's `url` names a known provider host
- **THEN** the scan produces exactly one detection for it, of kind `mcp_server`, and no `endpoint_reference` or `config_endpoint` detection from the same file

#### Scenario: A malformed MCP config degrades to line scanning
- **WHEN** a file named `.mcp.json` contains invalid JSON with a provider URL in its text
- **THEN** the scan completes without error, produces no `mcp_server` detections, and the URL still surfaces via the existing line scanning

### Requirement: Remote MCP servers resolve via the provider KB
For a server entry declaring a `url`, the scanner SHALL resolve the URL's host against the existing provider KB endpoint matching: a known provider host resolves to that provider's jurisdiction and sovereignty; a loopback host resolves to `local`; a URL carrying an environment template (e.g. `${MCP_URL}`) in its host SHALL surface with jurisdiction `unknown` (runtime-resolved); any other host SHALL surface as `custom_endpoint` with jurisdiction `unknown`, never a guess.

#### Scenario: A known provider host resolves
- **WHEN** a server entry's `url` host matches a provider KB endpoint
- **THEN** the detection carries that provider's id and resolved jurisdiction

#### Scenario: An unknown remote host is explicit
- **WHEN** a server entry's `url` host matches no KB endpoint and is not loopback
- **THEN** the detection's jurisdiction is `unknown`

#### Scenario: A templated URL is runtime-resolved
- **WHEN** a server entry's `url` is `${MCP_GATEWAY_URL}/sse`
- **THEN** the detection's jurisdiction is `unknown`

#### Scenario: A loopback server is local
- **WHEN** a server entry's `url` host is a loopback address
- **THEN** the detection resolves to `local`

### Requirement: Stdio MCP servers resolve via the bundled MCP-server map
For a server entry declaring a `command`, the scanner SHALL extract the server package identifier from the command and arguments (e.g. an `npx`/`uvx` package name) and resolve it against a bundled `mcp_servers.json` map naming the operated service's provider id. A mapped package resolves to that provider's jurisdiction and sovereignty from the provider KB; an unmapped package SHALL surface with jurisdiction `unknown`. The map SHALL carry an `updated` review date in the same field the existing KB drift check reads, so it participates in the weekly staleness check.

#### Scenario: A known stdio server resolves to its service
- **WHEN** a server entry runs a package present in the MCP-server map
- **THEN** the detection resolves to the mapped provider and its jurisdiction

#### Scenario: An unmapped stdio server is explicit
- **WHEN** a server entry runs a package absent from the MCP-server map
- **THEN** the detection's jurisdiction is `unknown`

### Requirement: MCP detections flow through existing evaluation and reporting
Detections of kind `mcp_server` SHALL be evaluated against the residency policy, honour inline waivers, and appear in every existing output format through the existing rendering paths, with no new CLI flag required.

#### Scenario: An MCP flow violates the policy
- **WHEN** a configured MCP server resolves to a jurisdiction outside the active classification's allow-list
- **THEN** the finding fails with reason `residency`, identical in shape to any other flow

#### Scenario: MCP findings appear in existing formats
- **WHEN** a scan with MCP detections renders as text, JSON, SARIF, or SBOM
- **THEN** the `mcp_server` findings appear through the existing format contracts with kind `mcp_server`
