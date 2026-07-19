# add-aliyun-coverage

## Why

Alibaba Cloud is the largest China cloud and its AI stack (Model Studio/Bailian via DashScope, PAI-EAS inference, Qwen, ModelScope) is exactly the east side of the east-west boundary borderlint exists to map — yet the KB covers only the DashScope Python SDK and two DashScope hosts. The official DashScope Java SDK, PAI-EAS online-inference endpoints, and ModelScope are all invisible today, in every language borderlint scans.

## What Changes

- **DashScope JVM coverage**: `alibaba_dashscope` gains `jvm: ["com.alibaba.dashscope"]` — the official Java SDK (Maven `com.alibaba:dashscope-sdk-java`). No official npm or .NET SDK exists; Model Studio's documented path for those languages is the OpenAI SDK against the compatible-mode endpoint, which the existing `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` hosts already catch — noted on the entry (OpenRouter precedent).
- **PAI-EAS endpoints**: new `alibaba_pai` provider for PAI-EAS online inference (`<uid>.<region>.pai-eas.aliyuncs.com`, service name in the URL path), with the region resolved from the host.
- **New `aliyun` region scheme**: Aliyun mainland tokens carry no trailing digit (`cn-hangzhou`, `cn-shenzhen`, `cn-hongkong`), so the existing aws scheme regex cannot resolve them. New scheme maps mainland cities → `cn`, `cn-hongkong` → `hk`, and the numbered international tokens (including `ap-southeast-1` → `sg`, `ap-northeast-1` → `jp`, `eu-central-1` → `de`, `us-east-1`/`us-west-1` → `us`, `me-east-1` → `ae`; full map in design decision 2). Unmapped tokens degrade to `unknown`, never a guess.
- **ModelScope**: new `modelscope` provider — the CN model hub and its HF-style inference API (`api-inference.modelscope.cn`, Python SDK `modelscope`), jurisdiction `cn`. The east-side analogue of the `huggingface` entry.
- **Sovereignty**: `alibaba_pai` and `modelscope` → `cn`.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `jurisdiction-classification`: MODIFIED "Region-specific endpoint resolution" — adds three scenarios for Aliyun regional hosts (PAI-EAS): mainland/Hong Kong, international, and unmapped-token degradation to `unknown`. The requirement's SHALL text is unchanged; the scheme is a new instance of the existing mechanism.

## Impact

- `borderlint/kb.py`: `_ALIYUN_RE` + `_ALIYUN_REGION` map, one new branch in the region-scheme resolver.
- `borderlint/data/providers.json`: `jvm` key + note on `alibaba_dashscope`; new `alibaba_pai` and `modelscope` entries.
- `borderlint/data/sovereignty.json`: two new `cn` entries.
- `tests/test_borderlint.py`: DashScope Java import, PAI-EAS regional host resolution (mainland, HK, international), ModelScope import + endpoint.
- Zero new dependencies. README provider count (90+) still accurate.

## Non-goals

- No Bailian OpenAPI management-plane SDKs (`alibabacloud_bailian*`) — lifecycle management, not inference egress.
- No generic `alibabacloud`/`aliyun-*` OpenAPI SDK coverage — far too broad; only AI egress surfaces qualify.
- No PAI-DSW/DLC/training coverage — training infrastructure, not data egress from scanned code.
- No ModelScope local-pipeline modeling beyond the import signal — local inference stays unflagged by the endpoint side; the SDK import still surfaces for review, matching `huggingface_hub` handling.
