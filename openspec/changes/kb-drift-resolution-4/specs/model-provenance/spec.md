# model-provenance Delta

## ADDED Requirements

### Requirement: Nimble, Laya, Strands Decider, and Clef model families resolve provenance
The bundled provenance map SHALL resolve the model families surfaced by the 2026-10-05
freshness run to their base families' blocs, keeping the full literal as evidence: Bespoke
Nimble (LoRA on Qwen3.5-9B) and Strands Decider (LoRA + pointer head on Qwen3.5-2B,
AWS-published) inherit Alibaba's bloc (bloc `cn`); the three Laya checkpoints inherit their
encoder bases' bloc — ModernBERT-large (Answer.AI/LightOn, assigned via the Answer.AI-led
release) for english and typed-decisions, JHU mmBERT for multilingual — and Cloudflare's
clef line resolves as Cloudflare's own (bloc `us`). Because the name collides with the
existing Nimbleway provider, no bare `nimble` stem SHALL exist: Bespoke's model resolves
only via qualified forms. Pattern stems MUST be specific enough that identifiers outside
these families do not resolve through them.

#### Scenario: Qwen adapters inherit Alibaba's bloc
- **WHEN** model references `bespoke/bespokelabs/Bespoke-Nimble-9B` and
  `strands_decider/strands-decider-2B-hobson-v19` are detected
- **THEN** both resolve to bloc `cn` with organisation labels naming Alibaba and the
  respective tuner (Bespoke, AWS Strands)

#### Scenario: Qualified Nimble route forms resolve without a bare stem
- **WHEN** model references `bespoke/nimble` and `bespoke/nimble-latest` are detected
- **THEN** both resolve to bloc `cn`

#### Scenario: Laya checkpoints inherit encoder-base blocs
- **WHEN** model references `laya/english`, `laya/multilingual`, and
  `laya/typed-decisions` are detected
- **THEN** all three resolve to bloc `us` with organisation labels naming the encoder base
  and the Laya tune

#### Scenario: Clef resolves via the hub-qualified pattern
- **WHEN** model references `cloudflare/@cf/cloudflare/clef-flash` and `cloudflare/clef`
  are detected by the freshness checker's suffix walk
- **THEN** both are covered by the `cloudflare/clef` pattern resolving to bloc `us` with
  organisation Cloudflare

#### Scenario: Generic stems do not over-match
- **WHEN** unrelated model references sharing a stem prefix (for example a hypothetical
  `nimble-search-1` or `clefable-2b`) are detected
- **THEN** `nimble-search-1` does not resolve through any new pattern (no bare `nimble`
  stem exists) and `clefable-2b` does not resolve through the clef pattern; both keep
  provenance `unknown`
