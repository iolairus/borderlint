# Proposal: plain-english-documentation

## Why

The documentation is accurate but often hard to scan. Noun-to-verb conversions such as “gates,”
insider terms such as “eval-set,” and long, dense sentences make readers work to understand how to
install and use borderlint. Independent review also found places where simplification blurred
provider overrides, policy activation, and the agent enforcement workflow.

## What Changes

- Rewrite the README around the reader's tasks: install, scan, understand results, set a policy,
  and enforce it in CI.
- Clarify the capability and contribution guides, agent-integration instructions, and user-facing
  metadata and example comments.
- Follow Plain English Campaign guidance: use short sentences, active verbs, direct instructions,
  everyday words, and useful lists. Replace awkward noun-to-verb conversions and unnecessary
  nominalisations with direct wording.
- Document AWS Bedrock China's sovereignty override and require an active-class allow-list before
  sovereignty or provenance allow-list and unknown-handling checks apply. Keep `deny_models`
  independent of that allow-list.
- Give agent snippets a coherent baseline-scan and post-edit-scan workflow. Distinguish policy
  enforcement from SBOM comparison, including how to accept a pair by updating the baseline.
- Correct the Jenkins example's instructions and add objective documentation checks for
  terminology, structure, and factual preservation.
- Keep commands, field names, output samples, citations, technical distinctions, legal limits, and
  integration safeguards accurate and complete.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `documentation-accuracy`: current documentation must be easy to understand as well as accurate,
  with direct wording, clear instructions, and preserved technical and legal meaning.
- `agent-integrations`: snippets must include both baseline and post-edit scans and accurately
  distinguish policy scans, waivers, and independent SBOM comparison.

## Impact

- Rewrite `README.md`, `CAPABILITIES.md`, `CONTRIBUTING.md`, and `backlog/README.md` as needed.
- Review `integrations/claude-code.md`, `integrations/claude-code-skill.md`,
  `integrations/claude-plugin/skills/borderlint-check/SKILL.md`, and `integrations/cursor.mdc`.
- Review descriptions and comments only in `pyproject.toml`, `action.yml`,
  `.pre-commit-hooks.yaml`, `.claude-plugin/marketplace.json`,
  `integrations/claude-plugin/.claude-plugin/plugin.json`, `examples/ci/github-actions.yml`,
  `examples/ci/gitlab-ci.yml`, and `examples/ci/Jenkinsfile`.
- No scanner, policy, knowledge-base, report, or CLI behavior changes. Agent snippets clarify when
  to run the existing commands.

## Non-goals

- No product renaming, rebranding, or product feature changes.
- No simplification that removes a material limitation, citation, safeguard, or legal distinction.
- No rewrite of historical OpenSpec changes, historical backlog records, templates, managed
  instruction blocks, or current normative specifications beyond this change's deltas.
- No new prose-linting dependency or subjective readability score as a CI pass/fail target.
