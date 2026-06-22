## ADDED Requirements

### Requirement: Resolve GCP (Vertex AI) region-coded endpoint host

borderlint SHALL resolve a Google Vertex AI endpoint host that carries a GCP region
(`<region>-aiplatform.googleapis.com`, or the `aiplatform.<us|eu>.rep.googleapis.com` multi-region
form) to the corresponding jurisdiction. When the host carries no region (the global
`aiplatform.googleapis.com` endpoint), the jurisdiction SHALL be `unknown`.

#### Scenario: Regional Vertex host resolves
- **WHEN** an endpoint reference contains `asia-east2-aiplatform.googleapis.com`
- **THEN** the flow resolves to jurisdiction `hk`

#### Scenario: A European Vertex region resolves
- **WHEN** an endpoint reference contains `europe-west4-aiplatform.googleapis.com`
- **THEN** the flow resolves to jurisdiction `nl`

#### Scenario: The global Vertex endpoint is unknown
- **WHEN** an endpoint reference contains the regionless `aiplatform.googleapis.com`
- **THEN** the flow resolves to jurisdiction `unknown`
