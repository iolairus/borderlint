## Why

A service often exposes the same model behind several regional endpoints — a CN endpoint, an SG
endpoint, an HK endpoint. Teams must ensure a configuration is wired to the *right* regional
endpoint for the data it carries (customer PII must not route through the CN endpoint when policy
allows only HK/SG). borderlint can already define custom hosts via `--providers`, but that file
currently *replaces* the bundled knowledge base and requires full provider entries — too heavy for
"these internal hosts are in these jurisdictions." This change makes the user KB additive and adds a
simple endpoint→jurisdiction map.

## What Changes

- The user-supplied knowledge base is **merged** with the bundled one — user entries add to it and,
  on a host/SDK/package conflict, take precedence — instead of replacing it.
- A user file may declare a simple **`endpoints` map** (`host → jurisdiction code`) for internal
  endpoints, merged additively, with no full provider definition required:
  ```json
  { "endpoints": { "llm-cn.acme.com": "cn", "llm-hk.acme.com": "hk", "llm-sg.acme.com": "sg" } }
  ```

## Capabilities

### Modified Capabilities
- `jurisdiction-classification`: the user-supplied KB merges with (rather than replaces) the bundled
  KB, and supports a flat host→jurisdiction endpoints map.

## Impact

- `borderlint/kb.py` (merge bundled + user providers; load the `endpoints` map). No CLI change — the
  existing `--providers <file>` carries `providers` and/or `endpoints`. No new dependencies.

## Non-goals

- Refreshing the **public** provider registry — a separate freshness concern (a scheduled upstream
  refresh), not this change.
- A new flag or policy mechanism — internal endpoints resolve to jurisdictions, and the existing
  classification allow-lists + deny-by-default catch a config wired to the wrong regional endpoint.
