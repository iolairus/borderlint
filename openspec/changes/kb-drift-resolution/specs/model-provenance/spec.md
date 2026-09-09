# model-provenance Delta

## ADDED Requirements

### Requirement: September drift-run model families resolve provenance
The bundled provenance map SHALL resolve model identifiers of the twelve families surfaced by
the 2026-09-07 freshness run — ByteDance Seed, Baidu CoBuddy, and StepFun Step (bloc `cn`);
Microsoft MAI, Google nano-banana, Microsoft Research multilingual-e5, Thinking Machines Lab
Inkling, poolside Laguna, PrismML Ternary-Bonsai, and BigScience mt0 (bloc `us`); JetBrains
Mellum (bloc `eu`); MindAI Macaron (bloc `sg`) — to their developer organisations' blocs,
keeping the full literal as evidence. Pattern stems MUST be specific enough that identifiers
outside these families do not resolve through them.

#### Scenario: Chinese-bloc family resolves
- **WHEN** a model reference `deepinfra/ByteDance/Seed-1.8` is detected
- **THEN** it resolves to provenance bloc `cn` with developer organisation ByteDance

#### Scenario: US-bloc family resolves
- **WHEN** a model reference `deepinfra/thinkingmachines/Inkling` is detected
- **THEN** it resolves to provenance bloc `us` with developer organisation Thinking Machines Lab

#### Scenario: EU and Singapore families resolve
- **WHEN** model references `wandb/JetBrains/Mellum2-12B-A2.5B-Instruct` and
  `novita/mindai/macaron-v1-tall` are detected
- **THEN** the first resolves to provenance bloc `eu` and the second to bloc `sg`

#### Scenario: Generic stems do not over-match
- **WHEN** an unrelated model reference sharing a generic stem prefix (for example a
  hypothetical `seedling-1b` or `stepwise-2`) is detected
- **THEN** it does not resolve through the new patterns and keeps provenance `unknown`
