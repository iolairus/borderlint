# add-aliyun-coverage — design

## Context

Region schemes live in `kb.py`: per-scheme regex + token→jurisdiction map, dispatched on the
provider's `region_scheme` field (`aws`, `azure`, `gcp` exist; `kb.py:60-72`). The
`alibaba_dashscope` entry already resolves its two hosts via `endpoint_jurisdictions`. Aggregator
and hub modeling precedents: `huggingface` (hub + inference API), `openrouter` (no-SDK note).

## Goals / Non-Goals

**Goals:**
- Aliyun AI egress visible in every scanned language: DashScope Java imports, PAI-EAS endpoint
  literals with region-accurate jurisdictions, ModelScope imports and inference endpoints.
- Only verified, official surfaces — every SDK coordinate and endpoint pattern confirmed against
  Maven/PyPI/Aliyun docs during implementation (real-world validation gate).

**Non-Goals:** management-plane OpenAPI SDKs; PAI training products; generic Alibaba Cloud SDKs.

## Decisions

1. **`jvm: ["com.alibaba.dashscope"]` on the existing `alibaba_dashscope` entry** — the official
   Java SDK (`com.alibaba:dashscope-sdk-java`, Maven Central). No official npm/.NET SDK exists;
   the entry's note records that OpenAI-compatible usage rides the existing hosts (OpenRouter
   precedent), so drift reviews don't re-litigate.
2. **New `aliyun` region scheme, not reuse of `aws`**: Aliyun mainland tokens carry no trailing
   digit (`cn-hangzhou`, `cn-shenzhen`, `cn-hongkong`), which `_AWS_RE`
   (`[a-z]{2}(-gov)?-[a-z]+-\d`) cannot match, and `cn-hongkong` → `hk` must not fall into a
   generic `cn-*` rule. `_ALIYUN_RE` matches both shapes; `_ALIYUN_REGION` maps `cn-hongkong` →
   `hk` and the numbered international tokens (`ap-southeast-1` → `sg`, `ap-southeast-3` → `my`,
   `ap-southeast-5` → `id`, `ap-northeast-1` → `jp`, `ap-northeast-2` → `kr`,
   `us-east-1`/`us-west-1` → `us`, `eu-central-1` → `de`, `eu-west-1` → `gb`, `me-east-1` → `ae`).
   Mainland tokens are mapped as a class: any `cn-*` token not in the explicit map resolves `cn`
   (city enumeration would churn; `cn-hongkong` is the one exception and is checked first).
   Tokens outside both the map and the class rule → None → provider default (`unknown`).
3. **`alibaba_pai` as its own provider** (`endpoints: ["pai-eas.aliyuncs.com"]`,
   `region_scheme: "aliyun"`, `jurisdiction: "unknown"`) rather than folding into
   `alibaba_dashscope` — different product, different hosts, different region mechanics; folding
   would misreport the provider name in findings. Public EAS hosts are
   `<uid>.<region>.pai-eas.aliyuncs.com` with the service name in the URL path
   (`/api/predict/<service>`); the substring match and region parse are label-position-agnostic,
   and task 4.1 verifies the pattern.
4. **`modelscope` modeled like `huggingface`**: `sdks: ["modelscope"]`,
   `endpoints: ["api-inference.modelscope.cn"]`, `jurisdiction: "cn"` — but *not* an aggregator:
   ModelScope inference is Alibaba-hosted, so jurisdiction is determinate (`cn`), unlike the HF
   router. The SDK import surfaces local-pipeline use for review the same way `huggingface_hub`
   does.
5. **Sovereignty**: `alibaba_pai`, `modelscope` → `cn` (Alibaba corporate control; PRC law).
   International PAI regions stay `cn` for sovereignty even when residency resolves elsewhere —
   the compelled-disclosure question follows the operator, mirroring how `aws_bedrock` stays `us`
   outside its ring-fenced China regions.

## Risks / Trade-offs

- [Aliyun international tokens overlap AWS tokens] → several tokens *disagree* between clouds
  (`eu-west-1`: AWS Ireland vs Aliyun London; `ap-southeast-3`: AWS Jakarta vs Aliyun Kuala
  Lumpur; `ap-southeast-5`: AWS Malaysia vs Aliyun Jakarta) — which is exactly why the scheme is
  dispatched per provider; no cross-provider bleed is possible.
- [`pai-eas.aliyuncs.com` substring also matches internal-VPC variants
  (`<uid>.vpc.<region>.pai-eas.aliyuncs.com` — vpc label before the region)] → intended: the
  region token still sits immediately before the `.pai-eas` suffix, so the same resolution
  applies.
- [ModelScope SDK is predominantly local-pipeline usage] → import-level detection is the point
  (surface for review, waivable); the endpoint entry only fires on actual inference-API hosts.
- [Aliyun region list churns] → unmapped tokens degrade to `unknown`, never to a wrong
  jurisdiction; weekly drift owns additions.

## Open Questions

None.
