# Proposal: cn-data-practices-curation

## Why

Three of the top-10 token-volume providers — DeepSeek (#1/#5/#9), Tencent Hunyuan (#2) and
Zhipu GLM (#6) — have data-practices entries whose every fact is `null` because primary sources
could not be reached during the earlier curation pass. Fresh research has now located and
verified their governing documents: DeepSeek's policies on its CDN, Tencent's TokenHub
Privacy Policy Module (the successor to the dead Hunyuan doc IDs), and Zhipu's full terms/privacy
set on docs.bigmodel.cn. Reviewers currently see "not curated" for the three highest-traffic
Chinese providers; the facts are now available to curate.

## What Changes

- Fill the `deepseek` entry: training default `opt-out` (policy-level opt-out described;
  no API carve-out), CN residency, purpose-bound retention with no fixed window, no
  documented zero-retention tier; citations to cdn.deepseek.com policy URLs.
- Fill the `tencent_hunyuan` entry: 30-day diagnostic/usage retention (explicitly including
  output information, longer for billing) citing the TokenHub Privacy Policy Module; training
  default remains null (no explicit statement found); subprocessors remain null.
- Fill the `zhipu` entry: training default `no` for identifiable content with the anonymisation
  training carve-out quoted verbatim in the locator; China-only storage; minimum-necessary
  retention with buffer-period deletion; named subprocessor list (Alipay, WeChat Pay, Sensors
  Analytics, NetEase Qiyu, Aliyun/Baidu SMS).
- Replace each entry's explanatory "sources unreachable" note with the new citations.

## Capabilities

### New Capabilities
- (none)

### Modified Capabilities
- `provider-data-practices`: the existing bundled-curated-facts requirement is exercised for
  three previously-null providers; no requirement text changes — this change fills entries
  under the already-shipped schema.

## Impact

- `borderlint/data/data_practices.json`: three entries updated; KB website provider pages and
  evidence-pack register render the new facts automatically.
- No loader, renderer, CLI, or detection changes. Advisory only; verdicts unaffected.

## Non-goals

- No re-curation of entries that are already complete (openai, anthropic, google_gemini,
  azure_openai, aws_bedrock, xiaomi_mimo, nvidia_nim, alibaba_dashscope, moonshot).
- No claim about in-PRC consumer-app variants beyond what the cited documents state.
- No changes to drift behaviour; staleness coverage applies automatically via per-entry dates.
