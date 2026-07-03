## 1. Provenance knowledge base

- [x] 1.1 Create `borderlint/data/provenance.json`: advisory note, `updated` date, model-ID
      patterns (managed-platform IDs, bare API names, aggregator-qualified IDs, hub repo IDs) →
      `{org, bloc}`, and first-party provider defaults (OpenAI, Anthropic, DeepSeek, Mistral,
      Zhipu, Moonshot, xAI, Cohere, AI21, Azure OpenAI, …) — no defaults for multi-model hosts
      (Bedrock, Vertex) or aggregators (D3)
- [x] 1.2 Extend `kb.py`: load the provenance map, `_valid_provenance` against the vocabulary
      (`us eu cn uk ru in il ca unknown`), user-KB merge with precedence and invalid-token
      rejection (Requirement: Provenance bloc vocabulary; User provenance overrides)

## 2. Resolution & detection

- [x] 2.1 Implement `kb.resolve_provenance(model_ref, provider_id)`: anchored longest-match over
      patterns, tier-2 first-party provider default, else `unknown` (Requirement: Two-tier
      provenance resolution; D3, D4)
- [x] 2.2 Extend `detect.py`: `model_reference` detection kind matching string literals against
      the map's anchored patterns in Python and TS/JS scans (Requirement: Detect model
      references)
- [x] 2.3 Add `provenance: str = "unknown"` to `Detection`; populate in `scan()` via same-file
      binding — model reference binds to provider detections in its file, standalone finding
      otherwise (Requirement: Model references bind to same-file provider detections)

## 3. Policy evaluation

- [x] 3.1 Extend `policy.py`: mirror the vocabulary constant, validate `provenance` block tokens
      at load time (Requirement: Optional provenance policy block)
- [x] 3.2 Evaluate the opt-in `provenance` block in `evaluate()`: allow-list mismatch →
      `provenance` reason; `unknown` → `provenance_unknown` per `on_unknown`; absent block →
      no provenance reasons ever (Requirement: Provenance deny-by-default evaluation)
- [x] 3.3 Extend `_severity`: `provenance` in `fail_on` gates mismatches; `on_unknown: "fail"`
      gates `provenance_unknown` on its own — symmetric, no double gate (Requirement: Provenance
      failure set with a symmetric unknown gate; D5)
- [x] 3.4 Confirm waiver downgrade covers provenance failures and never overrides a provider
      deny (Requirement: Waiver applies to provenance findings)

## 4. Reporting

- [x] 4.1 Extend `report.py`: `PROVENANCE` display map, text segment, JSON `provenance` field,
      Mermaid label (provenance appended when it differs from sovereignty — design open
      question, confirm against real diagrams), SARIF message, SBOM `provenances`; REASON
      entries for `provenance` / `provenance_unknown` (Requirement: Provenance in report output)

## 5. Tests

- [x] 5.1 Resolution: pattern match per ID form (managed-platform, bare, aggregator-qualified,
      hub), first-party default, multi-model host → `unknown`, longest-match precedence
- [x] 5.2 Detection & binding: same-file binding, standalone model reference, no false positive
      on a resembling variable name
- [x] 5.3 Policy: absent-block regression guard, mismatch, allow, `unknown` warn/fail (symmetric
      gate), `fail_on`, waiver, invalid tokens in user KB and policy
- [x] 5.4 Reporting: provenance across text/JSON/Mermaid/SARIF/SBOM

## 6. Docs & examples

- [x] 6.1 `examples/residency.json`: annotated `provenance` block
- [x] 6.2 `CAPABILITIES.md` §3.2 provenance subsection + capability map row; `README.md`
      mention alongside sovereignty
