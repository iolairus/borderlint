# model-provenance Delta

## ADDED Requirements

### Requirement: Bedrock India-region prefix and azure/whisper form resolve provenance
The bundled provenance map SHALL treat the Bedrock cross-region inference-profile prefix
`in.` (India) as a passthrough org: the prefix carries no provenance, so it is stripped and
the remainder matched against the family patterns, exactly as the existing `us.`, `eu.`,
`apac.`, `au.`, `jp.`, `global.`, and `us-gov.` region prefixes are. The map SHALL also
resolve the qualified `azure/whisper` form — the same OpenAI model already covered as
`azure_ai/whisper`, now carried by litellm under the `azure` provider namespace — to OpenAI
(bloc `us`). A bare `whisper` stem SHALL NOT exist: the name collides with unrelated
identifiers (for example `whispering-pines`), so the model resolves only via qualified
forms.

#### Scenario: India-region inference profile resolves through the passthrough
- **WHEN** a model reference `in.moonshotai.kimi-k3` is detected
- **THEN** the `in.` region prefix is stripped and the remainder resolves through the
  `moonshotai.` pattern to bloc `cn` with organisation Moonshot AI

#### Scenario: azure/whisper resolves like azure_ai/whisper
- **WHEN** a model reference `azure/whisper` is detected
- **THEN** it resolves to bloc `us` with organisation OpenAI

#### Scenario: Generic stems do not over-match
- **WHEN** unrelated model references sharing a stem prefix (for example a hypothetical
  `whispering-pines` or `in.inhouse-7b` with no family pattern for the remainder) are
  detected
- **THEN** `whispering-pines` does not resolve through any new pattern (no bare `whisper`
  stem exists) and `in.inhouse-7b` strips the region prefix but matches no family pattern;
  both keep provenance `unknown`
