## ADDED Requirements

### Requirement: Mermaid root node identifies the scanned codebase
The Mermaid flow map's application (root) node SHALL be labelled with the scanned codebase's name and,
when determinable, its version — derived from a project manifest (`pyproject.toml` `[project]`, or
`package.json`) at the scan root, or from a git tag — and SHALL fall back to the scan directory's name,
and to a generic label when no name is determinable. The label SHALL be escaped like any other Mermaid
label.

#### Scenario: package.json names the root node
- **WHEN** the scan root contains a `package.json` with name `acme-bot` and version `1.2.3` and is not a git repository
- **THEN** the Mermaid application node is labelled `acme-bot@1.2.3`

#### Scenario: pyproject names the root node
- **WHEN** the scan root contains a `pyproject.toml` with `[project]` name `acme` and version `0.4.0` and is not a git repository
- **THEN** the Mermaid application node is labelled `acme@0.4.0`

#### Scenario: a git tag supplies the version
- **WHEN** the scan root is a git repository whose latest tag is `v2.0.0`
- **THEN** the Mermaid application node's version is `v2.0.0`

#### Scenario: fallback to the directory name
- **WHEN** the scan root has no manifest and no determinable version
- **THEN** the Mermaid application node is labelled with the scan directory's name
