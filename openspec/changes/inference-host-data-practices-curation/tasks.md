# Tasks: inference-host-data-practices-curation

## 1. Entry curation (all citations: URL + locator + retrieved 2026-10-10)

- [x] 1.1 `fireworks_ai`: training `no` (ToS §3.6); retention = ZDR default for inference,
  Response API `store=true` 30-day exception; subprocessors via DPA §6.2 naming
  trust.fireworks.ai/subprocessors; enterprise_tier: org-wide ZDR enforcement, DPA
  incorporated for all customers
- [x] 1.2 `together_ai`: training `no` (opt-in, docs "Training opt-in"); retention =
  stored until user deletes, no fixed window, product-improvements secondary use disclosed,
  self-serve ZDR; subprocessors via trust.together.ai (named via privacy/docs pages);
  enterprise_tier: VPC/EU dedicated deployments, no documented change to defaults
- [x] 1.3 `groq`: training `no` (Services Agreement §4.2); retention = none by default,
  reliability/abuse logs ≤30 days, batch files 30 days; self-serve ZDR all customers;
  subprocessors trust.groq.com/subprocessors; enterprise_tier: offline agreements may
  supersede, public DPA + BAA
- [x] 1.4 `cohere`: training `opt-out` (dashboard toggle, paying accounts; trial keys train
  with no documented opt-out); retention = logged prompts deleted after 30 days;
  subprocessors trustcenter.cohere.com via Enterprise Data Commitments FAQ;
  enterprise_tier: ZDR by approval, DPA on request
- [x] 1.5 `mistral`: training `opt-out` primary (free-tier Studio; paid API excluded by
  default disclosed in tier fact per D2); retention = 30 rolling days abuse monitoring,
  request-based ZDR on paid stateless endpoints; subprocessors trust.mistral.ai/subprocessors
  via DPA §7.1; enterprise_tier: enterprise opted out by default
- [x] 1.6 `perplexity`: training `no` for the API (docs privacy-security page); retention =
  zero retention the API default; subprocessors trust.perplexity.ai/subprocessors via DPA
  §6; enterprise_tier: DPA, SOC 2 — consumer app split noted per D1
- [x] 1.7 `deepinfra`: training `no` (ToS §7(b)) with Google/Anthropic partner-model caveat
  (D3); retention = contractual ZDR, support-request retention ≤30 days, image/bulk paths
  noted; subprocessors docs.deepinfra.com/account/subprocessors (Stripe, AWS, GCP);
  enterprise_tier: DPA by execution, dedicated deployments
- [x] 1.8 `openrouter`: training `no` for the routing layer (privacy policy "Enterprise and
  API Users"); retention = ZDR own default (DPA §2.4(a)), downstream varies; entry discloses
  downstream providers may train unless routing restricted (D3); subprocessors
  trust.openrouter.ai via Enterprise agreement Schedule 3; enterprise_tier: contractual
  ZDR, EU-only processing addendum, in-region routing
- [x] 1.9 `cerebras`: training `no` via purpose-scoped license quoted in locator (D5);
  retention = inputs/outputs not retained, logs deleted "when no longer necessary" — no
  bounded window disclosed; subprocessors trust.cerebras.ai URL via DPA Annex I;
  enterprise_tier: DPA adds processor commitments, posture unchanged
- [x] 1.10 `sambanova`: training `no` via purpose-limited license (ToS §2.1) quoted in
  locator (D5); retention null (undocumented for hosted API); subprocessors
  trust.sambanova.ai; enterprise_tier: sovereign/on-prem ZDR marketing scoped to
  self-hosted, not the hosted API
- [x] 1.11 Bump `updated` in `borderlint/data/data_practices.json` to 2026-10-10

## 2. Tests

- [x] 2.1 Extend data-practices tests: the ten entries load with the expected training
  defaults (`no` ×8, `opt-out` ×2), every non-null fact carries a complete citation, no
  entry claims a source was unreachable, each key exists in providers.json, and the SambaNova
  retention fact is null

## 3. Validation

- [x] 3.1 Run the full test suite
- [x] 3.2 Run `scripts/kb_drift.py` and confirm the data-practice gap list drops by ten
  (102 → 92)
- [x] 3.3 `openspec validate inference-host-data-practices-curation --strict`
