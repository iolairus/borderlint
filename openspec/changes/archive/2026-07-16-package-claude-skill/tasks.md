## 1. Plugin structure

- [x] 1.1 Create `integrations/claude-plugin/.claude-plugin/plugin.json` (name `borderlint`, description; no version — design D4)
- [x] 1.2 Move the skill body from `integrations/claude-code-skill.md` to `integrations/claude-plugin/skills/borderlint-check/SKILL.md`, dropping the copy-this-file line, keeping frontmatter, the scan/surface/waiver instructions, and the Backstop paragraph (SBOM diff gate) intact
- [x] 1.3 Replace `integrations/claude-code-skill.md` with a two-line pointer stub: canonical path + plugin install command (design D2)
- [x] 1.4 Create `.claude-plugin/marketplace.json` at the repo root (marketplace `borderlint`, owner, one plugin entry sourced `./integrations/claude-plugin`) — design D1/D5

## 2. Validation

- [x] 2.1 Add a manifest-validation test to `tests/test_borderlint.py`: both manifests parse, required fields present, plugin source path and SKILL.md exist, frontmatter has `name`/`description` (design D3; plugin-packaging "Manifest validity is enforced by the test suite")
- [x] 2.2 Run the full test suite green

## 3. Documentation

- [x] 3.1 Update the README agentic-coding section: plugin marketplace commands as the primary Claude Code install, manual SKILL.md placement and CLAUDE.md/AGENTS.md rules-fragment append as fallbacks, Cursor unchanged (agent-integrations "Documented installation")

## 4. Plugin validation

- [x] 4.1 Run `claude plugin validate` locally against the repo and fix anything it flags (design D3 mitigation)

<!-- Post-merge follow-up (not an implementation task): submit the plugin at
platform.claude.com/plugins/submit for the anthropics/claude-plugins-community catalog
— see proposal "What Changes", last bullet. -->
