## Context

Every renderer lives in `report.py` with the signature `(findings, kb, policy=None) -> str`;
the CLI dispatches on `--format` and treats the SBOM as an artifact (always exit 0). The
regimes/arrangements machinery (`_regimes`, `_arrangements`) already turns a home location and
flagged destinations into reference links. Findings carry provider, jurisdiction, sovereignty,
provenance, model, `model_org`, reasons, severity, waiver — the inventory columns exist; what's
missing is the audit envelope and the document framing.

## Goals / Non-Goals

**Goals:** one command produces the document a DPO files, with enough context to stand alone in
an audit trail; zero new dependencies; deterministic except where the audit context itself is
the value (timestamp, commit).
**Non-Goals:** PDF/HTML; policy adjudication; changing existing formats.

## Decisions

### D1 — Markdown document on stdout
**Decision:** `--format evidence` renders GitHub-flavoured markdown: header block (envelope),
inventory table, waiver register, arrangement references, summary counts.
**Rationale:** Markdown files cleanly in a ticket, a wiki, or a repo; converts to PDF with any
standard tool; renders in the PR where the scan ran. Same `(findings, kb, policy)` renderer
shape as every sibling.
**Alternatives rejected:**
- *PDF.* Rejected: a rendering dependency in a zero-dependency tool.
- *JSON with an audit envelope.* Rejected: machines already have `--format json`; the filing
  artifact is for humans, and wrapping JSON in framing just recreates the hand-assembly step.
- *HTML.* Rejected: styling surface with no filing advantage over markdown.

### D2 — Envelope fields resolve locally, degrade loudly
**Decision:** The envelope carries tool version, the three KB `updated` dates, scan timestamp
(UTC, ISO-8601), git commit of the scanned path (`git rev-parse HEAD` via stdlib subprocess,
2-second timeout), policy file SHA-256, classification, and home location. Any unresolvable
field renders as `unavailable` — never silently omitted.
**Rationale:** An auditor reading the pack must be able to tell "not applicable" from
"forgotten". Subprocess git keeps zero runtime deps and zero network; the scan path itself is
untouched (the envelope is assembled in the CLI layer, not the scanner).
**Alternatives rejected:**
- *A git library dependency.* Rejected: zero-dependency invariant.
- *Omit unavailable fields.* Rejected: absence is indistinguishable from tool failure in a
  filed document.

### D3 — Artifact semantics: always exit 0
**Decision:** Evidence mirrors the SBOM: the command exits 0 regardless of verdicts.
**Rationale:** The pack's job is to *record* failures, waivers included, not to gate; a CI
pipeline runs the gating scan and the evidence export side by side. A nonzero exit would make
"file the evidence of a failing state" impossible — the exact moment a DPO most needs it.
**Alternatives rejected:**
- *Gate like text/JSON.* Rejected above; also breaks `scan … > evidence.md` in a failing build.

### D4 — Timestamp honours SOURCE_DATE_EPOCH
**Decision:** The scan timestamp uses `SOURCE_DATE_EPOCH` when set, else current UTC.
**Rationale:** One environment variable keeps reproducible-build pipelines byte-deterministic
(the SBOM precedent for artifact determinism) without a CLI flag.

### D5 — Regime annex is data, regime-first, org-supplied blanks
**Decision:** A bundled `evidence_regimes.json` maps regime → annex heading, citations, and
expected fields, each field tagged `static` (filled from findings: destinations, axes, transfer
mechanism references, classification-as-categories) or `org` (rendered as a marked blank:
purpose, data-subject scale, recipient legal entity, retention). The join is the existing
`regime_of(home_location)` display string — entries keyed `"PDPO"`, `"PIPL"`, `"Macao PDPA"`,
`"PDPA (SG)"` — so `cn` and `CN-GBA` both reach the PIPL entry through shipped code and no new
token vocabulary is invented. First coverage: PDPO (PCPD cross-border guidance), PIPL + GBA SC
(PIA and route framing), Macao PDPA (with the Macao GBA SC variant), PDPA (SG) (s.26 / PDPC
transfer documentation). Home locations outside the covered set — or `home_regime`-only
policies — render the generic pack with no annex; the annex prints the data file's `updated`
date.
**Rationale:** Regime expectations are citations and field lists — data, not logic; the KB
freshness machinery already knows how to keep dated data honest. The `static`/`org` split keeps
the tool's never-adjudicate posture: it fills what code proves and names what it cannot know.
**Alternatives rejected:**
- *International-framework-first (GDPR RoPA / ISO 27701).* Rejected by the user's call: the
  audience files under PDPO/PIPL/PDPA first; framework mappings are follow-on data.
- *Per-regime templates hardcoded in `report.py`.* Rejected: regulator guidance changes on its
  own cadence; data files get `updated` dates and drift review, code does not.
- *Auto-filling purpose/scale from heuristics.* Rejected: fabricating filing answers is the
  one unforgivable failure mode for an audit artifact.

## Risks / Trade-offs

- **[Envelope trust]** The pack asserts commit/digest but is not signed; a tampered document
  can claim anything. → Out of scope, documented: signing belongs to the CI system (the
  release pipeline's attestations are the precedent); the digest lets a verifier recompute.
- **[Table width]** Inventories with many axes are wide. → Locations render as a sub-list per
  flow rather than a column; the table keeps seven columns.

## Migration Plan

1. `report.evidence(findings, kb, policy, envelope)` + envelope assembly in `cli.py`.
2. Format choice + artifact exit; tests per scenario; README/CAPABILITIES.
3. Rollback: revert — no existing format changes.

## Open Questions

None.
