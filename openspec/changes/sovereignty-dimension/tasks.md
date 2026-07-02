## 1. Sovereignty knowledge base

- [ ] 1.1 Create `borderlint/data/sovereignty.json` with an `updated` date, a per-bloc `source` note, and a `providers` map keyed by provider id → sovereignty bloc, covering every provider in `providers.json` (us for OpenAI/Anthropic/Google/AWS/Azure/Meta/xAI/etc.; cn for DeepSeek/Alibaba/Tencent/Baidu/Zhipu/Moonshot/Volcengine/MiniMax; eu for Mistral; uk for Stability; ru for GigaChat; in for Sarvam; il for AI21; local for Ollama/local; unknown for aggregators and custom endpoints)
- [ ] 1.2 Add an optional `sovereignty` field to each entry in `borderlint/data/providers.json` mirroring the map (provider-level), and a host-level `sovereignty` override on the AWS-China ring-fenced case (Sinnet-operated `cn-north-1`/`cn-northwest-1` → `cn`) to validate the override path
- [ ] 1.3 Document in `sovereignty.json` that the map is advisory (surfaces compelled-disclosure exposure, never adjudicates legality)

## 2. KB resolution

- [ ] 2.1 In `borderlint/kb.py`, add a `resolve_sovereignty(provider_id, host)` function that returns the sovereignty bloc: host-level override → provider-level value → bundled map → `unknown`; loopback hosts → `local`
- [ ] 2.2 Extend the flow/detection dataclass to carry a `sovereignty` attribute, populated during resolution; ensure region-in-endpoint providers (Bedrock, Azure OpenAI, Vertex) inherit the provider sovereignty regardless of resolved residency (D3)
- [ ] 2.3 Add a `_valid_sovereignty(token)` guard accepting only `us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`, `local`, `unknown`; reject user-supplied tokens outside the vocabulary with an error
- [ ] 2.4 Merge user-supplied sovereignty overrides (provider-id and host-level) additively over the bundled map, with user entries taking precedence on conflict

## 3. Policy evaluation

- [ ] 3.1 In `borderlint/policy.py`, parse the optional `sovereignty` block (`classifications`, `on_unknown` default `warn`); when absent, set a flag that disables all sovereignty evaluation (D4, non-breaking)
- [ ] 3.2 Add a `sovereignty` reason to `evaluate()`: when the block is present and the active classification has a sovereignty allow-list, a flow whose sovereignty is outside the list gets `sovereignty`; `local` is exempt (mirrors residency `local` exemption); `unknown` follows `on_unknown`
- [ ] 3.3 Extend `_severity()` and the `fail_on` handling to recognise `sovereignty`; default `fail_on` does NOT include `sovereignty` (warns only unless opted in)
- [ ] 3.4 Extend the waiver path to downgrade a `sovereignty` failure to `waived`, but never override an explicit provider deny-list entry

## 4. Reporting

- [ ] 4.1 In `borderlint/report.py`, add a `SOVEREIGNTY` label map (`us`→"United States", `eu`→"European Union", `cn`→"Mainland China", `uk`→"United Kingdom", `ru`→"Russia", `in`→"India", `il`→"Israel", `local`→"Local", `unknown`→"Unknown")
- [ ] 4.2 Add a `Sovereignty` column to the text report (alongside jurisdiction, never replacing it)
- [ ] 4.3 Add a `sovereignty` field to each finding in the JSON report
- [ ] 4.4 Append the sovereignty bloc to Mermaid node labels (inside the existing double-quoted, escaped label)
- [ ] 4.5 Add `sovereignty` to the `REASON` map in `report.py` ("sovereignty outside the allow-list for this data class")

## 5. Examples and docs

- [ ] 5.1 Add an annotated `sovereignty` block to `examples/residency.json` showing a `customer-pii` sovereignty allow-list of `eu`, `uk`, `local` with `fail_on: ["sovereignty"]`
- [ ] 5.2 Update `CAPABILITIES.md` with a sovereignty subsection: the dimension, the bloc vocabulary, the opt-in policy block, and the non-adjudicative scope note
- [ ] 5.3 Update `README.md` to mention the sovereignty dimension and link to the capabilities subsection

## 6. Tests

- [ ] 6.1 `test_sovereignty_resolution`: Bedrock `ap-east-1` → residency `hk`, sovereignty `us`; DeepSeek → `cn`; Stability → `uk`; GigaChat → `ru`; Sarvam → `in`; AI21 → `il`; Mistral → `eu`; Ollama/loopback → `local`; litellm/custom host → `unknown`
- [ ] 6.2 `test_sovereignty_host_override`: AWS China Sinnet host resolves to sovereignty `cn` via the host-level override
- [ ] 6.3 `test_sovereignty_policy_absent`: a policy with no `sovereignty` block produces no `sovereignty` reason and exit code is unchanged (regression guard)
- [ ] 6.4 `test_sovereignty_evaluation`: allow-list `eu`,`uk`,`local`; a `us`-sovereignty flow gets `sovereignty` reason; `eu` passes; `local` exempt; `unknown` warns under `on_unknown: warn`
- [ ] 6.5 `test_sovereignty_fail_on`: with `fail_on: ["sovereignty"]` a mismatch fails the run; without it, the same mismatch only warns
- [ ] 6.6 `test_sovereignty_waiver`: a justified waiver downgrades a sovereignty failure to `waived`; a provider deny-list entry is not waived
- [ ] 6.7 `test_sovereignty_reporting`: text column present, JSON `sovereignty` field present, Mermaid label includes the bloc
- [ ] 6.8 `test_sovereignty_invalid_token`: a user-supplied sovereignty map with an unrecognised bloc is rejected with an error

## 7. Validation

- [ ] 7.1 Run `openspec validate sovereignty-dimension --strict` and resolve any reported issues
- [ ] 7.2 Run the full `pytest` suite and confirm green
- [ ] 7.3 Manually run `borderlint scan` on `examples/` with the annotated sovereignty policy and confirm the report shows the new dimension
