## 1. Knowledge base

- [ ] 1.1 Add JS/TS package names per provider (e.g. `@anthropic-ai/sdk`, `@google/generative-ai`, `cohere-ai`, `@mistralai/mistralai`, `@aws-sdk/client-bedrock-runtime`)
- [ ] 1.2 Add aggregator/router entries (litellm; langchain + `@langchain/*` / `langchain_*`; llama-index; aisuite) with jurisdiction `unknown`

## 2. TypeScript / JavaScript detection

- [ ] 2.1 Add a regex-based JS/TS import scanner for `.ts/.tsx/.js/.jsx/.mjs/.cjs` (import / require / dynamic import) mapping package → provider
- [ ] 2.2 Wire it into the path walker alongside the Python and text scanners

## 3. Aggregator detection

- [ ] 3.1 Detect aggregator libraries in Python (import) and JS/TS (import/require) as flows resolving to `unknown`

## 4. Tests & dogfood

- [ ] 4.1 Tests: TS `import OpenAI from "openai"` → OpenAI `[us]`; `require("@anthropic-ai/sdk")` → Anthropic `[us]`; dynamic `await import("openai")` detected; `@mistralai/mistralai` → Mistral `[eu]`; aggregator `import litellm` (py) → `unknown`; `@langchain/openai` (js) → `unknown`; a TS endpoint literal (`https://api.openai.com`) is still detected by the text scan
- [ ] 4.2 Re-scan `retire` (TS) and `TellMeWhy` (wrapper) and confirm the previously-missed flows are now detected
