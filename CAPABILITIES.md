# borderlint — Capability Set

> **Status:** shipped. The full P1 (MVP) and most of P2 are built and tested. The map below marks
> each capability as ✅ shipped, next, or later.

## 1. Purpose

borderlint answers one question about your codebase: **where does our AI data go, and does that
comply with our data-residency policy?** Residency means the jurisdiction where data is processed
or stored.

It scans code without running it, before deployment. It treats Western and Chinese providers
evenly. It is designed for teams that work across Mainland China, Hong Kong, and other jurisdictions.

> **v1 focus — Hong Kong & GBA companies.** borderlint v1 is built for organisations whose home
> location is Hong Kong or the Greater Bay Area (GBA). It answers: does our AI data stay within Hong
> Kong or the GBA, or leave it? It supports Hong Kong entities under PDPO and GBA or Mainland
> entities under PIPL, including the GBA Standard Contract route between them.
>
> Residency policies for arbitrary home jurisdictions, such as a US company's own rules, are
> outside the v1 scope. Other supported APAC/EMEA home locations add informational legal context.

## 2. Positioning

| Most existing tools | borderlint |
|---|---|
| Runtime gateways or proxies | Scans code in CI before deployment |
| EU-centred | Covers Mainland China, Hong Kong, Singapore, and other east-west routes |
| Enterprise platforms | Dependency-free CLI, MIT licence, vendor-neutral, useful without configuration |
| Generic AI governance | Focuses on data residency and cross-border flows |

## 3. Jurisdiction model

borderlint uses three concepts to describe jurisdictions and transfer rules.

**Discrete entities** include `us`, `eu`, `sg`, and `uk` (or `gb`). They also distinguish `cn`
(Mainland China in general), `CN-GBA` (the nine Mainland GBA cities), `hk` (Hong Kong), and `mo`
(Macao). A Shenzhen endpoint is `CN-GBA`; a Beijing endpoint is `cn`.

**Zones** group entities for a data-transfer arrangement. The `GBA` policy alias covers the nine
Mainland GBA cities and Hong Kong. It excludes Macao, which has a separate Mainland–Macao contract
reference.

**Transfer arrangements** are legal mechanisms that may allow a flow that residency rules would
otherwise block. borderlint links to these mechanisms for reference. It does not decide whether
they apply to you.

The flagship example is the **GBA Standard Contract**:

> “Standard Contract for the Cross-boundary Flow of Personal Information within the
> Guangdong-Hong Kong-Macao Greater Bay Area (Mainland, Hong Kong)”.
>
> It permits personal-information flows in both directions between Hong Kong and the nine Mainland
> GBA cities: Guangzhou, Shenzhen, Zhuhai, Foshan, Huizhou, Dongguan, Zhongshan, Jiangmen, and
> Zhaoqing. It lifts the general Mainland framework's volume restriction and reduces the transfer
> assessment from six areas to three. It also shortens the filing process to 10 working days.
>
> It is voluntary. It took effect on 13 December 2023 and expanded to all sectors on 1 November
> 2024. Hong Kong's Digital Policy Office and the CAC of Guangdong administer it. Macao is outside
> this variant.
>
> Source: [digitalpolicy.gov.hk — GBA cross-boundary data flow](https://www.digitalpolicy.gov.hk/en/our_work/digital_infrastructure/mainland/gbacbdf/cross-boundary_data_flow/index.html)

A separate [GBA Standard Contract (Mainland, Macao)](https://www.dsedt.gov.mo/en/web/public/pg_tpd_gbadata_contract)
covers Macao ↔ Mainland GBA flows. It does not add `mo` to the `GBA` policy alias.

This model lets a policy allow personal data within the GBA while blocking Beijing (`cn`) and
handling Macao separately. A flat “China or not China” model cannot express that distinction.

### Home locations beyond the GBA

A declared `home_location` of `jp`, `kr`, `sg`, `au`, `uk` (or `gb`), `eu`, or `my` adds that
jurisdiction's legal context to a flow that violates policy:

- Japan: APPI Article 28.
- Korea: PIPA Article 28-8.
- Singapore: PDPA section 26.
- Australia: Australian Privacy Principle 8.
- UK: UK IDTA.
- EU: GDPR Chapter V.
- Malaysia: PDPA section 129.

The EU produces a GDPR reference, not a regime tag. Support for `ae`, `in`, and `id` is deferred
until their cross-border instruments become operational.

**Legal scope:** borderlint links to relevant arrangements but does not decide whether they apply
to you. That decision depends on your home jurisdiction, data classes, and users. You express your
accepted position through the entities and zones in your policy. The links support that choice;
they do not make it for you.

### Resolved jurisdiction values

Every flow resolves to one of these values:

- A lowercase country code based on ccTLD or ISO 3166-1, such as `hk`, `cn`, `sg`, `my`, `us`,
  `gb`, or `mo`.
- `CN-GBA` for the nine Mainland GBA cities.
- `local` for loopback or on-host inference.
- `unknown` when static evidence is insufficient.

Policies can also use `GBA` as an alias for `hk` plus `CN-GBA`. There is no `overseas` catch-all.

`local` is exempt from the residency allow-list because it is not a cross-border transfer.
`unknown` follows the top-level `on_unknown` setting: `warn` by default or `fail`. Every other
unlisted jurisdiction fails by default. This lets you express precise agreed-location rules, such
as allowing `sg` but not `my` for customer PII.

### Regulatory context

For Hong Kong and the GBA, borderlint covers PDPO, PIPL, the two GBA Standard Contract variants,
and Macao PDPA. You can declare a supported `home_location` or a legacy `home_regime` of `pdpo` or
`pipl`.

Reports add relevant regime tags and arrangement links to flows that violate policy. These details
never change the verdict. GDPR remains a reference, never a regime tag.

### 3.1 Sovereignty — who may compel disclosure

**Sovereignty** describes which government may compel the provider to disclose data, regardless of
where the endpoint sits. It is a separate check from residency.

A US-headquartered provider such as AWS, Azure, GCP, OpenAI, or Anthropic remains subject to US
compelled-disclosure law in every hosting region. Relevant laws include the CLOUD Act 2018, FISA
702, and Patriot Act §215.

For example, AWS Bedrock in `ap-east-1` has residency `hk` and sovereignty `us`. It can pass a Hong
Kong residency policy while still carrying US disclosure exposure. Residency alone cannot express
a rule such as “customer PII may rest in `hk` but must not be under US compelled-disclosure law”.

**Sovereignty blocs:** `us`, `eu` (the EU/EEA as one unit), `cn`, `uk` (distinct from the EU), `ru`,
`in`, `il`, `ca`, `jp`, `kr`, `sg`, `au`, `ae`, `ch`, `vn`, `local`, and `unknown`.

The bloc comes from the provider's home legal regime, not the endpoint region. `local` means
self-hosted inference with no external provider sovereign. `unknown` covers aggregators, custom
endpoints, and unmapped providers.

**Optional policy block:**

```json
"sovereignty": {
  "on_unknown": "warn",
  "classifications": { "customer-pii": ["eu", "uk", "local"] }
}
```

Without this block, borderlint reports sovereignty but does not check it against the policy. With
the block, mismatches warn unless you add `sovereignty` to `fail_on`. `local` is exempt from the
allow-list, matching the residency exemption.

**Legal scope:** the sovereignty map reports potential compelled-disclosure exposure. It does not
decide whether a statute applies to a particular flow. That answer depends on the provider's
corporate structure, the data, and your jurisdiction. borderlint reports the bloc; your policy
sets the response.

### 3.2 Provenance — who developed the model weights

**Provenance** identifies the model developer and the legal bloc under which that developer
operates. It is a third separate check.

AWS Bedrock in `ap-east-1` serving DeepSeek-R1 has residency `hk`, sovereignty `us`, and provenance
`cn`. Self-hosted Qwen through Ollama has residency `local`, sovereignty `local`, and provenance
`cn`.

**Resolution uses two steps:**

1. Resolve a model reference found in code through the bundled provenance map. Matching is
   case-insensitive and anchored; the longest prefix wins.
2. Without a model reference, use the provider's first-party default when it serves only its own
   models. Multi-model hosts and aggregators remain `unknown`.

Model references include managed-platform IDs such as `anthropic.claude-…`, API names such as
`gpt-4o` or `qwen2.5-72b`, aggregator-qualified IDs such as `deepseek/deepseek-r1`, and hub
repositories such as `Qwen/…`.

A model reference binds to an eligible provider flow in the same file. Without one, it becomes a
standalone `model_reference` finding. That finding describes weights origin, not a network flow,
so it has no residency verdict. References never bind across files or to agent-tool and
observability endpoints.

Qualified IDs can reveal provenance through a router. For example, `deepseek/deepseek-r1` through
OpenRouter has provenance `cn` while residency and sovereignty remain `unknown`.

**Local models:** borderlint recognises GGUF/MLX redistributor repositories such as
`mlx-community/…`, `TheBloke/…`, `bartowski/…`, and `unsloth/…`. It ignores the repackaging
organisation and resolves the underlying model family. It also recognises model-file basenames,
including `.gguf`, `.onnx`, and `.safetensors`, plus local-runtime tags such as `llama3.2`, `phi4`,
`gemma2:9b`, and `qwq:32b`.

Tool names that merely resemble a family, such as `llama_index` and `llama-cpp-python`, do not
match. borderlint ignores curated launcher namespaces (`ollama/`, `vllm/`, `lmstudio/`) and
host-like registry segments (`docker.io/library/…`, `mirror.internal/…`). These namespaces say
where weights came from, not who developed them.

An arbitrary leading segment remains significant. For example, `src/deepseek/client.py` resolves
nothing. A URL with `https://` also resolves nothing under the current namespace rules; use the
scheme-less `huggingface.co/…` form for the documented behaviour. Removing this limitation is a
known follow-up.

**Provenance blocs:** `us`, `eu`, `cn`, `uk`, `ru`, `in`, `il`, `ca`, `jp`, `kr`, `sg`, `au`,
`ae`, `ch`, and `unknown`. This is the sovereignty vocabulary without `local` and `vn`. Weights
always have a developer, and `vn` is not currently a provenance bloc.

Fine-tunes and distillations inherit the base family's bloc. Reports name the developer
organisation when the map knows it.

**Optional policy block:**

```json
"provenance": {
  "on_unknown": "warn",
  "classifications": { "customer-pii": ["us", "eu"] }
}
```

Without the block, borderlint reports provenance but does not check it against the policy. With
the block, mismatches warn unless you add `provenance` to `fail_on`. Setting its `on_unknown` to
`fail` makes unknown provenance fail on its own.

`deny_models` contains anchored model-ID prefixes that block a family regardless of host or bloc.
Denied models fail by default and cannot be waived inline. The provenance map reports weights
origin; it does not decide whether export controls apply.

## 4. Policy and execution model

The policy is a JSON file that maps each data class to its acceptable jurisdictions:

```json
{
  "non-pii":      ["hk", "CN-GBA", "cn", "mo", "sg", "us", "gb"],
  "employee-pii": ["hk", "CN-GBA"],
  "customer-pii": ["hk", "CN-GBA", "sg"]
}
```

- **Built-in data classes:** `non-pii`, `employee-pii`, and `customer-pii`. You can add your own.
- **Jurisdiction values:** lowercase country codes plus `CN-GBA`, `GBA`, `local`, and `unknown`.
- **Deny by default:** an unlisted country or `CN-GBA` fails. You do not need to list every
  forbidden country.
- **Local and unknown:** `local` is exempt from the residency allow-list. `unknown` follows the
  top-level `on_unknown` setting.
- **Your decision:** you know your obligations and choose each list. borderlint enforces that
  choice; it does not make the legal decision for you.

Each run uses one data class. For example, a service handling customer PII runs with
`customer-pii`:

```bash
borderlint scan ./service --policy residency.json --classification customer-pii
```

borderlint detects the providers on that path, maps each flow to a jurisdiction, and fails when a
flow falls outside your list.

Use it as a CI check before merge or deployment. A supply-chain and container scan for dependencies
and images is planned for later.

This model avoids guessing what data a path handles. Your pipeline declares the data class, and
borderlint checks the resulting flows.

## 5. Capability map

Status: **✅** = shipped · **next** = planned next · **later** = deferred. The full P1 MVP and most
of P2 have shipped.

### A. Detection — find AI data flows

| # | Capability | Status |
|---|---|---|
| A1 | Detect AI provider SDK imports in Python using the AST | ✅ |
| A2 | Detect AI provider endpoint and base-URL references in Python strings | ✅ |
| A3 | Scan `.env`, `.yaml`, `.toml`, `.json`, and `.ini` files for endpoint hosts | ✅ |
| A4 | Scan TypeScript and JavaScript imports, including dynamic imports | ✅ |
| A5 | Detect managed vector databases and other data sinks, such as Pinecone | ✅ |
| A6 | Detect curated Langfuse and LangSmith SDKs and telemetry endpoints; six exact case-sensitive keys and documented hosted mappings are supported. Other vendors, generic OpenTelemetry, and arbitrary URLs remain out of scope | ✅ (limited scope) |
| A7 | Detect Model Context Protocol (MCP) servers and explicit agent-tool endpoints through structured config scanning and `mcp_server` / `agent_tool_endpoint` findings | ✅ |
| A8 | Scan Java and Kotlin imports with endpoint, call-path, and waiver support matching JavaScript | ✅ |
| A9 | Scan C# `using` directives with endpoint, call-path, and waiver support matching JVM | ✅ |

### B. Classification — locate each flow

| # | Capability | Status |
|---|---|---|
| B1 | Map providers to jurisdictions through the bundled knowledge base | ✅ |
| B2 | Honour region-specific endpoints, such as `dashscope-intl` in Singapore versus `dashscope` in Mainland China | ✅ |
| B3 | Mark region-dependent providers such as Azure OpenAI and Bedrock as `unknown` without a region | ✅ |
| B4 | Resolve region-coded AWS, Azure, GCP Vertex, Aliyun, and Huawei hosts when the region is present | ✅ |
| B5 | Add informational PDPO, PIPL, Macao PDPA, APPI, PIPA, SG/MY PDPA, Privacy Act/APP, and UK GDPR/DPA 2018 context; GDPR remains a reference rather than a tag | ✅ |
| B6 | Resolve flows to country codes, `CN-GBA`, `local`, or `unknown`; support `GBA`, deny unlisted jurisdictions, exempt `local`, and apply `on_unknown` | ✅ |

### C. Policy and governance — decide what is allowed

| # | Capability | Status |
|---|---|---|
| C1 | JSON policy mapping each data class to acceptable jurisdictions | ✅ |
| C2 | Provider allow and deny lists | ✅ |
| C3 | Configurable `warn` or `fail` handling for unknown jurisdictions | ✅ |
| C4 | Configurable `fail_on` set | ✅ |
| C5 | Inline waivers with a required justification | ✅ |
| C6 | Different rules for different data classes | ✅ |
| C7 | Organisation-level base policies that repositories extend | later |
| C8 | Discrete entities and zones such as `hk` and `GBA` in residency targets | ✅ |
| C9 | Relevant transfer-arrangement links, including the GBA Standard Contract, as context without enforcement | ✅ |
| C10 | Home locations or legacy home regimes that change informational legal context without changing verdicts | ✅ |
| C11 | Optional per-class sovereignty allow-lists (§3.1) | ✅ |
| C12 | Optional per-class provenance allow-lists (§3.2) | ✅ |
| C13 | Evidence pack with audit details, waiver and data-practices registers, and legal annexes; organisation-supplied fields remain marked blanks | ✅ |

### D. Reporting and output

| # | Capability | Status |
|---|---|---|
| D1 | Human-readable CLI report grouped by provider and jurisdiction | ✅ |
| D2 | JSON output for other tools | ✅ |
| D3 | Mermaid data-flow map grouped by jurisdiction | ✅ |
| D4 | SARIF output for GitHub code scanning | ✅ |
| D5 | AI data-flow software bill of materials (SBOM) export | ✅ |
| D6 | Compare SBOMs to identify flows added or removed by a change | ✅ |
| D7 | Self-contained HTML report with no scripts or fetched resources | ✅ |
| D8 | Shields.io badge JSON for CI dashboards and pull requests; always exits zero | ✅ |
| D9 | Deterministic Suricata TLS-SNI alert rules from knowledge-base endpoints and an optional policy; always exits zero | ✅ |

### E. Integration

| # | Capability | Status |
|---|---|---|
| E1 | `borderlint scan <path>` CLI with a non-zero exit on violations in text, JSON, Mermaid, or SARIF format | ✅ |
| E2 | Inventory mode without a policy | ✅ |
| E3 | Ready-made GitHub Action | ✅ |
| E4 | pre-commit hook | ✅ |
| E5 | GitHub Actions, Jenkins, GitLab CI, and generic CI recipes | ✅ |
| E6 | Per-run `--classification` input | ✅ |
| E7 | Supply-chain and container scanning | later |
| E8 | Claude Code plugin and rules, Claude Code skill, and Cursor rules that scan before adding AI dependencies and report new flows | ✅ |

### F. Knowledge base

| # | Capability | Status |
|---|---|---|
| F1 | Bundled provider knowledge base with SDKs, endpoints, and jurisdictions | ✅ |
| F2 | Broad Western and Chinese provider coverage | ✅ |
| F3 | User-supplied knowledge-base overrides through `--providers custom.json` | ✅ |
| F4 | Community provider contributions through pull requests | ✅ |
| F5 | Versioned knowledge bases with provenance and review dates | ✅ |
| F6 | Cross-border arrangement links and summaries for reference only | ✅ |
| F7 | Advisory provider data practices with per-fact citations; never part of a verdict | ✅ |
| F8 | Generated provider and model-developer website | ✅ |
| F9 | Weekly provider, provenance, sovereignty, SDK, data-practice, and review-date checks | ✅ |

### G. Optional enrichment

| # | Capability | Status |
|---|---|---|
| G1 | Classify whether a payload is likely to contain personal data | later |
| G2 | Deterministic plain-language explanations and remediation hints through `--explain` | ✅ |
| G3 | Create a starter policy from current flows through `borderlint init` | ✅ |

### H. Companion project

| # | Capability | Status |
|---|---|---|
| H1 | `borderlint-bench`: a separate, living evaluation of whether frontier models honour residency and tool-scope constraints | later |

## 6. Non-goals

- borderlint is not a runtime gateway or proxy. It checks code before deployment.
- It is not a general static-analysis or secret scanner. Its focus is AI data residency and
  cross-border flows.
- It is not a data-loss-prevention product. It reports where data can flow; it does not inspect
  runtime payloads.
- It does not provide legal advice. Regime tags and transfer references are context, not rulings.
- It does not decide which transfer arrangement applies to you. You choose the accepted entities
  and zones in your policy.
- It does not resolve individual cities within `CN-GBA`.
- It is not a global residency solver in v1. Hong Kong and the GBA remain the focus; other
  supported home locations add informational context.
- GDPR remains a transfer reference, not a regime tag. Unmapped home locations add no derived
  legal context.

## 7. Primary users

The v1 focus is companies based in Hong Kong or the Greater Bay Area:

- Platform and DevOps leads who govern AI adoption across clouds and regions.
- Regulated teams in finance, gaming, and health that operate across east-west boundaries.
- Privacy and security engineers who need evidence of where AI data goes in CI.

## 8. Guiding principles

- **Vendor-neutral:** apply the same checks to Western and Chinese providers.
- **Deterministic core:** work offline; never require AI enrichment.
- **Useful without configuration:** the first scan produces a flow inventory.
- **Clear about limits:** report region-dependent and runtime-supplied values as `unknown`, not
  guessed locations.
- **MIT, single-purpose, finishable.**

## 9. MVP delivered

The MVP covered A1–A3, B1–B3, C1–C4, D1–D3, E1–E2, and F1–F3. It detected AI flows, mapped them
to jurisdictions, and checked them against a residency policy with an east-west knowledge base.

The jurisdiction model (B6) and zone-aware policy (C8) shipped in the MVP. The GBA Standard
Contract reference (C9) followed.

The v1 interface is a JSON policy mapping data classes to acceptable jurisdictions, plus one
`--classification` per run. Teams use it in CI before production. Supply-chain and container
scanning remain later work.
