## Context

`report.mermaid()` hardcodes the root node as `Your application`. The CLI knows the scan path; passing
it lets the renderer derive a codebase label. Other formats already self-identify (the SBOM envelope
carries borderlint version + KB date), so this is Mermaid-only.

## Goals / Non-Goals

**Goals:** root node shows `<name>@<version>` when determinable; graceful fallback. **Non-Goals:**
non-root nodes; monorepo per-package manifests; network tag lookup.

## Decisions

- **Resolution order.** `name` = manifest name (`pyproject.toml` `[project].name` → `package.json`
  `.name`) → scan-directory basename. `version` = git tag (`git describe --tags --abbrev=0`) → manifest
  version. Label = `f"{name}@{version}"`, or just `name`, or `Your application` if no name resolves.
- **Git tag preferred over manifest version**, as the actual released ref; both identify the codebase.
- **Git is best-effort.** stdlib `subprocess`, 2 s timeout; any failure (git absent, not a repo, no
  tags — the common case for `--depth 1` clones) is swallowed and the scan never fails. `# ponytail:
  best-effort, never blocks the scan`.
- **pyproject parsed with `tomllib` when importable (3.11+), else a minimal `[project]` name/version
  regex** — `requires-python >=3.10`, so the fallback keeps it zero-dep on 3.10.
- **Mermaid-only; label escaped via `_mlabel`.** SBOM/JSON/SARIF/text and the SBOM determinism
  guarantee are untouched.

## Risks / Trade-offs

- A manifest without a name → falls back to the directory name; never errors.
- A `package.json` in a JS sub-tree but scanning a Python root, or vice versa → pyproject is tried
  first, then package.json; for a true monorepo with neither at root, the directory name is used.
