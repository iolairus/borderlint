# Design: kb-drift-resolution-6

## Research basis (all primary sources, 2026-10-11)

- **microsoft_365_copilot** — litellm's handler
  (`litellm/llms/microsoft_365_copilot/chat/handler.py`) posts to
  `https://graph.microsoft.com/beta/copilot/conversations` and `…/{id}/chat`; Microsoft
  Learn documents the same beta endpoint (preview terms). Microsoft chooses the served
  model; the privacy doc states prompts/responses stay in the Microsoft 365 service
  boundary and are not used to train foundation LLMs.
- **scaledown** — litellm's `litellm/llms/scaledown/chat/transformation.py` sets
  `DEFAULT_API_BASE = "https://api.scaledown.xyz"`; ScaleDown's docs show the same host.
  Legal entity ScaleDown, Inc. (Ramona, CA; Delaware governing law). Its DPA commits to
  US-only processing, zero retention, no training on customer data, and names only
  compute subprocessors (AWS, GCP, Modal) — no third-party model vendor in the data path.
  The five endpoint names map to five task APIs (classify, compress, extract, summarize,
  and a Jev-compatible decisions API backed by its classifier).
- **MAI-Code** — the official `microsoft/MAI-Code` repository: "We are Microsoft AI…
  MAI-Code is our family of in-house coding models"; GitHub's changelog announces
  MAI-Code-1.1-Flash in Copilot (2026-08-11).
- **Microsoft-Decision-1** — Microsoft's own announcement (Microsoft Command Line blog):
  "our new model for fast decision-scoring… post-trained on Qwen3.5-9B", available in
  Foundry and through OpenRouter; Foundry catalog lists publisher Microsoft.

## Decisions

- **D1 — `graph.microsoft.com` is the only endpoint host for `microsoft_365_copilot`.**
  It is the documented inference host (litellm handler + Microsoft Learn). The Entra
  token host `login.microsoftonline.com` is generic authentication shared by every
  Microsoft cloud call and carries no AI signal; it is not recorded. The Graph host is
  likewise a shared surface (most Graph traffic is not Copilot), but jurisdiction
  classification is unaffected: all Graph traffic is Microsoft/us either way. The note
  records the shared-surface caveat and the preview status rather than pretending the
  host is Copilot-exclusive.
- **D2 — `api.scaledown.xyz`, not the `.ai` hosts.** The API host is `.xyz` per litellm's
  transformation and the vendor's own docs; the `.ai` domain serves the SPA and docs.
  Recording the wrong host would silently miss every real flow.
- **D3 — one `scaledown/` org-namespace pattern, never bare stems.** The five families
  are single common English words; bare `classify`/`extract`/`summarize` stems would
  over-match across every ecosystem. A `scaledown/` prefix pattern (the `qwen/`
  convention) covers all five observed ids and future ScaleDown endpoints, matching only
  litellm's qualified form. Bloc `us` on the clef precedent: own SLMs, no upstream model
  vendor, until lineage documentation says otherwise. Tier-2 default `us` likewise:
  ScaleDown serves only its own models.
- **D4 — `mai-code` joins the existing `mai-*` family as both bare and qualified forms.**
  The KB already carries `mai-ds`, `mai-1`, `mai-thinking`, `mai-cyber`, `mai-image` →
  Microsoft AI/us, some with `azure_ai/`-qualified mirrors. `mai-code` (bare) and
  `github_copilot/mai-code` (qualified) follow the same convention; the GitHub Copilot
  surface is where litellm observes it.
- **D5 — Microsoft-Decision-1 inherits Alibaba's bloc.** The provenance map's own rule
  ("fine-tunes and distillations inherit the base family's bloc") and the Bespoke Nimble /
  Strands Decider precedents assign `cn`: Microsoft-Decision-1 is post-trained
  Qwen3.5-9B. The organisation label names base and tuner — `Alibaba (Microsoft
  Decision-1 post-training)` — matching `Alibaba (Bespoke Nimble LoRA)`. Patterns:
  `microsoft-decision` (bare, distinctive enough to anchor safely) and
  `azure_ai/microsoft-decision` (the observed qualified form). The OpenRouter mirror is
  documented but unobserved upstream; adding a pattern for an id no client has been seen
  using is deferred to the wave that surfaces it.
- **D6 — no tier-2 default for `microsoft_365_copilot`; qualified `chat` only.** Copilot
  routes across model vendors at Microsoft's discretion (Azure OpenAI; Anthropic models
  are documented in M365 Copilot), so an unbound flow on this provider is honestly
  `unknown`. The bound form resolves via the qualified
  `microsoft_365_copilot/chat` pattern → Microsoft/us; a bare `chat` stem would match
  everything and resolves nothing honestly.

## Risks

- **`cn` on a Microsoft-branded model will surprise.** Mitigated by the org label naming
  base and tuner, by the spec scenario stating the inherit-base rationale, and by the
  plain-language explanation surfacing the matched organisation.
- **The Graph host over-attributes.** Any Graph SDK usage classifies as
  `microsoft_365_copilot`. Jurisdiction is correct regardless (Microsoft/us); the note
  carries the caveat. If false-positive provider attribution ever matters, the fix is
  scanner-side path sensitivity — out of scope here.
- **`scaledown/` covers future endpoint names automatically.** Acceptable: the bloc
  assignment follows the vendor, and the vendor's DPA constrains the data path; a
  future third-party model behind ScaleDown would arrive with lineage documentation and
  a re-review.
