# kb-freshness — delta for kb-site-sdk-keys

## ADDED Requirements

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

## MODIFIED Requirements

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
