# agent-integrations Specification

## Purpose
TBD - created by archiving change add-agent-integrations. Update Purpose after archive.
## Requirements
### Requirement: Agent snippets instruct a pre-addition scan
The project SHALL ship integration snippets for AI coding agents (at minimum Claude Code and
Cursor) that instruct the agent to run a borderlint scan before introducing any AI SDK import,
endpoint reference, or model identifier — using the project's policy when one exists and
inventory mode otherwise — and to surface any resulting new non-`local` flow in the conversation
before it is committed.

#### Scenario: Claude Code snippet content
- **WHEN** the Claude Code rules fragment is installed in a project
- **THEN** it instructs the agent to run a borderlint scan — against the project policy when one exists, inventory mode otherwise — before adding an AI dependency or endpoint, and to report new non-local flows before committing

#### Scenario: Cursor snippet content
- **WHEN** the Cursor rules file is installed in a project
- **THEN** it instructs the agent with the same instruction content as the Claude Code fragment, adapted to the tool's format

### Requirement: Snippets reference the enforcement backstop
Each shipped snippet SHALL reference the SBOM `diff` gate as the enforcing backstop and the
inline waiver syntax as the recorded path for deliberately accepted flows, so agent behavior
degrades into enforcement rather than silence.

#### Scenario: Backstop referenced
- **WHEN** any shipped snippet is read
- **THEN** it names the SBOM diff gate and the inline waiver syntax with its justification requirement

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

