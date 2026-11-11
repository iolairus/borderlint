# Design: agent-tool-endpoint-detection

## Context

The archived `mcp-config-scanning` change handles remote and stdio servers in four structurally parsed JSON filenames. The generic config detector only recognizes AI-model key stems, while generic text scanning only recognizes hosts already present in the KB. Consequently, an explicitly declared but private or unmapped MCP/agent-tool URL outside those files is invisible.

## Goals / Non-Goals

**Goals:**
- Surface explicit MCP/agent-tool destinations with honest provider and jurisdiction resolution.
- Preserve clickable, sanitized evidence without duplicating generic detections.
- Reuse all existing evaluation and reporting paths.

**Non-Goals:**
- Infer tool usage from arbitrary URLs or runtime behavior.
- Broaden structured MCP parsing or repair unrelated stdio launcher/locality behavior.
- Redesign provenance policy for non-model services.

## Decisions

- **Curated declaration keys, not broad URL scanning.** Start with `mcp`, `mcp_server`, `mcp_gateway`, and `agent_tool` stems paired with `url`, `endpoint`, `base_url`, or `host`, including snake_case, environment-style, and camelCase equivalents. Do not accept bare `url`, `tool_url`, authentication URLs, or arbitrary `MCP_*` names such as `MCP_AUTH_URL`; those do not reliably identify a tool data destination. Add framework-specific names only with real fixtures.
- **New kind `agent_tool_endpoint`.** Keep `mcp_server` as the contract for structural server entries and use the new kind for key-based declarations in ordinary source/config files. Downstream formats already treat kinds as opaque strings.
- **Reuse endpoint trust rules.** A KB host inherits its curated provider, residency, and sovereignty; loopback is `local`; an unmapped static host is `custom_endpoint`/`unknown`; a templated or otherwise runtime-resolved destination is `custom_endpoint`/`unknown`. Never infer location from a TLD, package name, or path.
- **Sanitize evidence at capture.** Record `<key> -> <host>` for static destinations and `<key> -> runtime-resolved` for dynamic ones. Strip userinfo and do not retain paths, queries, fragments, headers, or assignment values. This is stricter than emitting the raw declaration because agent configs commonly carry credentials.
- **Explicit detection wins for its declaration.** Suppress a generic `endpoint_reference` or `config_endpoint` for the same key/value occurrence rather than changing global deduplication. A known host elsewhere in the file retains normal detection behavior.
- **Structural MCP files retain precedence.** Valid recognized MCP configs remain claimed by the existing structural parser. The new scanner applies to ordinary scanned files and to malformed MCP files after the existing fallback; it does not alter valid structural parsing.
- **No model provenance assigned to tool endpoints.** Exclude `agent_tool_endpoint` detections from same-file model-reference attachment and first-party tier-2 provenance defaults. A model reference still binds to another eligible provider flow in the file, or stands alone when the tool endpoint is the only flow. Provenance policy evaluation remains unchanged.
- **No new policy or reporting layer.** Existing residency, `on_unknown`, waivers, exit codes, and output renderers apply unchanged.

## Alternatives Considered

- **Add `mcp` to the generic AI environment stems.** Rejected: it would reuse `config_endpoint`, could not distinguish tool flows for binding/exclusion, and a broad `MCP_*` match would include authentication and other non-tool endpoints.
- **Reuse `mcp_server` for every declaration.** Rejected: a loose key assignment is not necessarily a complete server entry, and preserving the existing structural-kind contract avoids confusing consumers.
- **Scan every URL or common tool-call expression.** Rejected: ordinary application URLs would create substantial false positives without evidence that an agent sends data there.
- **Bundle stdio locality and provenance-policy fixes.** Rejected: those are independent semantic changes with their own compatibility impact and deserve focused proposals.

## Risks / Trade-offs

- [Risk] Curated keys miss framework-specific declarations → Mitigation: validate against real configurations and add only evidence-backed aliases later; unknown runtime discovery remains out of scope.
- [Risk] New findings can make previously clean scans warn or fail → Mitigation: this is intended A7 coverage; document it in release notes and retain existing waiver and `on_unknown` controls.
- [Risk] A static host does not prove actual transmission or downstream egress → Mitigation: reports describe a configured potential destination, not observed traffic or transitive flows.
- [Risk] Duplicate suppression can hide a distinct same-line reference if implemented by line alone → Mitigation: match the declaration occurrence/host, not every detection on the line, and test two declarations on one line.

## Real-world validation (gate before merge)

Validate the selected key forms against public agent/MCP configuration examples and at least two real repositories using explicit endpoint declarations. Include unknown private hosts, known KB hosts, loopback, templates, credentials/query strings, commented examples, and similarly named authentication keys. Record fixtures and results in the PR without copying secrets.
