# model-provenance Delta

## ADDED Requirements

### Requirement: MAI-Code, ScaleDown, Copilot Chat, and Microsoft Decision families resolve provenance
The bundled provenance map SHALL resolve the following drift-run families, all patterns
matched case-insensitively, anchored, longest-first per the existing matching rules:

- `mai-code` and the qualified `github_copilot/mai-code` → bloc `us`, organisation
  Microsoft AI (the MAI-Code in-house coding-model family, per the official
  `microsoft/MAI-Code` repository), mirroring the existing `mai-*` bare/qualified
  convention.
- `scaledown/` as an org-namespace prefix → bloc `us`, organisation ScaleDown, covering
  every endpoint name behind it (`classify`, `compress`, `decisions`, `extract`,
  `summarize`): ScaleDown serves its own task-specific small language models. NO bare
  `classify`, `compress`, `decisions`, `extract`, or `summarize` stem SHALL exist — each
  is a generic English word that would over-match unrelated identifiers. The map's tier-2
  provider defaults SHALL map `scaledown` → `us` (a first-party-only provider).
- The qualified `microsoft_365_copilot/chat` form → bloc `us`, organisation Microsoft.
  NO bare `chat` stem SHALL exist. The provider SHALL carry NO tier-2 default: Microsoft
  routes Copilot across model vendors, so unbound flows remain `unknown`.
- `microsoft-decision` and the qualified `azure_ai/microsoft-decision` → bloc `cn`,
  organisation naming base and tuner (`Alibaba (Microsoft Decision-1 post-training)`):
  Microsoft-Decision-1 is Microsoft-published but documented by Microsoft as post-trained
  on Qwen3.5-9B, so the fine-tunes-inherit-base rule assigns Alibaba's bloc (the Bespoke
  Nimble LoRA precedent).

#### Scenario: MAI-Code resolves on both surfaces
- **WHEN** model references `github_copilot/mai-code-1.1-flash` and `mai-code-1-flash` are
  detected
- **THEN** the first resolves through the qualified pattern and the second through the
  bare stem, both to bloc `us` with organisation Microsoft AI

#### Scenario: ScaleDown endpoint names resolve only under the namespace
- **WHEN** model references `scaledown/classify`, `scaledown/compress`,
  `scaledown/decisions`, `scaledown/extract`, and `scaledown/summarize` are detected
- **THEN** each resolves to bloc `us` with organisation ScaleDown

#### Scenario: Generic stems do not over-match
- **WHEN** unrelated model references sharing a stem (for example a hypothetical
  `chat-with-pdfs`, `classification-9b`, or `summarize-pro-2`) are detected
- **THEN** none resolves through any new pattern (no bare `chat`, `classify`,
  `summarize`, or sibling stems exist); each keeps provenance `unknown` unless an
  existing pattern independently covers it

#### Scenario: Copilot Chat resolves qualified; unbound Copilot flows stay unknown
- **WHEN** a model reference `microsoft_365_copilot/chat` is detected, and separately an
  unbound flow on provider `microsoft_365_copilot` carries no model reference
- **THEN** the reference resolves to bloc `us` with organisation Microsoft, and the
  unbound flow keeps provenance `unknown` (the provider has no tier-2 default — Copilot
  routes across model vendors)

#### Scenario: Microsoft-Decision-1 inherits the Qwen bloc
- **WHEN** model references `azure_ai/Microsoft-Decision-1` and `Microsoft-Decision-1`
  are detected
- **THEN** both resolve to bloc `cn` with the organisation label naming base and tuner
  (`Alibaba (Microsoft Decision-1 post-training)`), per the fine-tunes-inherit-base rule
  — publisher branding does not override weight lineage

#### Scenario: Unbound ScaleDown flows inherit the first-party default
- **WHEN** an unbound flow on provider `scaledown` carries no model reference
- **THEN** it resolves provenance `us` via the tier-2 provider default (ScaleDown serves
  only its own models)
