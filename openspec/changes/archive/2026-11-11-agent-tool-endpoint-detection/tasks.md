# Tasks: agent-tool-endpoint-detection

## 1. Detection — Detect explicitly declared agent-tool endpoints

- [x] 1.1 Add curated MCP/agent-tool key recognition for the agreed snake_case, environment-style, and camelCase forms, rejecting bare URLs, bare `tool_url`, and authentication-key lookalikes.
- [x] 1.2 Emit `agent_tool_endpoint` detections with known-host, loopback, unknown-static, and runtime-templated resolution through the existing KB and host-classification rules.
- [x] 1.3 Capture key-plus-sanitized-host or runtime-resolved evidence; test userinfo, paths, queries, fragments, headers, and secrets are not retained.
- [x] 1.4 Suppress only generic detections for the same explicit declaration, preserve structural MCP parser precedence, and cover two declarations on one line.

## 2. Provenance — Model references bind to same-file provider detections

- [x] 2.1 Exclude `agent_tool_endpoint` from model-reference attachment while preserving binding to other eligible same-file flows and standalone-reference behavior.

## 3. Tests — detection and downstream contracts

- [x] 3.1 Add unit coverage for every recognized key family and resolution branch, plus arbitrary URL, `tool_url`, `MCP_AUTH_URL`, commented-example, malformed-value, and duplicate-precedence negatives.
- [x] 3.2 Add end-to-end policy tests for allowed, disallowed, unknown-warn, unknown-fail, local, and justified-waiver findings, including exit codes.
- [x] 3.3 Exercise text, JSON, SARIF, SBOM, evidence, HTML, Mermaid, and badge renderers with the new kind; verify no schema additions or renderer crashes.
- [x] 3.4 Perform the design's real-world validation against public examples and at least two repositories; record sanitized fixtures, findings, and rejected key names in the PR.

## 4. Documentation — A7 closure

- [x] 4.1 Document explicit MCP/agent-tool endpoint keys, static-analysis limits, unknown handling, and evidence sanitization in README.
- [x] 4.2 Update A7 in `CAPABILITIES.md` to shipped, noting both structured MCP config scanning and explicit agent-tool endpoint detection; leave A6 for its separate change.

## 5. Verification — full change acceptance

- [x] 5.1 Run `openspec validate agent-tool-endpoint-detection --strict` and the complete pytest suite.
- [x] 5.2 Run representative CLI scans to confirm output, duplicate suppression, sanitized evidence, waivers, and exit statuses end to end.
