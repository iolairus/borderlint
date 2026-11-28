<!-- borderlint agent rules — copy this section into your project's CLAUDE.md or AGENTS.md. -->

## AI data-flow checks (borderlint)

borderlint checks residency (where AI data goes), sovereignty (which government may compel the
provider to disclose it), and provenance (who developed the model weights).

1. **Install these rules.** Append this section to your project's `CLAUDE.md` or `AGENTS.md`.
2. **Check every AI change before making it.** This includes:
   - An AI SDK import, such as `openai`, `anthropic`, or `langchain`.
   - An AI endpoint or provider URL, including an OpenAI-compatible `base_url`.
   - A model identifier from Bedrock, Hugging Face, Ollama, or another provider.
   - An LLM endpoint in configuration or `.env`.
   - A Model Context Protocol (MCP) server under `mcpServers` (VS Code: `servers`) in `.mcp.json`,
     `claude_desktop_config.json`, `.cursor/mcp.json`, or `.vscode/mcp.json`, using either a remote
     `url` or stdio `command` and `args`.
3. **Run borderlint first.** If the project has a residency policy, find its path in the project or
   CI configuration and run:
   `borderlint scan . --policy <project-policy-path> --classification <the project's data class>`.
   Otherwise, run inventory mode: `borderlint scan .`.
4. **Report the change before committing.** If the addition introduces a flow whose jurisdiction is
   not `local`, or a provider or router that resolves to `unknown`, name it in the conversation.
   Include the provider, residency jurisdiction, sovereignty bloc, and provenance bloc when a model
   ID is involved. Let the human decide whether to proceed.
5. **Record every accepted flow.** Add an inline waiver on the finding's line using the file's
   comment syntax and a genuine justification: `# borderlint: allow <justification>` or
   `// borderlint: allow <justification>`. borderlint ignores waivers without a justification.
   Waivers cannot override provider or model denies.
6. **Keep the enforcement checks in place.** The pre-commit hook runs its configured scan. The CI
   AI data-flow software bill of materials (SBOM) `diff` check exits 1 when the current SBOM adds a
   non-`local` provider/jurisdiction pair, including `unknown`, that is absent from the baseline.
   It does not fail for every new endpoint or model. Discuss the flow when you make the decision,
   not after the build fails.
