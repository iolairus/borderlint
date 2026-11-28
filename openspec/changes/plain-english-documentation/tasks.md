# Tasks: plain-english-documentation

## 1. Establish the documentation baseline

- [x] 1.1 Review the four main guides for the D3 terminology, structure, and duplication checks;
      record files or sections that need no edit (design D1–D3, D5; specs: direct language, reader tasks)
- [x] 1.2 Review the four integration files for the same checks and record any file that needs no
      edit (design D3, D5; specs: direct language, reader tasks)
- [x] 1.3 Review the eight metadata and CI example files for unclear descriptions or comments;
      record files that need no edit (design D3, D5; specs: direct language, consistent terminology)
- [x] 1.4 Add the README and CAPABILITIES preservation checklists to design D4, citing current
      specifications, CLI help, implementation, or tests for each material claim (design D4)
- [x] 1.5 Add the CONTRIBUTING and backlog README preservation checklists to design D4, including
      curation rules and workflow semantics (design D4)
- [x] 1.6 Add the integration preservation checklists to design D4, including installation,
      pre-addition scan, waiver, SBOM-diff, frontmatter, and single-source requirements (design D4)
- [x] 1.7 Add the metadata and CI example preservation checklists to design D4, including versions,
      schemas, installation sources, commands, and non-zero policy-scan behavior (design D4)

## 2. Rewrite the main guides

- [x] 2.1 Rewrite the README introduction, quick start, and three-check explanation; establish the
      required command order and first-use definitions (design D1–D4; specs: all)
- [x] 2.2 Rewrite the README policy and CI sections, preserving allow-list, unknown, deny, waiver,
      exit-code, and installation behavior (design D1–D4; specs: all)
- [x] 2.3 Rewrite the README MCP, agent-integration, and observability sections, preserving every
      detection and static-analysis limit (design D1–D4; specs: all)
- [x] 2.4 Rewrite the README output-format and internal-endpoint sections, preserving export exit
      codes, examples, and regional-endpoint behavior (design D1–D4; specs: all)
- [x] 2.5 Rewrite the README capability and scope sections, removing unnecessary repetition without
      losing supported features, limitations, or deferred work (design D1–D4; specs: all)
- [x] 2.6 Rewrite the README KB-maintenance, development, AI-assistance, and license sections while
      preserving review dates, commands, model attributions, and project conventions (design D1–D4)
- [x] 2.7 Clarify CAPABILITIES sections 1–4 while preserving jurisdiction, sovereignty, provenance,
      policy, and legal semantics (design D1–D4; specs: direct language, preserved meaning)
- [x] 2.8 Clarify CAPABILITIES sections 5–9 while preserving every capability ID, status, deferred
      item, non-goal, and guiding principle (design D1–D4; specs: direct language, preserved meaning)
- [x] 2.9 Rewrite CONTRIBUTING provider setup, schema, jurisdiction, and drift-check guidance with
      direct numbered steps (design D1–D4; specs: all)
- [x] 2.10 Rewrite CONTRIBUTING data-practice and regulator-profile guidance, preserving every
      citation, review-date, curation, and advisory-use rule (design D1–D4; specs: all)
- [x] 2.11 Rewrite CONTRIBUTING custom-provider and other-contribution guidance and clarify
      `backlog/README.md`, preserving override and workflow semantics (design D1–D4; specs: all)

## 3. Clarify integrations and supporting descriptions

- [x] 3.1 Clarify `integrations/claude-code.md` and `integrations/cursor.mdc` while preserving
      frontmatter, trigger scope, installation, waiver, and SBOM-diff instructions (design D3–D5)
- [x] 3.2 Clarify the canonical Claude plugin skill and legacy pointer while preserving frontmatter
      and the single canonical skill body (design D3–D5; spec: reader tasks)
- [x] 3.3 Clarify descriptions and comments in `pyproject.toml`, `action.yml`, and
      `.pre-commit-hooks.yaml` where the baseline found a problem; change no versions or behavior
      (design D5; specs: direct language, consistent terminology)
- [x] 3.4 Clarify marketplace and plugin JSON descriptions where needed; change no names, sources,
      versions, keywords, or schema fields (design D5; specs: direct language, preserved meaning)
- [x] 3.5 Clarify comments in the three CI example files where needed; change no release pins,
      installation commands, scan commands, triggers, or job behavior (design D5)

## 4. Review and verify

- [x] 4.1 Mark every design D4 preservation item verified against current behavior and record the
      per-file result for the PR Verification section; verify all internal links (design D4, D6)
- [x] 4.2 Search included narrative prose for every D3 term and justify literal occurrences; check
      README command order, first-use definitions, numbered procedures, and terminology consistency
      (design D2, D3, D6; specs: direct language, reader tasks)
- [x] 4.3 Verify documented commands and examples against CLI help and tests; parse edited JSON and
      YAML, compare agent snippets with their contracts, and confirm excluded files are unchanged
      (design D4–D6; spec: clarity edits preserve meaning)
- [x] 4.4 Run the full pytest suite, build the package, run `git diff --check`, and run
      `openspec validate plain-english-documentation --strict`; review the final diff for unintended
      behavior or metadata changes (design D6)
