## Context

borderlint resolves each detected AI flow to a **jurisdiction** (residency): the country/zone where
the endpoint physically sits. A HK entity's policy then allow/deny-lists that residency. This
captures *where the bytes rest* but not *who can compel their disclosure*. A US-headquartered
hyperscaler (AWS, Azure, GCP, OpenAI, Anthropic) is subject to US compelled-disclosure statutes
(CLOUD Act 2018, FISA 702, Patriot Act §215) irrespective of the region the endpoint is hosted in.
So a flow to AWS Bedrock `ap-east-1` (residency `hk`) is residency-clean for a PDPO policy yet
remains under **US sovereignty** for disclosure. Today borderlint cannot express "customer PII may
rest in `hk` but must not be under US compelled-disclosure jurisdiction" — a posture many HK/GBA
and EU entities in fact hold.

The current model has one axis (residency) and one verdict family. We add a second, orthogonal
axis (sovereignty) that is **opt-in**: when the policy declares no `sovereignty` block, behaviour
is byte-identical to today.

## Goals / Non-Goals

**Goals:**
- Model sovereignty as a distinct, per-flow attribute derived from the provider's home legal
  regime for compelled disclosure (not the endpoint region).
- Ship a bundled, maintainable sovereignty map covering the blocs that are practically distinct.
- Let a policy optionally constrain sovereignty per classification, with the same deny-by-default
  and `fail_on` ergonomics as residency.
- Keep the change non-breaking: existing policies and reports gain a column, never lose one.

**Non-Goals:**
- Adjudicating whether a statute legally applies (borderlint surfaces; the policy decides).
- Modelling EU-US Data Privacy Framework adequacy or transfer mechanisms.
- Open-weights provenance / export-control risk (separate later change).
- A sovereign for every UN member state; we model blocs.
- Runtime enforcement; borderlint is and remains a static CI check.

## Decisions

### D1 — Sovereignty is a separate attribute, not a replacement for residency
**Decision:** Each flow carries both `jurisdiction` (residency, unchanged) and `sovereignty` (new).
**Rationale:** Residency and sovereignty answer different questions and can diverge (Bedrock
`ap-east-1` = residency `hk`, sovereignty `us`). Collapsing them loses information a policy needs.
**Alternatives rejected:**
- *Fold sovereignty into jurisdiction codes (e.g. `us-controlled-hk`).* Rejected: combinatorial
  explosion of tokens, breaks the existing ccTLD model, and conflates two axes in one namespace.
- *Replace residency with sovereignty.* Rejected: residency is still independently meaningful
  (PDPO agreed-locations is a residency commitment, not a sovereignty one).

### D2 — Sovereignty blocs: `us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`, `local`, `unknown`
**Decision:** Model a small set of blocs, not per-country sovereigns.
**Rationale:** For compelled disclosure, the practical groupings are: US (CLOUD Act family), EU/EEA
(harmonised intra-EU regime; compelled disclosure routes through the member state but the bloc is
the meaningful unit for a policy), CN (DSL/CSL/PIPL), UK (Investigatory Powers Act, post-Brexit
distinct from EU), RU (SORM/Federal Security Service access), IN (DPDP Act + IT Act), IL (Israeli
surveillance framework). `local` = self-hosted, no external sovereign. `unknown` = not determinable.
**Alternatives rejected:**
- *Just `us`/`eu`/`cn` (the user's initial framing).* Rejected: incomplete. UK is a distinct
  post-Brexit sovereign (Stability AI is UK-HQ); Sber/GigaChat is RU; Sarvam is IN; AI21 is IL.
  Collapsing UK into EU or RU/CN would mislabel real compelled-disclosure exposure.
- *Per-country sovereigns (one per ccTLD).* Rejected: maintenance burden and false precision —
  most states' compelled-disclosure regimes are not meaningfully distinct for a policy's purposes,
  and we lack authoritative per-country data. Blocs are honest about our resolution ceiling.
- *An `other` catch-all.* Rejected: mirrors the `overseas` anti-pattern borderlint deliberately
  avoids; `unknown` is the honest token for "not determinable".

### D3 — Sovereignty is derived from the provider, not the endpoint host
**Decision:** Sovereignty is a property of the **provider** (its home legal regime), resolved from
the provider KB entry. Region-in-endpoint providers (Bedrock, Azure OpenAI, Vertex) inherit the
provider's sovereignty regardless of the resolved residency.
**Rationale:** Compelled disclosure reaches the provider at its corporate seat, not the data
centre. AWS Bedrock in `ap-east-1` is still AWS (US). This is the whole point of the dimension.
**Alternatives rejected:**
- *Derive sovereignty from the endpoint region.* Rejected: this would reproduce residency and
  defeat the purpose. The CLOUD Act reaches across regions precisely because the provider, not
  the region, is the legal target.
- *Per-endpoint-host sovereignty overrides.* Kept as an optional escape hatch in the KB
  (`sovereignty` on a host entry) for the rare case where a provider runs a genuinely
  ring-fenced subsidiary under a different sovereign (e.g. a CN-only JV), but the default is
  provider-level.

### D4 — Opt-in policy block; default unchanged
**Decision:** Policy gains an optional `sovereignty` block:
```json
"sovereignty": {
  "on_unknown": "warn",
  "classifications": { "customer-pii": ["eu", "uk", "local"] },
  "fail_on": ["sovereignty"]
}
```
When absent, no sovereignty evaluation occurs and no `sovereignty` reason is ever produced.
**Rationale:** Non-breaking adoption; teams opt in classification-by-classification.
**Alternatives rejected:**
- *Make sovereignty mandatory with a default allow-all.* Rejected: silent behaviour change for
  existing users on upgrade. Opt-in is the honest default.

### D5 — Aggregators and custom endpoints resolve to sovereignty `unknown`
**Decision:** Multi-provider routers (litellm, langchain, openrouter) and custom OpenAI-compatible
hosts resolve to sovereignty `unknown`, governed by `on_unknown`.
**Rationale:** The destination provider — and thus its sovereign — is chosen at runtime; borderlint
cannot statically know it. This mirrors the existing residency `unknown` handling.
**Alternatives rejected:**
- *Inherit from the most-restrictive possible destination.* Rejected: false precision and would
  over-fail legitimate aggregator use.

### D6 — Reporting: additive column/label, never replacing residency
**Decision:** Text report gains a `Sovereignty` column; JSON gains a `sovereignty` field per
finding; Mermaid node labels append the bloc. The exit code logic adds `sovereignty` to the
reason set; `fail_on` defaults do **not** include it (opt-in).
**Rationale:** Visibility without forcing a verdict change.
**Alternatives rejected:**
- *Separate sovereignty report mode.* Rejected: fragments the output; the two dimensions are most
  useful seen together.

## Risks / Trade-offs

- **[Sovereignty map accuracy]** Compelled-disclosure exposure is a legal, not purely technical,
  attribute and can change (e.g. EU-US DPF status). → Mitigation: the map is bundled JSON with an
  `updated` date and a `source` note per bloc; documented as advisory, never adjudicative. Users
  can override via the user-supplied KB.
- **[EU bloc granularity]** Treating the EU as one bloc hides member-state differences (a French
  provider answers to France). → Mitigation: documented as a deliberate modelling ceiling; the
  `eu` token is the bloc, residency stays per-country. A future change can split if needed.
- **[Provider corporate-structure complexity]** Some providers operate ring-fenced subsidiaries
  under a different sovereign (e.g. AWS China operated by Sinnet). → Mitigation: per-host
  `sovereignty` override in the KB for the known cases; `unknown` for the rest.
- **[Adoption friction]** A new dimension is cognitive load. → Mitigation: opt-in, default off,
  and the report column appears even when unconstrained (informational).

## Migration Plan

1. Add `sovereignty.json` and optional `sovereignty` fields to `providers.json` (additive).
2. Extend `kb.py` to resolve sovereignty per flow (provider-level, host-override).
3. Extend `policy.py` with the optional `sovereignty` block and `sovereignty` reason.
4. Extend `report.py` to render the new column/field/label.
5. No data migration: existing policies without the block behave identically.
6. Rollback: revert the code; the `sovereignty` fields in JSON are ignored by old code.

## Open Questions

- Should `local` sovereignty be implicitly allowed even when not in the allow-list (mirroring the
  residency `local` exemption)? Lean: yes, by symmetry — self-hosted inference has no external
  sovereign. To confirm in spec.
- Whether to surface a sovereignty reference link (e.g. CLOUD Act text) analogous to arrangement
  references. Lean: defer; reference links are a residency-feature today.
