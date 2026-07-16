## Context

The borderlint-check skill exists as `integrations/claude-code-skill.md` — already valid Agent
Skills format (YAML frontmatter with `name`/`description` + markdown body) — but installation is
manual copy-paste. Claude Code plugin marketplaces are git repos with a
`.claude-plugin/marketplace.json` manifest; a plugin is a directory with
`.claude-plugin/plugin.json` and a `skills/` folder. A marketplace manifest may reference plugins
by relative path inside the same repo, so no dedicated repo is needed. Anthropic's community
marketplace accepts submissions that pass `claude plugin validate` plus automated safety checks.

## Goals / Non-Goals

**Goals:**
- One-command install of the borderlint-check skill from the existing repo.
- Single canonical copy of the skill content.
- CI catches a malformed manifest or a dangling path before users hit it.
- Ready to submit to `anthropics/claude-plugins-community` unmodified.

**Non-Goals:**
- Marketplace surfaces beyond one skill (no commands, hooks, MCP servers).
- Version pinning or release automation for the plugin manifest.
- Packaging for non-Claude platforms.

## Decisions

**D1 — Plugin lives at `integrations/claude-plugin/`, referenced by relative path.**
The marketplace manifest at the repo root points to `./integrations/claude-plugin`. Keeps all
agent-integration assets under `integrations/` where the spec already anchors them.
*Alternative rejected:* a separate `iolairus/borderlint-plugin` repo — a second repo to version,
and it decouples the skill from the codebase it documents; the same-repo mechanism exists
precisely to avoid this.

**D2 — The plugin's `SKILL.md` is canonical; `integrations/claude-code-skill.md` becomes a
pointer.** The skill content moves (not copies) to
`integrations/claude-plugin/skills/borderlint-check/SKILL.md`. The old path keeps a short stub
telling manual installers where the file now lives, preserving inbound links (the file is
referenced from the shipped v1.8.0 README and Post 3).
*Alternative rejected:* two synced copies — the KB drift lesson applies; two hand-maintained
copies of agent instructions will diverge.
*Alternative rejected:* deleting the old path — breaks published links for a one-line stub's
worth of savings.

**D3 — Manifest validation is a pytest test using stdlib `json`, not `claude plugin validate`
in CI.** The test asserts: both manifests parse; `marketplace.json` has `name`, `owner`,
`plugins[]` with `name` + `source`; the relative source path exists; `plugin.json` has `name`;
the skill file exists with `name:` and `description:` frontmatter. Runs in the existing suite
with zero new dependencies.
*Alternative rejected:* installing the Claude Code CLI in CI for `claude plugin validate` — a
heavyweight npm dependency in a zero-dep Python repo to check two small JSON files. Run it
manually before the community-marketplace submission instead.

**D4 — `plugin.json` omits `version`.** Optional field; omitting it avoids adding a fifth
version pin to the release checklist. The community marketplace pins submissions to a commit
SHA, so consumers get reproducibility from the catalog, not from the manifest.
*Alternative rejected:* syncing version with `pyproject.toml` — recurring release friction for
no consumer benefit.

**D5 — Marketplace name `borderlint`, plugin name `borderlint`.** Install reads
`/plugin install borderlint@borderlint`. Slightly redundant, but both names are user-facing and
anything else (`borderlint-skill@borderlint-marketplace`) is longer without being clearer.

## Risks / Trade-offs

- [Manifest schema drifts as the plugin spec evolves] → the pytest checks only documented-stable
  required fields; run `claude plugin validate` manually before submission to catch the rest.
- [Community-marketplace submission is rejected] → the self-hosted marketplace still works; the
  submission is a follow-up task, not a merge gate.
- [Stub file confuses readers expecting the full skill] → stub is two lines: what moved, where
  to find it, and the install command.

## Migration Plan

Additive files plus one content move; no rollback complexity. If the plugin mechanism
misbehaves, deleting `.claude-plugin/` and restoring the skill body to the old path reverts
fully.

## Open Questions

None.
