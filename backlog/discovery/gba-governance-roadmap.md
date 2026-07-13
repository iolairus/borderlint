---
type: project
created: 2026-07-03
updated: 2026-07-08
tags:
  - borderlint
  - ai-governance
  - data-privacy
  - gba
  - roadmap
---

# borderlint — feature review & enhancement roadmap (GBA practitioner lens)

> Drafted 2026-07-02 against v1.2.1; current release **v1.7.0** (2026-07-08). Working copy lives untracked in the repo at
> `backlog/discovery/gba-governance-roadmap.md`; items feed `/req-capture` or `/opsx:propose`
> when picked up.

## Progress log

**2026-07-08 — dogfooding memorybox: local-inference visibility ([v1.7.0](https://pypi.org/project/borderlint/)).**
Scanning a fully local-inference app exposed four gaps, closed in #59–#61: environment
directories are now excluded by their **markers** (PEP 405 `pyvenv.cfg`, conda's `conda-meta/`)
in a single-pass pruning walk — memorybox's 21GB `.venv-cuda` had produced 397KB of
site-packages noise; the **HF transformers / sentence-transformers local runtime** joins the KB
(local/local, multi-model → provenance from bound refs), turning invisible on-box inference
into proper inventory rows; `.onnx`/`.safetensors` join the GGUF **basename rule** (deny_models
inherits it); and moondream/`vikhyatk/`/florence-2/clip-vit families resolve. Review catches:
an ADDED requirement duplicating the shipped exclusion requirement, a motivating example the
change didn't actually cure, and the pruning-walk shape itself. memorybox's final inventory:
4 flows, 3 ok (Florence-2/Microsoft, moondream2/M87 Labs, CLIP/OpenAI — all local/local/us),
1 honest unknown. Two apps dogfooded today; both scans converted tool blind spots into shipped
fixes same-day.


**2026-07-08 — dogfooding TellMeWhy hardens detection ([v1.6.0](https://pypi.org/project/borderlint/)).**
Scanning a real app (TellMeWhy) surfaced four gaps, all fixed and shipped same-day (#55–#57):
a tsconfig `baseUrl: "."` false positive (config values now require host shape); env-style
endpoint keys — `TELLMEWHY_LLM_SERVER_URL` in a scanned `.env` sat unread while flows reported
unknown; now segment-matched (AI stem + URL/ENDPOINT/BASE/HOST suffix), with review-driven
value rules (env-getter captures skipped, compose service hosts accepted behind a scheme);
`edge_tts` and `whisper_local` KB entries — the scan now shows children's speech text flowing
to a US-sovereign Microsoft endpoint (the app's one genuine violation) and on-box Whisper STT
as `local`/`local`/`us`; and the example policy moved to `home_location`, unlocking the PDPO
evidence annex. The TellMeWhy evidence pack went from 4 flows to 10, with the story changing
from "three unknowns" to "one actionable sovereignty violation".


**2026-07-08 — P1-3 evidence pack shipped ([v1.5.0](https://pypi.org/project/borderlint/)).**
`evidence-pack` (#54): `--format evidence` renders the filing artifact — audit envelope (git
commit, policy SHA-256, KB review dates, `SOURCE_DATE_EPOCH`-deterministic timestamp),
three-axis inventory with model identifiers and developer orgs, waiver register, cross-border
references, and regime annexes for **PDPO, PIPL (+ GBA SC), Macao PDPA, PDPA (SG)** keyed by
the shipped `regime_of` join (spec review killed an invented token vocabulary and fixed the
exit-code contract at the baseline requirement rather than beside it). Static fields fill from
the scan; purpose/scale/recipients/retention render as marked org-supplied blanks — a
pre-filled template, never a fabricated filing. Exports are artifacts: evidence exits 0 in a
failing state, which is precisely when a DPO files it. Framework annexes phase 2 accepted:
GDPR RoPA → NIST AI RMF → ISO/IEC 42001 (27701 rides on RoPA; COBIT excluded — no honest field
mapping). **P1 is now complete except P1-2 (declared transfer route), the last roadmap item of
the original top tier.**


**2026-07-08 — provenance filters by family, not just bloc ([v1.4.0](https://pypi.org/project/borderlint/)).**
`provenance-model-deny` (#52), answering "can I filter by lab or only bloc?": the provenance
block gains `deny_models` — anchored model-id prefixes banning a family regardless of serving
host or bloc ("no DeepSeek weights anywhere" without touching Qwen). Semantics mirror the
provider deny exactly — default member of the failure set, waiver-proof, lifted only by a
reviewed `fail_on` edit — after spec review caught the design claiming a "hardest-statement"
provider-deny precedent that the shipped code never had. Deny matching reuses the map's full
normalization, so GGUF paths, redistributor repos, and `@`-version pins can't dodge it (both
dodges tested). The KB's per-pattern developer org now reaches findings as `model_org`
("exaone-3.5 — LG AI Research") across text/JSON/SBOM — the evidence pack (P1-3) gets readable
vendor names for free. Honest limit spec'd: an unbound `import deepseek` flow can't match an
identifier-based deny; the bloc allow-list still governs it via tier 2. v1.4.0 is a proper
minor: genuine feature surface, unlike the 1.3.2 tooling tag.


**2026-07-06 — the freshness queue answers "anything to do?" in one line (v1.3.2).**
`kb-drift-structural-residue` (#50): the suppression file gained a `residue` block — exact ids
or `/`|`-`-terminated prefixes, each with a reason — classifying uncovered model ids after
matching, so acknowledgment can never affect coverage. [Issue #39](https://github.com/iolairus/borderlint/issues/39)
now opens with "**Nothing actionable.** Acknowledged residue: 194 ids" and a collapsed
reason-grouped count block. Seeded from the human review of 2026-07-05: the current uncovered
set bulk-acknowledged as exact keys (169), pricing buckets + fal_ai paths as prefixes (25), and
the seven surfacing providers moved to reasoned ignores. Exact-key semantics were the review's
demand and a test caught the first implementation violating them — new upstream ids surface as
actionable, acknowledged ids never swallow their variants. v1.3.2 tags the milestone; the wheel
is unchanged from 1.3.1 (drift tooling lives outside the package).


**2026-07-05 — the issue #39 close-out campaign: seven PRs, [v1.3.1 released](https://pypi.org/project/borderlint/).**
The weekly freshness queue went from 56 uncovered providers + ~200 uncovered model families at
seed to its honest floor (7 providers awaiting classification, ~100 structurally unresolvable
family stems). The loop the tool preaches ran end-to-end: the report surfaced gaps, a human
triaged them with recorded judgments, every fix landed spec-first, and two designs were
materially changed by review findings.

- **Version-pinned model identifiers** (#43 `versioned-model-identifiers`, #46
  `default-latest-version-pins`): a trailing `@<digit-led version>` — later plus the closed
  `@default`/`@latest` set — strips before matching; digit-led is the load-bearing rule that
  keeps emails out. Spec review simulated the fix against the live upstream and caught a missing
  bare `codestral` pattern and a hyphenated-version regex gap before implementation.
- **Drift suppression list** (#44 `kb-drift-provider-aliases`): `scripts/kb_drift_aliases.json`
  records route aliases (33) and reasoned out-of-scope ignores; alias targets are
  existence-validated and fail the weekly job loudly; the scanner provably never reads it.
- **Curation batches** (#42, #45): ~80 provenance patterns hand-assigned across the campaign —
  first `ae` (jais/G42), `ru` (GigaChat), `il` (Jurassic-2) families; Bedrock cross-region
  prefixes as passthroughs. Human-approved provider adds: **AWS SageMaker**, **Snowflake
  Cortex**, **Lemonade** (AMD local). Researched ignores: parallel_ai, tinyfish.
- **Provider-context rules** (#47 `kb-drift-model-provider-context`): the model check skips
  ignored providers' ids and covers speech-tier ids via first-party defaults. Review narrowed
  the rule from all 29 defaulted providers to speech-category only — blanket coverage would
  have hidden the next novel first-party family (the `o1` case) from pattern curation.
- **`ch` bloc** (#48 `ch-bloc-apertus`): Switzerland is outside the EU/EEA, so Apertus
  (ETH Zürich/EPFL) had no honest bloc; FADP/BÜPF source note; vocabulary now 16 blocs.
- **v1.3.1** (#49): rollup release + README refresh (85+ providers, version-pin example,
  alias-list note, stale v1.1.4 CI/pre-commit tags finally moved). Note: additive features in a
  patch version — semver purists would have cut 1.4.0; deliberate call.

Deliberately left in the queue: darkbloom/pinstripes/llamagate (no public info), morph/reducto/
inception/tensormesh (researched, not elected as providers this pass), and the structural
residue (multi-model-host path ids, litellm pricing buckets, bare-word ids like `command`).

**2026-07-04 — [v1.3.0 released to PyPI](https://pypi.org/project/borderlint/)** rolling up the
day's four PRs: the provenance dimension (#37), the four-axis KB freshness check (#38), the
completed bloc vocabulary (#40), and a README presenting all three dimensions as first-class
(#41, which also carried the version bump). Published via Trusted Publishing with attestations.
The §1 capability table below now describes the released state, not just `main`.

**2026-07-04 — three changes shipped to `main`:**

- **P1-1 Model provenance dimension** ✅ (PR #37, archived as `model-provenance-dimension`).
  As designed in §4, plus beyond the sketch: local-LLM identifier coverage (GGUF basenames,
  MLX/quantizer passthrough orgs, Ollama tags with a tool-name stoplist), two-tier resolution
  (bound model reference → first-party provider default), standalone `model_reference` findings
  exempt from residency/sovereignty evaluation. Non-breaking; policy block opt-in.
- **KB freshness extension** ✅ (PR #38, `kb-freshness-provenance`). The §4 "honest limits"
  freshness item, closed: the weekly job now checks provenance model coverage (litellm keys
  through the real matcher, aggregated by family, capped at 50), sovereignty completeness
  (every provider id mapped to a valid bloc), and `updated`-date staleness (90 days, all
  bundled KBs). One standing issue updated in place — [#39](https://github.com/iolairus/borderlint/issues/39)
  is now the curation queue.
- **P2-6 Vocabulary completion** ✅ (PR #40, `bloc-vocabulary-completion`). Grew beyond the
  sketch: `jp kr sg au ae` (not just the four), across **both** dimensions, with legal-source
  notes (APPI, PIPA, PDPA/CPC, TOLA 2018, UAE PDPL) and the deferred model families — Falcon
  (ae), EXAONE/Solar/HyperCLOVA (kr), PLaMo/Sarashina/ELYZA/Swallow/rinna (jp), SEA-LION (sg).
  `au` is vocabulary-only until a family or provider needs it.

Remaining top of queue: **P1-2 declared transfer route** (last P1 item; P1-3 shipped
2026-07-08 — see the campaign entry above), then P2-4 drift mode / P2-5 waiver expiry, then P2-4 drift mode / P2-5 waiver expiry. Curation feed: issue #39,
converged as of 2026-07-05 (see the campaign entry above) — anything new at the top of either
section is genuine signal now.

## 1. What the tool is today

**Intent.** A static, CI-embedded linter answering one question from the codebase: *where, and
to whom, is our AI data flowing — and does that satisfy our policy?* Deliberately narrow: pre-ship,
developer-side, zero runtime dependencies, east-west even-handed, HK/GBA home base as the v1 target.

**Shipped capability (v1.3.1):**

| Dimension | What it does |
|---|---|
| Detection | Python AST + TS/JS imports/requires/dynamic imports; endpoint strings; config files |
| Residency | Flow → jurisdiction (ccTLD/ISO + `CN-GBA`/`GBA` zones); AWS/Azure/GCP region-in-host resolution |
| Sovereignty | Flow → compelled-disclosure bloc (`us eu cn uk ru in il ca jp kr sg au ae ch local unknown`), provider home regime, host-level ring-fence overrides (Sinnet) |
| Provenance | Flow → model-weights bloc (sovereignty vocabulary minus `local`); model-reference matching incl. GGUF/MLX/Ollama and `@`-version-pinned forms; two-tier resolution; opt-in policy block + `deny_models` family ban; `model_org` on findings *(added 2026-07-04, deny 2026-07-08)* |
| Policy | Classification-keyed allow-lists, deny-by-default, provider allow/deny, `fail_on`, `on_unknown`, inline waivers |
| Regimes | `home_location` → regime tag (PDPO, PIPL, APPI, PIPA, PDPA, APP, GDPR…) + cross-border arrangement references incl. both GBA Standard Contract variants (HK & Macao) |
| Reporting | text, JSON, Mermaid, SARIF, AI-dataflow SBOM, evidence pack (audit envelope + regime annexes: PDPO, PIPL/GBA SC, Macao PDPA, PDPA-SG) |
| KB | 87 providers + provenance map (207 patterns, 16 blocs incl. `ch`), dated, user-mergeable; weekly freshness check across providers (alias/ignore-suppressed), model coverage (provider-context aware, version-pin aware, actionable/residue split with one-line summary), sovereignty completeness, staleness |

**The edge**: nobody else does static residency + sovereignty with GBA zones and the GBA SC as
first-class objects. The KB is the moat; the orthogonal-dimension policy model is the architecture
that makes each new governance axis cheap to add.

## 2. Gaps from a GBA practitioner's seat

A privacy officer / AI-governance lead in HK or the Mainland GBA cities works in terms of:

1. **Transfer routes, not just destinations.** PIPL gives three routes out (CAC security assessment,
   standard contract filing, certification) plus the 2024 Provisions exemptions; the GBA SC is a
   fourth, narrower route (PI only, HK/Macao ↔ 9 cities, no "important data"). borderlint names the
   arrangements but cannot express *"we operate under the GBA SC route — flag anything that route
   cannot carry."*
2. **Evidence, not exit codes.** The artifact a DPO actually files is a transfer inventory / RoPA
   appendix / PIA annex. The JSON output is close but has no audit framing (policy version, commit,
   scan date, waiver inventory).
3. **Drift, not snapshots.** Governance review is periodic; the question each month is *"what flows
   are new since the last sign-off?"*
4. **Sensitive PI tiers.** PIPL sensitive PI and PDPO's stricter expectations are a severity tier,
   not just another classification string.
5. **Model supply chain.** Regulators (HKMA GenAI guidance, OGCIO framework, CAC filings) now ask
   *whose model is it* — provenance of the weights, separate from who serves them.

## 3. Enhancement roadmap

Sizing = scope, not effort. **KB** = data-file only; **policy** = policy/eval change; **engine** = new detection or resolution pass.

### P1 — highest value for the GBA audience

| # | Enhancement | Scope | Why it wins |
|---|---|---|---|
| 1 | ✅ **Model provenance dimension** (§4) — *shipped 2026-07-04, PR #37* | KB + engine + policy | Regulator-driven, asked-for, and the orthogonal-dimension pattern makes it the third cheap axis |
| 2 | **Declared transfer route** — policy declares `route: gba_sc \| pipl_sc \| cac_assessment \| certification`; borderlint flags flows the declared route cannot carry (e.g. GBA SC declared, flow lands in `sg`; GBA SC declared, classification tagged `important-data`) | policy | Turns arrangement *references* into a static, checkable constraint — the single most PIPL-native feature possible without adjudicating legality |
| 3 | ✅ **Evidence pack** — *shipped 2026-07-08, PR #54* — `--format evidence`: transfer inventory with scan timestamp, git commit, policy hash, per-flow (provider, residency, sovereignty, provenance, arrangement, waiver, code location), active-waiver table | engine (report only) | Converts CI output into the artifact a DPO files; near-pure reporting work on data already collected |

### P2 — strong practitioner value, next wave

| # | Enhancement | Scope | Why |
|---|---|---|---|
| 4 | **Drift mode** — `borderlint diff <ref>`: flows added/removed/changed since a tag or commit | engine | Matches how governance review actually happens (periodic sign-off of the delta) |
| 5 | **Waiver expiry + inventory** — `borderlint: allow(until=2026-12-31, reason=…)`; expired waiver → finding; waiver-ageing table in reports | engine (small) | Waivers without expiry become permanent exceptions; auditors ask for the register |
| 6 | ✅ **Vocabulary completion** — *shipped 2026-07-04, PR #40, as `jp kr sg au ae` across both dimensions plus the deferred model families* | KB | Asymmetry between the two dimensions is a correctness gap, same class as the Cohere/`ca` fix |
| 7 | **Sensitive-PI tier** — reserved classification semantics (`sensitive-pii`) with regime-aware annotations (PIPL Art. 28-32, PDPO guidance) and a stricter default posture | policy | The tier every GBA privacy program already runs internally |
| 8 | **IaC / deployment-config scanning** — Terraform, Bicep, K8s manifests, `.env` templates declaring endpoints/regions/model IDs | engine | Enterprises pin regions in IaC, not application code; large blind spot |

### P3 — later, still on-thesis

| # | Enhancement | Scope |
|---|---|---|
| 9 | **Regulator profiles** — `--profile hkma` / `ogcio` / `cac`: annotate findings with the matching regulator expectation as reference links (same advisory pattern as arrangements) | KB |
| 10 | **Java/Kotlin detection** — HK/GBA finance is JVM-heavy; largest coverage gap by industry | engine (large) |
| 11 | **Purpose tags** — distinguish transient inference vs persisted embeddings (vector-store category already exists; generalise to a `purpose` axis) | policy |
| 12 | **Org policy inheritance** — `extends:` a central policy with per-repo overrides, for multi-entity groups | policy (small) |

### Explicitly not doing (keeps the thesis sharp)

- No runtime gateway, no payload inspection, no legal adjudication. Route checking (P1-2) flags
  *route/destination contradictions*; it never computes "you must file a CAC assessment" — volume
  thresholds are unknowable statically and are declared by the org, not inferred.
- No per-city resolution inside `CN-GBA` (existing non-goal; nothing above requires it).
- EU-US DPF / adequacy modelling stays deferred.

## 4. Model provenance in the control policy

> ✅ **Shipped 2026-07-04** as designed below (PR #37, archived change `model-provenance-dimension`),
> with two additions discovered during the build: local-LLM identifier coverage (GGUF/MLX/Ollama)
> and a first-party provider default tier so bare `import openai` flows resolve `us` instead of
> drowning the dimension in `unknown`. Kept for the design record.

### The concept

Third orthogonal axis. For any flow:

- **Residency** — where the bytes rest (endpoint region).
- **Sovereignty** — who can compel disclosure (serving provider's home regime).
- **Provenance** — who developed the model weights, and under which export-control/legal regime.

The axes genuinely decouple:

| Flow | Residency | Sovereignty | Provenance |
|---|---|---|---|
| Bedrock `ap-east-1` serving Claude | `hk` | `us` | `us` (Anthropic) |
| Bedrock `ap-east-1` serving DeepSeek-R1 | `hk` | `us` | `cn` |
| Azure serving Mistral Large | region-dep. | `us` | `eu` |
| Self-hosted Qwen via Ollama | `local` | `local` | `cn` |
| OpenRouter → `deepseek/deepseek-r1` | `unknown` | `unknown` | `cn` |

Row 2 and row 4 are the cases residency+sovereignty cannot see: a US-sovereign, HK-resident flow
running PRC-origin weights, and a fully local flow whose weights carry a foreign provenance.
Both matter to practitioners today — US export-control direction on weights, sector rules on
PRC-origin models (and the mirror image: Mainland entities mandated to prefer domestic models),
HKMA-style model supply-chain questions.

### Design (mirrors the sovereignty pattern deliberately)

1. **KB**: `borderlint/data/provenance.json` — model-ID pattern → developer org → bloc, reusing the
   sovereignty vocabulary (`us eu cn uk ru in il ca local unknown`; `local` unused here, `unknown`
   the default). Patterns cover the ID forms that appear statically in code:
   - Bedrock model ARNs/IDs: `anthropic.claude-*`, `deepseek.r1*`, `meta.llama*`, `mistral.*`
   - Bare API model strings: `gpt-*`, `claude-*`, `gemini-*`, `qwen*`, `glm-*`, `ernie-*`
   - Aggregator-qualified IDs: `deepseek/deepseek-r1`, `qwen/qwen-2.5-72b` (OpenRouter/LiteLLM
     prefixes carry the org — these *upgrade* resolution where sovereignty is `unknown`)
   - Hub repo IDs: `Qwen/…`, `mistralai/…`, `meta-llama/…` (HF `from_pretrained`, `ollama pull`)
2. **Detection**: new kind `model_reference`, found by scanning string literals near existing
   detections. Association rule kept deliberately simple: a model reference binds to a provider
   detection in the same file; otherwise it stands alone as its own finding. No cross-file binding.
3. **Detection field**: `provenance: str = "unknown"`, populated like `sovereignty`.
4. **Policy**: opt-in `provenance` block, same shape as `sovereignty` — per-classification
   allow-lists, `on_unknown`, `fail_on: ["provenance"]`. Absent block → reported, never gates.
   Waivers apply. Symmetric `on_unknown` gate (apply the v1.2.1 lesson from day one).
5. **Reporting**: provenance column/field in all five formats, same as sovereignty.
6. **Semantics — advisory, base-family provenance.** Fine-tunes and distillations inherit the base
   family's bloc (a Llama fine-tune is `us`-provenance). The KB surfaces exposure; it does not
   adjudicate export-control applicability — same posture as the sovereignty map's note.

### Honest limits

- Model IDs passed through variables/env at runtime resolve to `unknown` — acceptable; `unknown`
  is a first-class, policy-governable answer everywhere else in the tool already.
- Derivative-weights provenance is genuinely fuzzy (Qwen-distilled-into-Llama exists). The
  base-family rule is a documented simplification, revisitable.
- ~~The KB needs the same freshness discipline as providers.json; fold into the existing
  kb-freshness machinery.~~ Done 2026-07-04 (PR #38): weekly model-coverage diff against the
  litellm catalog, sovereignty completeness audit, staleness warnings, one standing issue.

### Suggested sequencing

Provenance lands as one OpenSpec change (`model-provenance-dimension`), structurally a sibling of
`sovereignty-dimension`: proposal explicitly un-defers the item deferred in that change's
non-goals. P1-2 (declared transfer route) and P1-3 (evidence pack) are independent changes;
evidence pack benefits from landing after provenance so the inventory carries all three axes.
