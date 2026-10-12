# Proposal: kb-drift-resolution-6

## Why

The post-#116 freshness run (2026-10-11) reports two uncovered upstream providers and eight
unresolved model families — a wave with two distinct shapes: two Microsoft surfaces newly
carried by litellm (the Microsoft 365 Copilot Chat API and two Microsoft-published models,
one of them a Qwen post-train), and ScaleDown's task-specific SLM API with five endpoint
names. Until each item is assigned by hand, these flows classify as `unknown` and the
review queue cannot converge.

## What Changes

- Add a bundled provider entry for `microsoft_365_copilot`: endpoint host
  `graph.microsoft.com` (the Graph beta Copilot Chat API — litellm creates a conversation
  and posts chat turns against it; documented in litellm's handler and Microsoft Learn),
  jurisdiction `us`, sovereignty `us`. The note records that the API is preview, that
  Microsoft chooses the served model, and that the host is the shared Microsoft Graph
  surface — every Graph call is Microsoft/us regardless, so jurisdiction classification is
  unaffected by the non-AI traffic sharing the host. The generic Entra token host is NOT
  an endpoint.
- Add a bundled provider entry for `scaledown`: endpoint host `api.scaledown.xyz` (the
  API host in litellm's transformation and ScaleDown's own docs — distinct from the
  `.ai` marketing/docs hosts), jurisdiction `us`, sovereignty `us`. ScaleDown, Inc.
  (Ramona, CA; Delaware governing law) commits in its DPA to processing exclusively on
  US infrastructure with zero retention and no training on customer data.
- Add provenance patterns for the eight families:
  - `us` — `github_copilot/mai-code` (plus the bare `mai-code` stem, mirroring the
    existing `mai-*` convention): MAI-Code is Microsoft AI's in-house coding-model family
    per the official `microsoft/MAI-Code` repository.
  - `us` — a single `scaledown/` org-namespace pattern covering all five observed
    endpoint names (`classify`, `compress`, `decisions`, `extract`, `summarize`):
    ScaleDown serves its own task-specific SLMs and its DPA places no third-party model
    vendor in the data path — own models until lineage says otherwise (the `clef`
    precedent). NO bare stems under any circumstances: `classify`, `extract`, and
    `summarize` are maximally generic words.
  - `us` — the qualified `microsoft_365_copilot/chat` form: Microsoft selects the model
    behind the Copilot Chat API. NO bare `chat` stem under any circumstances.
  - `cn` — `azure_ai/microsoft-decision` (plus the bare `microsoft-decision` stem):
    Microsoft-Decision-1 is Microsoft-published but documented by Microsoft as post-trained
    on Qwen3.5-9B, so the fine-tunes-inherit-base rule assigns Alibaba's bloc, with the
    organisation label naming base and tuner (the Bespoke Nimble precedent). This is the
    wave's one counter-intuitive call: a Microsoft-branded model classifying `cn` on
    weight lineage, exactly as the AWS-published Strands Decider did.
- Add a tier-2 provider default `scaledown` → `us` (serves only its own models).
  `microsoft_365_copilot` gets NO default: Copilot is documented to route across model
  vendors, so unbound flows stay honestly `unknown`.
- Bump the review dates of the touched knowledge-base files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `jurisdiction-classification`: two new hosted providers resolve with documented endpoint
  hosts, jurisdiction `us`.
- `model-provenance`: the drift-run families resolve to their developers' blocs, including
  the Qwen-inheritance call on Microsoft-Decision-1.

## Impact

- `borderlint/data/providers.json` (+2 entries), `sovereignty.json` (+2 `us` mappings),
  `provenance.json` (+6 patterns, +1 provider default), tests.
- No drift-suppression changes: every item resolves via entries or patterns; nothing is
  residue this wave.
- Issue #39's actionable sections drop from 2 providers + 8 families to zero. The
  data-practice gap queue grows 92 → 94: both new providers join it honestly (both publish
  terms worth curating — ScaleDown's DPA is unusually specific).

## Non-goals

- No data-practice curation: the gap queue stays the declared standing backlog.
- No scanner or checker changes: every item resolves via KB data; matching semantics are
  unchanged.
- No handling of the OpenRouter mirror of Microsoft-Decision-1
  (`openrouter/microsoft/microsoft-decision-1`): not in this drift report; a future wave
  resolves it via the same inherit-base rule.
- No EU Data Boundary / Flex Routing residency modelling: `microsoft_365_copilot` records
  provider jurisdiction only; per-tenant processing-region routing is out of the KB's
  scope.
