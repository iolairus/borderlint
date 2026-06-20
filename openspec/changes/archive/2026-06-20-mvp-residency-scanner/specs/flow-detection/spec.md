## ADDED Requirements

### Requirement: Detect AI provider SDK usage
The system SHALL detect usage of known AI provider SDKs in a scanned codebase and record each as a
detection identifying the provider.

#### Scenario: Python source imports a provider SDK
- **WHEN** a Python source file imports a known provider SDK (for example `openai`)
- **THEN** a detection is recorded identifying that provider, with the source file and line number

### Requirement: Detect AI provider endpoint references
The system SHALL detect references to known AI provider endpoint hosts in source files and in
configuration/text files, and record each as a detection identifying the provider.

#### Scenario: Endpoint host appears in a source string
- **WHEN** a scanned file contains a known provider endpoint host (for example `api.deepseek.com`)
- **THEN** a detection is recorded identifying that provider, with the file and line number

#### Scenario: Endpoint host appears in a configuration file
- **WHEN** a configuration or text file (for example `.env`) contains a known provider endpoint host
- **THEN** a detection is recorded identifying that provider

### Requirement: Exclude non-source locations
The system SHALL exclude version-control, dependency, and build directories from scanning so that
vendored or generated code does not produce detections.

#### Scenario: Match inside an excluded directory
- **WHEN** a provider endpoint host appears in an excluded directory (for example `node_modules`)
- **THEN** no detection is recorded for that location

### Requirement: Record traceable evidence
Each detection SHALL record the provider, the matched evidence, the file path, and the line number.

#### Scenario: Detection carries file and line
- **WHEN** any detection is produced
- **THEN** it includes the provider, the matched evidence, the file path, and the line number

### Requirement: Resilient scanning
The system SHALL continue scanning the remaining files when an individual file cannot be parsed.

#### Scenario: A file fails to parse
- **WHEN** a file cannot be parsed during a scan
- **THEN** the scan continues and other files are still scanned

### Requirement: De-duplicate detections
The system SHALL report at most one detection for the same provider, evidence, file, and line.

#### Scenario: Same flow detected more than once
- **WHEN** the same provider would be detected more than once at the same file and line
- **THEN** only one detection is reported for it
