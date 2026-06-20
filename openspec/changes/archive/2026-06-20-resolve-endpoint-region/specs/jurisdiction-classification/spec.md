## ADDED Requirements

### Requirement: Resolve region-coded endpoint host
The system SHALL resolve a region-coded endpoint host to a jurisdiction when the region is present
in the matched text, before falling back to unknown.

#### Scenario: Bedrock host carries a Hong Kong region
- **WHEN** a detected endpoint contains `bedrock-runtime.ap-east-1.amazonaws.com`
- **THEN** the resolved jurisdiction is `hk`

#### Scenario: Bedrock host carries a Mainland China region
- **WHEN** a detected endpoint contains `bedrock-runtime.cn-north-1.amazonaws.com.cn`
- **THEN** the resolved jurisdiction is `cn`

#### Scenario: Region is not present in the host
- **WHEN** a detected endpoint is a standard `<resource>.openai.azure.com` host with no region token
- **THEN** the resolved jurisdiction is unknown
