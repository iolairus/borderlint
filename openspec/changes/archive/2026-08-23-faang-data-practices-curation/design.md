# Design: faang-data-practices-curation

## Context

The four target providers are detectable and sovereignty-mapped but lack data-practice entries,
so the evidence pack and KB website render them as "not curated". Their governing documents sit
in doc families already cited by sibling entries, and each platform publishes explicit
training/retention commitments.

## Goals / Non-Goals

**Goals:**

- Four cited entries under the existing schema; every fact traceable to a primary source.
- Tier distinctions (Copilot business/consumer; Vertex vs AI Studio) captured in locators or
  the enterprise_tier fact rather than generalised away.

**Non-Goals:**

- No schema/loader/renderer changes; no re-curation of complete entries.

## Decisions

### D1: Cite platform-specific terms, not company-wide privacy policies
Meta → Model API Terms of Service (ai.developer.meta.com; updated 2026-08-21) plus its
subprocessor list (forwork.meta.com/legal/mfw-subprocessor-list/); Google → Cloud Service
Specific Terms "Training restriction" + the generative-AI zero-data-retention page (note: Vertex
docs rebranded under Gemini Enterprise Agent Platform — the ZDR page moved there, last updated
2026-08-21); Microsoft → Foundry data-privacy documentation (learn.microsoft.com, the same doc
family cited for `azure_openai`); GitHub → Generative AI Services Terms (March 2026).
Company-wide policies are fallback locators only where platform docs defer to them.
*Alternative rejected:* citing corporate privacy policies — too coarse for reviewer questions.

### D2: Tier/service facts live in `enterprise_tier`, scoped in locators
Meta's Model API terms split by service tier: Standard Services content is not used to train
Meta Models (§5.1), while Discounted Services content MAY be used for training by default
(§6.1) — so `training_default` records the Standard posture and `enterprise_tier` discloses the
Discounted split. GitHub replaced the Copilot Product-Specific Terms with the Generative AI
Services Terms (March 2026, deprecated the former effective 5 March 2026): cite those, whose
commitment is training-shaped (§3) with retention varying per product documentation (§6).
*Alternative rejected:* separate fields per tier — schema churn for a note-shaped fact;
citing the deprecated Copilot PST — superseded terms would go stale on arrival.

### D3: Region-scoped Vertex processing noted, not encoded as jurisdictions
Vertex rep endpoints (`aiplatform.eu.rep…`) already resolve jurisdiction via the endpoint map;
the data-governance citations note that prompts/outputs stay region-scoped per the deployment
type (Global/DataZone caveats belong to azure_foundry's sibling entry). No jurisdiction changes
here — that would belong to a providers.json change.

### D4: Facts that differ per deployment stay null with scope caveats
Azure Foundry spans multiple model catalogs (first-party and partner models) whose terms can
differ; where the cited document doesn't state a blanket commitment for all catalog models, the
entry says so rather than over-claiming. The same rule governs github_copilot's retention:
per-product variance is disclosed as a locator caveat instead of a single blanket window.

## Risks / Trade-offs

- [Vendor docs move] → per-entry `reviewed` + citations make drift visible on the 90-day cycle.
- [Tier confusion] → locators name the exact tier/plan the commitment applies to.

## Migration Plan

Additive curation only; rollback restores prior absence from git history.

## Open Questions

- None blocking; exact locator wording resolved against the live documents during curation.
