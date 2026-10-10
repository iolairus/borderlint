# Design: kb-drift-resolution-5

## Context

The 2026-10-08 freshness run (post-#109, ahead of the Monday issue refresh) surfaces three
model families and one stale KB. The wave is small and mechanical — no new providers, no
judgment calls on bloc assignment: `in.moonshotai.kimi-k3` is Bedrock's India-Geo
cross-region inference profile for Kimi K3 (AWS documents US, India, and Global profiles
for the model), `azure/whisper` is OpenAI's Whisper under litellm's `azure` namespace
(already covered as `azure_ai/whisper`), and `azure/model-router` is the same Azure Foundry
routing feature already acknowledged as `azure_ai/model-router`. `evidence_regimes.json`
crossed the 90-day review interval on 2026-10-06 — its first staleness firing.

## Goals / Non-Goals

**Goals:**

- Drain the model-family section to zero, each resolution a recorded human judgment.
- Close the `evidence_regimes.json` 90-day review: verify all four regime summaries
  (PDPO, PIPL, Macao PDPA, PDPA SG) against their sources, record in-window legal changes,
  bump `updated`.

**Non-Goals:**

- No data-practice curation; no scanner/checker changes; no re-review of
  `arrangements.json`/`regimes.json` (passed 2026-10-02).

## Decisions

### D1: `in.` joins the region-prefix passthroughs

Bedrock's India-Geo inference profiles prefix model ids with `in.` (e.g.
`in.moonshotai.kimi-k3`); the prefix says where inference runs, not whose weights they are.
Adding `in.` to `passthrough_orgs` (with `us.`, `eu.`, `apac.`, `au.`, `jp.`, `global.`,
`us-gov.`) strips it so the existing `moonshotai.` pattern resolves Moonshot AI `cn`.
Alternative rejected: a literal `in.moonshotai.` pattern would resolve this one id but
teach the map nothing about the India profile form — the next `in.`-prefixed model of any
family would drift again.

### D2: `azure/whisper` is a qualified pattern; the bare-stem ban stands

litellm carries Whisper under both `azure_ai` and `azure` namespaces. The qualified
`azure/whisper` pattern → OpenAI `us` mirrors the wave-2 `azure_ai/whisper` entry. A bare
`whisper` stem remains forbidden (collides with `whispering-pines`-style names); the
existing `whisper-` dash-anchored prefix is unaffected. Near-miss tests pin both
`whispering-pines` and a non-OpenAI remainder after a stripped `in.` prefix to `unknown`.

### D3: `azure/model-router` is residue, by the exact-key/variant rule

The aliases file already acknowledges `azure_ai/model-router` as the Azure Foundry
model-routing feature — a routing product, not a model. The same product surfaced under
the `azure` namespace is a new variant of an exact-key acknowledgment, which the freshness
spec deliberately keeps actionable; it gets its own residue entry citing the same
structural reason. Alternative rejected: broadening the existing key to a shared stem
(`model-router` without a namespace) would suppress unrelated future ids sight-unseen.

### D4: `evidence_regimes.json` review is verify-then-bump, same as wave 3

Each citation in the four regime summaries is checked against its source (PCPD guidance
and s.33 status; PIPL transfer routes and the 2024 Provisions; Macao Law 8/2005; PDPA
s.26 and PDPC guidelines). In-window changes are recorded in the summary text where they
alter what a filing should document; if nothing material changed, only the `updated` date
moves. Wave-3 watch items (Japan APPI ~2028 in-force, Korea PIPA in force 2026-09-11) do
not touch these four regimes. Any summary found inaccurate is corrected in this change —
a stale date bump over a wrong summary would be dishonest anchoring.

## Risks / Trade-offs

- [`in.` passthrough could strip a genuine `in.`-prefixed id that is not a Bedrock profile]
  → the prefix list is explicit and Bedrock-documented; a non-Bedrock remainder simply
  matches no family pattern and stays `unknown` (near-miss test pins this).
- [Legal review finds a summary needs rewriting, growing the change] → accepted: the
  review is the point of the staleness firing; corrections land in the same change with
  the date bump.

## Open Questions

- (none — all assignments follow standing rules and documented id forms)
