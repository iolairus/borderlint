## 1. Scanner

- [ ] 1.1 Single-pass `os.walk` in `scan()` pruning env subtrees at their marker (`pyvenv.cfg` file / `conda-meta` dir); `site-packages` joins the name set; single-file scans bypass marker logic (D1, "Exclude non-source locations")

## 2. Tests

- [ ] 2.1 Temp tree: `.venv-cuda/pyvenv.cfg` + site-packages with an AI import → excluded; sibling app file → detected; `conda-meta` variant; bare `site-packages/` with no marker → excluded

## 3. Validation

- [ ] 3.1 Full suite + `openspec validate venv-marker-ignore --strict`; direct (unstaged) memorybox scan shows no venv noise
