## 1. Project scaffolding

- [ ] 1.1 Create the `borderlint` Python package and `pyproject.toml` (console entry point `borderlint`, PyYAML runtime dep, pytest dev dep)
- [ ] 1.2 Define core data models: Provider, Detection, Finding, Policy
- [ ] 1.3 Set up the pytest layout and a smoke test that imports the package

## 2. Provider knowledge base (jurisdiction-classification)

- [ ] 2.1 Author the bundled `providers.yaml` with east-west coverage (OpenAI, Anthropic, Google, Azure OpenAI, Bedrock, Mistral, Cohere + Tencent Hunyuan, Alibaba DashScope, DeepSeek, Moonshot, Zhipu, Baidu) — SDK names, endpoint hosts, jurisdictions
- [ ] 2.2 Encode region-specific endpoints (`dashscope-intl` → `sg` vs `dashscope` → `cn`) and region-in-endpoint unknowns (Azure OpenAI, Bedrock)
- [ ] 2.3 Implement the KB loader and lookups (match SDK, match endpoint, resolve jurisdiction) with `GBA` alias expansion to `hk` + `CN-GBA`
- [ ] 2.4 Support a user-supplied / override knowledge base
- [ ] 2.5 Tests: provider→jurisdiction resolution, `dashscope-intl` vs mainland, GBA expansion, unknown jurisdiction, custom KB

## 3. Flow detection (flow-detection)

- [ ] 3.1 Implement the Python AST scanner: SDK imports + endpoint string literals → detections with `file:line`
- [ ] 3.2 Implement the config/text scanner (`.env`, `.yaml`, `.toml`, `.json`, …) for endpoint hosts
- [ ] 3.3 Directory walking with exclusions (`.git`, `node_modules`, `venv`, build dirs) and detection de-duplication
- [ ] 3.4 Make scanning resilient: skip unparseable files and continue
- [ ] 3.5 Tests: import detection, endpoint detection, excluded dirs, resilience, evidence/`file:line`

## 4. Residency policy (residency-policy)

- [ ] 4.1 Implement the JSON policy loader (classification → allow-list, `on_unknown`, built-in + user-defined classifications)
- [ ] 4.2 Implement evaluation: per-run classification, deny-by-default, GBA alias, unknown handling → Findings with verdicts
- [ ] 4.3 Support provider allow/deny lists and a configurable failure set (default fails on residency + denied-provider)
- [ ] 4.4 Support a declared home regime (`pdpo` | `pipl`) that selects which arrangement references are surfaced
- [ ] 4.5 Tests: SG-in/MY-out deny-by-default, GBA token permits a CN-GBA flow, unknown=fail vs warn, user-defined classification, denied provider, failure-set config, home-regime selection

## 5. CLI & reporting (cli-and-reporting)

- [ ] 5.1 Implement `borderlint scan <path> --policy --classification --format` (argparse) with CI exit codes
- [ ] 5.2 Implement reporters: human-readable text, JSON, and Mermaid flow map
- [ ] 5.3 Implement inventory mode (no policy → report flows + jurisdictions, exit zero)
- [ ] 5.4 Surface arrangement reference links (GBA Standard Contract) relevant to the declared home regime for flagged cross-border flows
- [ ] 5.5 Tests: non-zero exit on violation, zero on clean, JSON/Mermaid output, inventory mode, arrangement link

## 6. Packaging, examples & verification

- [ ] 6.1 Add an example policy (`residency.json`) and an example app under `examples/`
- [ ] 6.2 Update README with quickstart, usage, and the honest limitations list
- [ ] 6.3 End-to-end check: run `scan` on the examples for both a violation and a clean case and confirm exit codes
