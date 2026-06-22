## 1. Pre-commit hook (E4)

- [x] 1.1 Add `.pre-commit-hooks.yaml` defining the `borderlint` hook: `entry: borderlint scan`,
      `language: python`, `pass_filenames: false`, `require_serial: true`, with name/description.
- [x] 1.2 Add a test asserting `.pre-commit-hooks.yaml` parses and the hook has the expected
      id/entry/`pass_filenames: false` (the spec's "scans the path, not the staged list" guarantee).
- [x] 1.3 Add a pre-commit usage snippet to README (a `repo:`/`rev:`/`hooks:` block with the
      required `args: [--policy, …, --classification, …]` so the gate is real).

## 2. Contribution workflow (F4)

- [x] 2.1 Write `CONTRIBUTING.md`: KB entry schema (each field, required vs. optional), the valid
      jurisdiction tokens (ccTLD/ISO + `CN-GBA`, `GBA`, `local`, `unknown`), and the add-a-provider
      PR flow; state jurisdictions are human-assigned, never auto-merged from the drift check.
- [x] 2.2 Cross-link: README "Keeping the KB fresh" and `CONTRIBUTING.md` reference each other.

## 3. Status & validation

- [x] 3.1 Flip E4 and F4 to ✅ in `CAPABILITIES.md`; remove the pre-commit item from README "Scope".
- [x] 3.2 `openspec validate precommit-and-contribution --strict` passes; full pytest suite green.
