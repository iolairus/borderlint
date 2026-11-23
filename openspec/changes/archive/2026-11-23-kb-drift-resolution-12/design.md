# Design: kb-drift-resolution-12

## Research basis

Primary sources were reviewed on 2026-11-23 against the live LiteLLM catalog and issue #39. The
wave contains four providers, 42 model ids in 22 families, 16 stale data-practice entries, and two
regulator profiles. Forty-one model ids have defensible direct or inherited provenance; one has
undisclosed lineage. Dates below describe this research and are advanced to the actual implementation
review date if implementation occurs later.

## D1 — Provider classification and adjacent endpoint facts

- **Gnani / Vachana Speech APIs:** `speech`; endpoint `api.vachana.ai`; SDK imports `gnani`,
  `livekit.plugins.gnani`, `pipecat_gnani`; residency `unknown`; sovereignty `in`; no provenance
  default. Public shared-API hosting is not located by the Indian EULA or by private/on-prem
  deployment options. Exclude separate Agent Builder host `api.inya.ai`. Add a reasoned SDK
  exemption for undocumented JVM/.NET packages. Sources: https://docs.gnani.ai/api/introduction/introduction,
  https://docs.gnani.ai/python-sdk/introduction, https://docs.gnani.ai/livekit/introduction,
  https://docs.gnani.ai/pipecat/introduction, https://www.gnani.ai/legal/eula.
- **Gradium:** `speech`; SDK `gradium`; hosts `api.gradium.ai`, `eu.api.gradium.ai`,
  `us.api.gradium.ai`; default `unknown`, regional overrides `eu`/`us`; sovereignty `eu`; no
  provenance default. The global host selects a nearby EU/US cluster without a residency promise.
  Regional guarantees require paid enrollment; control-plane/account data remains EU. Do not map
  on-device Phonon `ptts`/`phonon-tts`; exempt undocumented JVM/.NET SDKs. Sources:
  https://docs.gradium.ai/guides/data-residency.md, https://gradium.ai/terms-of-service,
  https://docs.gradium.ai/guides/installation.md.
- **ResetData AI Platform:** `inference`; `api.resetdata.ai`; no dedicated SDK keys; residency and
  sovereignty `au`; no provenance default. Notes distinguish Australian inference hosting from
  possible overseas handling of account/support data and workload-specific contractual review.
  Existing suffix patterns already resolve all six current hosted models, so no ResetData
  passthrough or patterns are needed. Sources: https://docs.resetdata.ai/security/data-handling/,
  https://docs.resetdata.ai/get-started/quickstart/, https://resetdata.com.au/terms,
  https://resetdata.com.au/privacy-policy.
- **Vispark Lab:** `inference`; `api.lab.vispark.in` and `api.vispark.in`; no dedicated SDK keys;
  residency and sovereignty `in`; add provider default `vispark: in` because Vispark states all Lab
  models are developed in-house. Indian model datacenters/hosting are explicit. Exclude docs/auth
  hosts. Sources: https://api.lab.vispark.in/v1/models, https://lab.vispark.in/privacy,
  https://vispark.in/terms.
- **Xiaomi adjacent correction:** add `token-plan-sgp.xiaomimimo.com` → `sg` and
  `token-plan-ams.xiaomimimo.com` → `eu`; retain CN → `cn`. AMS is only documented as European
  Cluster, not a country. Update CN-only/Team notes. Sources:
  https://mimo.mi.com/static/docs/tokenplan/Token%20Plan/quick-access.md,
  https://mimo.mi.com/static/docs/tokenplan/Token%20Plan/team.md.
- **Zhipu adjacent correction:** add `api.z.ai` endpoint jurisdiction `sg`; distinguish domestic
  BigModel/PRC terms from Z.ai's Singapore law and SIAC arbitration. Do not change provider
  sovereignty solely from legal forum: no new legal-entity domicile is established. Sources:
  https://docs.z.ai/legal-agreement/terms-of-use, https://docs.z.ai/legal-agreement/privacy-policy.

## D2 — Exact provenance resolution

All patterns are case-insensitive, start-anchored prefixes. Fully qualified forms are required for
runtime matching; the drift checker's arbitrary suffix walk is not a runtime substitute. Unless
stated otherwise, add no provider default or residue.

- **Prisma → Gnani AI/in:** exact `prisma-v2.5`, `prisma-v3.0`, `gnani/prisma-v2.5`,
  `gnani/prisma-v3.0`. Choose exact versions over `prisma-v`; future versions remain visible.
  Sources: https://docs.gnani.ai/api/STT/models/overview,
  https://docs.gnani.ai/api/STT/models/prisma-v2-5,
  https://docs.gnani.ai/api/STT/models/prisma-v3.
- **Gradium → Gradium/eu:** exact `gradium-tts-202602`, `gradium-tts-beta`,
  `gradium/gradium-tts-202602`, `gradium/gradium-tts-beta`, and `gradium/default`; never bare
  `default` or broad `gradium-tts-`. Hosted routes do not inherit separate Phonon lineage. Sources:
  https://docs.gradium.ai/guides/text-to-speech.md,
  https://docs.gradium.ai/guides/release-notes/2026-06.md,
  https://docs.gradium.ai/guides/release-notes/2026-09.md.
- **Vispark Vision → Vispark/in:** `vispark/vision-`; reject bare `vision-` and `vispark/`.
  From-scratch is a provider-authored claim. Sources: https://api.lab.vispark.in/v1/models,
  https://vispark.in/.
- **Jina base-ID prefixes:** `jina-embeddings-v5-text-small` → Alibaba (Jina AI post-train)/cn;
  `...-text-nano` → EuroBERT collaboration (Jina AI post-train)/eu; `...-omni-small` → Alibaba
  (Jina AI post-train; Qwen vision/audio encoders)/cn; `...-omni-nano` → EuroBERT collaboration
  (Jina AI post-train; Alibaba Qwen vision/audio encoders)/eu. Distillation teachers and auxiliary
  encoders do not displace the text backbone. Reject broad v5/v6 coverage. Sources:
  https://huggingface.co/jinaai/jina-embeddings-v5-text-small,
  https://huggingface.co/jinaai/jina-embeddings-v5-text-nano,
  https://arxiv.org/html/2602.15547, https://arxiv.org/html/2605.08384.
- **Tiny Aya → Cohere/ca:** `tiny-aya-`, `CohereLabs/tiny-aya-`, `cohere_chat/tiny-aya-`.
  Ground-up pretraining; teacher models are not weight ancestry. Sources:
  https://docs.cohere.com/docs/tiny-aya, https://arxiv.org/html/2603.11510,
  https://huggingface.co/CohereLabs/tiny-aya-base.
- **Geo CA:** add `ca.` to `passthrough_orgs`; existing Amazon/Anthropic patterns resolve the three
  ids. This is a routing qualifier, never Canadian attribution. Source:
  https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html.
- **Span → Respan (Keywords AI Inc.)/us:** `respan/span-01`, `openrouter/respan/span-01`; covers
  base/lite/:free and the specialized `span-01-security` member of the same first-party family,
  without asserting base lineage. Span-02's separate Gemma lineage remains outside the anchor. Sources:
  https://openrouter.ai/respan/span-01, https://www.respan.ai/legal/terms-of-use.
- **Baseten Bison/Groundhog → Google (Base Labs post-train)/us:**
  `baseten/decision-models/baseten-bison`, `baseten/decision-models/baseten-groundhog`,
  `baselabs/bison`, `baselabs/groundhog`; Gemma bases are explicit. Sources:
  https://www.baseten.co/resources/changelog/bison-1-and-groundhog-1-available-on-baseten/,
  https://huggingface.co/baselabs/bison-1, https://huggingface.co/baselabs/groundhog-1.
- **Ideogram → Ideogram AI/ca:** `ideogram/ideogram-3.0`, `ideogram/ideogram-4.0`,
  `together_ai/ideogram/ideogram-3.0`, `together_ai/ideogram/ideogram-4.0`. No broad Ideogram or
  Together pattern. Sources: https://docs.together.ai/docs/serverless/models,
  https://developer.ideogram.ai/v2/api-reference/images/generate/ideogram-3,
  https://huggingface.co/ideogram-ai/ideogram-4-fp8.
- **Juggernaut Flux → Black Forest Labs (RunDiffusion tune)/eu:**
  `rundiffusion/juggernaut-pro-flux`, `rundiffusion/juggernaut-lightning-flux`, and the two
  `together_ai/rundiffusion/...` forms. Do not transfer SDXL lineage from Juggernaut XL. Sources:
  https://www.rundiffusion.com/juggernaut-flux, https://bfl.ai/legal/imprint.
- **North exact versions:** `north-mini-code-1.0` plus `cohere_chat/` and `coherelabs/` forms →
  Cohere / Cohere Labs/ca; `north-small-translate-1.0` plus those namespaces → Cohere (Command A+
  base)/ca. No broad `north-`. Sources: https://docs.cohere.com/docs/north-mini-code-1.0,
  https://huggingface.co/CohereLabs/North-Mini-Code-1.0/raw/main/README.md,
  https://cohere.com/north-small-translate-tech-report.
- **Sarvam-105B → Sarvam AI/in:** `sarvam-105b`, `sarvam/sarvam-105b`; existing `sarvamai/` stays.
  Sources: https://docs.sarvam.ai/api/token-factory/models/sarvam-105b,
  https://www.sarvam.ai/blogs/sarvam-30b-105b.
- **Sonic → Cartesia/us:** `cartesia/sonic`, `together_ai/cartesia/sonic`; no bare `sonic`.
  Sources: https://docs.together.ai/docs/text-to-speech, https://www.cartesia.ai/sonic.
- **Liquid d1 → Liquid AI/us:** `liquid/d1`, `openrouter/liquid/d1`; deprecation does not make it
  residue or justify borrowing other d1 checkpoint lineage. Sources:
  https://www.liquid.ai/blog/d1-decision-model, https://docs.liquid.ai/lfm/help/deprecations.
- **Fuyu → Adept AI/us:** `fuyu-8b`, `adept/fuyu-8b`, `nvidia_nim/adept/fuyu-8b`; architecture
  metadata is not inheritance. Sources: https://huggingface.co/adept/fuyu-8b/raw/main/README.md,
  https://build.nvidia.com/adept/fuyu-8b.md.
- **Genie → Google/us:** `genie-4`, `gemini/genie-4`; not Genie 3/5 or Databricks Genie. Sources:
  https://aistudio.google.com/docs/models/genie-4.md, https://deepmind.google/models/genie/.
- **Kev → Alibaba (Jared Palmer Kev LoRA/pointer head)/cn:** `kev-4b`, `jaredpalmer/kev-4b`,
  `openrouter/jaredpalmer/kev-4b`; frozen Qwen3.5-4B-Base. Sources:
  https://huggingface.co/jaredpalmer/kev-4b/raw/main/README.md,
  https://github.com/jaredpalmer/kev.
- **Kokoro → Columbia University (hexgrad/@rzvzn Kokoro fine-tune)/us:** `kokoro-82m`,
  `hexgrad/kokoro-82m`, `together_ai/hexgrad/kokoro-82m`; explicit StyleTTS2-LJSpeech base.
  Sources: https://huggingface.co/hexgrad/Kokoro-82M/raw/main/README.md,
  https://github.com/yl4579/StyleTTS2.
- **Tev1 → Alibaba (Together AI supervised fine-tune)/cn:** exact `tev1-4b-experimental`,
  `together/tev1-4b-experimental`, `together_ai/together/tev1-4b-experimental`,
  `togethercomputer/tev1-4b-experimental`, and
  `openrouter/togethercomputer/tev1-4b-experimental`. Remove broad `together/` and
  `together_ai/together/` US mappings rather than layering an override over a false default.
  Sources: https://huggingface.co/togethercomputer/Tev1-4B-experimental,
  https://github.com/togethercomputer/tev1.
- **Zamba2 → Zyphra/us:** `zamba2-`, `zyphra/zamba2-`, `nvidia_nim/zyphra/zamba2-`; tokenizer and
  architecture components do not change weight ancestry. Sources:
  https://build.nvidia.com/zyphra/zamba2-7b-instruct.md,
  https://huggingface.co/Zyphra/Zamba2-7B-Instruct/raw/main/README.md.

## D3 — Exact residue

Add only `together_ai/prunaai/p-image-ideogram`: Pruna/Ideogram collaboration is documented, but no
base checkpoint or fine-tune relationship is disclosed; prompt-schema compatibility is not lineage
(judged 2026-11-23). Sources:
https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/p-image-ideogram.html,
https://www.together.ai/models/p-image-ideogram. No broad Pruna/P-Image residue; future `-v2`
remains actionable. Existing Replicate P-Image entries remain separate.

## D4 — Data-practice corrections

Set every re-verified citation retrieval date and entry review date to the implementation review
date. Preserve null as “not established publicly,” not “none.” DeepSeek alone receives a date-only
review; all other entries require content changes.

- **Alibaba DashScope:** retain training `no`, enterprise, null subprocessors. Replace retention:
  no fixed window; stored Member Content may be removed/inaccessible without deletion instruction;
  customer backs up; processing occurs where Alibaba/affiliates/subcontractors maintain Model
  Studio facilities. Cite Product Terms §§4.48.1(b),(g)(iv),(g)(viii):
  https://www.alibabacloud.com/help/en/legal/latest/alibaba-cloud-international-website-product-terms-of-service.
- **Anthropic:** retain training `no`, null retention/enterprise. Set subprocessors to
  https://www.anthropic.com/subprocessors, identified by DPA Schedule 4:
  https://www.anthropic.com/legal/data-processing-addendum.
- **AWS Bedrock:** training null → `no`; replace retention with per-Region `none` ZDR, new-account
  `inherit`, Responses `store=true` default and `store=false` limitation, documented OpenAI/Fable
  abuse exceptions and destination-Region storage; add AWS-wide subprocessors and replace legacy
  provider-sharing tier text with `aws_review`/Fable/ZDR terms. Sources:
  https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html,
  https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html,
  https://aws.amazon.com/compliance/sub-processors/. Do not repeat categorical “never stores.”
- **Azure Foundry / Azure OpenAI:** replace dead Foundry URLs with
  https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy; retain
  training `no`, stateless/stateful geography, DPA pointer, approval and `ContentLogging=false`.
  Add human-review-only sample storage and MAM cutoff: pre-2026-11-01 approvals continue; later
  models lose MAM on a future announced date with ≥30 days notice. Do not claim withdrawal has
  occurred. Companion: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/abuse-monitoring.
- **DeepSeek:** no fact change; preserve `opt-out` and narrow no-self-serve-API-opt-out caveat.
  Reverify https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html,
  https://cdn.deepseek.com/policies/en-US/model-algorithm-disclosure.html,
  https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html.
- **GitHub Copilot:** scope primary training `no` to volume-licensed commercial users; individual
  Free/Pro/Pro+/Max may train unless opted out. Retention is feature-specific: Actions-based cloud
  chat 28 days; cloud-sandbox chat account lifetime. Remove universal legacy-terms grandfathering.
  Sources: https://github.com/customer-terms/github-generative-ai-services-terms,
  https://docs.github.com/en/copilot/how-tos/manage-your-account/manage-policies,
  https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github.
- **Google Gemini Developer API:** retain Paid Service training `no`; add paid safety/legal logging,
  transient facility caching, Search/Maps 30-day grounding retention, unpaid improvement/human
  review with no numeric general window. Use https://business.safety.google/subprocessors/ under
  DPA §11.2 and service scope; absence of Gemini rows is not a zero-subprocessors claim. Explain
  Paid/Unpaid/Workspace/EEA-UK-Swiss distinctions. Sources: https://aistudio.google.com/docs/terms,
  https://business.safety.google/processorterms/, https://business.safety.google/services/.
- **Meta Llama:** current Model API Terms; Standard training `no`; retention includes security,
  safety, abuse, policy review and improvements. Use incorporated Meta for Work subprocessor URL.
  Replace Discounted with Contributor; Coding Harness defaults Contributor, Standard is prospective;
  Contributor lacks per-request exclusion; Hosted Platforms separate. Sources:
  https://dev.meta.ai/legal/terms-of-service, https://dev.meta.ai/legal/geographic-use-policy,
  https://www.meta.com/legal/meta-for-work/subprocessor-list/.
- **Moonshot:** retain general `opt-out`, ordinary retention, null subprocessors; strengthen
  retention locator to User Content plus §6. Add enterprise no-training default and sales-approved
  ZDR; prompts/responses deleted on response subject to law; safety review continues; Batch,
  uploaded images/videos, operational data and third-party models/connectors/plugins excluded.
  Source: https://platform.kimi.ai/docs/guide/zero-data-retention.md.
- **NVIDIA NIM:** hosted trial API training null → `yes`; normally no post-session content storage,
  no-Subscription fine-tuning User Content 30 days and Generated Content 90 days, security/abuse
  logs no fixed window. Production Subscription terms separate; self-hosted out of scope; null
  subprocessors. Source: https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf.
- **OpenAI:** retain training `no` and enterprise facts. Abuse logs generally up to 30 days but
  endpoint-dependent; Responses at least 30 days by default/`store=true`; ZDR/MAM CSAM image/file
  and notified Private/Safety Retention exceptions. Replace subprocessor locator with current two
  tables. Sources: https://developers.openai.com/api/docs/guides/your-data,
  https://openai.com/policies/data-processing-addendum/.
- **Tencent TokenHub:** training null → `no`; ZDR in Singapore/Frankfurt/Silicon Valley means no
  Customer/Service Generated Content storage; otherwise generally up to 30 days after request;
  configuration/diagnostic generally 30 days, longer for billing. Retain null subprocessors/tier.
  Sources: https://www.tencentcloud.com/document/product/1300/78950,
  https://www.tencentcloud.com/document/product/1300/78953.
- **Vertex AI:** retain training `no` and correct locator to Service Specific Terms §18. Rewrite
  retention for conditional abuse logging, Search 3-day/Maps 30-day grounding, opt-in BigQuery
  logging without TTL, Interactions default store, in-memory and durable caches ≤24h, Live 24h,
  CodeMender/Deep Research 7 days, Sandbox TTL, and OpenAI flagship partner logs ≤30 days in Google
  US multi-region with approval-gated project ZDR. ZDR is model/feature/contract dependent. Sources:
  https://cloud.google.com/terms/service-terms,
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/zero-data-retention?hl=en,
  https://cloud.google.com/terms/advanced-ai-safety-addendum.
- **Xiaomi MiMo:** retain international training `no` and retention; direct international policy
  URL; add Europe/Singapore storage, requestable restrictions subject to law/fees, Individual `tp-`
  vs Team `ttp-`, and Team administration/statistics/billing. Sources:
  https://privacy.mi.com/XiaomiMiMoPlatformos/en_GB/, https://mimo.mi.com/docs/terms/user-agreement,
  and Token Plan sources in D1.
- **Zhipu:** update domestic agreement effective 2026-09-04 and clause locators; disclose
  anonymized training, generated-data optimization, and broad non-personal-content licence. Split
  retention: domestic China/minimum-necessary/statutory/backup/product buffers; Z.ai API content
  real-time without server storage and other Customer Data generally Singapore until termination
  subject to law. Scope seven domestic subprocessors to domestic surfaces; no international list
  established; null enterprise. Sources: https://docs.bigmodel.cn/cn/terms/user-agreement.md,
  https://docs.bigmodel.cn/cn/terms/privacy-policy.md, https://docs.z.ai/legal-agreement/terms-of-use,
  https://docs.z.ai/legal-agreement/privacy-policy.

## D5 — Regulator-profile review

- **HKMA:** replace the superseded 2019 citation with Annex A ART guidance
  https://brdr.hkma.gov.hk/eng/doc-ldg/docId/20261015-2-EN. All three classes seed only `hk`.
  Remove `CN-GBA` from non-PII: the GBA Standard Contract concerns personal-information flows and
  is not a non-personal-operational-data basis. Notes identify conservative product policy, not a
  localisation mandate; remove Sandbox 2024–2026 and erroneous Korean PIPC wording. Supporting:
  https://www.hkma.gov.hk/eng/news-and-media/press-releases/2026/10/20261015-3/,
  https://www.pcpd.org.hk/english/news_events/media_statements/press_20231213.html.
- **MAS:** retain current-effective 2024 information-paper citation and `sg`-only seeds. Add final
  Guidelines issued 2026-10-07, effective 2027-10-07, §§5–6 due 2028-10-07; they complement rather
  than supersede the paper and impose no onshore-only rule. Sources:
  https://www.mas.gov.sg/publications/monographs-or-information-paper/2024/artificial-intelligence-model-risk-management,
  https://www.mas.gov.sg/regulation/guidelines/guidelines-on-artificial-intelligence-risk-management-for-financial-institutions.

## D6 — KB-site null-regime handling

Gradium introduces the first provider endpoint override using `eu`, whose jurisdiction reference
has `regime: null` because GDPR is a transfer-arrangement reference rather than a single EU regime.
Filter null names in `_regime_names` before sorting. This is the minimal correction: retain the
jurisdiction and arrangement rendering, add no synthetic EU regime, and leave the package runtime
unchanged. Existing `test_kb_site_generator` must build the full site and assert Gradium renders.

## Alternatives and decisions

- **Date-only stale refresh rejected:** 15 entries and HKMA have material source changes. A date
  bump would preserve known inaccuracies.
- **Broad family/provider patterns rejected:** exact Prisma/Gradium/North and qualified generic
  stems keep future lineage visible. `vispark/vision-` and `tiny-aya-` are bounded family stems;
  Vispark alone has an explicit all-first-party provider default.
- **Full Together override rejected:** removing false broad US patterns is safer than leaving them
  to capture unknown future Together models.
- **Pruna attribution rejected:** neither Pruna/eu nor Ideogram/ca is defensible without lineage;
  exact residue is not negative provenance data.
- **MAS citation switch deferred:** citing future-effective 2026 Guidelines as the primary current
  source would misstate status; retain 2024 and disclose transition.
- **Sarvam default/old residue excluded:** adjacent questions discovered in research do not belong
  to this actionable wave and need separate review.
