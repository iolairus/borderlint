# kb-freshness Specification

## Purpose
TBD - created by archiving change scheduled-kb-refresh. Update Purpose after archive.
## Requirements
### Requirement: Scheduled coverage check
The system SHALL provide a scheduled job that periodically produces a freshness report covering:
upstream providers not yet in the bundled provider knowledge base and not suppressed by the
curated alias/ignore list, upstream model identifiers not covered per the model provenance
coverage check — split into actionable families and acknowledged structural residue — bundled
provider entries with missing or invalid sovereignty blocs, and bundled knowledge bases whose
last-reviewed date exceeds the review interval. Sections with no items SHALL be omitted; when
every section is empty, no review item SHALL be raised; when a review item from a previous run
is still open, it SHALL be updated rather than duplicated.

#### Scenario: A new upstream provider is surfaced
- **WHEN** the scheduled check runs and the upstream list contains a provider absent from the bundled knowledge base and not suppressed by the alias/ignore list
- **THEN** that provider is reported for review, with a prompt to assign endpoint host(s), a jurisdiction, and a sovereignty bloc by hand — or to record it as an alias or out-of-scope entry

#### Scenario: An uncovered model family is surfaced
- **WHEN** the scheduled check runs and an upstream model identifier is uncovered per the model provenance coverage check and not acknowledged as structural residue
- **THEN** its family is reported for review in the actionable provenance section

#### Scenario: No drift
- **WHEN** the scheduled check runs and every section of the freshness report is empty
- **THEN** no review item is raised

#### Scenario: A persistent condition does not duplicate the review item
- **WHEN** the scheduled check runs with a non-empty report and a review item from a previous run is still open
- **THEN** the open item is updated with the current report and no duplicate is raised

#### Scenario: An exact-key acknowledgment does not cover future variants
- **WHEN** the residue list acknowledges an identifier as an exact key and a new variant of it later appears uncovered
- **THEN** the new variant appears in the actionable family section

### Requirement: Deterministic coverage diff
Every freshness computation SHALL be a pure, offline function of the bundled knowledge bases,
supplied upstream data, a supplied curated suppression list, and a supplied reference date,
returning exactly the uncovered, incomplete, or stale items, with no network access.

#### Scenario: Uncovered providers computed from a fixture
- **WHEN** the provider diff runs against a fixed upstream list, the bundled knowledge base, and a fixed suppression list
- **THEN** it returns exactly the upstream providers absent from the bundled knowledge base and not suppressed, with no network access

#### Scenario: Provenance and sovereignty checks computed from fixtures
- **WHEN** the model coverage, sovereignty completeness, and staleness checks run against fixed inputs
- **THEN** each returns exactly the uncovered families, incomplete entries, or stale knowledge bases, with no network access

### Requirement: Human-assigned jurisdictions
The coverage check SHALL NOT auto-assign a jurisdiction, endpoint host, sovereignty bloc, or
provenance bloc to any discovered item; each emitted gap record carries none of these, leaving
every assignment for human curation.

#### Scenario: Emitted gap record has no jurisdiction or endpoint
- **WHEN** the check surfaces a new provider
- **THEN** the emitted gap record carries no jurisdiction, no endpoint host, and no sovereignty bloc

#### Scenario: Uncovered model families carry no bloc
- **WHEN** the check surfaces an uncovered model family
- **THEN** the emitted record carries no provenance bloc

### Requirement: Knowledge base provenance
The bundled knowledge base SHALL carry a last-reviewed date as an ISO-8601 (`YYYY-MM-DD`) value in a
top-level metadata field, exposed when the knowledge base is loaded.

#### Scenario: KB carries an ISO date
- **WHEN** the bundled knowledge base is loaded
- **THEN** its last-reviewed date is available as an ISO-8601 `YYYY-MM-DD` value

### Requirement: Refresh does not affect scans
The coverage check SHALL be dev/CI-only; the scanner and knowledge-base load path SHALL perform no
network access.

#### Scenario: The scan path makes no network request
- **WHEN** the knowledge base is loaded and a scan runs
- **THEN** no network request is made

### Requirement: Community contribution workflow

The project SHALL document how to contribute a provider to the bundled knowledge base, covering
the KB entry schema and the rule that jurisdictions are human-assigned via pull request. The
documentation MUST stay consistent with the existing "Human-assigned jurisdictions" requirement
(no auto-merge from an upstream feed).

#### Scenario: KB entry schema is documented
- **WHEN** a contributor consults the contribution guide
- **THEN** it documents each KB entry field (`id`, `name`, `category`, `sdks`, `npm`, `jvm`,
  `dotnet`, `endpoints`, `jurisdiction`, `region_scheme`, `endpoint_jurisdictions`), marks which
  are required versus optional, and lists the valid jurisdiction tokens (ccTLD/ISO codes plus
  `CN-GBA`, `GBA`, `local`, `unknown`)

#### Scenario: Jurisdictions stay human-assigned
- **WHEN** a new provider is contributed via pull request
- **THEN** the guide requires its jurisdiction to be assigned by a human reviewer, never
  auto-merged from the drift check's output

### Requirement: Model provenance coverage check
The scheduled check SHALL compare upstream model identifiers against the bundled provenance map
using the same resolution behaviour the scanner applies, counting an identifier as covered when
the identifier or its remainder after a provider-qualifying prefix resolves. An identifier whose
upstream provider is marked out-of-scope in the curated suppression list SHALL be excluded from
the comparison; an identifier whose upstream provider resolves — directly or through the alias
list — to a bundled speech-category provider with a first-party provenance default SHALL count
as covered. Identifiers of inference providers SHALL keep surfacing when unresolved — as actionable
families, or as acknowledged residue counts when a residue entry classifies them. Uncovered
identifiers not acknowledged as residue SHALL be reported aggregated by model family, each
family carrying a model count and one example identifier. The report section SHALL be bounded in length and SHALL disclose how
many families were omitted when the bound is exceeded.

#### Scenario: A provider-qualified identifier counts as covered
- **WHEN** an upstream model identifier carries a provider-qualifying prefix and its remainder resolves via the provenance map
- **THEN** the identifier is not reported as uncovered

#### Scenario: An out-of-scope provider's identifiers are excluded
- **WHEN** an upstream model identifier belongs to a provider marked out-of-scope in the suppression list
- **THEN** the identifier does not appear in the model-coverage comparison at all

#### Scenario: A speech provider's tier identifiers count as covered
- **WHEN** an upstream model identifier belongs to a provider that resolves to a bundled speech-category provider with a first-party provenance default
- **THEN** the identifier is not reported as uncovered

#### Scenario: A first-party inference provider's novel family still surfaces
- **WHEN** an upstream model identifier belongs to a first-party inference provider and no pattern resolves it
- **THEN** the identifier is reported as uncovered, so the family reaches pattern curation

#### Scenario: A multi-model host's identifiers still face matching
- **WHEN** an upstream model identifier belongs to a multi-model host with no first-party default and no pattern resolves it
- **THEN** the identifier is reported as uncovered

#### Scenario: An uncovered family is aggregated
- **WHEN** several upstream model identifiers of one family resolve to no provenance entry
- **THEN** the report lists that family once, with the number of identifiers and one example

#### Scenario: The section bound is disclosed
- **WHEN** the number of uncovered families exceeds the section bound
- **THEN** the section states how many further families were omitted

### Requirement: Sovereignty completeness check
The scheduled check SHALL report every bundled provider entry whose sovereignty bloc is missing
or outside the sovereignty bloc vocabulary, identifying the provider and the offending value.

#### Scenario: A provider without a sovereignty bloc is reported
- **WHEN** a bundled provider entry carries no sovereignty bloc
- **THEN** the report names that provider in the sovereignty section

#### Scenario: Complete entries raise nothing
- **WHEN** every bundled provider entry carries a bloc from the sovereignty vocabulary
- **THEN** the sovereignty section is empty

### Requirement: SDK coverage check
The scheduled check SHALL report every bundled provider entry that carries at least one package
key (`sdks` or `npm`) but lacks a `jvm` or `dotnet` key, unless the provider is recorded in the
curated suppression list as SDK-exempt with a stated reason. The check SHALL identify the
provider and the missing keys, SHALL NOT assign or suggest package names, and SHALL fail loudly
on an exemption without a reason or naming a provider absent from the bundled knowledge base.
The exemption list SHALL be consumed only by the check, never by the scanner.

#### Scenario: A provider with SDK-key gaps is surfaced
- **WHEN** the scheduled check runs and a bundled provider carries an `npm` or `sdks` key but no `jvm` or `dotnet` key and is not SDK-exempt
- **THEN** the report names that provider and which package keys are missing, for manual curation

#### Scenario: A reasoned exemption is suppressed
- **WHEN** a bundled provider with SDK-key gaps is recorded in the exemption list with a stated reason
- **THEN** it does not appear in the SDK coverage section

#### Scenario: An exemption without a reason fails loudly
- **WHEN** the exemption list records a provider with an empty reason
- **THEN** the check fails with an error naming the entry

#### Scenario: An exemption for an unknown provider fails loudly
- **WHEN** the exemption list names a provider id absent from the bundled knowledge base
- **THEN** the check fails with an error naming the id

#### Scenario: The SDK section is omitted when empty
- **WHEN** every bundled provider with package keys also carries `jvm` and `dotnet` keys or is SDK-exempt
- **THEN** the SDK coverage section is omitted from the report

#### Scenario: The scanner never reads the exemption list
- **WHEN** the knowledge base is loaded and a scan runs
- **THEN** the exemption list is not consulted and detection behavior is unchanged

### Requirement: Knowledge base staleness warning
The scheduled check SHALL warn about each bundled knowledge base whose last-reviewed date is
older than the review interval, naming the knowledge base, its last-reviewed date, and its age.

#### Scenario: A stale knowledge base is flagged
- **WHEN** a bundled knowledge base's last-reviewed date is older than the review interval
- **THEN** the report includes a staleness warning naming it, its date, and its age

#### Scenario: A recently reviewed knowledge base is not flagged
- **WHEN** a bundled knowledge base's last-reviewed date is within the review interval
- **THEN** no staleness warning is raised for it

### Requirement: Upstream provider aliases and out-of-scope names are suppressed
The scheduled check SHALL exclude from the new-provider section any upstream name that is
either mapped as an alias of a covered provider or marked out-of-scope with a stated reason,
via a curated suppression list consumed only by the check — never by the scanner; the model
provenance coverage check SHALL consume the same list for its provider-context rules and its
acknowledged-residue classification. An alias
whose target provider id is absent from the bundled knowledge base SHALL fail the check
loudly; an out-of-scope entry without a reason SHALL fail the check loudly. Names that are
neither aliased nor ignored SHALL continue to surface.

#### Scenario: A route alias of a covered provider is suppressed
- **WHEN** the upstream list contains a name mapped as an alias of a provider present in the bundled knowledge base
- **THEN** the name does not appear in the new-provider section

#### Scenario: An out-of-scope tool is suppressed with a reason
- **WHEN** the upstream list contains a name marked out-of-scope with a stated reason
- **THEN** the name does not appear in the new-provider section

#### Scenario: An alias to a missing provider fails loudly
- **WHEN** the suppression list maps an upstream name to a provider id absent from the bundled knowledge base
- **THEN** the check fails with an error naming the alias and the missing id

#### Scenario: An ignore without a reason fails loudly
- **WHEN** the suppression list marks an upstream name out-of-scope with an empty reason
- **THEN** the check fails with an error naming the entry

#### Scenario: An unlisted upstream name still surfaces
- **WHEN** the upstream list contains a name that is neither covered, aliased, nor ignored
- **THEN** the name appears in the new-provider section as before

#### Scenario: The scanner never reads the suppression list
- **WHEN** the knowledge base is loaded and a scan runs
- **THEN** the suppression list is not consulted and detection behavior is unchanged

### Requirement: Acknowledged structural residue is separated from actionable items
The scheduled check SHALL classify uncovered model identifiers that match a curated residue
list — exact identifiers or id-prefixes, each carrying a stated reason — as acknowledged structural residue, rendered
in a separate collapsed report section as per-class counts with the reason, never among the
actionable families and never as raw id lists. Classification SHALL apply only to identifiers
the coverage check already failed to resolve, so a residue entry can never affect coverage. A
residue entry without a reason SHALL fail the check loudly. Uncovered identifiers matching no
residue entry SHALL remain in the actionable family section.

#### Scenario: A pricing-bucket id is acknowledged, not actionable
- **WHEN** an uncovered identifier matches a residue prefix with a stated reason
- **THEN** it is counted in the residue section under that reason and absent from the actionable families

#### Scenario: Residue never affects coverage
- **WHEN** an identifier matching a residue prefix also resolves via the provenance map
- **THEN** it is covered, and the residue entry plays no part

#### Scenario: A residue entry without a reason fails loudly
- **WHEN** the residue list contains a prefix with an empty reason
- **THEN** the check fails with an error naming the entry

#### Scenario: Unacknowledged identifiers stay actionable
- **WHEN** an uncovered identifier matches no residue prefix
- **THEN** it appears in the actionable family section as before

### Requirement: The report leads with an actionable summary
The freshness report SHALL open with a one-line summary stating the count of actionable
providers, actionable model families, providers with SDK-key gaps, and acknowledged residue
identifiers, so a reader can tell whether anything requires a decision without reading the
sections.

#### Scenario: The summary line reflects the sections
- **WHEN** the report renders with two actionable providers, three actionable families, one provider with SDK-key gaps, and ten acknowledged residue identifiers
- **THEN** the leading line states those four counts

#### Scenario: Nothing actionable is visible at a glance
- **WHEN** every section except the residue section is empty
- **THEN** the summary line states zero actionable items
