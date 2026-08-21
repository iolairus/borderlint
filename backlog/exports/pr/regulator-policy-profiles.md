<!-- PR for /opsx change regulator-policy-profiles -->

## Summary

Turning a regulator's published AI guidance into an automated guardrail currently means reading
the PDF yourself and hand-translating its expectations into a `residency.json`. This change adds
bundled, cited regulator profiles that pre-seed the `init` wizard's allow-list walk from
published guidance: `borderlint init --profile hkma` (HKMA High-level Principles on Artificial
Intelligence) or `--profile mas` (MAS AI Model Risk Management information paper). Defaults are
conservative — onshore-only for personal-data classes; CN-GBA is pre-seeded for non-pii only,
under the GBA Standard Contract rationale. Provenance travels with the seed: the wizard prints
the regulator, guidance URL, retrieval date and an explicit not-legal-advice disclaimer, and the
emitted policy carries `_profile` metadata keys. Composition, not replacement: seeded
jurisdictions are offered keep-as-default in the interactive walk (droppable), and scripted mode
unions profile ∪ observed ∪ home. Without `--profile`, behaviour is byte-identical to before.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/regulator-policy-profiles/` |
| Spec deltas | ADDED `regulator-profiles` (5 requirements); ADDED `policy-init` (`Profile flag` requirement) |

## Changes

- `borderlint/data/regulator_profiles.json` (new): two seed profiles with seat(s), regulator
  name, `{url, retrieved}` citation, per-class default allow-lists, notes explaining the
  conservative choices, ISO-8601 `reviewed` per profile, and a top-level `updated` so the file
  joins the weekly drift staleness glob.
- `borderlint/kb.py`: `load_regulator_profiles()` with loud validation — seat well-formedness,
  citation completeness, ISO review date, jurisdiction-vocabulary check on every default token;
  errors always name the offending profile id.
- `borderlint/init.py`: profile resolution (unknown id exits non-zero listing available ids);
  seeded jurisdictions offered keep-as-default in the walk while observed unseeded ones keep
  drop-as-default; non-interactive union; provenance + disclaimer rendering to stderr; `_profile`
  metadata in the emitted policy (loader ignores unknown keys); seat/home mismatch warns but
  proceeds.
- `borderlint/cli.py`: `--profile <id>` on the init subparser.
- `tests/test_borderlint.py`: loader schema/rejection tests, unchanged-behaviour-without-flag
  test, verbatim prompt-semantics assertions, union composition, emitted-file loadability and
  key-shape diff, unknown-id rejection, mismatch warning.
- `CONTRIBUTING.md` / `README.md`: profile schema table, curation rules, `--profile` usage.

## Verification

- [x] `openspec validate regulator-policy-profiles --strict` passes
- [x] All tasks in tasks.md checked (14/14)
- [x] Tests covering each acceptance scenario (full suite: 182 passed)
- [x] Review pass closed four seams with live probes: real argparse wiring of `--profile`,
  drift-glob pickup of the new data file, zero network references in the runtime path,
  and droppable-seed behaviour (answering `n` to a seeded prompt excludes it from the policy)
