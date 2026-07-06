## 1. KB

- [ ] 1.1 Plumb org through load: `load_kb`/`set_provenance_patterns` carry (pattern, bloc, org); `match_model` returns `(identifier, bloc, org)` (None for user patterns); update call sites incl. the exact-tuple assertion in tests (D4)
- [ ] 1.2 Expose the normalization steps for deny matching (basename / passthrough / version-pin) as a reusable helper (D2)

## 2. Detection

- [ ] 2.1 `Detection.model_org: str | None`; threaded in `_attach_models` and standalone findings (D4)

## 3. Policy

- [ ] 3.1 Load + validate `deny_models` (strings, length ≥ 3 lowercased; error names the entry) (D5, "Optional provenance policy block")
- [ ] 3.2 Evaluate: identifier normalized via the `kb` argument (lowercase raw-prefix fallback when `kb=None`) vs deny prefixes → `model_denied` reason on bound flows and standalone references; no identifier → no match (D1, D2, D6, "Model deny-list evaluation")
- [ ] 3.3 Severity: `model_denied` joins the default `fail_on` set beside `denied_provider`; the waiver gate blocks it identically (D3, "Waiver applies to provenance findings")

## 4. Reporting

- [ ] 4.1 REASONS entry for `model_denied`; text ` [model: X — Org]`; JSON `model_org`; SBOM per-site org ("The model's developer organisation is reported")

## 5. Docs & validation

- [ ] 5.1 README provenance paragraph + `examples/residency.json` gain `deny_models`; CAPABILITIES row
- [ ] 5.2 Tests per scenario: deny on Bedrock-bound ref, redistributor dodge, standalone, no-model no-deny, waiver override refused, load-time rejection, org in JSON/text, user-pattern no-org unchanged
- [ ] 5.3 Full suite + `openspec validate provenance-model-deny --strict`
