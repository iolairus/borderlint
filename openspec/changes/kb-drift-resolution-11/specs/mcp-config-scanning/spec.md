## ADDED Requirements

### Requirement: Reviewed stdio launcher identities resolve to existing services

The bundled MCP-server map SHALL replace the invalid `@modelcontextprotocol/server-sqlite`
identifier and add exactly these reviewed launch identities for existing provider targets:

- Local: `mcp-server-sqlite` and image `mcp/sqlite`; binaries `mcp-server-filesystem`,
  `mcp-server-memory`, `mcp-server-everything`, `mcp-server-sequential-thinking`, and
  `mcp-server-postgres`.
- Brave Search: package `@brave/brave-search-mcp-server`, binary `brave-search-mcp-server`,
  and images `mcp/brave-search` and `docker.io/mcp/brave-search`.
- Notion: binary `notion-mcp-server` and image `mcp/notion`.
- Sentry: binaries `sentry` and `sentry-mcp`.

The existing GitHub mappings (`@modelcontextprotocol/server-github`, `github-mcp-server`, and
`ghcr.io/github/github-mcp-server`), Slack mapping (`@modelcontextprotocol/server-slack`), and
Google Drive mapping (`@modelcontextprotocol/server-gdrive`) SHALL be retained. Other valid
archived identifiers that still occur in existing configurations SHALL remain mapped. No
`mcp-server-fetch`, `mcp-server-git`, or `mcp-server-time` mapping SHALL be added.

#### Scenario: Official SQLite launch forms resolve locally
- **WHEN** MCP config invokes `uvx mcp-server-sqlite` or the `mcp/sqlite` image
- **THEN** the server resolves to `local`

#### Scenario: Reviewed local reference binaries resolve
- **WHEN** MCP config invokes `mcp-server-filesystem`, `mcp-server-memory`,
  `mcp-server-everything`, `mcp-server-sequential-thinking`, or `mcp-server-postgres`
- **THEN** each server resolves to `local`

#### Scenario: Every current Brave launch form resolves
- **WHEN** MCP config invokes `@brave/brave-search-mcp-server`, `brave-search-mcp-server`,
  `mcp/brave-search`, or `docker.io/mcp/brave-search`
- **THEN** each server resolves to `brave_search`

#### Scenario: Notion and Sentry launch forms resolve
- **WHEN** MCP config invokes `notion-mcp-server`, `mcp/notion`, `sentry`, or `sentry-mcp`
- **THEN** the first two resolve to `notion` and the last two to `sentry`

#### Scenario: Invalid SQLite and unreviewed reference binaries are not retained
- **WHEN** the bundled map is loaded
- **THEN** `@modelcontextprotocol/server-sqlite` is absent, `mcp-server-sqlite` maps to `local`,
  and no fetch, git, or time binary mapping is present
