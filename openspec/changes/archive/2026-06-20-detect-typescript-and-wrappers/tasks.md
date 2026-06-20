## 1. Knowledge base

- [x] 1.1 Add JS/TS package names per provider (e.g. `@anthropic-ai/sdk`, `@google/generative-ai`, `cohere-ai`, `@mistralai/mistralai`, `@aws-sdk/client-bedrock-runtime`)
- [x] 1.2 Add aggregator/router entries (litellm; langchain + `@langchain/*` / `langchain_*`; llama-index; aisuite) with jurisdiction `unknown`

## 2. TypeScript / JavaScript detection

- [x] 2.1 Add a regex-based JS/TS import scanner for `.ts/.tsx/.js/.jsx/.mjs/.cjs` (import / require / dynamic import) mapping package → provider
- [x] 2.2 Wire it into the path walker alongside the Python and text scanners

## 3. Aggregator detection

- [x] 3.1 Detect aggregator libraries in Python (import) and JS/TS (import/require) as flows resolving to `unknown`

## 4. Tests & dogfood

- [x] 4.1 Tests: TS `import OpenAI from "openai"` → OpenAI `[us]`; `require("@anthropic-ai/sdk")` → Anthropic `[us]`; dynamic `await import("openai")` detected; `@mistralai/mistralai` → Mistral `[eu]`; aggregator `import litellm` (py) → `unknown`; `@langchain/openai` (js) → `unknown`; a TS endpoint literal (`https://api.openai.com`) is still detected by the text scan
- [x] 4.2 Dogfood: an internal TypeScript app uses local llama.cpp (correctly clean — no cross-border flow); an internal Python service uses dynamic httpx (out-of-scope runtime endpoint, see follow-up); aggregator + TS detection proven by re-scanning litellm (24.8k router flows) and adding Vercel AI SDK (`@ai-sdk/*`) coverage
