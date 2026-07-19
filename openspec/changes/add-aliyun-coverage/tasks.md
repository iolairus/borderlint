# add-aliyun-coverage — tasks

## 1. Knowledge base

- [x] 1.1 alibaba_dashscope: add `jvm: ["com.alibaba.dashscope"]` and the no-official-npm/.NET note — design decision 1
- [x] 1.2 Add `alibaba_pai` (endpoints `pai-eas.aliyuncs.com`, `region_scheme: "aliyun"`, jurisdiction unknown) and `modelscope` (sdks `modelscope`, endpoint `api-inference.modelscope.cn`, jurisdiction cn) to providers.json — design decisions 3-4
- [x] 1.3 sovereignty.json: `alibaba_pai` and `modelscope` → `cn` — design decision 5

## 2. Engine

- [x] 2.1 kb.py: `_ALIYUN_RE` + `_ALIYUN_REGION` (mainland cities → cn, cn-hongkong → hk, numbered international tokens per design) and the `aliyun` branch in the region-scheme resolver — spec: Region-specific endpoint resolution (both new scenarios)

## 3. Tests

- [x] 3.1 PAI-EAS host resolution: `svc.cn-hangzhou.pai-eas.aliyuncs.com` → cn, `svc.cn-hongkong.…` → hk, `svc.ap-southeast-1.…` → sg, unmapped token → unknown — spec: all three Aliyun scenarios
- [x] 3.2 DashScope Java import (`import com.alibaba.dashscope.aigc.generation.Generation;`) resolves alibaba_dashscope; ModelScope Python import + inference endpoint resolve cn — design decisions 1, 4
- [x] 3.3 Full suite green

## 4. Real-world validation (before merge)

- [x] 4.1 Verify `com.alibaba:dashscope-sdk-java` root package, the `modelscope` PyPI import name, and the PAI-EAS host pattern (incl. VPC variant) against Maven Central / PyPI / Aliyun docs
- [x] 4.2 Scan at least two real OSS codebases with Aliyun AI usage (e.g. a dashscope-sdk-java consumer, a ModelScope example repo); fix what real code exposes before merge

## 5. Docs

- [x] 5.1 CONTRIBUTING.md: extend the `region_scheme` enum (`"aws" | "azure" | "gcp"`, line ~35) with `"aliyun"`; README/CAPABILITIES only if a claim becomes stale (provider count line stays 90+) — proposal Impact
