## ADDED Requirements

### Requirement: AI data-flow SBOM export
The CLI SHALL provide a `--format sbom` export that emits a policy-independent JSON inventory of every
detected AI flow — each provider with its name, resolved jurisdiction(s), and call sites (file and
line) — under an envelope carrying a schema identifier, the borderlint version, and the KB review date.
The export SHALL be deterministic (no wall-clock timestamp, components sorted) and SHALL NOT gate CI.

#### Scenario: SBOM lists every detected flow
- **WHEN** `--format sbom` runs over a path with AI provider usage
- **THEN** the output is a JSON document whose components list each provider with its jurisdiction(s) and call sites

#### Scenario: The SBOM is policy-independent and does not gate
- **WHEN** `--format sbom` runs with a policy under which a detected flow would fail
- **THEN** the document still lists that flow with no severity or verdict, and the process exits 0

#### Scenario: The SBOM is deterministic
- **WHEN** the same path is scanned twice with `--format sbom`
- **THEN** the two outputs are byte-identical
