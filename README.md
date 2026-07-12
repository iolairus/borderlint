# borderlint

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-borderlint-2188ff?logo=githubactions&logoColor=white)](https://github.com/marketplace/actions/borderlint-ai-data-residency-lint)

**Map and govern where your AI data and traffic flow — who can compel its disclosure, and whose
model weights it runs.**

A static, in-CI linter for **AI data residency, sovereignty, and model provenance across APAC &
EMEA**, with first-class **HK / GBA** support. borderlint statically scans your repo (**Python
and TypeScript/JavaScript**) for AI provider usage and evaluates each flow against three
orthogonal dimensions:

- **Residency** — *where the bytes rest*. Each flow resolves to a jurisdiction (ccTLD/ISO codes
  plus the `CN-GBA` / `GBA` tokens); a flow outside the allow-list for the declared data class
  fails the build.
- **Sovereignty** — *which government can compel disclosure*. A US-headquartered provider (AWS,
  Azure, GCP, OpenAI, Anthropic) is subject to the CLOUD Act regardless of the endpoint region;
  a flow to AWS Bedrock `ap-east-1` is residency-clean for a PDPO policy (residency `hk`) yet
  remains under **US sovereignty**. An optional `sovereignty` block constrains this per class.
- **Provenance** — *whose model weights the flow runs*. Model references in code — a Bedrock
  model ID, a bare API model string, an aggregator-qualified ID, a HF repo, a `.gguf` path, an
  Ollama tag — resolve to the developer's bloc. Bedrock `ap-east-1` serving DeepSeek-R1 is
  residency `hk`, sovereignty `us`, **provenance `cn`**; self-hosted Qwen is `local`/`local`/`cn`.
  An optional `provenance` block constrains this per class.

Declare a home base — **HK, Macao, the GBA, Japan, Korea, Singapore, Australia, the UK, the EU,
or Malaysia** — and flagged flows are tagged with the matching regime (PDPO, PIPL, APPI, PIPA,
PDPA, the Privacy Act, GDPR …) and its cross-border reference. Western and Chinese providers are
treated evenly. **Zero runtime dependencies.**

## Use

```bash
python -m borderlint scan ./service --policy residency.json --classification customer-pii
```

- No `--policy` → **inventory mode** (lists flows + jurisdictions, exits 0).
- `--format json|mermaid|sarif|sbom|evidence` — machine output, a flow map, **SARIF** for GitHub code-scanning,
  a deterministic **AI data-flow SBOM**, or an **evidence pack** — a fileable markdown transfer
  inventory with an audit envelope (git commit, policy SHA-256, KB review dates), all three
  governance axes with developer orgs, a waiver register, and a regime annex (PDPO, PIPL + GBA SC,
  Macao PDPA, PDPA-SG) that fills what the scan proves and leaves marked blanks for what only the
  organisation knows. Exports are artifacts, not gates: they exit 0.
- `diff <baseline.sbom> <current.sbom>` — compare two SBOMs; **exits 1 when the PR adds a new
  non-`local` flow** (new egress), else 0. Diff the base-branch SBOM against the PR's to gate new AI egress.
- `init [path]` — **scaffold a `residency.json`** instead of hand-writing one. It interviews you for
  a home base (HK, Macao, GBA, JP, KR, SG, AU, UK, EU, MY) and the data classes you handle, runs a
  read-only inventory scan of `path` (default `.`), then walks each observed jurisdiction and asks
  whether to keep it for each class — proposing allow-lists grounded in what your code actually
  reaches. Writes `residency.json` (refuses to overwrite without `--force`). For scripted/CI use,
  skip the prompts with `--home <seat> --classes <csv>`:
  ```bash
  borderlint init . --home hk --classes customer-pii,non-pii --output residency.json
  ```
- Accept a reviewed flow with an inline `# borderlint: allow <reason>` **waiver** (justification
  required; it's reported as *waived*, not hidden, and can't override an explicit provider `deny`).
- Exit code is non-zero on a violation, so it gates CI.

## Policy (the eval-set)

`residency.json` maps each data class to the jurisdictions you accept, and optionally to the
**sovereignty** and **provenance blocs** you accept for compelled-disclosure and model-origin
exposure:

```json
{
  "home_location": "hk",
  "classifications": {
    "customer-pii": ["hk", "CN-GBA", "sg"],
    "employee-pii": ["hk", "CN-GBA"],
    "non-pii":      ["hk", "CN-GBA", "cn", "mo", "sg", "us", "gb"]
  },
  "sovereignty": {
    "on_unknown": "warn",
    "classifications": { "customer-pii": ["eu", "uk", "local"] }
  },
  "provenance": {
    "on_unknown": "warn",
    "classifications": { "customer-pii": ["us", "eu", "uk"] },
    "deny_models": []
  }
}
```

**Residency — deny-by-default**: a flow to any code not on the list for the declared class fails —
so `sg` is allowed but `my` is not, matching a PDPO agreed-locations EULA. `GBA` is shorthand for
`hk` + `CN-GBA`.

**Sovereignty — opt-in, orthogonal to residency.** Residency says *where the bytes rest*;
**sovereignty** says *which government can compel disclosure* — a US provider (AWS, Azure, GCP,
OpenAI) is subject to the CLOUD Act regardless of the endpoint region. Add a `sovereignty` block
to constrain it per class. Bloc vocabulary: `us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`, `ca`, `jp`,
`kr`, `sg`, `au`, `ae`, `ch`, `local`, `unknown`. Absent the block, behaviour is unchanged (sovereignty is reported as a column but never
gates). `local` sovereignty is exempt (self-hosted = no external sovereign). See
[CAPABILITIES.md §3.1](CAPABILITIES.md) for the full model.

**Provenance — opt-in, orthogonal to both.** *Whose model weights* a flow runs, resolved in two
tiers: a model reference bound to the flow wins; absent one, a provider that serves only its own
models (OpenAI, Anthropic, DeepSeek …) resolves to its org's bloc, while multi-model hosts
(Bedrock, Vertex) and aggregators stay `unknown`. Aggregator-qualified IDs
(`deepseek/deepseek-r1` via OpenRouter) resolve provenance even where residency and sovereignty
are `unknown` — the one axis routers don't obscure. The `provenance` block mirrors the
sovereignty shape; vocabulary is the same minus `local` (weights always have a developer).
Fine-tunes inherit the base family's bloc. A `deny_models` list of anchored model-id prefixes
bans a family regardless of host or bloc — `"deny_models": ["deepseek"]` fails a Bedrock flow
serving DeepSeek-R1 even where `cn` weights are otherwise allowed; denies match after the same
normalization as the map (GGUF paths, redistributor repos, `@`-version pins can't dodge them),
sit in the default failure set like the provider deny, and cannot be waived inline. See
[CAPABILITIES.md §3.2](CAPABILITIES.md).

Declare your **`home_location`** — a GBA seat (`hk`/`mo`/`CN-GBA`) or an APAC/EMEA seat
(`jp`, `kr`, `sg`, `au`, `uk`, `eu`, `my`) — and a flagged flow is tagged with the **data-protection
regime** in play and linked to the relevant **cross-border arrangement** (the matching GBA Standard
Contract variant, PIPL cross-border, GDPR, the UK IDTA, APPI Art. 28, PIPA Art. 28-8, PDPA s.26/s.129,
APP 8) as reference links. (`home_regime` `pdpo`/`pipl` is still accepted.)

## Capabilities

- **Languages:** Python (AST) and TypeScript/JavaScript (`import` / `require` / dynamic `import()`),
  plus endpoint references in config/text files (incl. env-style keys like `MYAPP_LLM_SERVER_URL` in `.env`, compose, and settings files) and **OpenAI-compatible `/v1/chat/completions` calls**
  — even to a runtime-configured host (resolved to `unknown`, so `on_unknown: fail` gates it).
- **Providers:** 85+ across the east-west boundary — OpenAI, Anthropic, Google (Gemini + **Vertex
  AI**), Azure, Bedrock, Mistral, Cohere, Groq, Together, Perplexity, xAI, Cerebras, Fireworks,
  Replicate, SambaNova, Meta Llama, **AWS SageMaker, Snowflake Cortex** + **Tencent, Alibaba, DeepSeek, Moonshot, Zhipu/Z.ai, Baidu,
  Volcengine, MiniMax**, plus **AI21 (IL), Jina (DE), Voyage, GigaChat (RU), Sarvam (IN), Scaleway &
  OVHcloud (FR/EU)** and region-selectable clouds (**IBM watsonx, Oracle OCI, Cloudflare Workers AI,
  Heroku** → `unknown` until you pin a region) — with Python and JS/TS package names and the **Vercel
  AI SDK** (`@ai-sdk/*`).
- **Image / video / speech:** generation (**Stability AI, Black Forest Labs/Flux, Runway, Recraft**)
  and **speech-to-text / TTS** (**ElevenLabs, Deepgram, AssemblyAI, Soniox, Amazon Polly**) — tagged
  with their `category` and governed for residency like any other flow.
- **Vector stores (data sinks):** Pinecone, Weaviate Cloud, Qdrant Cloud, Zilliz/Milvus — flagged
  as `vector_store` and governed for residency (region is per-cluster, so default `unknown`).
- **Aggregators / routers:** litellm, langchain, LlamaIndex, aisuite, OpenRouter, AI/ML API, Vercel
  AI core & Gateway → `unknown` (runtime-routed), so `on_unknown: fail` blocks them for sensitive classes.
- **Jurisdictions:** ccTLD/ISO codes + `CN-GBA` / `GBA`; **AWS / Azure / GCP-Vertex region resolved
  from the endpoint host** where present (e.g. `bedrock-runtime.ap-east-1…` and
  `asia-east2-aiplatform.googleapis.com` → `hk`).
- **Sovereignty:** a per-flow bloc (`us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`, `ca`, `jp`, `kr`,
  `sg`, `au`, `ae`, `ch`, `local`, `unknown`) derived from the provider's home legal regime — orthogonal to residency. Opt-in
  policy block; reported in every output format; host-level overrides for ring-fenced
  subsidiaries (e.g. AWS China / Sinnet → `cn`).
- **Provenance:** whose model weights a flow runs — a third orthogonal bloc resolved from model
  references in code (`anthropic.claude-…`, `qwen2.5-72b`, `deepseek/deepseek-r1`, `Qwen/…`,
  version-pinned `claude-3-5-haiku@20241022`) or
  the provider's first-party default. Bedrock `ap-east-1` serving DeepSeek-R1 is residency `hk`,
  sovereignty `us`, provenance `cn`. Local LLM usage resolves too: GGUF/MLX redistributor repos
  (`TheBloke/…`, `mlx-community/…`), `.gguf` file paths, and Ollama tags (`llama3.2`, `qwen2.5`)
  — so a self-hosted Qwen reads `local`/`local`/`cn`. Opt-in `provenance` policy block, same
  shape as sovereignty, plus a `deny_models` family ban with provider-deny semantics; findings
  name the developer organisation when the map knows it.
- **Policy:** classification-keyed JSON eval-set, deny-by-default, provider allow/deny, configurable
  failure set, declared home regime.
- **Regimes & arrangements:** declared home location → data-protection regime tag + the cross-border
  mechanism reference for a flagged flow (context only, never adjudicated). GBA seats `hk`/`mo`/`CN-GBA`
  → PDPO / Macao PDPA / PIPL + the matching GBA Standard Contract; **APAC/EMEA seats `jp` (APPI), `kr`
  (PIPA), `sg`/`my` (PDPA s.26 / s.129), `au` (APP 8), `uk` (UK IDTA), `eu` (GDPR)** → their transfer
  mechanism. PIPL cross-border and GDPR are also surfaced for those destinations.
- **Output & CI:** text / JSON / Mermaid / SARIF / SBOM, an SBOM **`diff`** gate for new
  egress, inline **waivers**, exit codes, GitHub Action + Jenkins.

## Scope

For HK / CN / GBA / MO plus **JP / KR / SG / AU / UK / EU / MY** home bases (regime tags + cross-border
references). Not yet: AE / IN / ID (cross-border instruments not yet operational); other jurisdictions;
CycloneDX / SPDX SBOM export and optional LLM enrichment. Per-capability status — shipped vs. next
vs. later — is tracked in [`CAPABILITIES.md`](CAPABILITIES.md).

## Internal endpoints

Map your own regional endpoints to jurisdictions; they **merge** with the bundled provider KB (your
entries win on conflict):

```json
{ "endpoints": { "llm-cn.acme.internal": "cn", "llm-hk.acme.internal": "hk", "llm-sg.acme.internal": "sg" } }
```

```bash
borderlint scan . --providers internal-endpoints.json --policy residency.json --classification customer-pii
```

A configuration wired to the **wrong regional endpoint** — e.g. the CN endpoint for HK-only
customer PII — then fails the build, so you can't ship a service pointed at the wrong region.

A runnable end-to-end example is in [`examples/gba-resident-app/`](examples/gba-resident-app/) — a
GBA-resident app (internal Shenzhen endpoint → `CN-GBA`, plus Mainland / Western / local fallbacks). Run
it under `residency-hk.json` vs `residency-mo.json` and the surfaced **GBA Standard Contract** flips
between the *(Mainland, Hong Kong)* and *(Mainland, Macao)* variant, and the regime tag between PDPO and
Macao PDPA:

```bash
borderlint scan examples/gba-resident-app \
  --providers examples/gba-resident-app/internal-endpoints.json \
  --policy examples/gba-resident-app/residency-hk.json --classification customer-pii
```

The same scan renders to a data-flow map grouped by jurisdiction — Mermaid source in
[`dataflow.mmd`](https://github.com/iolairus/borderlint/blob/main/examples/gba-resident-app/dataflow.mmd),
rendered to PNG:

![borderlint AI data-flow map for the GBA-resident sample app, grouped by jurisdiction](https://raw.githubusercontent.com/iolairus/borderlint/main/examples/gba-resident-app/dataflow.png)

## CI

Same command in any pipeline. GitHub Actions (composite action):

```yaml
- uses: iolairus/borderlint@v1.7.0
  with: { path: ., policy: residency.json, classification: customer-pii }
```

Jenkins / anything else: `pip install borderlint && borderlint scan . --policy residency.json
--classification customer-pii` — a non-zero exit fails the stage. Full examples in `examples/ci/`.

pre-commit — catch a bad flow before it's committed (`.pre-commit-config.yaml`):

```yaml
- repo: https://github.com/iolairus/borderlint
  rev: v1.7.0
  hooks:
    - id: borderlint
      args: [--policy, residency.json, --classification, customer-pii]
```

The hook runs `borderlint scan` over the repo (the `args` are required for a real gate; without a
policy it runs inventory mode and always passes).

## Keeping the KB fresh

A weekly GitHub Action (`.github/workflows/kb-refresh.yml`) checks freshness on every axis:
providers we don't yet cover (diffed against litellm's registry), **model families the
provenance map doesn't resolve** (aggregated, so the issue lists families to curate rather than
thousands of model IDs), sovereignty-map completeness, and each bundled KB's last-reviewed date.
It maintains a single standing review issue, updated in place. Route aliases and out-of-scope
names are recorded in `scripts/kb_drift_aliases.json`; jurisdictions and blocs are assigned
**by hand**, never auto-merged. `borderlint --version` shows the KB's last-reviewed
date. To add or correct a provider, see [`CONTRIBUTING.md`](CONTRIBUTING.md) (KB schema + PR
workflow).

## Development

borderlint is built **spec-first** with [OpenSpec](https://github.com/Fission-AI/OpenSpec): every change
is a reviewed proposal (specs + design + tasks) gated by a `spec-reviewer` agent before any code is
written. To bootstrap the same workflow into another repo:

```bash
scripts/opsx-init.sh [--no-jira] /path/to/your/repo
```

It scaffolds `AGENTS.md`, `.claude/` (slash commands + the spec-reviewer gate), an empty `openspec/`, and
`workflow.yaml`. `--no-jira` trims it to the core loop — propose → review → apply → commit → ship.

## License

MIT © 2026 Iolaire McKinnon. Vendor-neutral by design.
