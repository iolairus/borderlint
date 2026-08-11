## Why

Developers and privacy reviewers need actionable, plain-language explanations for borderlint violations and remediation guidance. Currently findings are terse codes; users must interpret reasons and regime references themselves.

## What Changes

- Add optional `--explain` flag to `borderlint scan` that emits human-readable explanations and remediation hints per finding.
- Explanations are advisory, never required for gating; exit code unchanged.
- Hints are generated from deterministic templates, not LLM calls, preserving zero-runtime-deps core.
- Output formats `text` and `json` gain an `explanation` field per finding when `--explain` is set.

## Capabilities

### New Capabilities
- `plain-language-explanations`: per-finding plain-language explanation of why a flow violates residency/sovereignty/provenance and what to change.

### Modified Capabilities
- `cli-and-reporting`: CLI gains `--explain` flag and report renderers emit explanation fields.

## Impact

- `borderlint/cli.py`: parse `--explain`, pass flag through.
- `borderlint/report.py`: add explanation renderer, JSON schema extension.
- No KB changes; no breaking API.

## Non-goals

- No LLM enrichment, no auto-fix, no policy auto-generation.
- No change to gating semantics or SARIF/evidence formats.
