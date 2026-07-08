## Context

The provenance dimension resolves flows to blocs; the policy allow-lists blocs
(`policy.py` `mprov_*` bindings). The KB's patterns each carry `{org, bloc}`
(`provenance.json`), but `match_model` (`kb.py`) returns only `(identifier, bloc)`.
The provider deny-list (`providers.deny`) is the shipped precedent: `denied_provider` is a
default member of the failure set and a waiver cannot override it while it is in `fail_on`
(`policy.py` `_severity`/waiver gate). The KB's org is discarded at load time — `load_kb`
builds bloc-only pattern maps — so threading it means widening the pattern plumbing, not just
`match_model`'s return.

## Goals / Non-Goals

**Goals:** family-level deny expressible without blocking a whole bloc; org visible in
findings; deny undodgeable via redistributor paths or version pins.
**Non-Goals:** org-string policy tokens; allow-by-model; runtime model resolution.

## Decisions

### D1 — Deny by model pattern, not org string
**Decision:** `deny_models` entries are anchored lowercase model-id prefixes, the same currency
as the KB's patterns (`deepseek`, `deepseek.`, `deepseek/`).
**Rationale:** Patterns are what the KB curates and keeps fresh; a policy written against them
matches exactly what the scanner can see. Org strings would be a second taxonomy needing its
own vocabulary, validation, and freshness discipline — and orgs rename (Z.ai) faster than
their model prefixes do.
**Alternatives rejected:**
- *Deny by org name matched against the KB's org field.* Rejected: ties policy validity to KB
  org spellings ("LG AI Research" vs "LGAI"), which are display strings, not identifiers.
- *Deny by bloc with per-family exceptions.* Rejected: inverts into an allow-list with double
  negatives; the simple deny mirrors the provider deny users already know.

### D2 — Deny matching reuses the map's normalization pipeline
**Decision:** A deny entry matches when the flow's model identifier — after the same GGUF
basename, redistributor-passthrough, and version-pin normalization `match_model` applies —
starts with the entry.
**Rationale:** Without it, `TheBloke/deepseek-llm-7B-GGUF` or `deepseek-v3@2412` dodges a
`deepseek` deny; the deny must be at least as strong as the resolution it polices.
**Alternatives rejected:**
- *Raw-prefix matching on the literal.* Rejected: the dodge above; every normalization rule
  the map gained would become a deny bypass.

### D3 — Exactly the provider-deny semantics, one deny model
**Decision:** `model_denied` joins the failure set's defaults alongside `denied_provider`;
waivers cannot override it, mirroring the shipped waiver gate. Applies to bound flows and
standalone `model_reference` findings alike (both carry the weights signal the deny targets).
**Rationale:** Two denies with one semantics is learnable; an explicit deny is the org's
strongest statement, and the sanctioned escape hatch — a reviewed `fail_on` edit — is the same
for both. The spec review corrected an earlier draft that claimed the provider deny was
unconditional; aligning beats inventing a third, stronger severity pathway.
**Alternatives rejected:**
- *Unconditional failure, independent of `fail_on`.* Rejected: no shipped precedent; a new
  severity pathway for one reason complicates `_severity` and surprises anyone who has
  customized `fail_on`.
- *Waivable deny.* Rejected: subverts the one control meant to be non-negotiable; the
  escape hatch is editing the policy, which is reviewed.

### D4 — Org threading is additive reporting
**Decision:** `match_model` returns `(identifier, bloc, org)`; detections gain
`model_org: str | None`; JSON adds `model_org`, text renders ` [model: X — Org]`, SBOM carries
it per site. No format loses or changes an existing field.
**Rationale:** Same additive-reporting posture as every dimension change; the org makes deny
triage and future evidence packs readable without decoding model names.
**Alternatives rejected:**
- *Org only in the SBOM.* Rejected: deny triage happens in text/JSON CI output, not the SBOM.
- *A separate org lookup keyed by bloc.* Rejected: orgs belong to patterns, not blocs; a bloc
  holds many orgs.

### D5 — Load-time validation, minimum length
**Decision:** `deny_models` entries must be strings of length ≥ 3 after lowercasing; empty or
shorter entries fail policy load with an error naming the entry.
**Rationale:** A 1–2 character prefix (`m`) would deny half the map by accident; 3 matches the
identifier gate's own minimum.

### D6 — Deny evaluation needs the knowledge base argument
**Decision:** Deny matching normalizes via the KB (`evaluate(..., kb=...)`, which the CLI
always passes); with `kb=None` the deny falls back to lowercase raw-prefix matching.
**Rationale:** The normalization state (passthrough orgs) lives on the KB; the CLI path — the
only shipped caller — always supplies it, and the fallback degrades safely (a raw prefix still
matches the common unqualified forms).

## Risks / Trade-offs

- **[Over-broad deny]** `deepseek` also denies a hypothetical benign `deepseek-detector`
  utility string that resolves as a model reference. → Anchored prefixes and the existing
  identifier gate bound this; the failure is loud and the pattern is the user's own choice.
- **[Deny without a bound model]** `import deepseek` with no model string resolves provenance
  via tier 2 but carries no identifier — the deny cannot fire; the bloc allow-list still can.
  → Documented; evidence-based deny is the honest scope of static analysis.

## Migration Plan

1. `match_model` 3-tuple + call-site updates; `model_org` threading.
2. Policy load/validation, evaluation (`model_denied`), severity, waiver exclusion.
3. Reports; README + example policy; tests per scenario.
4. Rollback: revert — absent `deny_models`, behaviour is byte-identical.

## Open Questions

None.
