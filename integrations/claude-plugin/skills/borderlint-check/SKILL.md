---
name: borderlint-check
description: Run borderlint before adding any AI SDK, AI endpoint, or model identifier to the codebase. Use whenever a change introduces an AI provider dependency, an LLM endpoint or base_url, or a model id — check residency, sovereignty, and provenance before the code is committed.
---

# borderlint pre-addition check

When a change you are about to make introduces an AI SDK import, an AI endpoint reference, or a
model identifier:

1. Run the scan first — with the project's policy when one exists:
   `borderlint scan . --policy residency.json --classification <data class>`
   Otherwise inventory mode: `borderlint scan .`
2. If the addition introduces a flow that is not `local` — or a provider/router resolving to
   `unknown` — report it in the conversation before committing: provider, residency
   jurisdiction, sovereignty bloc, and provenance bloc when a model id is involved. Let the
   human decide.
3. If the flow is accepted, record it with an inline waiver carrying a real justification:
   `# borderlint: allow <reason>`. Unjustified waivers are ignored; waivers cannot override a
   provider or model deny.

Backstop: the pre-commit hook and the CI SBOM `diff` gate fail any PR that adds new
non-`local` AI egress — this skill moves the conversation to where the decision is made.
