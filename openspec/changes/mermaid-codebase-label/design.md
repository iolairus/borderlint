## Context

`report.mermaid()` hardcodes the root node as `Your application`. The CLI knows the scan path and
already does filesystem I/O (loading the policy, the KB). So the label is computed in a
`project_label(root)` helper the CLI calls, and `mermaid()` receives a plain string — the renderer
stays pure. Other formats already self-identify (the SBOM envelope carries borderlint version + KB date).

## Goals / Non-Goals

**Goals:** root node shows `<name>@<version>` when determinable; graceful, never-failing fallback;
`mermaid()` stays pure. **Non-Goals:** non-root nodes; monorepo per-package manifests; network tag lookup.

## Decisions

- **`mermaid()` stays pure; I/O lives in `project_label(root)`, invoked by the CLI.** The renderer takes
  `app_label="Your application"`. This preserves the renderer-purity pattern and keeps the filesystem/git
  reads in the same layer that already loads the policy and KB.
- **Resolution.** `name` = manifest name (PEP 621 `pyproject.toml` `[project].name` → `package.json`
  `.name`) → scan-directory basename. `version` = git tag (`git describe --tags --abbrev=0`) → the
  version from **the same manifest that supplied the name** (avoids mixing a pyproject name with a
  package.json version). Label = `f"{name}@{version}"`, or `name`, or `Your application`.
- **Only PEP 621 `[project]` is read.** A poetry project (`[tool.poetry]`, no `[project]`) and no
  `package.json` falls through to the directory name — a decided behaviour, not a bug.
- **Git is best-effort.** stdlib `subprocess`, ~2 s timeout, no network; any failure (git absent, not a
  repo, no tags — the common case for `--depth 1` clones) is swallowed and the scan never fails. The
  git-tag *scenario* is hedged on "git is available"; its test skips when `git` is not on PATH.
- **Single-line, escaped.** A manifest string can contain a newline or quote; `project_label` collapses
  whitespace to a single line and the label routes through `_mlabel` (`#`→`#35;`, `"`→`#quot;`) — the
  same escape the flow map already relies on.
- **pyproject parsed with `tomllib` when importable (3.11+), else a minimal `[project]` regex** —
  `requires-python >=3.10`, so the fallback keeps it zero-dep on 3.10.

## Risks / Trade-offs

- The generic `Your application` label now only fires when no name resolves at all (no manifest name and
  no directory basename — effectively a programmatic call without a root); a real scan always has a
  directory name. Acceptable — the generic stays as a backstop.
- git tag may differ from the manifest version (tag preferred as the released ref) — both identify the
  codebase; acceptable.
