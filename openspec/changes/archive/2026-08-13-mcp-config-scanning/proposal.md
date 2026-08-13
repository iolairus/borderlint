## Why

Teams are attaching MCP servers to Claude Code, Claude Desktop, Cursor, and VS Code by the dozen, and each configured server is a data flow no scanner reviews — the agent stack has become the fastest-growing source of unreviewed AI egress, beyond the application code borderlint already scans.

## What Changes

- Scan MCP configuration files (`.mcp.json`, `claude_desktop_config.json`, `.cursor/mcp.json`, `.vscode/mcp.json`) as a first-class detection surface.
- Remote servers (`url`-based, HTTP/SSE) resolve their host against the existing provider KB endpoint matching; unresolvable hosts surface as explicit `unknown`, loopback as `local`.
- Stdio servers (`command`/`args`-based) resolve their package name against a new bundled MCP-server map (`mcp_servers.json`) naming the operator and jurisdiction of the service the server talks to; unmapped packages surface as `unknown`.
- New detection kind `mcp_server`; detections flow through the existing evaluate/policy/waiver machinery and every existing output format unchanged.
- No new CLI flags; MCP configs are picked up by the normal `scan` walk.

## Capabilities

### New Capabilities
- `mcp-config-scanning`: detection and resolution of MCP server configurations — which servers an agent stack is wired to, where each sends data, evaluated against the residency policy like any other flow.

### Modified Capabilities
- `flow-detection`: the detection surface gains MCP config files and the `mcp_server` detection kind.

## Impact

- `borderlint/detect.py`: MCP config file recognition and structured parsing; new `mcp_server` kind.
- `borderlint/data/mcp_servers.json`: new bundled KB mapping known MCP server packages to operator, jurisdiction, and sovereignty; covered by the existing KB drift/review posture.
- `borderlint/report.py`: no format changes; `mcp_server` kind renders through existing paths.
- No breaking changes; no new runtime dependencies.

## Non-goals

- No runtime interception of MCP traffic; static config analysis only.
- No scanning of MCP server *source code* (a server's own egress is its author's codebase — scan that repo directly).
- No tool-level permission analysis (what a server can do), only data-flow resolution (where it sends data).
