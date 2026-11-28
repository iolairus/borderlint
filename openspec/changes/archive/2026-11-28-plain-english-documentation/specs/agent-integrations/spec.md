# agent-integrations Delta

## MODIFIED Requirements

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
