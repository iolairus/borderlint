## Why

Directory exclusion is name-based and unspecced: `.venv` and `venv` are skipped but `.venv-cuda`
is not, so scanning memorybox swept a virtualenv's site-packages and produced 397KB of
dependency findings (HuggingFace internals) drowning the app's own flows. Any nonstandard env
name (`.venv-cuda`, `venv310`, conda envs) has the same failure.

## What Changes

- Environment directories are excluded by **marker**, not name: a directory containing
  `pyvenv.cfg` (any Python venv regardless of name) or `conda-meta` (conda envs) is skipped as
  a subtree.
- `site-packages` joins the name-based exclusion list (dependency code is never the scanned
  application, wherever it sits).
- The existing exclusion requirement gains the marker rule and a faithful name enumeration
  (`.git`, `node_modules`, `__pycache__`, `.venv`, `venv`, `site-packages`, cache/build output).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `flow-detection`: the existing "Exclude non-source locations" requirement gains marker-based
  exclusion and the `site-packages` name.

## Impact

- `borderlint/detect.py` — pre-collect marker roots in `scan()`, skip files under them;
  `site-packages` in the ignore set.
- `tests/` — venv-with-nonstandard-name excluded; app code beside it still scanned.

## Non-goals

- No user-configurable exclude patterns (a future policy/CLI concern if evidence demands it).
- No gitignore parsing.
