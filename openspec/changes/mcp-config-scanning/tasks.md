## 1. MCP-server map

- [ ] 1.1 Create `borderlint/data/mcp_servers.json`: package identifier → provider id, with an `updated` date (the field `kb_drift.py` reads, so the weekly staleness check covers it); seed with the most-used public servers (reference servers, GitHub, Slack, Google Drive, Postgres, Brave Search, Sentry, Notion)
- [ ] 1.2 Add any missing service providers referenced by the map to `providers.json` as ordinary KB entries (surgical one-entry-per-line edits)
- [ ] 1.3 Load the map in `borderlint/kb.py` with validation (unknown provider id in the map → ValueError naming it)

## 2. Detection

- [ ] 2.1 Recognise the four MCP config filenames in `scan()` and route them to a structural parser that claims the file (no duplicate `endpoint_reference`/`config_endpoint` from line scanners)
- [ ] 2.2 Parse `mcpServers` (and VS Code's top-level `servers`): url entries → `kb.match_endpoint` (loopback → `local`, unknown host or templated URL → `unknown`); command entries → package identifier → MCP map lookup
- [ ] 2.3 Attribute the line of each server's name key; emit `Detection(kind="mcp_server")` with the server name and target as evidence
- [ ] 2.4 Malformed JSON falls back to line scanning; valid JSON without a server block → no detections; neither crashes

## 3. Tests

- [ ] 3.1 Unit tests: url-known, url-loopback, url-unknown, url-templated, stdio-mapped, stdio-unmapped, VS Code `servers` key, structural-parser claiming (no duplicate detections), malformed-JSON fallback, ignored-directory exclusion
- [ ] 3.2 End-to-end: `.mcp.json` fixture through `cli.main` with a policy — violation carries kind `mcp_server` and gates the exit code; JSON/SARIF render it
- [ ] 3.3 Real-world validation: run against Claude Code docs examples, two public repos with `.mcp.json`, and a real Claude Desktop config; record findings (and any KB gaps found) in the PR

## 4. Docs

- [ ] 4.1 README: MCP config scanning paragraph under the scan section, including the Claude Desktop out-of-tree note
