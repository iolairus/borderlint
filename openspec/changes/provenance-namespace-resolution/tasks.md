# Tasks: provenance-namespace-resolution

## 1. Data — named runtimes (model-provenance req, D1)

- [x] 1.1 Add `ollama/`, `vllm/`, `lmstudio/` to `passthrough_orgs` in
      `borderlint/data/provenance.json` and extend the passthrough note to say these are local-runtime
      launchers rather than quantizer hubs
- [x] 1.2 Confirm no bundled pattern begins with those three names (so stripping cannot change an
      existing resolution)

## 2. Resolution — host-like namespaces (model-provenance req, D2)

- [x] 2.1 Add `KB.model_candidates(literal)` in `borderlint/kb.py`: ordered normalized forms — today's
      form first, then one leading host-like segment dropped at a time with passthrough re-applied,
      then the final segment once a host segment has been dropped
- [x] 2.2 Rewrite `KB.match_model()` to iterate candidates against `_prov_prefixes` (longest-prefix wins
      within a candidate), returning the original literal as evidence
- [x] 2.3 Leave `normalize_model()` byte-for-byte unchanged in behaviour and document that it is the
      primary form of the candidate list

## 3. Deny list (residency-policy req)

- [x] 3.1 Evaluate `deny_models` against `KB.model_candidates()` in `borderlint/policy.py`, keeping the
      no-kb fallback and the no-bound-model rule

## 4. Tests

- [x] 4.1 Positive: runtime-qualified, host-qualified, multi-segment registry and HF-URL forms resolve to
      the developer bloc for both a `cn` and a `us` family
- [x] 4.2 Negative (regression guards): `src/deepseek/client.py`, `solarwinds-agent`, bare `falcon`,
      `dir/qwen2.5.zip` still resolve nothing
- [x] 4.3 End-to-end: `deny_models: ["deepseek"]` fails the four evasion references from the proposal
- [x] 4.4 Full suite green, including the pre-existing provenance and deny tests unchanged
- [x] 4.5 Boundary pins for the final-segment fallback (design R1): near-miss internal image names stay
      unmatched, and the accepted over-attribution cases are asserted so the trade-off cannot drift
- [x] 4.6 Pin the documented scheme limit (design R2): `https://…` resolves nothing, the scheme-less host
      form resolves
- [x] 4.7 Pin that the deny over-reach is fail-closed and scopable by narrowing the `deny_models` entry

## 5. Docs

- [x] 5.1 README provenance section: state that registry and runtime namespaces are stripped before
      matching, and name the residual limit (an unmapped family resolves through tier-2)
- [x] 5.2 Bump `updated` in `borderlint/data/provenance.json` — the map was touched (three passthrough orgs
      plus the note), and the freshness checker's 90-day staleness clock keys off that field
- [x] 5.3 Correct the README browser-URL claim: a URL carrying its scheme resolves nothing, so document
      the scheme-less host form and name scheme stripping as a follow-up rather than promising it
- [x] 5.4 Record the final-segment over-attribution trade-off in design.md (Risks R1) with mitigations,
      and mirror both accepted consequences into the spec deltas
