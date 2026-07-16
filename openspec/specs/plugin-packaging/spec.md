# plugin-packaging Specification

## Purpose
TBD - created by archiving change package-claude-skill. Update Purpose after archive.
## Requirements
### Requirement: Repository is an installable Claude Code plugin marketplace
The repository SHALL carry a `.claude-plugin/marketplace.json` manifest at its root declaring a
marketplace named `borderlint` whose plugin list contains a `borderlint` plugin sourced by
relative path from within the repository, in the manifest/layout contract Claude Code's plugin
loader consumes.

#### Scenario: Marketplace manifest shape
- **GIVEN** a checkout of the repository
- **WHEN** `.claude-plugin/marketplace.json` is parsed
- **THEN** it is valid JSON containing `name`, `owner`, and a `plugins` array with one entry named `borderlint` whose `source` is a relative path that exists in the repository

#### Scenario: Plugin manifest shape
- **GIVEN** the plugin directory referenced by the marketplace manifest
- **WHEN** its `.claude-plugin/plugin.json` is parsed
- **THEN** it is valid JSON whose `name` is `borderlint` and the plugin directory contains `skills/borderlint-check/SKILL.md`

### Requirement: Skill content is single-sourced in the plugin
The plugin's `skills/borderlint-check/SKILL.md` SHALL be the only full copy of the
borderlint-check skill in the repository; the previous manual-install path
(`integrations/claude-code-skill.md`) SHALL contain only a pointer to the canonical file and the
plugin install command. The pointer stub is a reference, not a shipped snippet; the canonical
SKILL.md carries the backstop reference required of shipped snippets.

#### Scenario: No duplicate skill body
- **GIVEN** the repository tree
- **WHEN** files containing the borderlint-check skill instructions are enumerated
- **THEN** exactly one file — the plugin's SKILL.md — contains the skill body, and the legacy path refers readers to it

#### Scenario: Skill frontmatter intact after the move
- **WHEN** the plugin's SKILL.md is read
- **THEN** its YAML frontmatter declares `name: borderlint-check` and a non-empty `description`, and the body retains the scan-first, surface-before-commit, and waiver instructions plus the backstop paragraph naming the SBOM diff gate

### Requirement: Manifest validity is enforced by the test suite
The test suite SHALL fail when either manifest is malformed JSON, a required manifest field is
missing, the plugin source path or skill file does not exist, or the skill frontmatter lacks
`name` or `description`.

#### Scenario: Broken manifest caught
- **GIVEN** a marketplace or plugin manifest with invalid JSON or a missing required field
- **WHEN** the test suite runs
- **THEN** a test fails identifying the manifest problem

#### Scenario: Dangling path caught
- **GIVEN** a manifest whose plugin source path or skill file reference does not exist on disk
- **WHEN** the test suite runs
- **THEN** a test fails identifying the missing path

