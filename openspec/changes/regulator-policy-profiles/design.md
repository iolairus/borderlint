# Design: regulator-policy-profiles

## Context

`borderlint init` interviews for a home base and data classes, runs a read-only inventory
scan, then walks observed jurisdictions per class to build a deny-by-default allow-list map.
The wizard's supported seats (`hk`, `mo`, `CN-GBA`, `jp`, `kr`, `sg`, `au`, `uk`, `eu`, `my`)
already align with the seats that have published AI guidance. Profiles are a new bundled-data
dimension over the same seat vocabulary, following the curation patterns of the other KBs.

## Goals / Non-Goals

**Goals:**

- One flag (`--profile hkma`) turns published regulator guidance into a pre-seeded policy walk.
- Provenance travels with the seed: citation + retrieval date in output and in the file.
- Composition, not replacement: profile ∪ observed jurisdictions; operator keeps final say.

**Non-Goals:**

- No legal analysis or sufficiency determination; no auto-updating from regulator sites.
- No profile coverage of every seat at seed time — one well-sourced profile beats five thin ones.
- No changes to detection, evaluation, or the emitted JSON shape.

## Decisions

### D1: Separate `regulator_profiles.json`, not fields on existing KBs
Profiles are advice-over-policy, not provider facts. A separate file keeps cadence and
curation independent and mirrors the `data_practices.json` precedent.
*Alternative rejected:* extending `providers.json` — wrong dimension entirely.

### D2: Defaults are allow-lists keyed by classification, validated against the jurisdiction vocabulary
Reuse makes profiles composable with the existing walk and loader; validation at load time
keeps bad tokens out of emitted policies (fail loud, naming the profile id).
*Alternative rejected:* free-form "expectations" text — not machine-usable as seeds.

### D3: Seed = pre-affirmed entries in the interactive walk; union in non-interactive mode
Interactive operators see seeded jurisdictions as keep/drop choices they can reverse;
scripted users get profile ∪ observed ∪ home. Both paths keep the operator's final say while
making the seed real.
*Alternative rejected:* prompt-per-seed ("add sg?") — doubles prompts for values the profile
already asserts.

### D4: Provenance as comments in the emitted JSON
JSON has no comment syntax, but the loader ignores unknown top-level keys only if they are
valid JSON — so provenance goes in as `_profile` metadata keys (leading underscore matches
the internal `_user` marker convention) rather than `//` lines, keeping the file strictly
loadable by any strict JSON parser.
*Alternative rejected:* `//`-style comments — breaks strict parsers; sidecar file — gets lost.

### D5: Two seed profiles (`hkma`, `mas`), schema open for more
HKMA's GenAI guidance anchors borderlint's GBA home turf; MAS's AI risk-management guidance
covers the second-strongest seat in the wizard's supported list. Both are financial-sector
regulators whose published expectations translate directly into conservative allow-list
defaults. EU-AI-Act and PDPO follow via PR once their defaults are sourced with citations.
*Alternative rejected:* shipping all four thinly-sourced together — weakens the curation moat.

### D6: Profile id → seat binding is advisory, not enforced
A profile records which seat(s) it targets, but `--profile hkma --home sg` is allowed with a
warning: operators may run entities across seats, and hard-binding would block legitimate use.
*Alternative rejected:* rejecting mismatched seat/home — brittle without a legal basis.

## Risks / Trade-offs

- [Guidance drifts after retrieval] → `reviewed` date + citation rendered everywhere; drift
  check gains a staleness section for profiles (same pattern as data practices).
- [Operators treat seeds as compliance answers] → mandatory disclaimer in wizard output;
  proposal and CONTRIBUTING framing state advisory status.
- [Defaults too conservative scare users] → every seed is droppable in the walk; notes field
  explains each deviation from open-by-default.

## Migration Plan

Purely additive: new data file, new flag, new render lines. Without `--profile`, behaviour is
byte-identical (spec'd). Rollback removes the flag and file; no policy migration needed.

## Open Questions

- Exact HKMA default allow-lists per class (resolved during implementation from the current
  guidance text, with URL + retrieval date recorded).
