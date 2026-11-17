## ADDED Requirements

### Requirement: Microsoft Web IQ service classification

The bundled provider KB SHALL identify Microsoft Web IQ through its documented SDK coordinates
and `api.microsoft.ai` host as category `service`. It SHALL resolve residency to `unknown` because
Microsoft documents no regional residency commitment, and sovereignty to `us`. It SHALL NOT carry
a model-provenance default or be aliased to the distinct Grounding with Bing product.

#### Scenario: Web IQ endpoint resolves without invented residency
- **WHEN** a detection matches `api.microsoft.ai/v3/search/web`
- **THEN** it resolves to provider `webiq`, category `service`, jurisdiction `unknown`, and
  sovereignty `us`

#### Scenario: Web IQ SDKs resolve
- **WHEN** imports or package references use `webiq`, `@microsoft/webiq`, `com.microsoft.webiq`,
  or `Microsoft.WebIQ`
- **THEN** they resolve to the same `webiq` provider entry
