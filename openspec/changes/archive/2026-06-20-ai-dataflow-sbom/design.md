## Context

Inventory mode (E2) already runs the scanner with no policy and wraps each detection as an `ok`
finding. Every renderer shares the `(findings, kb, policy)` signature. The SBOM is a new renderer over
that same data — it reads `f.detection`, ignores severity and policy, and emits a structured document.

## Goals / Non-Goals

**Goals:** a portable, deterministic, policy-independent inventory artifact; a single new `--format`
choice; zero scanner/policy change.

**Non-Goals:** CycloneDX/SPDX conformance; the diff behaviour (D6) itself.

## Decisions

- **Native schema, not CycloneDX/SPDX.** Alternative: emit CycloneDX 1.5 ML-BOM. Rejected for v1 — no
  "AI data-flow SBOM" standard is settled, the mapping (BOM-refs, component identity, serialNumber) is
  real work, and no consumer needs it yet. Schema id `borderlint.ai-dataflow-sbom/1` leaves room to add
  a CycloneDX exporter later. Calling it "SBOM" is the narrative; the artifact is an inventory manifest.
- **Deterministic — no wall-clock timestamp in the document.** Alternative: stamp generation time
  (conventional for SBOMs). Rejected — a timestamp makes every export differ, defeating the diff use
  case this exists to enable. The KB `updated` date is the meaningful "as-of" stamp (the data version);
  CI records when it ran. Byte-identical output requires a *total* order on every list — providers by
  id, sites by (file, line, kind, evidence) to break ties, jurisdictions sorted — plus
  `json.dumps(sort_keys=True)` so object key order can't drift. `# ponytail: deterministic >
  audit-timestamp; CI already records run time`.
- **Non-gating carve-out is a MODIFIED requirement, not silent.** The existing "CI exit code"
  requirement is unconditional (non-zero on any violation); `--format sbom` exits 0 regardless, so the
  change MODIFIES that requirement to scope the gate to non-export formats rather than contradicting it.
- **Component granularity = provider, with call sites nested.** Each component lists the provider's
  resolved jurisdiction(s) and every `{file, line, kind, evidence, jurisdiction}` site. A new provider
  or a new jurisdiction is a visible diff. No top-level scanned-path field — it is implicit in the
  sites (add when a consumer needs it).
- **The export does not gate CI (exit 0).** "Give me the manifest" is not "run the gate." Even with a
  failing `--policy`, `--format sbom` emits every flow severity-free and exits 0.

## Risks / Trade-offs

- Native schema means consumers can't drop it into existing SBOM tooling yet → acceptable; the schema
  id is versioned and a CycloneDX exporter is additive.
- No timestamp may surprise auditors expecting one → the KB date + external CI metadata cover provenance.
