# Proposal: agent-tool-endpoint-detection

## Why

A7 is partly shipped: structured MCP configs already produce `mcp_server` findings. Explicit endpoint declarations outside those four filenames still disappear when their host is not already in the provider KB. For example, `MCP_SERVER_URL=https://mcp.example.com/sse` in `.env` produces no finding, so an agent's configured data destination can evade inventory and policy review.

## What Changes

- Detect explicitly keyed MCP and agent-tool endpoint declarations in already scanned source and config files, including snake_case, environment-style, and camelCase forms such as `MCP_SERVER_URL`, `mcp_endpoint`, and `agentToolEndpoint`.
- Emit a new `agent_tool_endpoint` detection kind. Known hosts resolve through the provider KB; loopback resolves to `local`; unknown and runtime-templated destinations resolve to `unknown`.
- Report the declaration key and sanitized host (or a runtime-resolved marker), never URL credentials, paths, query strings, fragments, or header values.
- Give the explicit detector precedence over generic endpoint detection for the same declaration, avoiding duplicate findings.
- Exclude `agent_tool_endpoint` findings from same-file model-reference binding; tool services do not run the referenced model weights.
- Reuse existing residency, unknown-jurisdiction, waiver, reporting, and exit-code behavior. Add no CLI flag, policy block, runtime dependency, or network access.
- Update README and mark A7 shipped in `CAPABILITIES.md` after both structured MCP configs and explicit agent-tool endpoints are covered.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `flow-detection`: explicitly declared MCP/agent-tool endpoints become traceable flows, and model-reference binding excludes tool-only destinations.

## Impact

- `borderlint/detect.py`: curated key matching, endpoint resolution, duplicate suppression, and provenance-binding exclusion.
- `tests/test_borderlint.py`: detection, negative, policy, waiver, evidence-sanitization, and output coverage.
- `README.md` and `CAPABILITIES.md`: document and close A7.
- Existing structured MCP parsing and all downstream report schemas remain unchanged.

## Non-goals

- No arbitrary URL, `fetch()` call, or call-graph scanning without explicit tool context.
- No runtime `tools/list`, traffic interception, payload inspection, tool-permission analysis, or transitive egress claims.
- No new MCP config filenames, JSONC/YAML MCP parsers, launcher grammar expansion, or private stdio-map overrides.
- No changes to existing stdio locality mappings, including database-backed servers; that hardening is a separate change.
- No change to provenance policy handling of tool services with `unknown` provenance.
- No A6 observability/telemetry detection; it will be proposed separately.
