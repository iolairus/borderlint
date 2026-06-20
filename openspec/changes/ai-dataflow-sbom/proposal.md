## Why

borderlint's findings outputs (JSON, SARIF) answer "did anything **violate** the policy?" — they are
per-PR, policy-bound, and ephemeral. Governance needs the other artifact: a standing, portable
**census** of every AI dependency and where each one sends data, independent of any verdict. A DPO or
regulator asking "show me every place customer data leaves Hong Kong" wants one document, attachable
to a release and diffable over time. This adds an "AI data-flow SBOM" export.

## What Changes

- **`--format sbom`** — emit a **policy-independent** JSON inventory of every detected AI flow: each
  provider with its name, resolved jurisdiction(s), and call sites (file + line), under an envelope
  carrying a schema id, the borderlint version, and the KB review date.
- The export is **deterministic** (no wall-clock timestamp) so the same scan yields byte-identical
  output — making it diffable (the basis for a future "what new cross-border flows did this PR add?").
- The export **does not gate CI** — it is an artifact, not a check; it exits 0 even when a supplied
  policy would fail.

## Capabilities

### Modified Capabilities
- `cli-and-reporting`: a new `--format sbom` export alongside text / json / mermaid / sarif.

## Impact

- A `report.sbom(...)` renderer and one new `--format` choice; the scanner and policy engine are
  unchanged (the export reads the same detections inventory mode already produces). No new dependency.

## Non-goals

- Conforming to CycloneDX or SPDX. No "AI data-flow SBOM" standard exists; v1 ships a borderlint-native
  schema. A CycloneDX/SPDX mapping is deferred until a consumer needs to ingest it.
- The diff/PR-delta behaviour itself (D6) — this change only guarantees the determinism it depends on.
