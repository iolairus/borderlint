## Summary

Bumps borderlint to **v1.2.0** and elevates the sovereignty dimension (shipped in #34) into the README's initial description, policy example, and capabilities list — presenting it as a first-class concept alongside residency rather than a sub-note.

## What changes

- **README opening** — now describes borderlint as governing both *residency* (where the bytes rest) and *sovereignty* (who can compel disclosure), with the Bedrock `ap-east-1` example front and centre.
- **Policy section** — the example `residency.json` now includes the `sovereignty` block inline; the residency and sovereignty explanations sit side by side.
- **Capabilities list** — a new **Sovereignty** bullet alongside the Jurisdictions bullet.
- **Version bump** — `1.1.4` → `1.2.0` in `pyproject.toml` and `__init__.py`; description updated.

## Validation

- `pytest` — 96 passed ✓
- `borderlint --version` reports `1.2.0` ✓
