## 1. Codebase label

- [ ] 1.1 Add `project_label(root)` to `report.py`: read name + version from the **same** manifest — a PEP 621 `pyproject.toml` `[project]` table (NOT `[tool.poetry]`) or a `package.json` at the scan root; name falls back to the scan-directory basename. Version = `git describe --tags --abbrev=0` (best-effort) else the manifest version. Collapse the result to a single line; return `name@version`, or `name`, or `Your application` when no name resolves
- [ ] 1.2 git tag lookup via `subprocess` (~2 s timeout); swallow every error (git absent, not a repo, no tag) — never raises, never touches the network. Parse `pyproject.toml` with `tomllib` when importable, else a minimal `[project]` name/version regex (zero-dep on 3.10)
- [ ] 1.3 `report.mermaid()` takes an optional `app_label` (default `Your application`), escaped via `_mlabel`; the **CLI** computes `project_label(a.path)` and passes it — so `mermaid()` stays a pure function of `(findings, kb, app_label)` and the I/O lives in the helper the CLI invokes

## 2. Tests

- [ ] 2.1 Tests (each in a temp dir): `package.json` name+version → `name@version`; `pyproject.toml` `[project]` → `name@version`; a manifest name with no version (and no git) → bare `name`; a bare dir (no manifest) → the directory name; a name containing `"`/`#`/newline → escaped and single-line. A git-tag test that `git init`s + commits (with `-c user.name`/`user.email`) + tags, asserting the tag is used — **skipped when `git` is not on PATH** so a git-less environment is not a failure