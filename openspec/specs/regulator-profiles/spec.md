# regulator-profiles Specification

## Purpose
TBD - created by archiving change regulator-policy-profiles. Update Purpose after archive.
## Requirements
### Requirement: Bundled cited profiles
The system SHALL bundle a set of regulator profiles keyed by profile id, where each profile
records: the supported seat(s) it applies to, the regulator's name, a guidance citation
consisting of a URL and retrieval date, default classification allow-lists mapping each
handled class to jurisdiction tokens from the recognised vocabulary, and optional free-text
notes. Every profile SHALL carry an ISO-8601 `reviewed` date, every allow-list token
SHALL be validated against the existing jurisdiction vocabulary at load time, and the file
SHALL carry a top-level ISO-8601 `updated` date so the bundled knowledge base participates
in the scheduled staleness check.

#### Scenario: A complete profile loads
- **WHEN** the bundled profiles are loaded and one carries seat, regulator, citation, defaults, and review date
- **THEN** the profile is exposed by id with all fields intact

#### Scenario: An invalid profile fails loudly
- **WHEN** a profile references a jurisdiction token outside the recognised vocabulary or lacks a citation or review date
- **THEN** loading raises an error naming the profile id and the offending field

### Requirement: Profile-seeded init walk
When `--profile <id>` is supplied to `init`, the wizard SHALL pre-seed each handled
classification's allow-list with that profile's defaults: seeded jurisdictions are offered
in the walk with keep as the default answer, so each is present unless the operator
explicitly drops it; jurisdictions observed in the scan but absent from the profile SHALL
still be offered with the usual drop-by-default prompt. Supplying an unknown profile id
SHALL exit non-zero with an error listing the available ids.

#### Scenario: Seeded jurisdiction offered with keep as default
- **WHEN** init runs with a profile whose customer-pii defaults include `sg` and no `sg` flow is observed
- **THEN** `sg` is offered for customer-pii with keep as the default and lands in the allow-list unless dropped

#### Scenario: Observed jurisdiction still offered
- **WHEN** init runs with a profile and the scan observes a jurisdiction absent from the profile defaults
- **THEN** that jurisdiction is offered in the walk for each handled class

#### Scenario: Unknown profile rejected
- **WHEN** init runs with `--profile mas` and no such profile is bundled
- **THEN** borderlint exits non-zero and lists the available profile ids

### Requirement: Profile provenance rendering
The wizard SHALL state the profile's regulator, guidance citation, and retrieval date when a
profile is active, and the emitted policy file SHALL carry that provenance as comment lines;
the JSON keys of the emitted policy SHALL remain exactly those of the unprofiled path so the
file loads via the existing policy loader.

#### Scenario: Provenance shown during init
- **WHEN** init runs with the hkma profile
- **THEN** the output names the regulator and cites its guidance with retrieval date

#### Scenario: Emitted file stays loadable
- **WHEN** init writes a policy under a profile
- **THEN** the file loads via the existing policy loader and its JSON keys match the unprofiled shape

### Requirement: Human-curated profiles only
Profiles SHALL be populated exclusively by human curation via pull request; each profile's
defaults MUST cite the regulator guidance it derives from, and the system SHALL NOT fetch or
update profiles from regulator websites at runtime.

#### Scenario: No runtime fetching
- **WHEN** any borderlint command runs
- **THEN** no network request is made to resolve or refresh profiles

### Requirement: Advisory framing of profiles
Profile-seeded policies SHALL be presented as conservative starting points derived from the
cited guidance as of its retrieval date — not legal advice and not a determination of filing
sufficiency; the disclaimer SHALL appear in the wizard output whenever a profile is active.

#### Scenario: Disclaimer accompanies seeded walk
- **WHEN** init runs with any profile
- **THEN** the output states the seed is a starting point from the cited guidance, not legal advice

