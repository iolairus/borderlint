# Design: documentation-capability-sync

## Context

The repository has several documentation surfaces with different purposes: README and
CAPABILITIES describe the product, CONTRIBUTING describes maintenance, integration files guide
coding agents, and `examples/ci/` contains copyable consumer configuration. They have changed at
different times. The current specifications, implementation, tests, CLI help, and v1.19.0 package
metadata provide the verification baseline.

## Decisions

- **D1 — Use current behavior as the reference.** Reconcile claims with `openspec/specs/`, the
  CLI's actual arguments and formats, implementation where needed, and package version 1.19.0.
  Do not treat old README wording or archived proposals as authoritative. Where a synced spec's
  prose contradicts longstanding validation behavior, correct it through this change's delta:
  provenance excludes `vn` as well as `local`, while sovereignty includes both `vn` and `local`.
- **D2 — Review independent documentation surfaces in parallel, apply edits centrally.** Review
  README/CAPABILITIES, contributor/project guides, agent integrations, and CI/package examples as
  separate read-only scopes. Consolidate recommendations before editing to avoid duplicated or
  contradictory wording.
- **D3 — Limit edits to current consumer and maintainer documentation.** Include root product and
  contributor guides, `integrations/`, plugin metadata/documentation, and copyable examples.
  Exclude `openspec/changes/archive/`, `backlog/`, templates, and managed instruction blocks.
  Current OpenSpec specifications are review references, not wholesale documentation rewrite
  targets.
- **D4 — Prefer durable instructions, pin only actual release references.** CI action and source
  installation examples should use v1.19.0 where a release tag is required. PyPI instructions
  should use the published package without obsolete private-repository token guidance. General
  feature descriptions should avoid unnecessary version numbers.
- **D5 — Make minimal corrections without expanding scope.** Fix inaccurate, incomplete, or
  misleading capability statements and examples. Do not rewrite the documentation structure,
  rebrand the product, or add new reference material unrelated to current behavior.

## Risks / Trade-offs

- [A broad review could turn into a wholesale rewrite] → require each edit to correct a concrete
  mismatch with a current specification, command, or release fact.
- [Documentation examples can drift again at the next release] → avoid version numbers unless a
  tag or release pin is intrinsic to the example; existing release steps update the remaining
  references.
- [Agent instructions describe desired behavior rather than CLI features] → verify both their
  installation guidance and their references to the existing SBOM-diff and waiver backstops.

## Migration Plan

Documentation-only edits are additive or corrective and require no consumer migration. Validation
includes the full test suite, strict OpenSpec validation, CLI/help comparisons, and checks for
stale status and release references identified during review.
