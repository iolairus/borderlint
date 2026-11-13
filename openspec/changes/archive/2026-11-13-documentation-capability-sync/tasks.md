# Tasks: documentation-capability-sync

## 1. Review current documentation

- [x] 1.1 Compare README and CAPABILITIES with current specifications, CLI help, and v1.19.0;
      record concrete mismatches, including G2 (design D1, D2; specs: all)
- [x] 1.2 Review CONTRIBUTING and current project/maintainer guides for stale capability,
      installation, output-format, and contribution guidance (design D2, D3)
- [x] 1.3 Review Claude Code, Cursor, and plugin documentation/metadata against the
      agent-integration specification and shipped files (spec: Agent integration documentation)
- [x] 1.4 Review CI and package examples for stale release, privacy, installation, and usage
      guidance (spec: Installation and CI examples)

## 2. Apply corrections

- [x] 2.1 Mark G2 shipped and correct any other capability status or feature-summary drift found
      by review (specs: Capability statuses, Product documentation)
- [x] 2.2 Apply minimal README and contributor/project-guide corrections with no runtime behavior
      changes (design D5; spec: Product documentation)
- [x] 2.3 Correct agent integration and plugin documentation while preserving required scan,
      SBOM-diff, and waiver instructions (spec: Agent integration documentation)
- [x] 2.4 Update CI/package examples to current public distribution and v1.19.0 release references
      where applicable (design D4; spec: Installation and CI examples)
- [x] 2.5 Correct the model-provenance vocabulary delta to exclude `vn` alongside `local`, matching
      existing validation without changing runtime behavior (design D1)

## 3. Validation

- [x] 3.1 Re-check documented commands and formats against CLI help and current specifications;
      check edited files for stale G2/E5 statuses and superseded release references (design D1)
- [x] 3.2 Run the full pytest suite and `git diff --check`; update documentation-focused tests if
      required by existing test coverage (design D5)
- [x] 3.3 Run `openspec validate documentation-capability-sync --strict` and review the final diff
      to confirm archives, backlog history, and managed instruction blocks are unchanged (design D3)
