# Contributing to borderlint

The most valuable contribution is **the knowledge base** — the mapping from AI providers and
endpoints to jurisdictions in `borderlint/data/providers.json`. borderlint is vendor-neutral:
Western and Chinese providers are treated identically, and every entry is reviewed by a human.

borderlint is built **spec-first** with [OpenSpec](https://github.com/Fission-AI/OpenSpec) (see
`AGENTS.md`). Code changes go through propose → review → apply. KB and doc contributions are
lighter, but still follow the required OpenSpec proposal/review and branch workflow in `AGENTS.md`;
a pull request alone is not enough.

## Add or correct a provider

1. Edit `borderlint/data/providers.json` (add an entry, or fix an existing one).
2. Add the provider-id → sovereignty-bloc mapping in `borderlint/data/sovereignty.json`. If the
   provider serves only its own models, add its first-party default under `provider_defaults` in
   `borderlint/data/provenance.json`; multi-model hosts and aggregators deliberately omit it.
3. Curate the provider's entry in `borderlint/data/data_practices.json` using the rules below, or
   add a reasoned exemption under `data_practices_exempt` in `scripts/kb_drift_aliases.json`.
4. Run the suite: `pip install -e ".[dev]" && pytest`.
5. Open a PR. State your **sources** for the jurisdiction and any sovereignty/provenance
   assignments (provider docs, data-residency page, region list). A maintainer assigns/confirms
   the jurisdiction — see *Jurisdictions are human-assigned* below.

### Provider entry schema

Each object in the `providers` array:

| Field | Required | Type | Meaning |
|---|---|---|---|
| `id` | yes | string | Stable internal id (snake_case), e.g. `alibaba_dashscope`. |
| `name` | yes | string | Human-readable name shown in reports. |
| `category` | no | `inference` \| `vector_store` \| `aggregator` \| `speech` \| `observability` \| `service` | Provider type; defaults to `inference`. Use `vector_store` for a managed vector DBaaS (data-at-rest sink), `aggregator` for a multi-provider router, `speech` for a speech-to-text / text-to-speech API, `observability` for an AI tracing/telemetry provider such as Langfuse or LangSmith, and `service` for another operated service target such as an MCP integration or web-data API. JSON, SBOM, and evidence output include the category; text output adds labels only for vector stores and observability providers. |
| `jurisdiction` | yes | string | Default jurisdiction token for the provider (see tokens below). Use `unknown` when the host carries the region (Azure/Bedrock), the cluster region is chosen per-deployment (vector stores), or the provider is an aggregator. |
| `sdks` | no | string[] | Python import roots, e.g. `["openai"]`. Matched on `import x` / `from x …` and `x.<sub>`. |
| `npm` | no | string[] | JS/TS package names, e.g. `["@anthropic-ai/sdk"]`. Matched on import/require and `pkg/<sub>`. |
| `jvm` | no | string[] | Java/Kotlin import-package prefixes, e.g. `["com.openai"]`. Matched on `import` statements at dot boundaries (`com.openai.client.X`, not `com.openaiutils.X`). |
| `dotnet` | no | string[] | C# namespace prefixes, e.g. `["OpenAI"]`. Matched case-sensitively on `using` directives (plain/`global`/`static`/alias) at dot boundaries (`OpenAI.Chat`, not `OpenAIUtils.X`). |
| `endpoints` | no | string[] | Host substrings that identify the provider in code/config, e.g. `["api.openai.com"]`. |
| `endpoint_jurisdictions` | no | object | Per-host override of `jurisdiction`, e.g. `{"dashscope-intl.aliyuncs.com": "sg"}`. |
| `sovereignty_overrides` | no | object | Optional resolved-jurisdiction → sovereignty-bloc overrides for ring-fenced operations, e.g. `{"cn": "cn"}`; takes precedence over the provider-level sovereignty map. |
| `region_scheme` | no | `"aws"` \| `"azure"` \| `"gcp"` \| `"aliyun"` \| `"huawei"` | The host carries the cloud region; borderlint resolves the region → jurisdiction (e.g. `bedrock-runtime.ap-east-1…` and `asia-east2-aiplatform.googleapis.com` → `hk`, `….cn-hongkong.pai-eas.aliyuncs.com` → `hk`, `api-ap-southeast-1.modelarts-maas.com` → `hk` — Huawei's `ap-southeast-1` is CN-Hong Kong, not Singapore). |

Omit a field rather than setting it empty. At least one of `sdks`, `npm`, `jvm`, `dotnet`, or `endpoints`
should be present, or the entry can never match. The exception is an MCP-only `service` entry with
no direct SDK/endpoint keys: map each server package, binary, or container-image identifier to its
provider id in the `servers` map in `borderlint/data/mcp_servers.json`, so stdio MCP configurations
resolve to the operated service. Remote MCP URLs still resolve through `endpoints`.

### Jurisdiction tokens

Lowercase **ccTLD / ISO-3166** country codes (`hk`, `cn`, `sg`, `my`, `us`, `gb`, `mo`, …) plus
the special tokens **`CN-GBA`** (nine Mainland GBA cities), **`GBA`** (alias for `hk` + `CN-GBA`),
**`local`** (loopback inference), and **`unknown`** (region set at runtime / undeterminable).
Invalid tokens are rejected at load time in custom top-level `endpoints` maps and regulator-profile
`defaults`; provider-entry `jurisdiction` and `endpoint_jurisdictions` values are not validated on
that path.

### Jurisdictions are human-assigned

The weekly drift check (`scripts/kb_drift.py`, `.github/workflows/kb-refresh.yml`) reports uncovered
upstream providers and model families, missing/invalid sovereignty mappings, stale bundled KBs and
data-practice entries, providers with Python/npm keys but missing JVM/.NET keys, and providers
without data-practice curation. It reports existing ids and gaps, including an invalid configured
bloc, but proposes **no jurisdiction or bloc assignments**. Mapping a
provider to a jurisdiction, sovereignty, or provenance is human judgment and is **never
auto-merged**: a reviewer assigns it in the PR. This keeps the KB trustworthy as a residency source.
An upstream name that is a route alias of a covered provider, or not an AI model provider at all, is
recorded in `scripts/kb_drift_aliases.json` (with a reason for ignores) instead of the KB. Reasoned
`residue` entries acknowledge unactionable uncovered model ids, and `sdk_exempt` entries suppress
known JVM/.NET gaps. These suppression lists are read only by the drift check. After editing any
bundled KB, review it and advance its top-level `updated` date; update a data-practice entry's
`reviewed` date after re-verifying its facts.

## Data-practice facts (`data_practices.json`)

A separate, hand-curated KB answering the four questions privacy reviewers ask first:
does the provider train on customer API data by default, what is the retention window for
API inputs/outputs, where is the subprocessor list, and does an enterprise tier change the
answers. Strictly advisory — it never influences verdicts or exit codes.

Entry schema (one entry per provider id in `providers.json`):

| Field | Required | Meaning |
|---|---|---|
| `training_default` | no | `"yes"` \| `"no"` \| `"opt-out"`; omit (JSON `null`) when undocumented |
| `retention` | no | Free-text retention window for API inputs/outputs; conditions belong in the text |
| `subprocessors` | no | `{url, locator, retrieved}` link to the provider's subprocessor list |
| `enterprise_tier` | no | Free-text note on whether an enterprise/commercial tier changes the answers |
| `reviewed` | yes | ISO-8601 date you last verified every fact in the entry |
| `citations` | per fact | `{url, locator, retrieved}` for each non-null fact |

Curation rules:

- **Every fact needs a citation**: the source URL, a locator note naming where in the source
  the statement is made, and the date you retrieved it. Read the primary documentation — never
  copy from third-party summaries.
- **Unknown means null.** If a fact isn't publicly documented, leave it `null`; the renderers
  state "not curated" rather than guessing.
- **Human curation only.** The drift check reports providers without entries and entries whose
  `reviewed` date exceeds the 90-day interval — ids only, never proposed values. Facts are
  never auto-filled from upstream feeds. A provider deliberately left uncurated gets a reasoned
  entry under `data_practices_exempt` in `scripts/kb_drift_aliases.json`.
- Facts are statements about documented practices as of their retrieval dates — not legal advice.

## Regulator profiles (`regulator_profiles.json`)

Hand-curated profiles that pre-seed the `init` wizard's allow-list walk from a regulator's
published AI guidance (`borderlint init --profile <id>`). Strictly advisory: every seeded
jurisdiction stays operator-editable, and the wizard prints the profile's citation and an
explicit not-legal-advice disclaimer whenever one is active.

Profile schema (one entry per profile id):

| Field | Required | Meaning |
|---|---|---|
| `seats` | yes | Supported seat(s) the profile targets (e.g. `["hk"]`); mismatch with `--home` warns but proceeds |
| `regulator` | yes | Display name of the issuing regulator |
| `citation` | yes | `{url, retrieved}` link to the guidance the defaults derive from |
| `defaults` | yes | Per-classification allow-list of jurisdiction tokens (recognised vocabulary only) |
| `notes` | no | Free-text explaining the conservative choices |
| `reviewed` | yes | ISO-8601 date you last verified the profile against the guidance |

Curation rules:

- **Defaults must cite the guidance.** Record the source URL and retrieval date; read the
  primary document, never third-party summaries.
- **Conservative by default.** Seed onshore only unless the guidance itself endorses a
  cross-border arrangement (e.g. CN-GBA under the GBA Standard Contract for non-pii);
  explain deviations in `notes`.
- **Human curation only.** The file carries a top-level `updated` date and joins the weekly
  staleness check; nothing is fetched or updated at runtime.
- Profiles are starting points derived from cited guidance as of its retrieval date — never
  legal advice and never a determination of filing sufficiency.

## Custom / private providers (no PR needed)

To add providers for your own org without contributing them upstream, pass a user KB with
`--providers custom.json` — it merges over the bundled KB (your entries win on conflict). It
accepts the same `providers` schema, plus an `endpoints` shorthand for internal hosts:

```json
{ "endpoints": { "llm-cn.acme.internal": "cn", "llm-hk.acme.internal": "hk" } }
```

Custom KBs may also include optional top-level `sovereignty` and `provenance` objects. The first
maps provider ids to sovereignty blocs; the second maps model-ID prefixes to provenance blocs.
Both override bundled entries, and user provenance prefixes take precedence even over longer
bundled prefixes.

## Other contributions

Bug fixes, detection improvements, and docs are welcome via PR. Anything that changes tool
behaviour follows the OpenSpec flow in `AGENTS.md`. Keep changes small — one concern per PR.
