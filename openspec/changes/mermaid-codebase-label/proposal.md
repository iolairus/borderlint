## Why

The Mermaid flow map roots every diagram at a generic `Your application` node. The 10-repo sweep made
the cost obvious: ten exported maps that can't be told apart at a glance. Label the root node with the
**scanned codebase's name and version** where they can be determined, so each map self-identifies
(`langchain@0.3.27`, `borderlint@v0.9.2`).

## What Changes

- The Mermaid **root (application) node** is labelled with the codebase's name and version, derived from
  a project manifest (`pyproject.toml` `[project]`, or `package.json`) at the scan root, or a **git tag**.
- Falls back to the scan **directory name**, then to the generic `Your application` when nothing is
  determinable.
- Only the Mermaid root node changes — other formats, the rest of the map, and SBOM determinism are
  untouched. The label is escaped via `_mlabel` like any other.

## Capabilities

### Modified Capabilities
- `cli-and-reporting`: the Mermaid root node identifies the scanned codebase.

## Impact

- A `project_label(root)` helper (manifest read + best-effort `git describe`) and an optional `root`
  argument on `report.mermaid()`; the CLI passes the scan path. Stdlib only (`json`, `tomllib` or a
  regex fallback, `subprocess`) — no new dependency.

## Non-goals

- Naming nodes other than the root.
- Deep monorepo resolution (per-package manifests) — root manifest or directory name only.
- Fetching tags over the network — the git tag is read from the local repo, best-effort, and is absent
  for shallow clones.
