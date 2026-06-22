## Context

borderlint is a pip-installable CLI (`borderlint scan`) with a console entry point. It already
ships a GitHub composite action. Two P2 adoptability items remain: a pre-commit hook (E4) and a
documented contribution path for the provider KB (F4). Both are thin wrappers/docs over existing
behaviour — no change to the scanner, classifier, policy engine, or KB loader.

## Goals / Non-Goals

**Goals:**
- A `.pre-commit-hooks.yaml` that consumers reference from their `.pre-commit-config.yaml` to run
  `borderlint scan` as a commit gate.
- A `CONTRIBUTING.md` that documents the KB entry schema and the human-assigned-jurisdiction PR flow.

**Non-Goals:**
- New CLI flags or a per-file scan mode.
- Auto-merging KB contributions; CycloneDX/SPDX; GitLab recipes; LLM enrichment.

## Decisions

- **`language: python` hook.** pre-commit installs borderlint into its own managed virtualenv from
  this repo, so the hook needs no separate packaging. Alternative — `language: system` (assume
  borderlint is on PATH) — rejected: forces every consumer to pre-install it and breaks the
  zero-setup promise. Alternative — a Docker hook — rejected as heavyweight for a stdlib CLI.
- **`pass_filenames: false`, `entry: borderlint scan`.** borderlint resolves flows at directory
  granularity and de-duplicates across files; feeding pre-commit's staged-file list would fragment
  detection and break de-dup. So the hook scans the repo root (the `scan` default) and ignores the
  staged list. Consumers append `args: [--policy, …, --classification, …]` in their config.
- **`require_serial: true`.** A single scan over the tree; no benefit to parallel invocation.
- **F4 is docs-only.** The KB schema is already enforced by `kb.load_kb`/`_endpoints_provider`;
  CONTRIBUTING.md documents that contract rather than adding validation. The drift check
  (`scripts/kb_drift.py`) already surfaces gaps; the guide ties the two together.

## Risks / Trade-offs

- [A consumer expects the hook to scan only staged files] → README snippet and the hook
  `description` state it scans the configured path; this matches CI behaviour, which is the point.
- [Hook needs policy/classification args to gate meaningfully; with none it runs inventory mode and
  always passes] → document the required `args:` in the README example so the gate is real.
- [`language: python` rebuilds the env on borderlint version bumps] → acceptable; standard
  pre-commit behaviour, amortised by its cache.

## Migration Plan

Additive only. New files (`.pre-commit-hooks.yaml`, `CONTRIBUTING.md`) and doc edits; nothing to
roll back beyond deleting them. No version bump required for behaviour, but ships in the next release.
