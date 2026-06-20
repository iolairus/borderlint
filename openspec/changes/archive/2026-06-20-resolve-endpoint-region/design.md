## Context

Spec backfill for region resolution (capability B4), already implemented and shipped in code. AWS
Bedrock carries its region in the endpoint host; Azure OpenAI's standard host does not.

## Goals / Non-Goals

**Goals:** resolve a region-coded endpoint host to a ccTLD jurisdiction, with `unknown` as the safe
fallback.

**Non-Goals:** non-host region sources (SDK/config); resolving the standard `openai.azure.com` host;
sub-national (`CN-GBA`) resolution.

## Decisions

- **Extract the region token from the matched endpoint text via regex, then map AWS/Azure region →
  ccTLD.** Alternative: parse each SDK's config for a region argument. Rejected — outside the
  static-scan scope and unreliable.
- **Dynamic / interpolated regions stay `unknown`.** Alternative: assume a default region. Rejected
  — it would fabricate a jurisdiction the code does not actually pin.

## Risks / Trade-offs

- Region-map staleness as cloud providers add regions → extend the map; `unknown` remains the safe
  fallback, so a missing region never produces a wrong jurisdiction.
