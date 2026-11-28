# agent-integrations Specification

## Purpose
TBD - created by archiving change add-agent-integrations. Update Purpose after archive.
## Requirements
### Requirement: Agent snippets instruct a pre-addition scan

The project SHALL ship integration snippets for AI coding agents (at minimum Claude Code and
Cursor) that instruct the agent to run a baseline borderlint scan before introducing any AI SDK
import, endpoint reference, or model identifier — using the project's policy when one exists and
inventory mode otherwise. The snippets SHALL also instruct the agent to scan again after making
the proposed change and before committing, and to report any resulting new non-`local` or
`unknown` flow in the conversation.

#### Scenario: Claude Code snippet content

- **WHEN** the Claude Code rules fragment is installed in a project
- **THEN** it instructs the agent to run a baseline scan against the project policy or in inventory
  mode, scan again after the AI change before committing, and report new non-local or unknown flows

#### Scenario: Cursor snippet content

- **WHEN** the Cursor rules file is installed in a project
- **THEN** it instructs the agent with the same baseline and post-edit scan content as the Claude
  Code fragment, adapted to the tool's format

### Requirement: Snippets reference the enforcement backstop

Each shipped snippet SHALL distinguish the pre-commit hook's configured policy scan from the
independent SBOM `diff` check. It SHALL explain that justified inline waivers apply to policy
findings, while SBOM `diff` exits 1 for every added non-`local` provider/jurisdiction pair without
consulting policy allow-lists or waivers. Accepting such a pair SHALL require review and update of
the SBOM baseline.

#### Scenario: Backstop referenced

- **WHEN** any shipped snippet is read
- **THEN** it names the configured pre-commit policy scan, the justified inline waiver syntax, the
  independent SBOM `diff` behavior, and baseline review and update as the acceptance path for an
  added non-`local` pair

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

