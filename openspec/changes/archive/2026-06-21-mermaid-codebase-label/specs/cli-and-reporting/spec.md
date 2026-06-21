## ADDED Requirements

### Requirement: Mermaid root node identifies the scanned codebase
The Mermaid flow map's application (root) node SHALL be labelled with the scanned codebase's name and,
when determinable, its version. The name SHALL be read from a PEP 621 `pyproject.toml` `[project]` table
or a `package.json` at the scan root, falling back to the scan directory's name; the version SHALL be a
git tag when one is available, else the version from the **same manifest that supplied the name**. When
no name is determinable the node SHALL use a generic label. Resolution is best-effort: it reads only the
scan root's manifests and a local `git` invocation, accesses no network, and SHALL NOT fail the scan if
git is absent or returns no tag. The label SHALL be a single line, escaped like any other Mermaid label.
Only the Mermaid root node is affected; other output formats are unchanged.

#### Scenario: package.json names the root node
- **WHEN** the scan root contains a `package.json` with name `acme-bot` and version `1.2.3` and is not a git repository
- **THEN** the Mermaid application node is labelled `acme-bot@1.2.3`

#### Scenario: pyproject [project] names the root node
- **WHEN** the scan root contains a `pyproject.toml` `[project]` table with name `acme` and version `0.4.0` and is not a git repository
- **THEN** the Mermaid application node is labelled `acme@0.4.0`

#### Scenario: a git tag supplies the version when git is available
- **WHEN** the scan root is a git repository whose latest tag is `v2.0.0` and git is available
- **THEN** the Mermaid application node's version is `v2.0.0`

#### Scenario: a manifest name without a version
- **WHEN** the scan root's manifest supplies a name but no version and no git tag is available
- **THEN** the Mermaid application node is labelled with the bare name and no `@`

#### Scenario: fallback to the directory name
- **WHEN** the scan root has no manifest name and no determinable version
- **THEN** the Mermaid application node is labelled with the scan directory's name

#### Scenario: a label with metacharacters stays single-line and escaped
- **WHEN** a resolved name contains a double quote, a `#`, or a newline
- **THEN** the Mermaid application node label is escaped (`#`→`#35;`, `"`→`#quot;`) and rendered on a single line
