# Contributing to borderlint

The most valuable contribution is the provider knowledge base in `borderlint/data/providers.json`.
It maps AI providers and endpoints to residency (where data goes), sovereignty (which government
may compel disclosure), and provenance (who developed model weights). borderlint is vendor-neutral:
Western and Chinese providers receive the same review, and a person reviews every entry.

## Follow the development workflow

borderlint uses spec-first development with [OpenSpec](https://github.com/Fission-AI/OpenSpec).
Read `AGENTS.md` before changing code, knowledge bases, or documentation.

1. Create and review an OpenSpec proposal.
2. Create a feature branch.
3. Implement the approved tasks.
4. Run the tests and strict OpenSpec validation.
5. Open a pull request. Keep each pull request to one concern.

A pull request alone is not enough. Knowledge-base and documentation contributions follow the same
proposal, review, and branch workflow.

## Add or correct a provider

1. Add or edit the provider in `borderlint/data/providers.json`.
2. Add its provider-ID → sovereignty-bloc mapping in `borderlint/data/sovereignty.json`.
3. Add a first-party default under `provider_defaults` in `borderlint/data/provenance.json` only
   when the provider serves exclusively its own models. Omit this default for multi-model hosts
   and aggregators.
4. Add the provider's entry in `borderlint/data/data_practices.json` using the rules below. If you
   deliberately leave it uncurated, add a reason under `data_practices_exempt` in
   `scripts/kb_drift_aliases.json`.
5. Run `pip install -e ".[dev]" && pytest`.
6. Open a pull request with primary sources for the jurisdiction and any sovereignty or provenance
   assignments. Use provider documentation, data-residency pages, and region lists. A maintainer
   must assign or confirm these values.

### Provider entry schema

Each object in the `providers` array uses these fields:

| Field | Required | Type | Meaning |
|---|---|---|---|
| `id` | yes | string | Stable internal ID in snake_case, such as `alibaba_dashscope`. |
| `name` | yes | string | Human-readable name shown in reports. |
| `category` | no | `inference` \| `vector_store` \| `aggregator` \| `speech` \| `observability` \| `service` | Provider type; defaults to `inference`. Use `vector_store` for a managed vector database, `aggregator` for a multi-provider router, `speech` for a speech-to-text or text-to-speech API, `observability` for an AI tracing provider, and `service` for another operated service such as a Model Context Protocol (MCP) integration or web-data API. JSON, software bill of materials (SBOM), and evidence output include the category. Text output adds labels only for vector stores and observability providers. |
| `jurisdiction` | yes | string | Default jurisdiction token. Use `unknown` when the host carries the region, a vector-store cluster region is chosen per deployment, or the provider is an aggregator. |
| `sdks` | no | string[] | Python import roots, such as `["openai"]`. Matches `import x`, `from x …`, and `x.<sub>`. |
| `npm` | no | string[] | JavaScript/TypeScript package names, such as `["@anthropic-ai/sdk"]`. Matches import, require, and `pkg/<sub>`. |
| `jvm` | no | string[] | Java/Kotlin package prefixes, such as `["com.openai"]`. Matches imports at dot boundaries: `com.openai.client.X` matches, but `com.openaiutils.X` does not. |
| `dotnet` | no | string[] | C# namespace prefixes, such as `["OpenAI"]`. Matches plain, `global`, `static`, and alias `using` directives case-sensitively at dot boundaries. |
| `endpoints` | no | string[] | Host substrings that identify the provider, such as `["api.openai.com"]`. |
| `endpoint_jurisdictions` | no | object | Per-host jurisdiction overrides, such as `{"dashscope-intl.aliyuncs.com": "sg"}`. |
| `sovereignty_overrides` | no | object | Optional resolved-jurisdiction → sovereignty-bloc overrides for legally separated operations, such as `{"cn": "cn"}`. Takes precedence over the provider-level sovereignty map. |
| `region_scheme` | no | `"aws"` \| `"azure"` \| `"gcp"` \| `"aliyun"` \| `"huawei"` | The host carries a cloud region. borderlint maps it to a jurisdiction. For example, `bedrock-runtime.ap-east-1…` and `asia-east2-aiplatform.googleapis.com` resolve to `hk`. Huawei's `ap-southeast-1` means CN-Hong Kong, not Singapore. |

Omit optional fields instead of leaving them empty. Include at least one of `sdks`, `npm`, `jvm`,
`dotnet`, or `endpoints`; otherwise the entry cannot match.

The exception is a Model Context Protocol (MCP)-only `service` entry with no direct SDK or endpoint
keys. Map each server package, binary, or container image to the provider ID in the `servers` map in
`borderlint/data/mcp_servers.json`. Remote MCP URLs still resolve through `endpoints`.

### Jurisdiction tokens

Use lowercase ccTLD/ISO-3166 country codes such as `hk`, `cn`, `sg`, `my`, `us`, `gb`, and `mo`.
Also supported:

- `CN-GBA`: the nine Mainland GBA cities.
- `GBA`: an alias for `hk` plus `CN-GBA`.
- `local`: loopback inference.
- `unknown`: a region chosen at runtime or one that cannot be determined.

Custom top-level `endpoints` maps and regulator-profile `defaults` reject invalid tokens when they
load. That loading path does not validate provider-entry `jurisdiction` and
`endpoint_jurisdictions` values.

### Assign jurisdictions and blocs by hand

The weekly coverage check runs `scripts/kb_drift.py` through `.github/workflows/kb-refresh.yml`.
It reports:

- Upstream providers and model families that the bundled knowledge bases do not cover.
- Missing or invalid sovereignty mappings.
- Knowledge bases and data-practice entries that need a fresh review.
- Providers with Python or npm keys but missing JVM or .NET keys.
- Providers without curated data practices.

The check reports IDs and gaps. It never proposes or merges jurisdiction, sovereignty, or
provenance assignments. A reviewer must make those judgments in the pull request.

Record upstream route aliases and out-of-scope names in `scripts/kb_drift_aliases.json`, with a
reason for each ignored name. Use `residue` entries for acknowledged model IDs that need no action
and `sdk_exempt` entries for accepted JVM/.NET gaps. Only the coverage check reads these
suppression lists; the scanner does not.

After editing a bundled knowledge base, review it and advance its top-level `updated` date. After
re-verifying a data-practice entry's facts, advance its `reviewed` date.

## Curate data practices

`borderlint/data/data_practices.json` answers four questions for each provider:

1. Does the provider train on customer API data by default?
2. How long does it retain API inputs and outputs?
3. Where does it publish its subprocessor list?
4. Does an enterprise tier change these answers?

These facts are advisory. They never change verdicts or exit codes.

### Data-practice schema

| Field | Required | Meaning |
|---|---|---|
| `training_default` | no | `"yes"` \| `"no"` \| `"opt-out"`; use JSON `null` when undocumented |
| `retention` | no | Retention window for API inputs and outputs; include conditions in the text |
| `subprocessors` | no | `{url, locator, retrieved}` link to the provider's subprocessor list |
| `enterprise_tier` | no | Note explaining whether an enterprise or commercial tier changes the answers |
| `reviewed` | yes | ISO-8601 date when you last verified every fact |
| `citations` | per fact | `{url, locator, retrieved}` for each non-null fact |

Follow these rules:

- **Cite every fact.** Record the source URL, a locator naming where the statement appears, and
  the retrieval date. Read the provider's primary documentation, not third-party summaries.
- **Use null for unknown facts.** If public documentation does not answer a question, leave it
  `null`. Reports say “not curated” instead of guessing.
- **Curate by hand.** The weekly check reports missing entries and entries whose `reviewed` date is
  more than 90 days old. It never fills in facts. Record deliberate exemptions under
  `data_practices_exempt` in `scripts/kb_drift_aliases.json`.
- **Date every statement.** Facts describe documented practices as of their retrieval dates. They
  are not legal advice.

## Curate regulator profiles

`borderlint/data/regulator_profiles.json` supplies starting choices for `borderlint init --profile
<id>` from published regulator guidance. The profiles are advisory. You can change every suggested
jurisdiction, and `init` always prints the citation and a not-legal-advice disclaimer.

### Regulator-profile schema

| Field | Required | Meaning |
|---|---|---|
| `seats` | yes | Home locations the profile targets, such as `["hk"]`; a mismatch with `--home` warns but continues |
| `regulator` | yes | Display name of the issuing regulator |
| `citation` | yes | `{url, retrieved}` link to the guidance behind the defaults |
| `defaults` | yes | Per-classification allow-lists using recognised jurisdiction tokens |
| `notes` | no | Explanation of the conservative choices |
| `reviewed` | yes | ISO-8601 date when you last verified the profile against the guidance |

Follow these rules:

- **Cite the guidance.** Record the primary source URL and retrieval date. Do not use third-party
  summaries.
- **Start conservatively.** Suggest onshore locations only unless the guidance itself supports a
  cross-border arrangement. For example, CN-GBA may suit non-PII under the GBA Standard Contract.
  Explain any deviation in `notes`.
- **Curate by hand.** Advance the file's top-level `updated` date after review. The weekly check
  includes this date. borderlint never fetches or updates profiles at runtime.
- **Present profiles as starting points.** They reflect cited guidance as of its retrieval date.
  They are not legal advice and do not determine whether a filing is sufficient.

## Add custom or private providers

You can add your organisation's providers without contributing them upstream. Pass a custom
knowledge base with `--providers custom.json`. borderlint adds it to the bundled knowledge base,
and your entries win on conflict.

The file accepts the same `providers` schema plus an `endpoints` shorthand:

```json
{ "endpoints": { "llm-cn.acme.internal": "cn", "llm-hk.acme.internal": "hk" } }
```

You can also include top-level `sovereignty` and `provenance` objects. The first maps provider IDs
to sovereignty blocs. The second maps model-ID prefixes to provenance blocs. Both override bundled
entries. Your provenance prefixes take precedence even over longer bundled prefixes.

## Other contributions

Bug fixes, detection improvements, and documentation changes are welcome. Follow the OpenSpec
workflow in `AGENTS.md` for every behaviour change, and keep each pull request to one concern.
