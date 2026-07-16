## Why

The borderlint-check skill ships today as a copy-paste snippet in `integrations/`, which requires
users to find it, copy it, and keep it fresh by hand. Claude Code now resolves plugins from any
GitHub repo carrying a marketplace manifest, and Anthropic operates a central community
marketplace (`anthropics/claude-plugins-community`) surfaced in-product — a one-command install
and a central listing are the distribution channels the snippet is missing.

## What Changes

- The repo becomes a Claude Code plugin marketplace: `.claude-plugin/marketplace.json` at the
  repo root listing one plugin (`borderlint`) sourced from a plugin directory under
  `integrations/`.
- The plugin packages the existing borderlint-check skill (`.claude-plugin/plugin.json` +
  `skills/borderlint-check/SKILL.md`); users install with
  `/plugin marketplace add iolairus/borderlint` then `/plugin install borderlint@borderlint`.
- The skill content is single-sourced: the plugin's `SKILL.md` becomes the canonical file, and
  the manual-install path (`integrations/claude-code-skill.md`) is replaced by a pointer to it,
  eliminating drift between two copies.
- A test validates the manifests and skill frontmatter (JSON well-formed, required fields
  present, referenced paths exist) so CI catches a broken marketplace before users do.
- README documents the plugin install as the primary Claude Code path; manual copy (Claude Code
  without plugins, Cursor) remains documented.
- After merge and release: submit the plugin to the Anthropic community marketplace
  (platform.claude.com/plugins/submit) for central discovery.

## Capabilities

### New Capabilities
- `plugin-packaging`: the repository doubles as a Claude Code plugin marketplace exposing the
  borderlint-check skill as an installable plugin — manifest shape, plugin structure, skill
  single-sourcing, and manifest validation.

### Modified Capabilities
- `agent-integrations`: the Documented installation requirement changes — the README's
  agentic-coding section documents the plugin marketplace install as the primary Claude Code
  path, with manual snippet placement retained for Cursor and plugin-less setups.

## Impact

- New files: `.claude-plugin/marketplace.json`, `integrations/claude-plugin/.claude-plugin/plugin.json`,
  `integrations/claude-plugin/skills/borderlint-check/SKILL.md` (moved content).
- Changed: `integrations/claude-code-skill.md` (becomes a pointer), README agentic-coding
  section, `tests/test_borderlint.py` (manifest validation test).
- No runtime code changes, no new dependencies (stdlib `json` validation only), no effect on
  scan/diff/init behavior.

## Non-goals

- No listing on the curated `claude-plugins-official` marketplace (Anthropic-invite only).
- No Cursor or cross-platform marketplace packaging — the Agent Skills spec makes the SKILL.md
  portable, but other platforms' registries are out of scope.
- No plugin version automation or release-pin sync; the plugin manifest omits `version` to avoid
  a fifth release pin.
- No MCP server, hooks, or slash-command surfaces in the plugin — skill only.
