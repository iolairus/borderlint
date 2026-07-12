## Context

Borderlint currently supports six output formats: text, JSON, mermaid, SARIF, SBOM, and evidence. CI dashboards and PR descriptions need a visual indicator of residency compliance status. Shields.io provides a standard badge endpoint schema that any markdown renderer can consume via `img.shields.io/endpoint?url=…`.

## Goals / Non-Goals

**Goals:**
- Add `--format badge` that outputs shields.io endpoint JSON to stdout
- Color-code by policy result: green (clean), red (failures), blue (inventory mode)
- Keep the zero-dependency constraint — pure stdlib JSON construction
- Document consumption patterns (GitHub Pages, gist, Actions step)

**Non-Goals:**
- Hosting an HTTP endpoint ourselves; the user pipelines stdout to their hosting
- Custom labels or messages beyond the standard schema
- Supporting shields.io dynamic badges (only endpoint schema v1)

## Decisions

**Decision 1: Message format — count-based summary**
- Policy mode with failures: `"{N} flagged"` (red)
- Policy mode clean: `"clean"` (green)
- Inventory mode: `"{N} flows"` (blue)
- Rationale: Shields badges have limited character space; a count gives the essential signal without crowding. Alternatives considered: listing jurisdictions (too long), "pass"/"fail" (loses inventory mode distinction).

**Decision 2: Badge format as non-gating export (like SBOM/evidence)**
- `--format badge` exits 0 regardless of violations, matching SBOM/evidence behavior
- Rationale: The badge is consumed by a downstream pipeline step (writing to gist/Pages); failing the process would prevent the badge from being published. The exit-code semantics already exist for artifact exports.

**Decision 3: Single function in report.py**
- `report.badge(findings, kb, policy)` returns a string (JSON), consistent with existing renderers
- Rationale: Keeps the renderer pattern uniform; no new module needed.

## Risks / Trade-offs

[Risk] Shields.io endpoint URL may expire or change schema → Mitigation: Schema version is explicit (`schemaVersion: 1`); if shields changes, update the constant. The format is well-established and unlikely to break.

[Risk] Badge message truncation for large flow counts → Mitigation: Shields.io handles long messages; the count format is short by design.

## Migration Plan

No migration needed — additive feature. Users opt in by using `--format badge`.

## Open Questions

None.
