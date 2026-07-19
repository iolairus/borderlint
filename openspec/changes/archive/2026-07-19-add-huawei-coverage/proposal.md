# add-huawei-coverage

## Why

Huawei Cloud is the second pillar of the China AI stack: ModelArts Studio (MaaS) serves DeepSeek, Qwen, GLM, Kimi, and Huawei's own openPangu family on Ascend infrastructure through an OpenAI-compatible API, and Huawei's official SDK v3 family spans all four languages borderlint scans. None of it is in the KB today — a codebase calling `api.modelarts-maas.com` or importing the Pangu SDK is invisible in every language.

## What Changes

- **New `huawei_modelarts` provider**: ModelArts Studio (MaaS) endpoints — the `modelarts-maas.com` host family covers both the mainland `api.modelarts-maas.com` (no region token → provider default `cn`) and international `api-<region>.modelarts-maas.com` hosts.
- **New `huawei` region scheme**: Huawei reuses AWS-style token *syntax* with different geography — its `ap-southeast-1` is **CN-Hong Kong** (AWS: Singapore), `ap-southeast-3` is Singapore (AWS: Jakarta), `ap-southeast-2` is Bangkok (AWS: Sydney). A dedicated scheme maps Huawei tokens (mainland `cn-*` as a class → `cn`; all 18 international tokens explicitly per design decision 2, verified against Huawei's 33-region table); unmapped tokens degrade to `unknown`, never to the provider default. This is the sharpest demonstration yet of why region schemes dispatch per provider.
- **SDK coverage across all four languages** (curated to the AI services only, verified against registries during implementation): Huawei SDK v3 service packages for Pangu and ModelArts — Python `huaweicloudsdkpangulargemodels`/`huaweicloudsdkmodelarts`, Java `com.huaweicloud.sdk.pangulargemodels`/`com.huaweicloud.sdk.modelarts`, plus the npm (`@huaweicloud/huaweicloud-sdk-*`) and .NET (`HuaweiCloud.SDK.*`) variants if the v3 registries carry them (exact names confirmed by the validation gate).
- **Sovereignty**: `huawei_modelarts` → `cn`.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `jurisdiction-classification`: MODIFIED "Region-specific endpoint resolution" — adds three scenarios: the Huawei/AWS token-homonym trap (`ap-southeast-1` → `hk` on a Huawei host), the mainland default (no-token MaaS host → `cn`), and unmapped-token degradation (`unknown`, never the provider default). The requirement's SHALL text and all existing scenarios (including the Aliyun set) are unchanged.

## Impact

- `borderlint/kb.py`: `_HUAWEI_RE` + `_HUAWEI_REGION` map, one new branch in the region-scheme resolver.
- `borderlint/data/providers.json`: one new provider entry with per-language keys; `borderlint/data/sovereignty.json`: one `cn` entry.
- `tests/test_borderlint.py`: MaaS host resolution (mainland default, `ap-southeast-1` → hk homonym case, unmapped → unknown), SDK imports per language.
- `CONTRIBUTING.md`: `region_scheme` enum gains `"huawei"`. Zero new dependencies. README provider count 99 → 100.

## Non-goals

- No generic Huawei Cloud SDK coverage (`huaweicloudsdkcore`, ECS/OBS/etc.) — only AI egress surfaces qualify.
- No ModelArts management-plane endpoints (`modelarts.<region>.myhuaweicloud.com`) — lifecycle management, not inference egress (Bailian/Fabric precedent).
- No APIG-fronted deployed-service endpoints (`<id>.apig.<region>.huaweicloudapis.com`) — the host is Huawei's generic API gateway serving every cloud service; flagging it would tag non-AI traffic as AI flows. Drift candidate if a path-scoped signal emerges.
- No CodeArts/AgentArts/DataArts coverage — developer tooling and data governance, not model inference from scanned code.
