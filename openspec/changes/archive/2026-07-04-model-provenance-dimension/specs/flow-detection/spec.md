## ADDED Requirements

### Requirement: Detect model references
The system SHALL detect model references in scanned source as a `model_reference` detection
kind, by matching string literals against the anchored model-identifier patterns of the
provenance map. Detection SHALL cover the same languages and file kinds as provider detection.
Matching SHALL be anchored to model-identifier shapes; the system SHALL NOT flag arbitrary
substrings that merely resemble model names.

#### Scenario: A model identifier string literal is detected
- **WHEN** a scanned Python file contains the string literal `"claude-sonnet-4-6"` as a model argument
- **THEN** a `model_reference` detection is recorded with the file, line, and the matched identifier as evidence

#### Scenario: A resembling variable name is not flagged
- **WHEN** a scanned file contains a variable named `gpt` with no model-identifier string literal
- **THEN** no `model_reference` detection is recorded

### Requirement: Model references bind to same-file provider detections
A `model_reference` detection SHALL bind to a provider detection in the same file when the
file's matched model references resolve to exactly one distinct provenance bloc, assigning that
bloc to the flow; when several same-bloc references bind, the first matched reference's
identifier SHALL be recorded as the flow's model identifier, representing its siblings. When a
file's model references resolve to more than one distinct bloc, binding would be ambiguous: no
binding SHALL occur and each reference SHALL stand alone. A `model_reference` with no provider
detection in its file SHALL stand alone as its own finding. Binding SHALL NOT cross file
boundaries.

#### Scenario: Model reference in the same file as a provider flow
- **WHEN** a file contains both a provider detection and a matching model reference
- **THEN** the provider flow carries the model reference's provenance and both evidences are traceable

#### Scenario: Ambiguous blocs do not bind
- **WHEN** a file contains a provider detection and model references resolving to two distinct blocs
- **THEN** the provider flow keeps its two-tier provenance and each reference is reported as its own standalone finding

#### Scenario: Standalone model reference
- **WHEN** a file contains a matching model reference but no provider detection
- **THEN** a standalone `model_reference` finding is reported with its resolved provenance

### Requirement: Detections carry a provenance value
Each detection SHALL carry a provenance bloc, defaulting to `unknown`, populated during scanning
from the two-tier provenance resolution.

#### Scenario: A detection with no model reference on a first-party provider
- **WHEN** a provider that serves only its own models is detected with no bound model reference
- **THEN** the detection's provenance is the provider organisation's bloc
