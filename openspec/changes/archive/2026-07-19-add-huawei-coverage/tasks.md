# add-huawei-coverage — tasks

## 1. Knowledge base

- [x] 1.1 Add `huawei_modelarts` to providers.json: endpoints `["modelarts-maas.com"]`, `region_scheme: "huawei"`, `jurisdiction: "cn"`, Python/Java SDK keys (`huaweicloudsdkpangulargemodels`, `huaweicloudsdkmodelarts` / `com.huaweicloud.sdk.pangulargemodels`, `com.huaweicloud.sdk.modelarts`), note naming MaaS + served model families — design decisions 1-4
- [x] 1.2 Add npm/dotnet keys ONLY for names task 4.1 confirms published (`@huaweicloud/huaweicloud-sdk-*`, `HuaweiCloud.SDK.*`) — design decision 4
- [x] 1.3 sovereignty.json: `huawei_modelarts` → `cn` — design decision 5

## 2. Engine

- [x] 2.1 kb.py: `_HUAWEI_RE` (anchored to `.modelarts-maas.com`, token pattern `api-([a-z]{2}-[a-z]+-\d+)` — three-digit suffix `eu-west-101` and city tokens `my-kualalumpur-1`/`ru-moscow-1` must match) + `_HUAWEI_REGION` (mainland class rule → cn; 18 international tokens per design decision 2) and the `huawei` branch in the region-scheme resolver — a captured-but-unmapped token returns `"unknown"` explicitly; only the token-less host returns None → provider default — spec: all three new scenarios

## 3. Tests

- [x] 3.1 MaaS host resolution: `api.modelarts-maas.com` → cn (no token, provider default); `api-ap-southeast-1.modelarts-maas.com` → hk (homonym trap — same token is sg on an Aliyun host in the same test); `api-me-east-1.modelarts-maas.com` → sa (three-way homonym — ae on Aliyun); unmapped token → unknown (explicit, not the cn provider default) — spec: all three new scenarios
- [x] 3.2 SDK imports: Python `from huaweicloudsdkpangulargemodels...` and Java `import com.huaweicloud.sdk.pangulargemodels...` resolve huawei_modelarts (cn); dot-boundary negative for an unrelated `com.huaweicloud.sdk.ecs` import — design decision 4
- [x] 3.3 Full suite green

## 4. Real-world validation (before merge)

- [x] 4.1 Verify against registries and Huawei docs: Python/Java package names and root imports (PyPI huaweicloudsdkpangulargemodels + Maven com.huaweicloud.sdk:huaweicloud-sdk-pangulargemodels), npm/.NET availability and exact casing, the standalone `modelarts` PyPI question, and both MaaS host shapes — design decisions 2-4. (The region→location table is already verified against the ECS endpoint list, 33 regions; design decision 2's map is final unless Huawei has added regions since.)
- [x] 4.2 Scan at least two real OSS codebases with Huawei AI usage (e.g. huaweicloud-sdk-python-v3 samples, a MaaS/Pangu consumer); fix what real code exposes before merge

## 5. Docs

- [x] 5.1 CONTRIBUTING.md: `region_scheme` enum gains `"huawei"`; README provider count 99 → 100 — proposal Impact
