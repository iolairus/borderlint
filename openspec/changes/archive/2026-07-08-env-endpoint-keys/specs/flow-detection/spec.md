## MODIFIED Requirements

### Requirement: Detect AI endpoints declared in configuration
The system SHALL detect endpoints referenced by known AI-endpoint configuration keys (for example
`base_url`, `api_base`, `azure_endpoint`, `openai_api_base`, `endpoint`) in YAML, JSON, and TOML
files, and record each as a detection. The system SHALL also detect env-style keys —
underscore-segmented names, matched case-insensitively, whose final segment is `URL`,
`ENDPOINT`, `BASE`, or `HOST` and where some whole segment is an AI stem from a curated list —
in any scanned file, including `.env` files and settings-module assignments. Keys with no
AI-stem segment SHALL NOT be flagged. A captured value SHALL be treated as an endpoint only
when it is host-shaped, loopback, or carries an explicit URL scheme — a scheme-bearing value
MAY have a single-label host (a compose service name) and resolves as a custom endpoint; a
capture containing code-call punctuation (an environment getter) SHALL NOT be flagged.

#### Scenario: Custom endpoint in a YAML config
- **WHEN** a YAML file contains `base_url: https://llm.acme.cn/v1`
- **THEN** a detection is recorded for that endpoint

#### Scenario: Known provider endpoint via a config key
- **WHEN** a JSON file contains `"api_base": "https://api.deepseek.com"`
- **THEN** a detection is recorded identifying DeepSeek

#### Scenario: A prefixed env-style key resolves a packaged endpoint
- **WHEN** a scanned `.env` file contains `TELLMEWHY_LLM_SERVER_URL=http://localhost:8080`
- **THEN** a detection is recorded resolving to `local`

#### Scenario: A prefixed provider key resolves
- **WHEN** a config file contains `OPENAI_BASE_URL=https://api.openai.com/v1`
- **THEN** a detection is recorded identifying OpenAI

#### Scenario: A non-AI key is not flagged
- **WHEN** a config file sets a non-AI URL under a non-AI key (for example `database_url: https://db.example.com`)
- **THEN** no detection is recorded for it

#### Scenario: An AI-substring inside a segment does not match
- **WHEN** a scanned `.env` file contains `EMAIL_URL=https://mail.example.com`
- **THEN** no detection is recorded, because no whole segment is an AI stem

#### Scenario: A compose service hostname resolves as a custom endpoint
- **WHEN** a compose file contains `- OLLAMA_BASE_URL=http://ollama:11434`
- **THEN** a detection is recorded as a custom endpoint with `unknown` jurisdiction, governable by `on_unknown`

#### Scenario: An environment-getter assignment is not flagged
- **WHEN** a settings module contains `LLM_SERVER_URL = os.environ.get("TELLMEWHY_LLM_SERVER_URL", "http://localhost:8080")`
- **THEN** no detection is recorded for the assignment — the value is runtime-resolved; the packaged `.env` file is the declaration the scanner reads
