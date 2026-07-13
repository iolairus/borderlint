<!-- borderlint agent rules — copy this section into your project's CLAUDE.md or AGENTS.md. -->

## AI data-flow governance (borderlint)

Before adding any AI SDK import, AI endpoint reference, or model identifier to this codebase
(an `openai`/`anthropic`/`langchain`-style package, a provider URL, a Bedrock/HF/Ollama model
id, an OpenAI-compatible `base_url`, an LLM endpoint in config or `.env`):

1. **Run the border check first.** If the project has a residency policy (look for
   `residency.json` or the policy path used in CI):
   `borderlint scan . --policy residency.json --classification <the project's data class>`
   Otherwise run inventory mode: `borderlint scan .`
2. **Surface what changed.** If the addition would introduce a flow whose jurisdiction is not
   `local` — or a provider/router that resolves to `unknown` — say so in the conversation
   BEFORE committing, naming the provider, its residency jurisdiction, its sovereignty bloc,
   and (if a model id is involved) its provenance bloc. Let the human decide.
3. **Record accepted flows, never hide them.** If the human accepts the flow, add an inline
   waiver with a real justification on the flagged line:
   `# borderlint: allow <reason>` — an unjustified waiver is ignored, and a waiver cannot
   override a provider or model deny.

The pre-commit hook and the CI SBOM `diff` gate (which fails any PR that adds a new
non-`local` flow) will catch anything missed here — this rule exists so the flow is discussed
when the decision is made, not after the build breaks.
