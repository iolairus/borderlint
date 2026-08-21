# Tasks: regulator-policy-profiles

## 1. Profile data and loader

- [ ] 1.1 Create `borderlint/data/regulator_profiles.json` with the schema from design D2: per-profile seat(s), regulator name, citation `{url, retrieved}`, per-class default allow-lists, optional notes, ISO-8601 `reviewed` date, and a top-level ISO-8601 `updated` date so the file joins the drift staleness glob (D1, D2)
- [ ] 1.2 Add `load_regulator_profiles()` to `borderlint/kb.py`: validate jurisdiction tokens against the existing vocabulary, require citation + review date, fail loud naming the profile id (D2)
- [ ] 1.3 Add tests: complete profile loads; invalid token / missing citation / missing date each raise naming the id

## 2. Init integration

- [ ] 2.1 Add `--profile <id>` to the init subparser in `borderlint/cli.py`; unknown id exits non-zero listing available ids
- [ ] 2.2 Seed the interactive walk in `borderlint/init.py`: profile defaults appear as pre-affirmed keep choices per handled class; observed-but-unseeded jurisdictions still offered (D3)
- [ ] 2.3 Compose non-interactive mode: allow-list = profile ∪ observed ∪ home (D3)
- [ ] 2.4 Render provenance (regulator, citation, retrieval date) and the advisory disclaimer in wizard output when a profile is active; emit `_profile` metadata keys in the file (D4)
- [ ] 2.5 Warn on profile-seat/home mismatch instead of rejecting (D6)

## 3. Tests

- [ ] 3.1 Without `--profile`, wizard output and emitted policy are byte-identical to pre-profile behaviour
- [ ] 3.2 Seeded jurisdiction offered with keep-as-default and lands in the proposal unless dropped; observed unseeded jurisdiction still offered with drop-as-default
- [ ] 3.3 Non-interactive union composition test (`--home hk --classes customer-pii --profile hkma`)
- [ ] 3.4 Emitted file loads via `load_policy` and JSON keys match the unprofiled shape plus `_profile` metadata
- [ ] 3.5 Unknown profile id exits non-zero with available ids; mismatched seat warns but proceeds

## 4. Seed curation and docs

- [ ] 4.1 Curate the `hkma` and `mas` seed profiles from each regulator's current published AI guidance, recording URL + retrieval date and per-class defaults with a notes field explaining conservative choices (D5)
- [ ] 4.2 Document profiles in CONTRIBUTING.md (schema, human-curation rule, citation requirement) and mention `--profile` in README's init section

## 5. Validation

- [ ] 5.1 Run full pytest suite and fix regressions
- [ ] 5.2 Run `openspec validate regulator-policy-profiles --strict`
