# Proposal: kb-drift-resolution-11

## Why

The live 2026-11-17 drift run (issue #39) reports one uncovered provider, 59 unresolved model
families (145 ids), and a stale MCP-server KB. The model queue is dominated by newly enumerated
Replicate deployments: genuine first-party or derivative models are mixed with applications,
pipelines, and products whose base lineage is undisclosed. Treating every Replicate id as a model
would invent provenance; leaving real models unresolved weakens the provenance dimension.

Research also found two correctness issues beyond the new ids: Nace's current catalog retires API
v1.5 into undisclosed v1.1 lineage and routes `drex-latest` there too, and the MCP map's SQLite
launcher is not the official package identifier.

## What Changes

- Add **Microsoft Web IQ** as a `service` provider: documented Python/npm/JVM/.NET SDKs and
  `api.microsoft.ai`; residency `unknown` because Microsoft makes no regional residency commitment;
  sovereignty `us`; no provenance default. Record `webiq/search` as a search-operation residue.
- Add `replicate/` to provenance passthrough namespaces. It identifies the host, not the weights
  developer, matching the existing aggregator-passthrough rule and avoiding duplicate full-key
  patterns.
- Add 54 anchored owner/family patterns for the researched deployments: Alibaba/Wan, Bria,
  ElevenLabs, HeyGen, Ideogram, Inworld, Kuaishou/Kling, Lightricks/LTX, Luma, Real-ESRGAN,
  Perceptron/Isaac, PlayAI, Pruna derivatives, QuiverAI, Recraft, Resemble AI, Sync Labs,
  TypeSafe Jev (including its full Vercel AI Gateway key), OpenAI's CSAM classifier, and Nace's
  pinned open Max v1 checkpoint. Include the full OpenRouter Isaac key so the existing US prefix
  cannot win.
- Add exact residue for 55 cached-wave tool/pipeline/undisclosed-lineage ids among the original
  145, plus non-fixture `nace/drex-latest` and `nace/drex-v1.5`: 57 total. Remove the four
  API/moving patterns `drex-v1.5`, `nace/drex-v1.5`, `drex-latest`, and `nace/drex-latest`; retain
  immutable `nace-ai/drex-v1.5`, active v2.0 forms, and pinned Max v1. No whole-org residue prefixes.
- Correct and refresh `mcp_servers.json` with the exact local, Brave Search, Notion, and Sentry
  launchers enumerated in design. Retain existing GitHub/Slack/Drive keys without new identities;
  add no fetch/git/time servers. Advance its review date.
- Bump all touched KB dates and add coverage, full-key override, near-miss, retired/moving-alias,
  residue-expansion, and MCP regression tests.

## Capabilities

### New Capabilities
- (none)

### Modified Capabilities
- `jurisdiction-classification`: Web IQ resolves as a Microsoft search service with honest unknown
  residency and US sovereignty.
- `model-provenance`: Replicate hosting is stripped once; resolvable owner-qualified families gain
  provenance, while tools and unknown lineage remain explicitly unresolved.
- `mcp-config-scanning`: documented stdio launcher identities resolve to existing providers.

## Impact

- Provider, sovereignty, provenance, MCP, drift-alias, README, and test files.
- The current provider/model-family/stale-KB sections converge to zero; Web IQ joins the standing
  data-practice backlog.

## Non-goals

- No curation of the 111-entry data-practice backlog.
- No whole-Replicate or whole-developer provenance default and no guessed lineage.
- No MCP backend-host inference for self-hosted GitHub/Sentry/PostgreSQL; that needs separate
  scanner/spec work.
- No unrelated provider catalog expansion or release in this change.
