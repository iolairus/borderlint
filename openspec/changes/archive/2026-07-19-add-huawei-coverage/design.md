# add-huawei-coverage — design

## Context

Region schemes (`aws`, `azure`, `gcp`, `aliyun`) live in `kb.py` as per-scheme regex + token map,
dispatched on the provider's `region_scheme` field. The `alibaba_dashscope`/`tencent_tokenhub`
entries set the pattern for cn-default providers with international variants; `add-aliyun-coverage`
(just archived) set the pattern for a China-cloud regional scheme with class rules and
unknown-degradation.

## Goals / Non-Goals

**Goals:**
- Huawei ModelArts Studio (MaaS) egress visible in every scanned language, with the region trap
  (`ap-southeast-1` = CN-Hong Kong on Huawei) resolved correctly.
- Only verified surfaces: every SDK coordinate and endpoint confirmed against
  PyPI/Maven/npm/NuGet and Huawei docs during implementation.

**Non-Goals:** generic Huawei SDKs; ModelArts management plane; APIG deployed-service hosts;
CodeArts/AgentArts/DataArts.

## Decisions

1. **One provider id `huawei_modelarts`** (name "Huawei ModelArts (MaaS)") covering the MaaS
   serving platform and the Pangu/ModelArts SDK families — MaaS is the serving surface for both
   third-party models (DeepSeek, Qwen, GLM, Kimi) and openPangu, so one id reports the operator
   honestly; provenance comes from model references, as with Bedrock/Foundry/TokenHub.
2. **New `huawei` region scheme.** `_HUAWEI_RE` anchors to `.modelarts-maas.com` (GCP/Aliyun
   anchoring precedent) and captures the token from `api-<token>.` prefixes with
   `api-([a-z]{2}-[a-z]+-\d+)` — the `\d+` and multi-letter city shape matter: `eu-west-101`
   (Dublin) has a three-digit suffix and `my-kualalumpur-1` / `na-mexico-1` / `ru-moscow-1`
   carry full city names, so an Aliyun-style single-digit pattern would silently miss them.
   `_HUAWEI_REGION` (verified against Huawei's ECS region/endpoint table, 33 regions): mainland
   tokens as a class (`cn-*` → `cn`; all 15 current tokens fit — cn-east-2/3/4/5,
   cn-north-1/2/4/9/11/12, cn-south-1/2/4, cn-southwest-2/3); international tokens mapped
   explicitly — `ap-southeast-1` → `hk` (CN-Hong Kong), `ap-southeast-2` → `th` (Bangkok),
   `ap-southeast-3` → `sg` (Singapore), `ap-southeast-4` → `id` (Jakarta),
   `ap-southeast-5` → `ph` (Manila), `me-east-1` → `sa` (Riyadh), `ae-ad-1` → `ae` (Abu
   Dhabi), `af-north-1` → `eg` (Cairo), `af-south-1` → `za` (Johannesburg),
   `tr-west-1` → `tr` (Istanbul), `eu-west-0` → `fr` (Paris), `eu-west-101` → `ie` (Dublin),
   `la-north-2` → `mx` (Mexico City2), `na-mexico-1` → `mx` (Mexico City1),
   `sa-brazil-1` → `br` (São Paulo), `la-south-2` → `cl` (Santiago),
   `my-kualalumpur-1` → `my` (Kuala Lumpur), `ru-moscow-1` → `ru` (Moscow). A captured token
   outside map and class rule returns `"unknown"` explicitly — never `None`, which would fall
   through to the provider default `cn` (the resolver is `scheme_result or provider_default`)
   and misreport an unknown region as mainland. Only the token-less host returns `None`. The
   AWS/Aliyun-homonym disagreement (`ap-southeast-1`: hk here, sg there; `me-east-1`: sa here,
   ae on Aliyun) is contained by per-provider dispatch — the scheme is only consulted for
   `huawei_modelarts` hosts.
3. **Default jurisdiction `cn`**: the token-less `api.modelarts-maas.com` is the mainland
   platform (Chinese-site docs; served on Ascend infrastructure in mainland regions). The
   region scheme returning None falls through to this default — same mechanics as
   `alibaba_dashscope`.
4. **SDK curation (v1), AI services only**: Huawei's SDK v3 family is generated per service in
   all four languages. Curate the two AI-egress services — PanguLargeModels and ModelArts:
   Python `huaweicloudsdkpangulargemodels`, `huaweicloudsdkmodelarts`; Java
   `com.huaweicloud.sdk.pangulargemodels`, `com.huaweicloud.sdk.modelarts`; npm and .NET
   variants (`@huaweicloud/huaweicloud-sdk-*` scoped packages, `HuaweiCloud.SDK.*` namespaces)
   are added only after task 4.1 confirms the exact published names and casing — Huawei's v3
   registries do not uniformly cover every service in every language, and a guessed prefix is
   worse than a missing one. `huaweicloudsdkcore` is deliberately excluded (generic, non-AI).
   The standalone `modelarts` Python SDK (Huawei-mirror-distributed) is assessed in 4.1: include
   only if it is PyPI-published under an unambiguous import name.
5. **Sovereignty `cn`** for all regions including Hong Kong and international — Huawei corporate
   control under PRC law; the compelled-disclosure question follows the operator (TokenHub/PAI
   precedent).

## Risks / Trade-offs

- [Huawei international regions run by local partners could complicate the sovereignty story —
  concrete cases exist: `ae-ad-1` is OP5 and `my-kualalumpur-1` is OP6, Huawei's partner-operated
  regions] → out of scope for v1; provider-level `cn` is the conservative reading, and per-region
  `sovereignty_overrides` exist (Bedrock China precedent) if evidence for a ring-fence appears.
- [`modelarts-maas.com` may grow host variants (console, docs)] → the substring only fires on
  hosts containing the domain; non-API subdomains still name the same platform and jurisdiction
  facts, so a match is informative, not wrong.
- [SDK v3 casing/coverage per language is inconsistent] → contained by decision 4's
  verify-before-add rule; the endpoint entry alone already catches the dominant OpenAI-SDK
  compatible-mode usage in every language.
- [Huawei region list churns] → class rule for mainland; unmapped tokens degrade to `unknown`,
  never a guess; weekly drift owns additions.

## Open Questions

None.
