# agent-integrations Specification (delta)

## MODIFIED Requirements

### Requirement: Documented installation
The README SHALL document how to install each shipped snippet in its target tool. For Claude
Code the documented primary path SHALL be the plugin marketplace install
(`/plugin marketplace add iolairus/borderlint`, then `/plugin install borderlint@borderlint`),
with manual placement of the canonical SKILL.md and the `claude-code.md` rules fragment
(appended to `CLAUDE.md`/`AGENTS.md`) retained as documented fallbacks for plugin-less setups;
for Cursor the documented path remains manual placement of the rules file.

#### Scenario: Installation documented
- **WHEN** a user reads the README's agentic-coding section
- **THEN** it states the plugin marketplace commands as the primary Claude Code install, the manual SKILL.md placement and the CLAUDE.md/AGENTS.md rules-fragment append as fallbacks, and where the Cursor rules file goes
