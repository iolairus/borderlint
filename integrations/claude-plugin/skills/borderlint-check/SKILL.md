---
name: borderlint-check
description: Run borderlint before adding any AI SDK, AI endpoint, model identifier, or MCP server configuration to the codebase. Use whenever a change introduces an AI provider dependency, an LLM endpoint or base_url, a model id, or a structured MCP server entry with a remote url or stdio command/args — check residency, sovereignty, and provenance before the code is committed.
---

# borderlint pre-addition check

When a change you are about to make introduces an AI SDK import, an AI endpoint reference, a model
identifier, or structured MCP server configuration — including an MCP server under `mcpServers`
(VS Code: `servers`) in `.mcp.json`, `claude_desktop_config.json`, `.cursor/mcp.json`, or
`.vscode/mcp.json`, using a remote `url` or stdio `command` and `args`:

1. Run the scan first. If the project has a policy, discover its path and substitute it for
   `<project-policy-path>`:
   `borderlint scan . --policy <project-policy-path> --classification <data class>`
   Otherwise inventory mode: `borderlint scan .`
2. If the addition introduces a flow that is not `local` — or a provider/router resolving to
   `unknown` — report it in the conversation before committing: provider, residency
   jurisdiction, sovereignty bloc, and provenance bloc when a model id is involved. Let the
   human decide.
3. If the flow is accepted, record it with an inline waiver using the file's comment syntax and a
   required, real justification: `# borderlint: allow <justification>` or
   `// borderlint: allow <justification>`. Unjustified waivers are ignored; waivers cannot
   override a provider or model deny.

Backstop: the pre-commit hook enforces its configured scan. The CI SBOM `diff` gate fails when
the current SBOM adds a non-`local` provider/jurisdiction pair (including `unknown`) absent from
the baseline, not for every new endpoint or model. This skill moves the conversation to where the
decision is made.
