# Contributing to borderlint

The most valuable contribution is **the knowledge base** — the mapping from AI providers and
endpoints to jurisdictions in `borderlint/data/providers.json`. borderlint is vendor-neutral:
Western and Chinese providers are treated identically, and every entry is reviewed by a human.

borderlint is built **spec-first** with [OpenSpec](https://github.com/Fission-AI/OpenSpec) (see
`AGENTS.md`). Code changes go through propose → review → apply. KB and doc contributions are
lighter — a pull request against the files below is enough.

## Add or correct a provider

1. Edit `borderlint/data/providers.json` (add an entry, or fix an existing one).
2. Run the suite: `pip install -e ".[dev]" && pytest`.
3. Open a PR. State your **source** for the jurisdiction (provider docs, data-residency page,
   region list). A maintainer assigns/confirms the jurisdiction — see *Jurisdictions are
   human-assigned* below.

### Provider entry schema

Each object in the `providers` array:

| Field | Required | Type | Meaning |
|---|---|---|---|
| `id` | yes | string | Stable internal id (snake_case), e.g. `alibaba_dashscope`. |
| `name` | yes | string | Human-readable name shown in reports. |
| `category` | no | `inference` \| `vector_store` \| `aggregator` \| `speech` | Provider type; defaults to `inference`. Use `vector_store` for a managed vector DBaaS (data-at-rest sink), `aggregator` for a multi-provider router, `speech` for a speech-to-text / text-to-speech API. Surfaced in text/JSON/SBOM output. |
| `jurisdiction` | yes | string | Default jurisdiction token for the provider (see tokens below). Use `unknown` when the host carries the region (Azure/Bedrock), the cluster region is chosen per-deployment (vector stores), or the provider is an aggregator. |
| `sdks` | no | string[] | Python import roots, e.g. `["openai"]`. Matched on `import x` / `from x …` and `x.<sub>`. |
| `npm` | no | string[] | JS/TS package names, e.g. `["@anthropic-ai/sdk"]`. Matched on import/require and `pkg/<sub>`. |
| `jvm` | no | string[] | Java/Kotlin import-package prefixes, e.g. `["com.openai"]`. Matched on `import` statements at dot boundaries (`com.openai.client.X`, not `com.openaiutils.X`). |
| `dotnet` | no | string[] | C# namespace prefixes, e.g. `["OpenAI"]`. Matched case-sensitively on `using` directives (plain/`global`/`static`/alias) at dot boundaries (`OpenAI.Chat`, not `OpenAIUtils.X`). |
| `endpoints` | no | string[] | Host substrings that identify the provider in code/config, e.g. `["api.openai.com"]`. |
| `endpoint_jurisdictions` | no | object | Per-host override of `jurisdiction`, e.g. `{"dashscope-intl.aliyuncs.com": "sg"}`. |
| `region_scheme` | no | `"aws"` \| `"azure"` \| `"gcp"` \| `"aliyun"` \| `"huawei"` | The host carries the cloud region; borderlint resolves the region → jurisdiction (e.g. `bedrock-runtime.ap-east-1…` and `asia-east2-aiplatform.googleapis.com` → `hk`, `….cn-hongkong.pai-eas.aliyuncs.com` → `hk`, `api-ap-southeast-1.modelarts-maas.com` → `hk` — Huawei's `ap-southeast-1` is CN-Hong Kong, not Singapore). |

Omit a field rather than setting it empty. At least one of `sdks`, `npm`, `jvm`, `dotnet`, or `endpoints`
should be present, or the entry can never match.

### Jurisdiction tokens

Lowercase **ccTLD / ISO-3166** country codes (`hk`, `cn`, `sg`, `my`, `us`, `gb`, `mo`, …) plus
the special tokens **`CN-GBA`** (nine Mainland GBA cities), **`GBA`** (alias for `hk` + `CN-GBA`),
**`local`** (loopback inference), and **`unknown`** (region set at runtime / undeterminable).
Invalid tokens are rejected at load time.

### Jurisdictions are human-assigned

The weekly drift check (`scripts/kb_drift.py`, `.github/workflows/kb-refresh.yml`) lists upstream
providers borderlint does **not** yet cover — names only, **no jurisdiction**. Mapping a provider
to a jurisdiction is human judgment and is **never auto-merged**: a reviewer assigns it in the PR.
This keeps the KB trustworthy as a residency source. An upstream name that is a route alias of a
covered provider, or not an AI model provider at all, is recorded in
`scripts/kb_drift_aliases.json` (with a reason for ignores) instead of the KB — same PR workflow,
read only by the drift check.

## Custom / private providers (no PR needed)

To add providers for your own org without contributing them upstream, pass a user KB with
`--providers custom.json` — it merges over the bundled KB (your entries win on conflict). It
accepts the same `providers` schema, plus an `endpoints` shorthand for internal hosts:

```json
{ "endpoints": { "llm-cn.acme.internal": "cn", "llm-hk.acme.internal": "hk" } }
```

## Other contributions

Bug fixes, detection improvements, and docs are welcome via PR. Anything that changes tool
behaviour follows the OpenSpec flow in `AGENTS.md`. Keep changes small — one concern per PR.
