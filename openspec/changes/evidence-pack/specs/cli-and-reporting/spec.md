## ADDED Requirements

### Requirement: Evidence pack output format
The system SHALL provide an `evidence` output format rendering a self-contained transfer-
inventory document containing: an audit envelope; a per-flow inventory carrying the provider
and its category, residency jurisdiction, sovereignty bloc, provenance bloc with the developer
organisation and model identifier when known, applicable cross-border arrangement references,
the verdict with its reasons, and the code locations; a register of every active waiver with
its location and justification; and summary counts by verdict. Without a policy, the document
SHALL render in inventory framing — flows and axes without verdicts.

#### Scenario: The inventory carries all three axes and the org
- **WHEN** the evidence pack renders a flow with residency `hk`, sovereignty `us`, provenance `cn`, and a bound model with a known developer organisation
- **THEN** the flow's row shows all three axes, the model identifier, and the organisation

#### Scenario: Waivers are registered, not hidden
- **WHEN** a finding was waived with a justification
- **THEN** the waiver register lists its code location and justification, and the summary counts it as waived

#### Scenario: No policy still yields a fileable inventory
- **WHEN** the evidence pack renders from a scan with no policy
- **THEN** the document contains the envelope and the per-flow inventory without verdicts

### Requirement: Evidence audit envelope
The evidence pack SHALL open with an audit envelope stating: the tool version, the last-
reviewed dates of the bundled knowledge bases, the scan timestamp in UTC, the scanned path's
resolved git commit, the policy file's SHA-256 digest, and the declared classification and home
location. Each envelope field that cannot be resolved SHALL render as `unavailable` rather than
being omitted. Envelope resolution SHALL perform no network access, and the timestamp SHALL
honour `SOURCE_DATE_EPOCH` when set.

#### Scenario: The envelope pins the scan to a commit and a policy version
- **WHEN** the scanned path is a git repository and a policy file is supplied
- **THEN** the envelope states the commit hash and the policy digest

#### Scenario: Unresolvable fields are stated, not dropped
- **WHEN** the scanned path is not a git repository
- **THEN** the envelope's commit field reads `unavailable`

#### Scenario: A reproducible-build pipeline gets a deterministic pack
- **WHEN** `SOURCE_DATE_EPOCH` is set and the same tree and policy are scanned twice
- **THEN** the two evidence packs are byte-identical

### Requirement: Regime-aligned evidence annex
The evidence pack SHALL include a regime annex when the declared home location falls under a
regime present in the bundled regime-expectations data, mapping the inventory to that regime's
documented filing expectations with citations. Fields the static scan cannot determine SHALL
render as explicitly marked org-supplied blanks, never fabricated values. Home locations
outside the covered set SHALL receive the generic document with no annex. The expectations data
SHALL be bundled, carry a last-reviewed date, and remain advisory — references, never
adjudication of filing sufficiency.

#### Scenario: A Hong Kong home base gets the PDPO annex
- **WHEN** the policy declares `home_location` `hk` and the format is `evidence`
- **THEN** the pack includes an annex citing the PCPD cross-border guidance, with static fields filled from findings and org-supplied fields rendered as marked blanks

#### Scenario: A Mainland GBA home base gets PIPL and GBA SC framing
- **WHEN** the policy declares a `cn` or `CN-GBA` home location
- **THEN** the annex cites the PIPL PIA and transfer-route expectations and references the GBA Standard Contract where the flows qualify

#### Scenario: A Macao home base gets the Macao PDPA annex
- **WHEN** the policy declares `home_location` `mo`
- **THEN** the annex cites the Macao PDPA transfer expectations and references the (Mainland, Macao) GBA Standard Contract variant where the flows qualify

#### Scenario: A Singapore home base gets the PDPA annex
- **WHEN** the policy declares `home_location` `sg`
- **THEN** the annex cites PDPA s.26 and the PDPC transfer documentation expectations

#### Scenario: An uncovered home base gets no fake annex
- **WHEN** the policy declares a home location with no entry in the expectations data
- **THEN** the pack renders without a regime annex and states no annex is available for that regime

#### Scenario: A legacy home_regime-only policy gets the generic pack
- **WHEN** the policy declares `home_regime` but no `home_location`
- **THEN** the pack renders without a regime annex

## MODIFIED Requirements

### Requirement: CI exit code
The CLI SHALL exit with a non-zero status when any violation is found and a zero status otherwise,
except when an artifact-export format (`--format sbom` or `--format evidence`) is requested — an
export is not a gate and SHALL exit zero regardless of violations.

#### Scenario: Violation fails the build
- **WHEN** a scan finds at least one violation under a gating format
- **THEN** the CLI exits with a non-zero status

#### Scenario: Clean scan passes the build
- **WHEN** a scan finds no violations
- **THEN** the CLI exits with a zero status

#### Scenario: SBOM export does not gate
- **WHEN** `--format sbom` is requested and a scan finds a violation
- **THEN** the CLI exits with a zero status

#### Scenario: A failing state can still be filed as evidence
- **WHEN** the scan produces failing findings and the format is `evidence`
- **THEN** the document records the failures and the exit code is 0

### Requirement: Scan command
The CLI SHALL provide a `scan` command that takes a path to scan, an optional policy, an optional
active classification, and an output format (human-readable, JSON, Mermaid, SARIF, SBOM, or evidence).

#### Scenario: Scan a path against a policy
- **WHEN** the user runs the scan command with a path, a policy, and a classification
- **THEN** the path is scanned and detected flows are evaluated against the policy for that classification
