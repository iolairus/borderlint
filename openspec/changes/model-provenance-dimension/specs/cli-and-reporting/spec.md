## ADDED Requirements

### Requirement: Provenance in report output
Every report format SHALL surface each flow's provenance bloc alongside residency and
sovereignty, never replacing either: the text report SHALL include a provenance segment per
provider line; the JSON report SHALL include a `provenance` field per finding; the Mermaid
diagram SHALL reflect the provenance in the node label when it differs from the flow's
sovereignty (identical blocs would only repeat the label); the SARIF output SHALL include the
provenance in the result message; the SBOM SHALL include a `provenances` list per component.
The provenance reasons SHALL have human-readable descriptions in report output.

#### Scenario: Text report shows provenance
- **WHEN** the text report renders a flow with provenance `cn`
- **THEN** the provider line includes a provenance segment naming the bloc

#### Scenario: JSON report carries the provenance field
- **WHEN** the JSON report renders a finding
- **THEN** the finding object includes a `provenance` field with the flow's bloc

#### Scenario: SBOM aggregates provenances
- **WHEN** the SBOM renders a component with detections of provenance `us` and `cn`
- **THEN** the component's `provenances` list contains both blocs

### Requirement: No new required CLI flags for provenance
Provenance evaluation SHALL be driven entirely by the policy file; the CLI SHALL NOT require any
new flag to enable, evaluate, or report provenance.

#### Scenario: Existing invocation surfaces provenance
- **WHEN** a scan runs with only the existing flags against a policy without a provenance block
- **THEN** provenance is reported per flow and no provenance verdict is produced
