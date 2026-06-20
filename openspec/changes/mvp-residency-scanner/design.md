## Context

borderlint v1 is a static, developer-side CLI for HK/GBA entities that maps where an application's
AI data and traffic flow and governs them against a data-residency policy, in CI, before code
ships. The full agreed scope lives in `CAPABILITIES.md`; this change implements the P1 cut. There
is no prior art in `openspec/specs/` (greenfield).

## Goals / Non-Goals

**Goals:**
- Detect AI provider usage in a repo and resolve each flow to a jurisdiction with an east-west KB.
- Govern flows against a classification-keyed JSON policy with deny-by-default, expressible at
  country (ccTLD) granularity so a PDPO agreed-locations posture (e.g. `sg` in, `my` out) works.
- Run as a deterministic, offline CI gate with a clear exit code and readable/JSON/Mermaid output.

**Non-Goals:**
- Runtime gateway/proxy, DLP, general SAST; global residency solving; arrangement adjudication;
  per-city `CN-GBA` resolution; TypeScript scanning, SARIF, GitHub Action, LLM enrichment (later).

## Decisions

- **Static analysis over runtime interception.** Alternative: a runtime gateway. Rejected — the
  gateway space is crowded and EU-centric, and it governs after deploy; borderlint's value is
  pre-ship, in CI.
- **User-asserted classification per run over inferring the data class from code.** Alternative:
  heuristic/LLM PII inference. Rejected for v1 — unreliable and adds dependencies; the pipeline
  asserting `--classification` is precise, deterministic, and simple.
- **Deny-by-default country allow-lists over an "overseas" bucket.** Alternative: a coarse
  overseas catch-all. Rejected — it cannot express a PDPO agreed-locations EULA where `sg` is in
  scope but `my` is not.
- **Bundled, vendor-neutral, user-overridable YAML knowledge base.** Alternative: hardcoded
  provider tables. Rejected — the KB is the differentiator and must be contributable and overridable.
- **Deterministic core; optional LLM enrichment later.** Alternative: LLM-first classification.
  Rejected — CI must run offline and reproducibly.
- **Python + argparse + PyYAML; AST + endpoint-substring detection.** Alternative: regex-only
  (misses imports) or full taint analysis (overkill for v1). Chosen as the pragmatic middle.
- **Arrangements (GBA Standard Contract, …) surfaced as reference links, not enforced.**
  Alternative: encode arrangement logic. Rejected — applicability depends on the user's home regime,
  data classes, and user base, which borderlint cannot know.

## Risks / Trade-offs

- Static analysis misses endpoints injected purely at runtime → scan config/`.env` too; document
  the limit; a runtime mode is a future option.
- Knowledge-base staleness as providers change → versioned KB, user override, community PRs.
- Azure OpenAI / Bedrock region-in-endpoint → resolved as `unknown`; policy `on_unknown` knob
  (warn|fail); host-based region resolution is a later phase.
- False sense of completeness → the report states what was and was not covered; honest limitations.
