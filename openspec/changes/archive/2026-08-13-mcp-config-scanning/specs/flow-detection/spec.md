## ADDED Requirements

### Requirement: Detect MCP server configurations
The detection surface SHALL include MCP configuration files, producing detections of kind `mcp_server` — a new kind alongside `sdk_import`, `endpoint_reference`, `config_endpoint`, `api_call`, and `model_reference`. Resolution behavior is specified by the `mcp-config-scanning` capability; the existing exclusion rules (ignored directories, oversized files) and evidence rules (file, line, matched text) apply to MCP config files as to any other scanned file.

#### Scenario: MCP config detections carry the standard evidence
- **WHEN** a `.mcp.json` inside the scanned tree declares a server
- **THEN** the resulting detection has kind `mcp_server` and carries the config file path, the entry's line, and the server's identifying evidence

#### Scenario: Exclusion rules apply to MCP configs
- **WHEN** a `.mcp.json` sits under an ignored directory (e.g. `node_modules`)
- **THEN** it produces no detections
