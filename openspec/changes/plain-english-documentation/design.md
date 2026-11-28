# Design: plain-english-documentation

## Context

The current documentation describes a mature feature set, but several sections grew by adding
qualifications to existing paragraphs. The README mixes a quick start, detailed reference material,
limitations, and project history. Repeated terms such as “gates,” “surfaces,” “seats,” “scaffold,”
“eval-set,” and “orthogonal axes” slow comprehension. Agent instructions must remain precise
because they direct future code changes.

The [Plain English Campaign guide](https://www.plainenglish.co.uk/how-to-write-in-plain-english.html)
provides the editorial baseline: short sentences, active verbs, reader-focused language, direct
instructions, familiar words, fewer nominalisations, and useful lists. It does not require shorter
or less accurate technical content.

## Goals / Non-Goals

**Goals:**

- Help a new reader install borderlint, run a first scan, understand the result, and enforce a
  policy without decoding project-specific shorthand.
- Make detailed capability, contribution, and agent-integration documentation easier to scan.
- Preserve every material command, distinction, limitation, citation, and safeguard.

**Non-Goals:**

- No behavior changes, new documentation site, prose-linting service, or historical rewrite.
- No mechanical word-count target, banned-word list without context, or removal of necessary
  technical and legal vocabulary.

## Decisions

- **D1 — Give each document a clear job.** Make the README task-focused: what borderlint does,
  quick start, the three separate checks, policy, CI, common features, output, limits, and KB
  maintenance. Keep detailed capability status and jurisdiction concepts in CAPABILITIES. Keep
  schemas and maintenance procedures in CONTRIBUTING. Link between documents instead of repeating
  long explanations. Alternative: only replace individual words; rejected because long sentences
  and duplicated detail would remain.

- **D2 — Edit for the reader, not by formula.** Address the reader as “you,” make borderlint the
  actor where useful, and use imperative verbs for instructions. Aim for one main idea per sentence
  and the guide's 15–20-word average without enforcing a score. Split dense paragraphs and use
  lists only when they clarify steps or choices. Retain existing British spelling. Ordered
  installation and contribution procedures use numbered steps.

- **D3 — Apply a finite terminology map.** Replace the following unclear forms in narrative prose;
  keep them only inside literal commands, field names, quoted output, or proper names:

  | Unclear form | Required plain wording |
  |---|---|
  | `gate`, `gates`, or `gating` as a verb | Say what fails or is blocked, and name the exit code where relevant |
  | `surface` or `surfaces` as a verb | `show`, `report`, or `link to`, as accurate |
  | `seat` or `seats` for a configured location | `home location` or `home locations` |
  | `scaffold` or `scaffolds` as a verb | `create` or `generate` |
  | `eval-set` | `policy` |
  | `orthogonal axes` | `separate checks` |
  | `allow-list walk` | Describe the choices `init` asks the user to make |
  | `adjudicate` in explanatory prose | `decide whether the law applies` |
  | `perform evaluation` | `evaluate` |

  Define residency, sovereignty, provenance, software bill of materials (SBOM), and Model Context
  Protocol (MCP) at first use in each document that introduces them. Alternative: globally
  substitute words; rejected because legal terms, field names, output text, and ordinary nouns such
  as “policy” or “classification” must retain their exact meaning.

- **D4 — Preserve behavior through an inspectable claims inventory.** Before editing, add a
  per-file preservation checklist under this decision in `design.md`. Each item must name the
  commands, defaults, exit codes, limitations, citations, or safeguards to retain and the source
  checked: `openspec/specs/`, CLI help, implementation, or tests. Task 4.1 marks each item verified
  and summarizes the result in the PR's existing Verification section; do not create another
  documentation file. Always preserve deny-by-default behavior, unknown handling, non-waivable
  denies, advisory legal references, static-analysis limits, non-gating export exit codes, and the
  agent scan/waiver/SBOM-diff instructions.

  #### Preservation checklist

  - [x] **README.md — rewrite needed.** Preserve the four-command quick start; inventory and policy
    exit codes; all nine output formats; deny-by-default, unknown, local, deny, and waiver rules;
    the three checks and their vocabularies; detection languages and limits; observability host
    mappings; agent safeguards; 142-provider count; legal references; v1.19.3 pins; and the
    provenance scheme limitation. Sources: current CLI help, `providers.json`, and the
    `cli-and-reporting`, `residency-policy`, `flow-detection`, `model-provenance`,
    `mcp-config-scanning`, `policy-init`, and `kb-freshness` specifications and tests.
  - [x] **CAPABILITIES.md — rewrite needed.** Preserve every A1–H1 ID and status, deferred work,
    jurisdiction aliases and exceptions, three-check semantics, legal citations, non-goals, and
    guiding principles. Sources: all current specifications and `providers.json`.
  - [x] **CONTRIBUTING.md — rewrite needed.** Preserve provider and profile schemas, required
    fields, custom-provider precedence, human review, per-fact citations, review dates, null
    handling, exemptions, and the rule that data practices and profiles never change verdicts.
    Sources: `kb-freshness`, `provider-data-practices`, `regulator-profiles`, and
    `jurisdiction-classification` specifications and the bundled JSON schemas.
  - [x] **backlog/README.md — minor rewrite needed.** Preserve directory roles, command names,
    Jira-key format, draft IDs, and frontmatter ownership. Sources: `workflow.yaml` and `AGENTS.md`.
  - [x] **integrations/claude-code.md — rewrite needed.** Preserve the full AI/MCP trigger scope,
    policy discovery, inventory fallback, pre-commit reporting, three-check details, justified
    waiver syntax, deny exceptions, and exact SBOM-diff behavior. Add explicit installation steps.
    Sources: `agent-integrations`, `flow-detection`, `residency-policy`, and `cli-and-reporting`.
  - [x] **integrations/cursor.mdc — rewrite needed.** Preserve frontmatter and the same trigger,
    scan, reporting, waiver, and SBOM-diff behavior as the Claude rules; retain the Cursor install
    path. Sources: `agent-integrations`, `flow-detection`, and `cli-and-reporting`.
  - [x] **integrations/claude-plugin/skills/borderlint-check/SKILL.md — rewrite needed.** Preserve
    YAML frontmatter, the full trigger scope, scan-first behavior, justified waivers, and the
    SBOM-diff backstop. Keep this as the only full skill body. Sources: `agent-integrations` and
    `plugin-packaging`.
  - [x] **integrations/claude-code-skill.md — minor rewrite needed.** Keep this as a pointer, not a
    second skill body; preserve the canonical path and both installation routes. Source:
    `plugin-packaging`.
  - [x] **pyproject.toml — reviewed; no edit needed.** The short description is direct; preserve
    version 1.19.3, package metadata, dependencies, and build configuration. Source: package file.
  - [x] **action.yml — reviewed; no edit needed.** Input descriptions are clear; preserve all
    inputs, defaults, release behavior, and the composite steps. Sources: action file and CLI help.
  - [x] **.pre-commit-hooks.yaml — reviewed; no edit needed.** Preserve the hook entry point,
    directory-level scan, serial execution, and filename behavior. Source: `ci-integration`.
  - [x] **.claude-plugin/marketplace.json — simplify descriptions only.** Preserve the marketplace
    and plugin names, source, owner, keywords, category, and links. Source: `plugin-packaging`.
  - [x] **integrations/claude-plugin/.claude-plugin/plugin.json — simplify description only.**
    Preserve name, version 1.0.0, author, homepage, and license. Source: `plugin-packaging`.
  - [x] **examples/ci/github-actions.yml — clarify the leading comment only.** Preserve v1.19.3,
    checkout v4, triggers, path, policy, and classification. Source: current CI example.
  - [x] **examples/ci/gitlab-ci.yml — clarify comments only.** Preserve the Python image, PyPI
    install, scan command, and merge-request/default-branch triggers. Source: `ci-integration`.
  - [x] **examples/ci/Jenkinsfile — clarify comments only.** Preserve the virtual environment,
    PyPI install, policy scan, and non-zero stage failure. Source: `ci-integration`.

- **D5 — Use an exact review inventory.** Review every file below; edit only unclear wording and
  record “no edit needed” in the claims checklist where applicable:
  - Main guides: `README.md`, `CAPABILITIES.md`, `CONTRIBUTING.md`, and `backlog/README.md`.
  - Integrations: `integrations/claude-code.md`, `integrations/claude-code-skill.md`,
    `integrations/claude-plugin/skills/borderlint-check/SKILL.md`, and `integrations/cursor.mdc`.
  - Descriptions and comments only: `pyproject.toml`, `action.yml`, `.pre-commit-hooks.yaml`,
    `.claude-plugin/marketplace.json`, `integrations/claude-plugin/.claude-plugin/plugin.json`,
    `examples/ci/github-actions.yml`, `examples/ci/gitlab-ci.yml`, and `examples/ci/Jenkinsfile`.

  Preserve YAML/JSON syntax, versions, schemas, and the single canonical Claude skill body. Exclude
  `openspec/changes/archive/`, historical backlog records, `templates/`, `AGENTS.md`, `CLAUDE.md`,
  `.claude/`, and current normative `openspec/specs/` files except for this change's delta.
  Alternative: rewrite every Markdown file; rejected because historical and machine-read contracts
  have different purposes.

- **D6 — Validate clarity and fidelity separately.** Search included narrative prose for every term
  in D3 and justify any literal occurrence. Check the README command order and first-use
  definitions, numbered procedures, and consistent terminology. Verify links, commands, examples,
  metadata, and required agent instructions. Run strict OpenSpec validation, the full test suite,
  package build, and `git diff --check`. Alternative: add an automated readability gate; rejected
  because readability formulas cannot judge technical accuracy or useful detail.

## Risks / Trade-offs

- [A shorter README could hide an important limit] → use the claims inventory and link to the full
  capability and contribution references.
- [Plain wording could blur a legal or technical distinction] → retain exact field values,
  citations, and explicit limits; use the current specifications as the factual baseline.
- [Rewriting three agent snippets could create divergent instructions] → compare them against the
  agent-integration contract and keep only the canonical full Claude skill body.
- [A broad edit could bury documentation changes in unrelated metadata churn] → edit metadata only
  when its current description has the same clarity problem, and keep versions and schemas intact.

## Migration Plan

This is a documentation-only change. Readers need no migration. Review by document group, then
review the complete diff for consistency. Revert individual documentation edits if a technical
claim becomes unclear or inaccurate; no data or deployed behavior is affected.

## Open Questions

None. Use the existing file set and documentation roles rather than adding a new guide.
