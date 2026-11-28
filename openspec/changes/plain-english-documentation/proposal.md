# Proposal: plain-english-documentation

## Why

The documentation is accurate but often hard to scan. Noun-to-verb conversions such as “gates,”
insider terms such as “eval-set,” and long, dense sentences make readers work to understand how to
install and use borderlint.

## What Changes

- Rewrite the README around the reader's tasks: install, scan, understand results, set a policy,
  and enforce it in CI.
- Clarify the capability and contribution guides, agent-integration instructions, and user-facing
  metadata and example comments.
- Follow Plain English Campaign guidance: use short sentences, active verbs, direct instructions,
  everyday words, and useful lists. Replace awkward noun-to-verb conversions and unnecessary
  nominalisations with direct wording.
- Keep commands, field names, output samples, citations, technical distinctions, legal limits, and
  integration safeguards accurate and complete.
- Add objective documentation checks for terminology, structure, and factual preservation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `documentation-accuracy`: current documentation must be easy to understand as well as accurate,
  with direct wording, clear instructions, and preserved technical and legal meaning.

## Impact

- Rewrite `README.md`, `CAPABILITIES.md`, `CONTRIBUTING.md`, and `backlog/README.md` as needed.
- Review `integrations/claude-code.md`, `integrations/claude-code-skill.md`,
  `integrations/claude-plugin/skills/borderlint-check/SKILL.md`, and `integrations/cursor.mdc`.
- Review descriptions and comments only in `pyproject.toml`, `action.yml`,
  `.pre-commit-hooks.yaml`, `.claude-plugin/marketplace.json`,
  `integrations/claude-plugin/.claude-plugin/plugin.json`, `examples/ci/github-actions.yml`,
  `examples/ci/gitlab-ci.yml`, and `examples/ci/Jenkinsfile`.
- No scanner, policy, knowledge-base, report, CLI, or integration behavior changes.

## Non-goals

- No product renaming, rebranding, or feature changes.
- No simplification that removes a material limitation, citation, safeguard, or legal distinction.
- No rewrite of historical OpenSpec changes, historical backlog records, templates, managed
  instruction blocks, or current normative specifications beyond this change's delta.
- No new prose-linting dependency or subjective readability score as a CI pass/fail target.
