## Why

Apertus — the Swiss open-weights family from ETH Zürich/EPFL (`swiss-ai` org) — cannot be
expressed: Switzerland is outside the EU/EEA, so no existing bloc is honest, and the freshness
report lists the family as permanently uncoverable. Approved as part of the issue #39 triage.

## What Changes

- Both bloc vocabularies gain `ch` (sovereignty and provenance), with validation, display name
  ("Switzerland", matching the JURIS label), and a legal-source note (revised FADP 2023 + the
  BÜPF surveillance framework).
- Provenance patterns: `apertus` (distinctive stem) and `swiss-ai/` (hub org) → `ch`.
- Docs bloc lists updated.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `sovereignty`: the bloc vocabulary gains `ch`.
- `model-provenance`: the bloc vocabulary gains `ch`; the map covers Apertus.

## Impact

- `borderlint/kb.py`, `borderlint/policy.py`, `borderlint/report.py` — the five vocabulary
  copies; the "(use one of …)" error messages.
- `borderlint/data/sovereignty.json` (source note), `borderlint/data/provenance.json`
  (two patterns), both `updated` bumped.
- `README.md`, `CAPABILITIES.md` — bloc lists.

## Non-goals

- No jurisdiction/sovereignty change for `publicai` (Apertus's serving partner is not
  Swiss-jurisdiction); no other new blocs.
