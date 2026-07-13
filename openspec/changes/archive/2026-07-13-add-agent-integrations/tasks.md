# add-agent-integrations — tasks

## 1. Snippets

- [x] 1.1 `integrations/claude-code.md`: rules fragment (scan before adding AI SDK/endpoint/model id; policy if present else inventory; surface new non-`local` flows in conversation; SBOM diff backstop + waiver syntax) — spec: Agent snippets instruct a pre-addition scan, Snippets reference the enforcement backstop
- [x] 1.2 `integrations/claude-code-skill.md`: optional skill-file variant of 1.1 with frontmatter — spec: Agent snippets instruct a pre-addition scan, Snippets reference the enforcement backstop
- [x] 1.3 `integrations/cursor.mdc`: Cursor rules file with same instruction content adapted to .mdc frontmatter — spec: Agent snippets instruct a pre-addition scan, Snippets reference the enforcement backstop; design decision 2

## 2. Docs

- [x] 2.1 README "Agentic coding" section: what the snippets do, where each file goes (CLAUDE.md/AGENTS.md fragment or .claude/skills for Claude Code; .cursor/rules for Cursor) — spec: Documented installation
- [x] 2.2 CAPABILITIES.md: add integration row for agent snippets under §E — repo precedent (doc-only)
