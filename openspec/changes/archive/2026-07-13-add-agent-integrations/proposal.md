# add-agent-integrations

## Why

An increasing share of AI SDK imports and endpoint references are written not by a developer but by an AI coding agent solving the task in front of it — the fastest-growing source of unreviewed AI egress in a codebase. The existing gates (pre-commit, CI, SBOM diff) catch a bad flow after it is written; an agent that checks the border *before* adding the dependency catches it where the decision is actually made, in the conversation.

## What Changes

- New `integrations/` directory with copy-paste snippets that instruct AI coding agents to run borderlint before introducing AI dependencies:
  - **Claude Code**: a `CLAUDE.md` / `AGENTS.md` rules fragment, plus an optional skill file, telling the agent to run `borderlint scan` (against the project policy when one exists, inventory mode otherwise) before adding any AI SDK import, endpoint reference, or model id — and to surface any new non-`local` flow in the conversation before committing.
  - **Cursor**: an equivalent `.cursor/rules` `.mdc` file.
- Each snippet also points the agent at the SBOM `diff` gate as the enforcement backstop and at the inline-waiver syntax so a deliberately accepted flow is recorded, not hidden.
- README gains an "Agentic coding" section documenting installation for both tools (copy the fragment / drop in the rules file).

## Capabilities

### New Capabilities

- `agent-integrations`: the shipped agent-integration snippets — what they must instruct an agent to do and how they are installed.

### Modified Capabilities

(none — no CLI, KB, or policy behavior changes)

## Impact

- New: `integrations/claude-code.md`, `integrations/claude-code-skill.md`, `integrations/cursor.mdc`; README section.
- No runtime impact: the shipped package, CLI, and existing gates are untouched; snippets only invoke the existing `scan` and `diff` commands.
- No new dependencies.

## Non-goals

- **No MCP server** — a stdlib MCP stdio server is a possible follow-up change once the snippets prove demand; explicitly out of scope here.
- Unrelated to CAPABILITIES.md A7 ("detect MCP servers / agent tool endpoints by jurisdiction"), which is about *detecting* MCP usage in scanned code, not integrating borderlint into agents.
- No agent-specific automation beyond rules/skill files (no hooks, no wrappers, no per-agent packages).
- No claim of enforcement: snippets are advisory guidance to the agent; pre-commit, CI, and the SBOM diff remain the gates.
