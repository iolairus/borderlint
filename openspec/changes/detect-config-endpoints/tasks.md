## 1. Config-endpoint detection (flow-detection)

- [ ] 1.1 Define the AI-endpoint key set (`base_url`, `api_base`, `azure_endpoint`, `openai_api_base`, `endpoint`) and the code `base_url` / `baseURL` kwargs
- [ ] 1.2 Regex-scan YAML/JSON/TOML for `<ai-endpoint-key>: <url>` → extract the host → detection
- [ ] 1.3 Regex-detect `base_url=` / `baseURL:` client overrides in Python and JS/TS code → detection

## 2. Classification (jurisdiction-classification)

- [ ] 2.1 An anchored detection whose host is not in the KB resolves to `unknown`
- [ ] 2.2 A loopback / localhost host resolves to `local`

## 3. Policy (residency-policy)

- [ ] 3.1 Treat `local` as always permitted (never a violation), independent of the allow-list

## 4. Tests & dogfood

- [ ] 4.1 Tests: custom host in a YAML `base_url` → `unknown`; known host in a JSON `api_base` → `cn`; Python `base_url=` override → detected; `localhost` → `local` (passes a strict policy); a non-AI URL under a non-AI key is NOT flagged
- [ ] 4.2 Dogfood: re-scan a config-driven setup (a litellm config / a local-inference config) and confirm custom + local endpoints surface correctly
