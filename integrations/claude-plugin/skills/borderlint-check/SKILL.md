---
name: borderlint-check
description: Check AI data flows before adding any AI SDK, endpoint, model identifier, or Model Context Protocol (MCP) server configuration. Use before introducing an AI provider dependency, LLM endpoint or base_url, model ID, or structured MCP server entry with a remote URL or stdio command and arguments.
---

# borderlint pre-addition check

borderlint checks residency (where AI data goes), sovereignty (which government may compel the
provider to disclose it), and provenance (who developed the model weights).

1. **Install the skill using one of these methods.**
   - Install the plugin: run `/plugin marketplace add iolairus/borderlint`, then
     `/plugin install borderlint@borderlint`.
   - Copy this file manually to `.claude/skills/borderlint-check/SKILL.md` in your project.
2. **Check every AI change before making it.** This includes:
   - An AI SDK import, AI endpoint reference, or model identifier.
   - A Model Context Protocol (MCP) server under `mcpServers` (VS Code: `servers`) in `.mcp.json`,
     `claude_desktop_config.json`, `.cursor/mcp.json`, or `.vscode/mcp.json`, using either a remote
     `url` or stdio `command` and `args`.
3. **Run borderlint first.** If the project has a policy, find its path and run:
   `borderlint scan . --policy <project-policy-path> --classification <data class>`.
   Otherwise, run inventory mode: `borderlint scan .`.
4. **Report the change before committing.** If the addition introduces a flow that is not `local`,
   or a provider or router that resolves to `unknown`, name it in the conversation. Include the
   provider, residency jurisdiction, sovereignty bloc, and provenance bloc when a model ID is
   involved. Let the human decide whether to proceed.
5. **Record every accepted flow.** Add an inline waiver using the file's comment syntax and a
   genuine justification: `# borderlint: allow <justification>` or
   `// borderlint: allow <justification>`. borderlint ignores waivers without a justification.
   Waivers cannot override provider or model denies.
6. **Keep the enforcement checks in place.** The pre-commit hook runs its configured scan. The CI
   AI data-flow software bill of materials (SBOM) `diff` check exits 1 when the current SBOM adds a
   non-`local` provider/jurisdiction pair, including `unknown`, that is absent from the baseline.
   It does not fail for every new endpoint or model. Discuss the flow when you make the decision,
   not after the build fails.
