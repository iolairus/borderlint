## Why

Rendering litellm's flow map exposed two Mermaid defects. (1) A provider that resolves to **multiple
jurisdictions** (AWS Bedrock → `us`/`de`/`ie`/`unknown`, Azure → `fr`/`us`, DashScope → `cn`/`sg`)
emits the **same node id** under each zone; Mermaid de-duplicates by id, so the provider renders once
and the other zones collapse to empty/loose boxes (the stray `fr`/`de`/`ie` nodes). The map then
**understates where data actually goes**. (2) Subgraph titles mix display names (`Singapore`) with raw
codes (`fr`/`de`/`ie`) — only some jurisdictions have a `JURIS` display name, so titles are inconsistent.

## What Changes

- Emit a **distinct node per (provider, jurisdiction)** — id `<provider>__<juris>` — so a multi-region
  provider appears under **every** jurisdiction it reaches, each with its own edge from the app node.
- Title each jurisdiction subgraph by its **canonical code** (`sg`, `fr`, `cn`, `CN-GBA`, `local`,
  `unknown`) — matching the policy vocabulary, consistent across all zones.

## Capabilities

### Modified Capabilities
- `cli-and-reporting`: the Mermaid flow map renders one node per (provider, jurisdiction) and titles
  zones by code.

## Impact

- Node-id and subgraph-title changes in `report.mermaid()`. Other formats (text / JSON / SARIF / SBOM)
  unchanged — they keep the human-readable jurisdiction names. No new dependency.

## Non-goals

- Changing the human-readable jurisdiction names in text / JSON / SARIF / diff output (`OpenAI -> United
  States` still reads with the full name).
- Adding display names for every ccTLD (`de`/`fr`/`ie`) — codes are the canonical, consistent choice.
