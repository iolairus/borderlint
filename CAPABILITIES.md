# borderlint — Capability Set

> **Status:** shipped — v1.0.0. The full P1 (MVP) and most of P2 are built and tested; the
> capability map below tracks actual state (✅ shipped · next · later), not the original plan.

## 1. Purpose

`borderlint` answers one question from a developer's codebase: **where, and to whom, is our
AI data and traffic flowing — and does that satisfy our data‑residency policy?**

It is a **static, developer‑side** check (not a runtime gateway), it treats **Western and
Chinese providers evenly**, and it is built for teams operating across the **east‑west
boundary**, where data residency is a licence to operate rather than a nice‑to‑have.

> **v1 target — Hong Kong & GBA companies.** borderlint v1 is built for organisations whose
> home base is **Hong Kong or the Greater Bay Area**. It answers: *does our AI data stay within
> HK / the GBA, or leave it?* It is built to be useful to **HK entities (under the PDPO)** and
> **GBA / Mainland entities (under PIPL)**, including the **GBA Standard Contract** route between them. Solving residency for arbitrary home jurisdictions (a US or EU
> company's own rules) is **explicitly out of scope for v1**.

## 2. Positioning (what makes it different)

| Most existing tools | borderlint |
|---|---|
| Runtime gateways / proxies | Static, runs in CI before anything ships |
| EU‑centric | East‑west / APAC lens; Mainland China, HK, SG first‑class |
| Enterprise platforms | Single‑file CLI, MIT, vendor‑neutral, zero‑config first run |
| Generic AI governance | Narrow and sharp: *data residency & cross‑border flow* |

## 3. Jurisdiction model — discrete entities, zones & arrangements

borderlint treats jurisdiction as richer than flat country codes, with three concepts:

**Discrete entities** — e.g. `US`, `EU`, `SG`, `UK`, and crucially the distinct set
`CN` (Mainland China, general), `CN-GBA` (the nine Mainland Greater Bay Area cities),
`HK` (Hong Kong), and `MO` (Macao). `HK`, `CN`, and `CN-GBA` are deliberately separate:
a Shenzhen endpoint is `CN-GBA`; a Beijing endpoint is `CN`.

**Zones** — named groupings that span entities for the purpose of a data arrangement. The
**GBA** zone = the nine Mainland GBA cities together with Hong Kong (for personal-information
flow). Macao is **excluded** from the GBA data scheme.

**Transfer arrangements** — named legal mechanisms that *may* permit a flow residency alone
would block. borderlint surfaces these as **reference links** rather than adjudicating them
(see the scope note below). The flagship example:

> **GBA Standard Contract** — "Standard Contract for the Cross-boundary Flow of Personal
> Information within the Guangdong-Hong Kong-Macao Greater Bay Area (Mainland, Hong Kong)".
> Permits **bidirectional personal-information** flow between **Hong Kong** and the **nine
> Mainland GBA cities** — Guangzhou, Shenzhen, Zhuhai, Foshan, Huizhou, Dongguan, Zhongshan,
> Jiangmen, Zhaoqing. It **lifts the volume restriction** of the general Mainland framework,
> reduces the transfer assessment from six areas to three, and files in 10 working days.
> Voluntary; effective 13 Dec 2023, extended to all sectors 1 Nov 2024. Administered by HK's
> Digital Policy Office and the CAC of Guangdong. **Macao is not in scope.**
> Source: [digitalpolicy.gov.hk — GBA cross-boundary data flow](https://www.digitalpolicy.gov.hk/en/our_work/digital_infrastructure/mainland/gbacbdf/cross-boundary_data_flow/index.html)

In practice this lets a policy express *"personal data may stay within the GBA"* — permitting a
Shenzhen ↔ Hong Kong flow under the GBA Standard Contract — while still **blocking** a flow to
Beijing (`CN`, outside the zone) and treating Macao on its own footing. General tools see only
"China vs not-China"; borderlint can express the GBA carve-out that teams running Guangdong and
Hong Kong together actually rely on.

**Scope note (reference, not adjudication):** borderlint *surfaces* the relevant arrangement as
a reference link; it does **not** decide whether an arrangement legally applies to you — that
depends on your home jurisdiction, the data classes involved, and where your users sit. You
express your accepted posture by choosing the entities and zones in your policy (e.g.
`allow: [HK, GBA]`); the arrangement links are there to support that choice, not to make it.

**v1 resolution.** v1 resolves every flow to a **country code** (ccTLD / ISO 3166-1 — e.g. `hk`,
`cn`, `sg`, `my`, `us`, `gb`, `mo`), plus the special token **CN-GBA** (the nine Mainland GBA
cities) and the **GBA** zone alias (`hk` + `CN-GBA`). There is **no `overseas` grab-bag**: each
flow resolves to a specific country, and any code **not on the policy's allow-list fails by
default**. This lets a HK entity encode its **PDPO agreed-locations** policy exactly — e.g. allow
`sg` but not `my` for customer PII.

**Regulatory frame (v1).** borderlint v1 understands three regimes: **PDPO** (Hong Kong),
**PIPL** (Mainland China / GBA), and the **GBA Standard Contract** arrangement between them. The
user declares their **home regime** — a HK entity under PDPO, or a GBA / Mainland entity under
PIPL — and borderlint surfaces the regime and arrangement references relevant to a flagged flow.
Other regimes (e.g. GDPR) are reference-only and not a v1 focus.

## 4. Policy & execution model

**The policy is the eval set — a JSON file the user provides**, mapping each **data
classification** to the jurisdictions considered acceptable for that class:

```json
{
  "non-pii":      ["hk", "CN-GBA", "cn", "mo", "sg", "us", "gb"],
  "employee-pii": ["hk", "CN-GBA"],
  "customer-pii": ["hk", "CN-GBA", "sg"]
}
```

- **Classifications (v1, extensible):** `non-pii`, `employee-pii`, `customer-pii`.
- **Jurisdiction values (v1):** **ccTLD / ISO-3166 country codes** (lowercase: `hk`, `cn`, `sg`,
  `my`, `us`, `gb`, `mo`, …) plus the uppercase special tokens **`CN-GBA`** (nine Mainland GBA
  cities) and **`GBA`** (alias for `hk` + `CN-GBA`). **Deny by default:** any code a flow resolves
  to that is not on the list for that classification fails — there is no `overseas` catch-all.
- The user — who knows their home regime (PDPO / PIPL) and obligations — decides each list.
  borderlint **enforces** the list; it does not decide it.
- **Deny by default** mirrors a **PDPO agreed-locations** commitment: customer PII may flow to
  `sg` (named in your EULA) but a flow to `my` (not named) fails — without you enumerating every
  country on earth to forbid.

**Per execution, the run declares one classification** — the data class flowing through the path
being scanned (e.g. a service handling customer PII runs with `customer-pii`). borderlint detects
the AI providers that path talks to, resolves each to a jurisdiction, and fails if any falls
outside the acceptable list for that classification:

```
borderlint scan ./service --policy residency.json --classification customer-pii
```

**Where it runs (v1 execution contexts):**
- A **CI gate on the path to production** — block a merge/deploy that would send that data class
  to a jurisdiction the policy doesn't allow.
- A **supply-chain / container scan** (JFrog-style SCA) — inspect dependencies and container
  images for AI endpoints that would route data out of the allowed jurisdictions.

This keeps borderlint pragmatic: it never has to *guess* what data a path handles — the pipeline
asserts the classification, and borderlint governs the resulting flows.

## 5. Capability map

Status: **✅** = shipped (v1.0.0) · **next** = planned next · **later** = deferred. The full P1
MVP and most of P2 have shipped; the remaining work is re-tiered into next/later below.

### A. Detection — *find every AI data flow*
| # | Capability | Status |
|---|---|---|
| A1 | Detect AI provider **SDK imports** in Python (AST) | ✅ |
| A2 | Detect AI provider **endpoint/base‑URL references** in Python string literals | ✅ |
| A3 | Scan **config/text files** (`.env`, `.yaml`, `.toml`, `.json`, `.ini`) for endpoint hosts | ✅ |
| A4 | Scan **TypeScript / JavaScript** (regex imports; tree‑sitter only if precision demands) | ✅ |
| A5 | Detect **vector DBs / data sinks** that imply cross‑border storage (Pinecone, etc.) | ✅ |
| A6 | Detect **observability/telemetry** endpoints that exfiltrate prompts/traces | later |
| A7 | Detect **MCP servers / agent tool endpoints** by jurisdiction | later |

### B. Classification — *locate each flow*
| # | Capability | Status |
|---|---|---|
| B1 | Map provider → **jurisdiction** via bundled knowledge base | ✅ |
| B2 | Honour **region‑specific endpoints** (e.g. `dashscope-intl` → SG vs `dashscope` → CN) | ✅ |
| B3 | Mark **region‑in‑endpoint** providers (Azure OpenAI, Bedrock) as *Unknown* with guidance | ✅ |
| B4 | Resolve **Azure/Bedrock region** from the endpoint host when present | ✅ |
| B5 | Tag flows with the **v1 regimes** — PDPO (HK), PIPL (Mainland/GBA), GBA scheme — relevant to the declared home base | ✅ |
| B6 | Resolve flows to **country codes (ccTLD/ISO)** + special tokens **CN-GBA** / **GBA**; **deny-by-default** for codes not on the policy list | ✅ |
### C. Policy & governance — *decide what's allowed*
| # | Capability | Status |
|---|---|---|
| C1 | **Classification-keyed JSON policy** (the eval set): each data class → acceptable jurisdictions | ✅ |
| C2 | Provider **allow / deny lists** | ✅ |
| C3 | Configurable handling of **unknown jurisdiction** (`warn` \| `fail`) | ✅ |
| C4 | Configurable **`fail_on`** set (which findings break the build) | ✅ |
| C5 | **Inline annotations / waivers** to accept a specific flow with justification | ✅ |
| C6 | **Data‑class‑aware** rules (e.g. "personal data must stay in HK/SG", other data freer) | ✅ |
| C7 | Org‑level **shared/base policies** that repos extend | later |
| C8 | Residency targets may be **discrete entities or zones** (e.g. `allow: [HK, GBA]`) | ✅ |
| C9 | Surface **relevant arrangement reference links** for a flagged flow as *context* — e.g. **GBA Standard Contract**; reference only, not enforced (applicability depends on the user's home jurisdiction & data scope) | ✅ |
| C10 | Declare **home base / regime** — HK·PDPO or GBA/Mainland·PIPL — so defaults & surfaced references adapt | ✅ |

### D. Reporting & output
| # | Capability | Status |
|---|---|---|
| D1 | Human‑readable **CLI report** grouped by provider + jurisdiction | ✅ |
| D2 | **JSON** output for tooling | ✅ |
| D3 | **Mermaid** data‑flow map (app → providers, by jurisdiction) | ✅ |
| D4 | **SARIF** output (surfaces in GitHub code‑scanning) | ✅ |
| D5 | **Inventory / "AI data‑flow SBOM"** export | ✅ |
| D6 | Diff mode: *what new cross‑border flows did this PR introduce?* | ✅ |

### E. Integration
| # | Capability | Status |
|---|---|---|
| E1 | `borderlint scan <path>` CLI with non‑zero **exit code** on violations | ✅ |
| E2 | Zero‑config **inventory mode** when no policy file is present | ✅ |
| E3 | Ready‑made **GitHub Action** | ✅ |
| E4 | **pre‑commit** hook | ✅ |
| E5 | GitLab CI / generic CI recipes (GitHub Actions + Jenkins recipes shipped; GitLab pending) | next |
| E6 | Per-run **`--classification`** input (the data class on the scanned path) | ✅ |
| E7 | **Supply-chain / container scan mode** (JFrog-style SCA of dependencies & images) | later |

### F. Knowledge base — *the crown jewel*
| # | Capability | Status |
|---|---|---|
| F1 | Bundled provider KB: SDKs, endpoints, jurisdictions (US/EU/CN/HK/SG/UK/…) | ✅ |
| F2 | Broad **east‑west coverage**: OpenAI, Anthropic, Google, Azure, Bedrock, Mistral, Cohere + **Tencent Hunyuan, Alibaba Qwen/DashScope, DeepSeek, Moonshot, Zhipu, Baidu** | ✅ |
| F3 | **User‑supplied / override** KB (`--providers custom.json`) | ✅ |
| F4 | Community contribution workflow (add a provider via PR) | ✅ |
| F5 | Versioned KB with provenance/date stamps | ✅ |
| F6 | **Arrangements reference list** — links + one-line summaries of cross-border schemes (GBA Standard Contract; PIPL standard contract; GDPR SCCs / adequacy). Reference only — no enforcement logic | ✅ |

### G. Optional AI enrichment *(uses spare Claude capacity; never required)*
| # | Capability | Status |
|---|---|---|
| G1 | Classify "does this payload likely carry **personal data**?" | later |
| G2 | Plain‑language **explanation + remediation** hint per violation | next |
| G3 | Suggest a starter **policy** from a repo's current flows | later |

### H. Companion (separate repo, same family)
| # | Capability | Status |
|---|---|---|
| H1 | **borderlint‑bench** — living eval: *do frontier models honour the residency & tool‑scope constraints you set?* | later |

## 6. Non‑goals (explicitly out of scope)
- Not a **runtime gateway / proxy** (that space is crowded; we are pre‑ship, static).
- Not a full **SAST / secret scanner** — single concern: AI data residency & cross‑border flow.
- Not a **DLP** product; we flag *where* data flows, not inspect payload contents at runtime.
- Not **legal advice** — regime tags (PIPL/GDPR/PDPO) are context, not a compliance ruling.
- Does **not adjudicate which cross-border arrangement applies to you** (depends on your home jurisdiction, data classes, and user base) — it links to arrangements as reference; you choose your accepted entities/zones.
- Does **not resolve per-city location** within `CN-GBA` — the zone tag suffices for v1.
- Not a **global** residency solver in v1 — optimized for a **HK/GBA home base**; arbitrary home jurisdictions (a US/EU company's own residency logic) come later.
- Regimes **beyond PDPO / PIPL / GBA** (e.g. GDPR enforcement logic) are out of v1 — referenced, not implemented.

## 7. Primary users

*v1 focus: companies whose home base is **Hong Kong or the Greater Bay Area**.*
- Platform / DevOps leads governing AI adoption across multiple clouds and regions.
- Regulated‑industry teams (finance, gaming, health) operating across the east‑west boundary.
- Privacy / security engineers who must evidence *where AI data goes* in CI.

## 8. Guiding principles
- **Vendor‑neutral** — Western and Chinese providers treated identically.
- **Deterministic core** — works offline; AI enrichment is strictly optional.
- **Zero‑config is useful** — first run always produces a flow map.
- **Honest about limits** — region‑in‑endpoint and runtime‑injected values are surfaced, not hidden.
- **MIT, single‑purpose, finishable.**

## 9. MVP cut (delivered)
**The MVP was** A1–A3, B1–B3, C1–C4, D1–D3, E1–E2, F1–F3 — a genuinely useful, shippable
tool: a residency‑aware AI data‑flow scanner with an east‑west KB. The east-west **jurisdiction model** (B6) — discrete HK / CN / **CN-GBA** / MO entities and the **GBA** zone with zone-aware residency (C8) — shipped in the MVP; the named **GBA Standard Contract** arrangement (C9) shipped as a follow-on.

In short, **v1 solves it for a HK/GBA company**: detect AI flows, classify each flow to a country code (ccTLD) plus the CN-GBA / GBA tokens, and check them against an HK/GBA-centric residency policy tied to your declared regime (PDPO for HK, PIPL for GBA/Mainland) — not a global residency solver.

The v1 **interface** is concrete: a JSON policy mapping each data classification (`non-pii` / `employee-pii` / `customer-pii`) to acceptable jurisdictions, plus a per-run `--classification`, executed as a CI gate on the path to production (with a supply-chain/container scan mode later).
