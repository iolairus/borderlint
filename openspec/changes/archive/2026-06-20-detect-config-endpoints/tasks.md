## 1. Config-endpoint detection (flow-detection)

- [x] 1.1 Define the AI-endpoint key set (`base_url`, `api_base`, `azure_endpoint`, `openai_api_base`, `endpoint`) and the code `base_url` / `baseURL` kwargs
- [x] 1.2 Regex-scan YAML/JSON/TOML for `<ai-endpoint-key>: <url>` → extract the host → detection
- [x] 1.3 Regex-detect `base_url=` / `baseURL:` client overrides in Python and JS/TS code → detection

## 2. Classification (jurisdiction-classification)

- [x] 2.1 An anchored detection whose host is not in the KB resolves to `unknown`
- [x] 2.2 A loopback / localhost host resolves to `local`

## 3. Policy (residency-policy)

- [x] 3.1 Treat `local` as always permitted (never a violation), independent of the allow-list

## 4. Tests & dogfood

- [x] 4.1 Tests: custom host in a YAML `base_url` → `unknown`; known host in a JSON `api_base` → `cn`; Python `base_url=` override → detected; `localhost` → `local` (passes a strict allow-list AND does not trip `on_unknown: fail`); a non-AI URL under a non-AI key is NOT flagged
- [x] 4.2 Dogfood: re-scan a config-driven setup (a litellm config / a local-inference config) to verify the new requirements on real files — config-key detection, custom host → `unknown`, loopback → `local`
