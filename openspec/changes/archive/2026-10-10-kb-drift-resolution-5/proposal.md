# Proposal: kb-drift-resolution-5

## Why

The post-#109 freshness check (run 2026-10-08, ahead of the next weekly issue refresh)
reports three unresolved model families and the second-ever 90-day staleness firing —
`evidence_regimes.json` was last reviewed 2026-07-08. Until each item is assigned by hand,
these flows classify as `unknown` and the review queue cannot converge.

## What Changes

- Add the Bedrock India-region inference-profile prefix `in.` to the provenance map's
  passthrough orgs (alongside `us.`, `eu.`, `apac.`, `au.`, `jp.`, `global.`, `us-gov.`):
  `in.moonshotai.kimi-k3` then strips the region prefix and resolves through the existing
  `moonshotai.` pattern to Moonshot AI (bloc `cn`). The prefix carries no provenance — the
  model family in the repo name does.
- Add a qualified `azure/whisper` provenance pattern → OpenAI (bloc `us`), mirroring the
  existing `azure_ai/whisper` entry: litellm now carries the id under the `azure` provider
  namespace as well. No bare `whisper` stem under any circumstances — it collides with
  unrelated names like `whispering-pines`.
- Record `azure/model-router` as structural residue in `scripts/kb_drift_aliases.json` —
  the same Azure Foundry model-routing feature already acknowledged as
  `azure_ai/model-router`, now surfaced under the `azure` namespace. This is the
  exact-key/variant case the freshness spec predicts: an exact-key acknowledgment does not
  cover future variants, so the variant gets its own reasoned entry.
- Perform the 90-day legal review of `evidence_regimes.json` (PDPO, PIPL, Macao PDPA,
  PDPA SG filing-expectation summaries): verify each citation against its source, record
  any in-window legal changes, and bump the `updated` date.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `model-provenance`: the Bedrock `in.` region prefix passes through; the drift-run
  `azure/whisper` family resolves to OpenAI's bloc.

## Impact

- `borderlint/data/provenance.json` (+1 passthrough org, +1 pattern),
  `borderlint/data/evidence_regimes.json` (review + date bump),
  `scripts/kb_drift_aliases.json` (+1 residue entry), tests.
- No new providers, no sovereignty changes.
- The freshness report's actionable sections drop from 3 families + 1 stale KB to zero;
  the 102 data-practice gaps remain the standing backlog.

## Non-goals

- No data-practice curation: the gap queue (102) stays the declared standing backlog.
- No scanner or checker changes: every item resolves via KB data or an aliases entry.
- No re-review of `arrangements.json`/`regimes.json` — both passed the 2026-10-02 legal
  review; only `evidence_regimes.json` is in-window.
