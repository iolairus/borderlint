## Summary

Adds a **sovereignty** dimension to borderlint, modelling which government can compel disclosure of a flow's data — distinct from residency (where the endpoint physically sits).

A US-headquartered provider (AWS, Azure, GCP, OpenAI, Anthropic) is subject to US compelled-disclosure law (CLOUD Act 2018, FISA 702, Patriot Act §215) regardless of the endpoint region. So a flow to AWS Bedrock `ap-east-1` is residency-clean for a PDPO policy (residency `hk`) yet remains under **US sovereignty** for disclosure. Residency alone cannot express *"data may rest in `hk` but must not be under US compelled-disclosure jurisdiction"* — a posture many HK/GBA and EU entities in fact hold.

## What changes

- **New `sovereignty` dimension** — each flow carries a sovereignty bloc derived from the provider's home legal regime (not the endpoint region). Opt-in and non-breaking: absent the policy block, behaviour is identical to before.
- **Bloc vocabulary:** `us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`, `local`, `unknown`.
- **Bundled KB** (`borderlint/data/sovereignty.json`) — provider→bloc map, advisory (surfaces exposure, never adjudicates legality).
- **Host-level override** — AWS China regions (Sinnet/NWCD) override the provider sovereignty `us`→`cn`.
- **Policy** — optional `sovereignty` block with per-classification allow-lists, `on_unknown`, and `fail_on` support. Default `fail_on` excludes `sovereignty` (warns only unless opted in). `local` sovereignty is exempt. Waivers apply.
- **Reporting** — text column, JSON `sovereignty` field, Mermaid label append, SARIF message, SBOM `sovereignties`.
- **Docs** — `CAPABILITIES.md` §3.1, `README.md` mention, annotated `examples/residency.json`.

## Non-goals

- Does not adjudicate whether a statute legally applies (borderlint surfaces; the policy decides).
- Does not model EU-US Data Privacy Framework adequacy.
- Open-weights provenance / export-control risk deferred to a separate change.

## Validation

- `openspec validate sovereignty-dimension --strict` ✓
- `pytest` — 96 passed ✓ (8 new sovereignty tests)
- Manual `borderlint scan` on `examples/` confirms the new dimension in text + JSON output ✓

## Traceability

Change: `sovereignty-dimension` — proposal, design, specs, and tasks in `openspec/changes/sovereignty-dimension/`.

Commits:
- `spec(sovereignty-dimension)`: propose sovereignty dimension orthogonal to residency
- `feat(sovereignty)`: add sovereignty dimension orthogonal to residency
