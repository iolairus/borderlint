<!-- PR for /opsx change faang-data-practices-curation -->

## Summary

Completes data-practices coverage for every FAANG first-party AI platform in the KB. The four
platforms — Meta Llama API, Google Vertex AI, Microsoft Azure Foundry, and GitHub Copilot/Models
— were fully detectable with sovereignty mappings but rendered "not curated" in the evidence
pack and KB website, exactly where enterprise traffic concentrates. Each new entry is grounded
in its platform's current governing document (all verified live on 2026-08-23):

- **meta_llama** — training default **no** for Standard Services ("Meta will not use Content
  from Standard Services to train Meta Models", ToS §5.1); the **tier split is disclosed**:
  Discounted Services content MAY be used to train Meta models by default (§6.1), disassociated
  from your account/key. Retention per §4.4; subprocessor list published.
- **vertex_ai** — training default **no** citing the Cloud Service Specific Terms "Training
  Restriction" (no training/fine-tuning without prior permission, GA and pre-GA). Retention
  documents the per-feature conditions: abuse-monitoring prompt logging with an exemption path,
  non-disableable Grounding windows (3d Search / 30d Maps), opt-in request-response logging,
  Live-API session resumption, and project-isolated 24h in-memory caching.
- **azure_foundry** — mirrors the `azure_openai` posture from the current Foundry data-privacy
  doc (prompts/completions NOT used to train foundation models; stateless models;
  Global/DataZone processing scope; ContentLogging=false verification), plus a partner-catalog
  caveat.
- **github_copilot** — training default **no** citing the **GitHub Generative AI Services Terms**
  §3 ("GitHub will not use Inputs or Outputs to train generative AI models…"), which superseded
  the deprecated Copilot Product-Specific Terms on 2026-03-05; retention varies per product
  documentation.

All stale/unavailable claims: none. Strictly advisory — verdicts unchanged.

## Traceability

| Artifact | Reference |
|----------|-----------|
| Task (Jira) | N/A |
| OpenSpec change | `openspec/changes/faang-data-practices-curation/` |
| Spec deltas | ADDED `provider-data-practices` (`Curated facts for FAANG first-party AI platforms`; `Complete citations without stale notes`) |

## Changes

- `borderlint/data/data_practices.json`: four new entries (KB grows to 16 curated providers),
  each fact carrying url + locator + retrieval date 2026-08-23.
- `tests/test_borderlint.py`: new `test_data_practices_faang_entries_curated` asserting each
  entry's expected training default, verbatim locator quotes (Meta §5.1, GenAI Services §3,
  Foundry foundation-model commitment), tier-split disclosure, catalog caveat, providers.json
  membership, and absence of unavailability claims; schema test relaxed to allow the self-citing
  `subprocessors` object to also appear under `citations`.

## Verification

- [x] `openspec validate faang-data-practices-curation --strict` passes
- [x] All tasks in tasks.md checked (8/8)
- [x] Tests covering each acceptance scenario (full suite: 187 passed)
- [x] Review pass probed every scenario live plus rendering seams: KB website pages render the
  Data Practices sections with training rows for all four; evidence-pack scans of each platform's
  host produce register entries with citation links; loader validation passes on all citations
