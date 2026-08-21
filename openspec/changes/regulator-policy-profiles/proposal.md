# Proposal: regulator-policy-profiles

## Why

Turning a regulator's published AI guidance into an automated guardrail currently means reading
the PDF yourself and hand-translating its expectations into a `residency.json`. borderlint's
`init` wizard starts from a blank slate, so every operator re-derives the same answers for the
same regulator. Seeding the interview from a curated profile converts a standards document into
a starting policy in one flag — and HKMA's GenAI guidance is the home-turf credibility play for
borderlint's GBA audience.

## What Changes

- Add bundled, versioned regulator profiles: per supported seat, a profile carries a
  regulator name, guidance citation (URL + retrieval date), default classification
  allow-lists, and optional notes rendered during init.
- Extend `init` with a `--profile <id>` flag that pre-seeds the wizard: allow-lists start
  from the profile defaults instead of empty, and the operator keeps or drops from there.
- Non-interactive mode composes with profiles (`--home` + `--classes` + `--profile`) by
  taking the union of profile defaults and observed jurisdictions.
- Render the profile's provenance (regulator, citation, retrieval date) in the wizard output
  and as comments in the emitted policy file.
- Ship two seed profiles first — `hkma` (HKMA GenAI guidance) and `mas` (MAS guidance on
  AI risk management) — with the schema open for EU-AI-Act, PDPO additions via PR.

## Capabilities

### New Capabilities
- `regulator-profiles`: bundled, cited, versioned regulator profiles and their precedence,
  composition with observed jurisdictions, and provenance rendering.

### Modified Capabilities
- `policy-init`: the init command gains the `--profile` flag, pre-seeded walks, and
  provenance output; existing interview behaviour is unchanged when no profile is given.

## Impact

- New bundled data file (`borderlint/data/regulator_profiles.json`) plus loader validation;
  `borderlint/init.py` gains profile seeding; `borderlint/cli.py` gains the flag.
- Emitted policies gain comment lines only — the JSON shape is unchanged and stays loadable
  by the existing loader.
- No detection or evaluation changes; profiles are advisory starting points, never
  adjudication of regulatory sufficiency.

## Non-goals

- No legal analysis: profiles encode conservative defaults with citations, not advice, and
  every seeded value remains operator-editable in the walk.
- No new CLI subcommands; `--profile` extends `init` only.
- No auto-updating of profiles from regulator websites; curation stays human via PR.
- No coverage of seats without published AI-specific guidance in scope at seed time.
