<!-- borderlint agent rules — copy this section into your project's CLAUDE.md or AGENTS.md. -->

## AI data-flow governance (borderlint)

Before adding any AI SDK import, AI endpoint reference, model identifier, or structured MCP server
configuration to this codebase (an `openai`/`anthropic`/`langchain`-style package, a provider URL,
a Bedrock/HF/Ollama model id, an OpenAI-compatible `base_url`, an LLM endpoint in config or `.env`,
or an MCP server under `mcpServers` (VS Code: `servers`) in `.mcp.json`,
`claude_desktop_config.json`, `.cursor/mcp.json`, or `.vscode/mcp.json`, using a remote `url` or
stdio `command` and `args`):

1. **Run the border check first.** If the project has a residency policy, discover its path from
   the project or CI and substitute it for `<project-policy-path>`:
   `borderlint scan . --policy <project-policy-path> --classification <the project's data class>`
   Otherwise run inventory mode: `borderlint scan .`
2. **Surface what changed.** If the addition would introduce a flow whose jurisdiction is not
   `local` — or a provider/router that resolves to `unknown` — say so in the conversation
   BEFORE committing, naming the provider, its residency jurisdiction, its sovereignty bloc,
   and (if a model id is involved) its provenance bloc. Let the human decide.
3. **Record accepted flows, never hide them.** If the human accepts the flow, add an inline
   waiver on the flagged line using the file's comment syntax and a required, real justification:
   `# borderlint: allow <justification>` or `// borderlint: allow <justification>`.
   An unjustified waiver is ignored, and a waiver cannot override a provider or model deny.

As backstops, the pre-commit hook enforces its configured scan, and the CI SBOM `diff` gate fails
when the current SBOM adds a non-`local` provider/jurisdiction pair (including `unknown`) absent
from the baseline — not for every new endpoint or model. This rule exists so the flow is discussed
when the decision is made, not after the build breaks.
