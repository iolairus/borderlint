## ADDED Requirements

### Requirement: Capability statuses reflect shipped behavior

The capability map SHALL mark a capability shipped only when its current specification and
implementation are present, and SHALL NOT mark implemented capabilities as pending. In particular,
plain-language explanations and remediation hints (`--explain`) SHALL be listed as shipped.

#### Scenario: Reader checks explanation support
- **WHEN** a reader consults G2 in the capability map
- **THEN** it identifies `--explain` explanations and remediation hints as shipped rather than next

#### Scenario: Reader checks remaining work
- **WHEN** a reader compares the capability map with current specifications
- **THEN** shipped, next, and later statuses do not contradict the implemented behavior

### Requirement: Product documentation describes current capabilities

README and other current product documentation SHALL provide accurate commands and feature claims
for the shipped detection languages, flow categories, policy dimensions, output formats, and CI
integrations. Documentation MUST NOT present an unsupported command or omit a limitation whose
absence would materially mislead a user.

#### Scenario: User follows a documented command
- **GIVEN** a command is presented as supported by the current release
- **WHEN** it is compared with the CLI and current specifications
- **THEN** its arguments, formats, and described behavior are supported

#### Scenario: User reviews current integrations
- **WHEN** a reader consults the CI and capability summaries
- **THEN** GitHub Actions, Jenkins, and GitLab CI are represented as available integrations

### Requirement: Installation and CI examples use current distribution

Current installation and CI examples SHALL use the public PyPI package or the current release tag
as appropriate. They MUST NOT describe the public repository as private or require source-access
tokens for ordinary PyPI installation.

#### Scenario: Consumer copies a CI example
- **WHEN** a consumer uses a shipped GitHub Actions, Jenkins, or GitLab CI example
- **THEN** its installation source and release reference are current and its documented scan command
  remains policy-gated

### Requirement: Agent integration documentation is current

Claude Code and Cursor documentation SHALL describe the shipped installation paths and preserve
the specified pre-addition scan, SBOM-diff backstop, and justified-waiver guidance.

#### Scenario: User installs an agent integration
- **WHEN** a user follows the Claude Code or Cursor documentation
- **THEN** the referenced files and installation commands exist and match the current integration
  contract
