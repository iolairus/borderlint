## ADDED Requirements

### Requirement: Each resolved flow carries a sovereignty bloc
In addition to a jurisdiction (residency), each resolved flow SHALL carry a sovereignty bloc
resolved from the provider knowledge base. The sovereignty bloc SHALL be one of the values defined
by the sovereignty vocabulary. A provider KB entry MAY declare an optional `sovereignty` field; a
host-level `sovereignty` override on a KB entry SHALL take precedence over the provider-level value.

#### Scenario: A provider KB entry declares its sovereignty
- **WHEN** a provider KB entry declares `sovereignty: us`
- **THEN** a flow to that provider resolves to sovereignty `us` regardless of the endpoint region

#### Scenario: A host-level sovereignty override takes precedence
- **WHEN** a provider KB entry declares a host with a `sovereignty` override distinct from the provider-level value
- **THEN** a flow to that host resolves to the host-level sovereignty

### Requirement: Region-in-endpoint providers inherit provider sovereignty
For a region-in-endpoint provider (AWS Bedrock, Azure OpenAI, Vertex AI), the resolved sovereignty SHALL be the provider's sovereignty, independent of the region resolved for residency. The endpoint region determines residency only; it SHALL NOT determine sovereignty. This requirement MUST hold for every region-in-endpoint provider in the knowledge base.

#### Scenario: Bedrock sovereignty is the provider's, not the region's
- **WHEN** a flow is detected to AWS Bedrock in `ap-east-1` (residency `hk`)
- **THEN** the flow's sovereignty is `us` (AWS's home sovereign), not `hk`
