# model-provenance Delta

## ADDED Requirements

### Requirement: MiMo model identifiers resolve provenance
The bundled provenance map SHALL resolve MiMo model identifiers — bare (`mimo-v2.5-pro`) and
provider-qualified (`xiaomi/mimo-…`, `novita/xiaomimimo/…`) — to the provenance bloc of their
developer organisation, Xiaomi (bloc `cn`), keeping the full literal as evidence.

#### Scenario: Bare MiMo identifier resolves
- **WHEN** a model reference `mimo-v2.5-pro` is detected
- **THEN** it resolves to provenance bloc `cn` with developer organisation Xiaomi

#### Scenario: Provider-qualified MiMo identifier resolves
- **WHEN** model references `xiaomi/mimo-v2.5-pro` and `novita/xiaomimimo/mimo-v2-flash` are detected
- **THEN** both resolve to provenance bloc `cn`
