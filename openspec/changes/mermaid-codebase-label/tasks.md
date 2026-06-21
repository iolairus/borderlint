## 1. Codebase label

- [ ] 1.1 Add `project_label(root)` to `report.py`: name from `pyproject.toml` `[project]` / `package.json` (else the scan-directory basename); version from `git describe --tags --abbrev=0` (best-effort, `subprocess`, ~2 s timeout, all errors swallowed) else the manifest version; return `name@version`, or `name`, or `Your application` when no name resolves
- [ ] 1.2 Parse `pyproject.toml` with `tomllib` when importable, else a minimal `[project]` name/version regex (zero-dep on 3.10)
- [ ] 1.3 Add an optional `root` argument to `report.mermaid()`; label the application node `_mlabel(project_label(root))` when `root` is given, else `Your application`. The CLI passes the scan path

## 2. Tests

- [ ] 2.1 Tests: a temp dir with `package.json` (name+version) → `name@version`; a temp dir with `pyproject.toml` `[project]` → `name@version`; a temp git repo with a tag → the tag as the version; a bare dir (no manifest, no git) → the directory name; the Mermaid root node carries the label, escaped
