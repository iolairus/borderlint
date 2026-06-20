## Why

borderlint marked AWS Bedrock and Azure OpenAI flows as `unknown` because their jurisdiction is
not the provider default. AWS Bedrock encodes the region in the endpoint host
(`bedrock-runtime.<region>.amazonaws.com`), so it can be resolved — turning a quarter of `unknown`
flows (496 → 377 when scanning LiteLLM) into precise ccTLD jurisdictions, e.g. `ap-east-1` → `hk`.
This backfills the already-implemented B4 capability into the spec.

## What Changes

- Resolve a region-coded endpoint host to a ccTLD jurisdiction via an AWS/Azure region map
  (`bedrock-runtime.ap-east-1.amazonaws.com` → `hk`, `cn-north-1` → `cn`, `ap-southeast-1` → `sg`).
- When the region is not present in the host — the standard `<resource>.openai.azure.com`, or a
  region interpolated at runtime — the flow stays `unknown`.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `jurisdiction-classification`: add a requirement to resolve a region-coded endpoint host to a
  jurisdiction before falling back to `unknown`.

## Impact

- `borderlint/kb.py` (AWS/Azure region maps + region extraction) and
  `borderlint/data/providers.json` (`region_scheme` flags on Bedrock and Azure OpenAI). No new
  dependencies.

## Non-goals

- Resolving the Azure region from the standard `openai.azure.com` host (it is not encoded there) or
  from SDK/config — a later, non-host mechanism.
- Sub-national resolution: Mainland China regions map to `cn`, not `CN-GBA`.
