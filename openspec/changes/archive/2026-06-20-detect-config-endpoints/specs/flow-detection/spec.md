## ADDED Requirements

### Requirement: Detect AI endpoints declared in configuration
The system SHALL detect endpoints referenced by known AI-endpoint configuration keys (for example
`base_url`, `api_base`, `azure_endpoint`, `openai_api_base`, `endpoint`) in YAML, JSON, and TOML
files, and record each as a detection.

#### Scenario: Custom endpoint in a YAML config
- **WHEN** a YAML file contains `base_url: https://llm.acme.cn/v1`
- **THEN** a detection is recorded for that endpoint

#### Scenario: Known provider endpoint via a config key
- **WHEN** a JSON file contains `"api_base": "https://api.deepseek.com"`
- **THEN** a detection is recorded identifying DeepSeek

#### Scenario: A non-AI key is not flagged
- **WHEN** a config file sets a non-AI URL under a non-AI key (for example `database_url: https://db.example.com`)
- **THEN** no detection is recorded for it

### Requirement: Detect AI client endpoint overrides in code
The system SHALL detect an AI client endpoint override supplied in Python or JavaScript/TypeScript
code (for example a `base_url` argument) and record the referenced endpoint.

#### Scenario: base_url override in Python
- **WHEN** Python code constructs a client with `base_url="https://llm.acme.cn"`
- **THEN** a detection is recorded for that endpoint
