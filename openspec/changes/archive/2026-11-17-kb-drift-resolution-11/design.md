# Design: kb-drift-resolution-11

## Research basis (primary sources, reviewed 2026-11-17)

### Provider and moving routes

- **Microsoft Web IQ** — Microsoft describes Web IQ as model-agnostic retrieval/grounding, not an
  LLM, with Web Search at `api.microsoft.ai/v3/search/web`, no regional data-residency commitment,
  and cross-region routing expected. Official SDK documentation names `webiq`,
  `@microsoft/webiq`, `com.microsoft.webiq`, and `Microsoft.WebIQ`; terms identify the
  Microsoft-operated service. Sources: https://learn.microsoft.com/en-us/web-iq/resources/faq,
  https://learn.microsoft.com/en-us/web-iq/reference/web-search,
  https://learn.microsoft.com/en-us/web-iq/integrations/sdk,
  https://www.microsoft.com/en-us/webiq/webiq-legal. Do not alias the distinct product to Bing
  Grounding or Azure Foundry.
- **Nace Drex** — the pinned open Max v1 checkpoint declares Qwen3.8-27B as its base, but Nace's
  current catalog retires API v1.5 into v1.1 and forwards `drex-latest` and `drex-max` to v1.1. The
  v1.1 report says it uses internal proprietary models and does not disclose architecture or base
  lineage. Retired API v1.5 and moving-latest routes are therefore unknown-lineage routes, not
  stable Qwen ids. Sources:
  https://huggingface.co/nace-ai/drex-max-v1/raw/main/decision_config.json,
  https://console.nace.ai/docs/drex/reference/models, https://arxiv.org/html/2611.07854.
  Remove the four API/moving patterns `drex-v1.5`, `nace/drex-v1.5`, `drex-latest`, and
  `nace/drex-latest`; retain immutable `nace-ai/drex-v1.5` and active v2.0 forms, and add
  `nace-ai/drex-max-v1`. Do not transfer older Lucy/Max/Isaac disclosures to different versions.

### Resolvable model families

The 54 implementation patterns below use canonical owner/model forms after adding `replicate/` as
a passthrough. Bare forms are included only where the family stem itself is distinctive and safe.

- **OpenAI CSAM classifier** — `omni-moderation-csam-` → OpenAI/us. OpenAI documents the model id
  and states its teams trained the classifier. Sources:
  https://developers.openai.com/api/docs/guides/csam-classifier,
  https://openai.com/index/strengthening-online-child-safety/.
- **TypeSafe Jev** — `typesafe-ai/jev` and full `vercel_ai_gateway/typesafe-ai/jev` → TypeSafe
  AI/us. The full Vercel AI Gateway key is required because the runtime matcher has no arbitrary
  suffix walk. Vercel identifies this as TypeSafe's Jev, distinct from Bevelites' eu/jev product;
  TypeSafe terms identify the US company. Sources:
  https://vercel.com/ai-gateway/models/jev, https://docs.typesafe.ai/models,
  https://eu-jev.com/docs, https://typesafe.ai/terms.
- **Alibaba Wan** — `wan-3`, `alibaba/wan-3`, `wan-video/wan-2.`, and
  `wavespeedai/wan-2.1-` → Alibaba (Wan-AI)/cn; Pruna's `prunaai/wan-2.2-image` uses the same
  lineage with org `Alibaba (Wan-AI; Pruna AI optimized)`. Official Alibaba API/catalog pages and
  Wan repositories identify the models and variants; WaveSpeedAI and Pruna explicitly describe
  accelerated/derived Wan deployments. Sources:
  https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-api-reference,
  https://www.alibabacloud.com/help/en/model-studio/use-video-generation,
  https://github.com/Wan-Video/Wan2.2, https://github.com/Wan-Video/Wan2.1,
  https://replicate.com/prunaai/wan-2.2-image.
- **Bria** — `bria/fibo`, `bria/image-3.2`, `bria/expand-image`, and
  `bria/remove-background` → Bria AI/il. FIBO/FIBO Edit, BRIA-3.2, Expand Image, and RMBG-2.0
  have named Bria models or weights; Bria's terms identify the Tel Aviv company. Sources:
  https://huggingface.co/briaai/FIBO, https://huggingface.co/briaai/Fibo-Edit,
  https://github.com/Bria-AI/BRIA-3.2, https://huggingface.co/briaai/RMBG-2.0,
  https://bria.ai/terms-and-conditions.
- **ElevenLabs** — `elevenlabs/flash-v2.5`, `elevenlabs/turbo-v2.5`,
  `elevenlabs/v2-multilingual`, and `elevenlabs/v3` → ElevenLabs/us. Official model and Replicate
  catalogs identify these speech models; the separate Dubbing workflow is residue. Sources:
  https://elevenlabs.io/docs/models, https://replicate.com/elevenlabs/v3,
  https://elevenlabs.io/terms.
- **HeyGen** — `heygen/avatar-iv` and `heygen/avatar-v` → HeyGen/us. HeyGen's model
  documentation names Avatar IV/V rendering engines; translation modes and Video Agent are
  workflows, not the same model ids. Sources: https://developers.heygen.com/models,
  https://replicate.com/heygen/avatar-iv, https://www.heygen.com/terms.
- **Ideogram** — `ideogram-ai/ideogram-v2`, `ideogram-ai/ideogram-v3-`, and
  `ideogram-ai/ideogram-v4-` → Ideogram AI/ca. Official generation references enumerate the V2,
  V3, and V4 variants; Layerize is a separate design pipeline. Sources:
  https://developer.ideogram.ai/api-reference/api-reference/generate,
  https://developer.ideogram.ai/api-reference/api-reference/generate-v3,
  https://developer.ideogram.ai/api-reference/api-reference/generate-v4,
  https://ideogram.ai/legal/tos.
- **Inworld** — `inworld/realtime-tts-` → Inworld AI/us. Inworld's catalogs and launch notes
  identify the 1.5 Max/Mini and TTS-2 family; terms name Theai, Inc. dba Inworld AI in Mountain
  View. Sources: https://docs.inworld.ai/tts/tts-models.md,
  https://inworld.ai/blog/realtime-tts-2, https://www.inworld.ai/terms.
- **Kling** — `kling-v` and `kwaivgi/kling-v` → Kuaishou/cn. Kuaishou identifies Kling as its
  video model and documents the 2.1/2.5 variants. Lip Sync is a face/session feature with no
  separately identified weights family. Sources: https://klingai.com/document-api/api/video/2-5-turbo/text-to-video,
  https://klingai.com/document-api/guides/protocols/paid-service,
  https://klingai.com/quickstart/ai-lip-sync-guide.
- **Lightricks LTX** — `lightricks/ltx-2-distilled`, `lightricks/ltx-2-fast`,
  `lightricks/ltx-2-pro`, `lightricks/ltx-2.3-fast`, `lightricks/ltx-2.3-pro`, and
  `lightricks/ltx-2.5-fast` → Lightricks/il. Official model cards publish the corresponding LTX
  families; A2Vid and Retake are pipelines over LTX-2 rather than separate weights families.
  Sources: https://huggingface.co/Lightricks/LTX-2,
  https://huggingface.co/Lightricks/LTX-2.3, https://huggingface.co/Lightricks/LTX-2.5,
  https://raw.githubusercontent.com/Lightricks/LTX-2/main/packages/ltx-pipelines/README.md,
  https://www.lightricks.com/contact-us.
- **Luma** — `luma/photon` → Luma AI/us, covering Photon and Photon Flash. Luma's own API and
  launch material identify the family; Reframe Video is an operation on an undisclosed Ray
  version. Sources: https://lumalabs.ai/photon, https://docs.lumalabs.ai/docs/image-generation,
  https://docs.lumalabs.ai/docs/video-generation, https://lumalabs.ai/legal/privacy.
- **Real-ESRGAN** — `nightmareai/real-esrgan` → Tencent ARC Lab / Chinese Academy of Sciences/cn.
  NightmareAI is the packager; the upstream repository and paper identify the original developers
  and released weights. Sources: https://github.com/xinntao/Real-ESRGAN,
  https://github.com/NightmareAI/Real-ESRGAN, https://arxiv.org/abs/2107.10833.
- **Isaac 0.1** — `perceptron-ai-inc/isaac-0.1`, `perceptronai/isaac-0.1`,
  `perceptron/isaac-0.1`, `openrouter/perceptron/isaac-0.1`, and `isaac-0.1` → cn with org
  `Alibaba (Perceptron AI post-train; Google SigLIP2 vision)`. The model card declares Qwen3-1.7B
  and SigLIP2 bases. The full OpenRouter key is required because the existing
  `openrouter/perceptron/` US prefix otherwise wins; the longer `perceptron/` override likewise
  prevents the existing direct-provider US family default from misclassifying Isaac. Sources:
  https://huggingface.co/PerceptronAI/Isaac-0.1/raw/main/README.md,
  https://huggingface.co/api/models/PerceptronAI/Isaac-0.1,
  https://www.perceptron.inc/blog/introducing-isaac-0-1.
- **PlayDialog** — `playht/play-dialog` → PlayAI (formerly PlayHT)/us. PlayAI's SDK and launch
  material identify its conversational speech model; terms name Playht, Inc. in Palo Alto.
  Sources: https://github.com/playht/pyht, https://play.ai/terms,
  https://www.businesswire.com/news/home/20241125475299/en/PlayAI-Secures-%2421-Million-in-Seed-Funding-and-Releases-New-Model-for-Generative-AI-Conversations.
- **Pruna derivatives** — `prunaai/flux-fast` and `prunaai/flux-kontext-fast` →
  `Black Forest Labs (Pruna AI optimized)`/eu; `prunaai/hidream-l1-fast` →
  `HiDream.ai (Pruna AI optimized)`/cn; `prunaai/p-video-animate`, `prunaai/p-video-avatar`, and
  `prunaai/p-video-replace` → `Lightricks (LTX-2; Pruna AI endpoint)`/il. Pruna explicitly
  identifies FLUX/HiDream/Wan bases and attaches LTX-2 licenses to the three P-Video endpoints.
  Sources: https://replicate.com/prunaai/flux-fast,
  https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev,
  https://huggingface.co/HiDream-ai/HiDream-I1-Fast,
  https://docs.api.pruna.ai/guides/models/p-video-animate,
  https://docs.api.pruna.ai/guides/models/p-video-avatar,
  https://docs.api.pruna.ai/guides/models/p-video-replace.
- **QuiverAI Arrow** — `quiverai/arrow-1.1` → QuiverAI/ca, covering Max and vectorize variants.
  QuiverAI describes Arrow as its own vector-native model; terms give its Montréal address.
  Sources: https://quiver.ai/blog/introducing-arrow-1-1/,
  https://quiver.ai/blog/announcing-our-seed-round/, https://quiver.ai/legal/terms/.
- **Recraft** — `recraft-ai/recraft-20b`, `recraft-ai/recraft-v3`, and
  `recraft-ai/recraft-v4` → Recraft/us. Official docs identify the raster/SVG, Styles, Utility,
  and Pro generation variants; upscale/background/vectorize are tools. Sources:
  https://www.recraft.ai/docs/api-reference/models/recraft-v3,
  https://www.recraft.ai/docs/api-reference/models/recraft-v4,
  https://www.recraft.ai/docs/api-reference/models/recraft-v4-1,
  https://www.recraft.ai/legal/developer-terms.
- **Resemble AI Chatterbox** — `resemble-ai/chatterbox` → Resemble AI/us, covering base/Pro/Turbo.
  Cards identify the family and its Llama backbone where applicable; both developer and base are
  US. Sources: https://huggingface.co/ResembleAI/chatterbox,
  https://huggingface.co/ResembleAI/chatterbox-turbo,
  https://github.com/resemble-ai/chatterbox, https://www.resemble.ai/terms-of-service/.
- **Sync Labs** — `lipsync-2`, `react-1`, `sync/lipsync-2`, and `sync/react-1` → Sync Labs/us.
  Sync's own catalog lists all three as models; its privacy policy identifies Synchronicity Labs,
  Inc. in San Francisco. Sources: https://docs.sync.so/, https://sync.so/lipsync-2-pro,
  https://sync.so/react-1, https://sync.so/privacy.
- **Nace pinned Max v1** — `nace-ai/drex-max-v1` → Alibaba (Nace Drex post-train)/cn, restricted
  to the official open checkpoint namespace. It must not match the moving API aliases.

### Exact residue (no provenance pattern)

Add 57 exact full-key entries: 55 cached wave ids among the original 145, plus the non-fixture
`nace/drex-latest` and `nace/drex-v1.5` entries. In the grouped lists below, each bare suffix
inherits the full namespace printed at the start of that group; implementation must expand every
key to its full form as a separate exact entry. None ends in `/` or `-`, so future variants remain
visible. Every unknown judgment means the source names no defensible single base lineage; every
structural judgment identifies an operation/application rather than a separate weights family.

- `webiq/search`: Microsoft search operation, not a model.
- `nace/drex-max`, `nace/drex-max-v1.1`, `nace/drex-latest`, and `nace/drex-v1.5`: current
  moving/retired proprietary v1.1 lineage undisclosed; do not inherit the historical open
  checkpoint's cn bloc.
- Bria: `replicate/bria/eraser`, `generate-background`, `genfill`, `increase-resolution`,
  `product-cutout`, `product-packshot`, `product-shadow`, `video-erase-object`,
  `video-increase-resolution`, and `video-remove-background`. These are mixed-component or
  unidentified-checkpoint editing workflows. Sources: https://huggingface.co/briaai/erase,
  https://huggingface.co/briaai/increase-resolution, https://docs.bria.ai/video-editing-overview,
  and the corresponding official Replicate pages.
- `replicate/datalab-to/ocr`: generic OCR toolkit/pipeline with multiple detection/recognition
  components, not a bound Surya-2 checkpoint. Sources: https://replicate.com/datalab-to/ocr,
  https://github.com/datalab-to/surya/blob/v0.17.1/README.md.
- `replicate/decart/lucy-edit-2`: real proprietary model, base weights undisclosed; older Lucy Dev
  Wan lineage cannot be transferred. Sources: https://replicate.com/decart/lucy-edit-2,
  https://decart.ai/publications/lucy-2-introducing-sota-video-generation-in-realtime.
- `replicate/easel/ai-avatars`: model-agnostic likeness product with no named generator. Sources:
  https://replicate.com/easel/ai-avatars, https://replicate.com/blog/easel.
- `replicate/elevenlabs/dubbing`: localization job pipeline, not one disclosed speech model.
  Sources: https://elevenlabs.io/docs/product-guides/products/dubbing,
  https://elevenlabs.io/docs/api-reference/dubbing/create.
- Fifteen `replicate/flux-kontext-apps/` ids: `cartoonify`, `change-haircut`, `depth-of-field`,
  `face-to-many-kontext`, `filters`, `iconic-locations`, `impossible-scenarios`,
  `multi-image-kontext-max`, `multi-image-kontext-pro`, `multi-image-list`, `portrait-series`,
  `professional-headshot`, `restore-image`, `restyle-video-frame`, and `text-removal`. Fourteen are
  prompt/input/video adapters around hosted FLUX, not new weight families; face-to-many has no
  lineage disclosure. Sources: the corresponding official Replicate pages and
  https://replicate.com/black-forest-labs/flux-kontext-pro.
- HeyGen: `replicate/heygen/lipsync-precision`, `lipsync-speed`, and `video-agent` — translation
  modes and a composite production pipeline, not Avatar IV/V model ids. Sources:
  https://developers.heygen.com/reference/create-video-translation,
  https://replicate.com/heygen/video-agent.
- `replicate/ideogram-ai/layerize`: text detection/font matching/removal/layout design workflow.
  Sources: https://developer.ideogram.ai/v2/api-reference/images/layerize/ideogram-3,
  https://replicate.com/ideogram-ai/layerize.
- `replicate/intelligent-utilities/html-to-image`: deterministic html2image/browser screenshot
  utility. Sources: https://replicate.com/intelligent-utilities/html-to-image,
  https://github.com/vgalin/html2image.
- `replicate/kwaivgi/kling-lip-sync`: Kling face/session processing feature, not a separately
  disclosed model. Sources: https://klingai.com/document-api/api/video/lip-sync/face-detection,
  https://klingai.com/document-api/api/video/lip-sync.
- `replicate/lightricks/audio-to-video` and `replicate/lightricks/ltx-2-retake`: A2VidPipeline
  and RetakePipeline tasks over LTX-2, not new model families. Source:
  https://raw.githubusercontent.com/Lightricks/LTX-2/main/packages/ltx-pipelines/README.md.
- `replicate/luma/reframe-video`: video-reframe operation on an unidentified Ray version.
  Sources: https://replicate.com/luma/reframe-video, https://docs.agents.lumalabs.ai/.
- `replicate/philz1337x/clarity-pro-upscaler`: Pro's closed lineage is undisclosed; do not impute
  the separate open clarity-upscaler pipeline's Stable Diffusion components. Sources:
  https://replicate.com/philz1337x/clarity-pro-upscaler, https://clarityai.co/api,
  https://github.com/philz1337x/clarity-upscaler.
- `replicate/pixverse/lipsync`: a Solution/capability distinct from named PixVerse models, with no
  base lineage disclosed. Sources: https://docs.platform.pixverse.ai/model-capability-map-2394982m0,
  https://docs.platform.pixverse.ai/lipsync-43051219e0.
- Pruna unknowns: `replicate/prunaai/p-image`, `p-image-edit`, `p-image-edit-lora`,
  `p-image-lora`, `p-video-2-pro-avatar`, and `p-video-2-pro-replace`. P-Image materials credit
  multiple parties without one base checkpoint; the two 2-Pro routes are compound pipelines whose
  pages do not bind the sibling MiniMax lineage. Sources: https://www.pruna.ai/p-image,
  https://www.pruna.ai/p-image-edit, https://docs.api.pruna.ai/guides/models/p-video-2-pro-avatar,
  https://docs.api.pruna.ai/guides/models/p-video-2-pro-replace.
- Recraft tools: `replicate/recraft-ai/recraft-creative-upscale`, `recraft-crisp-upscale`,
  `recraft-remove-background`, and `recraft-vectorize`. Official API classifies them as image
  tools with no model field. Sources: https://www.recraft.ai/docs/api-reference/tools/upscale,
  https://www.recraft.ai/docs/api-reference/tools/remove-background,
  https://www.recraft.ai/docs/api-reference/tools/vectorize.
- `replicate/retro-diffusion/rd-animation`: real generation model, base checkpoint undisclosed;
  Stable Diffusion compatibility elsewhere is not lineage evidence. Sources:
  https://replicate.com/retro-diffusion/rd-animation, https://retrodiffusion.ai/app/guide.
- `replicate/veed/fabric-1.0`: real explicitly fine-tuned model, base family undisclosed. Source:
  https://replicate.com/veed/fabric-1.0.

### MCP launcher review

The official SQLite implementation is Python package/binary `mcp-server-sqlite`, not the scoped
npm key currently in the map. Replace that invalid key and add exactly these documented launch
identities to existing provider targets:

- local: `mcp-server-sqlite`, `mcp/sqlite`, `mcp-server-filesystem`, `mcp-server-memory`,
  `mcp-server-everything`, `mcp-server-sequential-thinking`, and `mcp-server-postgres`.
- brave_search: `@brave/brave-search-mcp-server`, `brave-search-mcp-server`, `mcp/brave-search`,
  and `docker.io/mcp/brave-search`.
- notion: `notion-mcp-server` and `mcp/notion`.
- sentry: `sentry` and `sentry-mcp`.

Sources:
https://raw.githubusercontent.com/modelcontextprotocol/servers-archived/main/src/sqlite/pyproject.toml,
https://raw.githubusercontent.com/modelcontextprotocol/servers-archived/main/src/sqlite/README.md,
https://github.com/modelcontextprotocol/servers,
https://github.com/modelcontextprotocol/servers-archived,
https://github.com/brave/brave-search-mcp-server,
https://github.com/makenotion/notion-mcp-server,
https://github.com/getsentry/sentry-mcp. Retain archived identifiers for existing configs. Retain
existing GitHub/Slack/Drive keys without adding new identities for those services, and add no
fetch/git/time servers in this wave.

## Decisions

- **D1 — Web IQ is a service with unknown residency, not an inference provider.** US sovereignty
  follows Microsoft; no region or model lineage is guessed. `webiq/search` is exact residue.
- **D2 — Add `replicate/` to `passthrough_orgs`.** Replicate identifies hosting, not development,
  exactly like the existing aggregator passthroughs. Canonical owner/model patterns then cover
  both SDK literals and LiteLLM's leading `replicate/` keys. Duplicating every pattern with a full
  Replicate prefix was rejected as redundant and easier to let drift.
- **D3 — Owner qualification is the default; bare stems are exceptional.** Only
  `omni-moderation-csam-`, `wan-3`, `kling-v`, `isaac-0.1`, `lipsync-2`, and `react-1` are
  distinctive enough to stand alone. No bare `v3`, `photon`, `arrow`, `fabric`, `flash`, `ltx`,
  `wan`, `recraft-`, or whole-org pattern. Full provider/gateway keys remain explicit; the runtime
  matcher gains no arbitrary suffix walk.
- **D4 — Exact residue is not negative provenance data.** Add 55 cached-wave entries plus two
  non-fixture Nace entries (57 total), expanding every grouped suffix to a full key. Residue must
  not become a broad owner prefix or hide a model already matched by a pattern. Future variants
  remain actionable.
- **D5 — Retired and moving Nace routes follow current served lineage.** Remove `drex-v1.5`,
  `nace/drex-v1.5`, `drex-latest`, and `nace/drex-latest`; retain immutable `nace-ai/drex-v1.5`
  and active v2.0 forms. Max v1's official HF checkpoint is cn, while retired v1.5 and current
  Max/v1.1/latest API routes remain unknown.
- **D6 — Isaac inherits Qwen despite other Perceptron models being US.** Add longer
  `perceptron/isaac-0.1` and full `openrouter/perceptron/isaac-0.1` cn overrides alongside official
  publisher and bare version-anchored forms, all using the same Alibaba/Perceptron/Google org.
- **D7 — Refresh MCP identities, not backend semantics.** Add only the exact local, Brave Search,
  Notion, and Sentry launchers enumerated above; retain existing GitHub/Slack/Drive keys and add no
  fetch/git/time servers. Self-hosted GitHub/Sentry and arbitrary PostgreSQL backends need
  host-aware scanner behavior and are explicitly deferred rather than hidden by a date bump.

## Risks / follow-ups

- Replicate can retarget a hosted slug without changing its id; exact residue and owner-qualified
  patterns make re-review manageable, and Nace demonstrates why retired API versions and moving
  aliases need scrutiny.
- Prefixes intentionally cover future variants in the same named family; a future disclosed base
  change requires a longer override or removal.
- MCP self-hosted destination attribution remains a known limitation outside this data-only wave.
- Data-practice gaps remain the standing human-curation queue and increase with Web IQ.
