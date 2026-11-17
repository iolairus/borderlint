# Tasks: kb-drift-resolution-11

## 1. Provider and sovereignty

- [x] 1.1 Add `webiq` / Microsoft Web IQ with category `service`, all four documented SDK families,
      `api.microsoft.ai`, jurisdiction `unknown`, a no-regional-commitment note, and sovereignty
      `us`; add no provenance default (design D1; spec: Microsoft Web IQ service classification)
- [x] 1.2 Add exact `webiq/search` search-operation residue and bump provider/sovereignty review
      dates (design D1)
- [x] 1.3 Update the README bundled-provider count from 137 to 138 (spec: documentation accuracy)

## 2. Replicate passthrough and resolvable provenance

- [x] 2.1 Add `replicate/` to `passthrough_orgs`; do not add a Replicate provider default or
      duplicate every pattern with a full Replicate prefix (design D2)
- [x] 2.2 Add OpenAI CSAM, TypeSafe Jev, Alibaba Wan (including Wan-Video/WaveSpeedAI/Pruna forms),
      and Bria patterns with the exact anchors and org labels in design (design D3)
- [x] 2.3 Add ElevenLabs speech, HeyGen Avatar, Ideogram, Inworld, Kling, LTX, and Luma Photon
      patterns, excluding their documented tool/pipeline ids (design D3, D4)
- [x] 2.4 Add Real-ESRGAN, Isaac, PlayDialog, Pruna derivatives, QuiverAI Arrow, Recraft,
      Chatterbox, and Sync Labs patterns with source-backed inheritance and org labels
      (design D3, D6)
- [x] 2.5 Add `nace-ai/drex-max-v1` cn; remove `drex-v1.5`, `nace/drex-v1.5`, `drex-latest`,
      and `nace/drex-latest` cn API/moving-alias patterns; retain active bare/nace/HF v2.0 and
      immutable HF v1.5 checkpoints, and bump `provenance.updated` (design D5)

## 3. Exact residue

- [x] 3.1 Add exact Nace Max/v1.1/latest unknown residue plus `nace/drex-v1.5`, distinct from
      immutable `nace-ai/drex-v1.5`; do not widen existing Drex v1.0 residue, but update its reason
      to distinguish active/immutable checkpoints from retired/moving API routes (design D4, D5)
- [x] 3.2 Add the exact Bria, Datalab, Decart, Easel, ElevenLabs Dubbing, and fifteen FLUX-app
      residue ids enumerated in design, with source-based structural/unknown reasons (design D4)
- [x] 3.3 Add exact HeyGen, Ideogram Layerize, HTML-to-image, Kling Lip Sync, LTX pipeline, Luma
      Reframe, Clarity Pro, and PixVerse Lip Sync residue ids (design D4)
- [x] 3.4 Add exact Pruna P-Image/2-Pro, Recraft tool, Retro Diffusion, and VEED Fabric residue
      ids; use no trailing `-` or `/` on any exact key (design D4)

## 4. MCP review

- [x] 4.1 Replace `@modelcontextprotocol/server-sqlite` with `mcp-server-sqlite` and add
      `mcp/sqlite`; retain valid archived package identifiers (design D7)
- [x] 4.2 Add exactly local binaries `mcp-server-filesystem`, `mcp-server-memory`,
      `mcp-server-everything`, `mcp-server-sequential-thinking`, and `mcp-server-postgres`; Brave
      `@brave/brave-search-mcp-server`, `brave-search-mcp-server`, `mcp/brave-search`, and
      `docker.io/mcp/brave-search`; Notion `notion-mcp-server` and `mcp/notion`; and Sentry
      `sentry` and `sentry-mcp`. Retain existing GitHub/Slack/Drive mappings; add no fetch/git/time
      launchers and no new provider targets (design D7)
- [x] 4.3 Advance `mcp_servers.json.updated` after the corrections; leave backend-aware
      self-hosting semantics for a separate change (design D7)

## 5. Tests

- [x] 5.1 Test Web IQ endpoint/SDK/category/jurisdiction/sovereignty and no provenance default
- [x] 5.2 Test Replicate passthrough equivalence for SDK and LiteLLM-qualified literals, plus
      near-misses proving owner namespaces remain load-bearing (design D2, D3)
- [x] 5.3 Add representative positive tests for every model-family group in tasks 2.2–2.5,
      including variants, inherited org labels, and the Isaac override of existing Perceptron/us
- [x] 5.4 Add guarded-stem tests: generic tools, future versions, unqualified Recraft, unrelated
      Wan/Kling/LTX/Photon/Arrow names, and whole-org near-misses remain unresolved (design D3)
- [x] 5.5 Replace the stale wave-7 Drex expectations at `tests/test_borderlint.py:3532-3572` so
      bare/nace API v1.5/latest are unknown while active v2.0 and immutable HF v1.5/Max v1 are cn;
      test exact residue behavior and future-variant visibility, including Nace moving aliases not
      resolving cn while pinned official Max v1 does (design D4, D5)
- [x] 5.6 Parameterize every launcher/image added in tasks 4.1–4.2, including SQLite uvx/image,
      both Brave image forms, and both Sentry binaries, and assert the invalid scoped SQLite npm id
      is absent (design D7)
- [x] 5.7 Run `kb_drift.model_coverage_gap` plus `split_residue` over all 145 wave-11 upstream ids
      and assert none remains actionable; separately from drift suffix coverage, assert direct
      `kb.match_model` coverage for all 90 provenance-assigned cached ids, including full
      `vercel_ai_gateway/typesafe-ai/jev`, and test `nace/drex-latest` after pattern removal

## 6. Verification

- [x] 6.1 Run the full pytest suite and JSON/load validation
- [x] 6.2 Re-run `scripts/kb_drift.py`: zero new-provider, uncovered-family, sovereignty, SDK, and
      stale-KB items from this wave; only the standing data-practice backlog and acknowledged
      residue remain
- [x] 6.3 Run `openspec validate kb-drift-resolution-11 --strict` and review the diff for accidental
      broad patterns, guessed lineage, or out-of-scope data-practice/backend changes
