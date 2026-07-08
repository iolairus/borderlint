## Why

Provenance filters by bloc only, so "no DeepSeek-family weights regardless of host" is only
expressible as "no `cn` weights" — which also blocks Qwen, GLM, and Kimi. Sector rules and
client policies sometimes name model families, not legal regimes (HKMA model-risk
questionnaires ask *which vendor's model*). The KB already records the developer org per
pattern, but it never reaches findings, so even reports make the reader decode `exaone-3.5`
into "LG AI Research" by hand.

## What Changes

- The `provenance` policy block gains an optional `deny_models` list of anchored model-id
  prefixes. A flow — or standalone model reference — whose model identifier matches a deny
  entry is reported with a `model_denied` reason — a default member of the failure set, exactly
  like `denied_provider`, and equally beyond the reach of waivers. Lifting it is an explicit,
  reviewed `fail_on` edit, never an inline comment.
- Deny matching uses the same identifier normalization as the provenance map (GGUF basename,
  redistributor-org stripping, version-pin stripping), so a denied family cannot be dodged by
  a `TheBloke/…` repo path or an `@`-version suffix.
- The developer organisation from the matched pattern is threaded onto findings: the JSON
  report gains a `model_org` field, the text report names the org beside the model, and the
  SBOM carries it per site.
- A flow with no bound model identifier cannot match a deny entry — the deny list is
  evidence-based, documented as such. Deny entries are validated at policy load (non-empty,
  minimum length).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `residency-policy`: the provenance block accepts `deny_models`; a new deny-evaluation
  requirement; the waiver requirement extends its no-override rule to model denies.
- `cli-and-reporting`: the model's developer organisation is reported when known.

## Impact

- `borderlint/kb.py` — `match_model` also returns the pattern's org.
- `borderlint/detect.py` — `model_org` on detections.
- `borderlint/policy.py` — `deny_models` load/validation + evaluation + severity.
- `borderlint/report.py` — org in text/JSON/SBOM; `model_denied` reason description.
- `README.md`, `examples/residency.json`, tests.

## Non-goals

- No org-string policy vocabulary: denies are model-id patterns, the currency the KB already
  maintains — org names as policy tokens would need their own freshness discipline.
- No allow-by-model (blocs remain the allow-list unit; deny is the targeted exception).
- No runtime resolution: an unbound model stays invisible to the deny list, same
  static-visibility posture as every other check.
