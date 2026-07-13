# add-agent-integrations — design

## Context

borderlint already gates after code exists (pre-commit, CI exit codes, SBOM diff). Agentic coding
moves the moment of decision earlier — into the agent conversation — and both major tools support
project-level instruction files (Claude Code: `CLAUDE.md`/`AGENTS.md` fragments and skills;
Cursor: `.cursor/rules/*.mdc`). This change is content-only: three small files plus README.

## Goals / Non-Goals

**Goals:**
- An agent with the snippet installed checks the border before adding an AI dependency and says
  so in the conversation, with the existing gates as backstop.

**Non-Goals:**
- MCP server (follow-up change if the snippets prove demand), hooks, wrappers, enforcement claims.

## Decisions

1. **Plain instruction files, one per tool, in `integrations/`** — copy-paste installation, no
   installer. *Alternative:* an `init`-style CLI installer — rejected: a code change and a
   maintenance surface for what is two files; *Alternative:* MCP server now — rejected: real
   build/maintenance cost before any evidence agents will use it (ponytail: snippets first).
2. **Same instruction text across tools**, adapted only to each tool's frontmatter/format, so
   behavior guidance can't drift between tools. Single source of wording: the Claude Code
   fragment; the Cursor file adapts its framing.
3. **Snippets instruct, gates enforce.** The text explicitly tells the agent the SBOM diff will
   catch what it misses and to use the inline waiver (with justification) for accepted flows —
   degradation path is enforcement, not silence.

## Risks / Trade-offs

- [Agents may ignore instructions] → accepted: advisory by design; the gates remain; snippet
  wording is imperative and scoped to a concrete trigger (adding AI deps/endpoints/model ids).
- [Tool rule formats change] → files are tiny; kb-refresh cadence of the repo suffices.

## Open Questions

None.
