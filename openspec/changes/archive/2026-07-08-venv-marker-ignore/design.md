## Context

`scan()` filters `p.parts` against a hardcoded name set (`.git`, `node_modules`, `__pycache__`,
`.venv`, `venv`, `build`, `dist`, …). Names are convention, not contract: memorybox's
`.venv-cuda` walked straight past it. Python venvs have a reliable marker — `pyvenv.cfg` at the
env root (PEP 405); conda envs carry `conda-meta/`.

## Goals / Non-Goals

**Goals:** any environment directory is excluded regardless of its name; the exclusion contract
is spec'd; zero cost when no envs exist.
**Non-Goals:** user-configurable excludes; gitignore semantics.

## Decisions

### D1 — Marker files over name patterns
**Decision:** The walk becomes a single-pass `os.walk` that detects markers per directory and
prunes environment subtrees in place — env contents are never traversed at all (the win on a
tree whose bulk *is* the env, like memorybox's 21GB `.venv-cuda`); `site-packages` joins the
name set for system/embedded layouts. `followlinks` stays off, matching the current
`rglob` behaviour of not descending symlinked venvs. Nox/tox per-session envs are covered for
free (each carries `pyvenv.cfg`). Pointing the scanner directly at a single file bypasses
marker collection, as today.
**Rationale:** PEP 405 guarantees `pyvenv.cfg` at every venv root; matching the artifact beats
guessing the christening. Name patterns (`venv*`, `.venv*`) would still miss `env-gpu/` and
would false-positive on legitimate source dirs named `venvtools/`.
**Alternatives rejected:**
- *Extend the name list (`.venv*`, `venv*`).* Rejected: chases conventions forever; the marker
  is the ground truth the interpreter itself uses.
- *A marker pre-pass with `rglob`.* Rejected: up to two extra full traversals, and the main
  walk still enumerates every env file only to filter it afterwards; pruning during one walk
  skips the subtree entirely.
- *Parse `.gitignore`.* Rejected: a scanner that trusts gitignore misses exactly the packaged
  envs people commit by accident — and adds a parser for a partial win.

## Risks / Trade-offs

- **[A repo that vendors an env on purpose]** Its dependency flows disappear from the scan. →
  Correct by design: the tool inventories the application's declarations; a vendored env's
  contents are the same noise class as node_modules, which has always been excluded.

## Migration Plan

1. Marker collection in `scan()` + `site-packages` in the name set; tests. Rollback: revert.

## Open Questions

None.
