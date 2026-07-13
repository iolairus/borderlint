# add-html-report-format — design

## Context

`report.py` holds one top-level function per format, all sharing the `(findings, kb, policy=None)`
signature; formats needing extra inputs (mermaid's label, evidence's envelope) take an extra arg and
are wired through lambdas in the `renderers` dict at `cli.py:92-95`. The audit envelope (`_envelope`
in `cli.py`) already gathers exactly the metadata the HTML header needs (path, commit, policy digest,
classification, KB review dates) but is currently built only when `--format evidence`. Scanned
repositories are untrusted input: evidence strings, paths, and waiver reasons flow into the report
verbatim today (safe in text/JSON; markup-significant in HTML).

## Goals / Non-Goals

**Goals:**
- One self-contained HTML document from a scan, offline-renderable, safe against markup injection
  from scanned content, covering both inventory and policy modes.
- Zero new dependencies; follow the existing per-format function pattern exactly.

**Non-Goals:**
- Evidence/filing semantics (markdown evidence pack remains the filing artifact — decision upheld
  from `2026-07-08-evidence-pack`).
- Graph rendering, JS interactivity, theming, PDF.

## Decisions

1. **`report.html(findings, kb, policy=None, envelope=None)`**, mirroring `evidence()`'s shape;
   wired via a lambda like evidence. *Alternative:* rebuilding metadata inside `report.py` —
   rejected, duplicates `_envelope`.
2. **Envelope built for html too**: `cli.py` builds the envelope when `a.format in ("evidence",
   "html")`. *Alternative:* a separate lighter header struct — rejected, the envelope is already
   the right fields and "absent field renders as 'unavailable'" semantics carry over.
3. **Pure stdlib string assembly with `html.escape(..., quote=True)` on every repo-derived string**
   (paths, evidence, model IDs, waiver reasons, provider names from a user-supplied KB).
   *Alternative:* a template engine — rejected, new dependency for one document.
4. **No embedded JavaScript at all; flow map as jurisdiction-grouped tables** (same grouping the
   text/mermaid renderers use). *Alternative:* inline-embedding mermaid.js (~2.8 MB) — rejected:
   bloats every report, adds a vendored-JS maintenance surface, and the spec's self-containment
   requirement is about resources, not about needing a graph.
5. **Severity chips via inline CSS classes** (`fail`/`warn`/`waived`/`ok`), single `<style>` block
   in the head; content readable when printed monochrome (chip text, not colour alone — keeps the
   report legible on paper, which is where compliance reviews still happen).
6. **Exit semantics**: `cli.py:97` export tuple becomes `("sbom", "evidence", "html")`.

## Risks / Trade-offs

- [Report grows with finding count; no pagination] → acceptable: scans of real services produce
  tens of flows, not thousands; plain tables degrade gracefully.
- [No graph view may disappoint mermaid users] → mermaid format still exists; README shows how to
  render it to PNG alongside.
- [Inline styles diverge visually over time from docs/site] → single `<style>` block, no shared
  asset to drift against; deliberate.

## Open Questions

None.
