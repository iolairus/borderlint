## 1. Drift checker

- [ ] 1.1 `upstream_models` returns `(key, litellm_provider)` pairs (D1)
- [ ] 1.2 `model_coverage_gap(models, kb, suppression=None)`: exclude ignored providers' ids; count speech-category first-party-default providers' ids (direct `_norm` id or alias target, `kb.default_provenance != "unknown"`, category `speech`) as covered; inference providers and multi-model hosts unchanged (D1, "Model provenance coverage check")
- [ ] 1.3 Wire in `main()`

## 2. Tests

- [ ] 2.1 Ignored provider's id excluded; speech provider's tier covered (via alias and direct); first-party inference provider's novel id still reported; multi-model host's uncovered id still reported
- [ ] 2.2 Update existing drift tests to the pair-based signature

## 3. Validation

- [ ] 3.1 Full suite + `openspec validate kb-drift-model-provider-context --strict`; live run measures the residue drop
