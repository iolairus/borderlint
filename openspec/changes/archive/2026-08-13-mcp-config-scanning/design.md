## Context

borderlint scans application code for AI data flows, but agent stacks now carry flows the code never shows: MCP servers configured in `.mcp.json`, `claude_desktop_config.json`, and editor equivalents. Each server is either a remote endpoint (url) or a local process (command) that talks to a service somewhere. The scanner walk already reads JSON files; MCP configs need structural parsing, not line-regex scanning, to attribute a jurisdiction per server.

## Goals / Non-Goals

**Goals:**
- One detection per configured MCP server, resolved to provider/jurisdiction/sovereignty or an explicit `unknown`.
- Reuse everything downstream: policy evaluation, waivers, all output formats, exit codes — zero new flags.
- A bundled, reviewable `mcp_servers.json` map for stdio servers, under the existing KB drift posture.

**Non-Goals:**
- No runtime traffic interception; no scanning of server source repos; no tool-permission analysis.
- No aggregator modeling of multi-backend servers in v1 — a server whose backend is user-configured maps to `unknown`.

## Decisions

- **Structural parse by filename, not content sniffing**: recognise the four known config filenames; parse JSON; iterate `mcpServers` (or VS Code's top-level `servers` — that file never uses `mcpServers`). Rejected regex line-scanning — a `url` in JSON already partially hits `_scan_config_endpoints`, but stdio servers are invisible to it and attribution per server entry needs structure. On a successful parse the structural parser claims the file so the line-scanner doesn't double-report its URLs; on malformed JSON the file falls back to ordinary line scanning, so a provider URL still surfaces rather than vanishing.
- **Remote resolution via `kb.match_endpoint`**: identical trust posture to config endpoints — known host, loopback → `local`, else `custom_endpoint`/`unknown`. No new resolution machinery.
- **Stdio resolution via a package→provider map**: `mcp_servers.json` maps package identifiers (`@modelcontextprotocol/server-github`, `mcp-server-postgres`, …) to an existing provider KB id, so jurisdiction and sovereignty come from one source of truth. New providers needed for popular servers' services (e.g. GitHub) are added as ordinary KB providers. Rejected embedding jurisdictions directly in the MCP map — two sources of truth would drift.
- **Line attribution**: record the line of the server's name key in the JSON source (scan the raw text for the key), so findings stay clickable evidence like every other detection.
- **Kind `mcp_server`**: a new kind string; downstream code treats kinds as opaque labels, so reports work unchanged.

## Risks / Trade-offs

- [Risk] The MCP server ecosystem churns fast; the map goes stale → Mitigation: the map carries the `updated` field `kb_drift.py` reads, so the weekly staleness check covers it; unmapped packages are loudly `unknown`, never silently dropped.
- [Risk] Env-var-templated URLs (`${MCP_URL}`) resolve at runtime → Mitigation: template-bearing URLs surface as `unknown`, consistent with the existing runtime-resolved posture.
- [Risk] Claude Desktop config lives outside the repo tree, so repo scans won't see it → Mitigation: documented; users point `scan` at the config path directly (a file argument already works).

## Real-world validation (gate before merge)

Per repo practice for detection features: validate against real MCP configs — at minimum the Claude Code docs examples, two public repos shipping `.mcp.json`, and a Claude Desktop config with both url and stdio servers — before the PR merges.
