# kb-website Specification

## ADDED Requirements

### Requirement: Site generation from the bundled knowledge base
The project SHALL provide a generator that renders the bundled knowledge base into a static
website consisting of an index page, one page per provider, and one page per model developer
organisation, aggregating that organisation's model-id patterns from the provenance map. The generator SHALL read only the bundled KB JSON —
the site is a projection of the KB and SHALL NOT contain hand-edited content. Every page SHALL
state the KB's last-reviewed dates and link back to the repository.

#### Scenario: Full generation
- **WHEN** the generator runs against the bundled KB
- **THEN** it emits an index, one page for every provider in the KB, and one page per model developer organisation in the provenance map

#### Scenario: KB is the single source
- **WHEN** a provider's KB entry changes and the generator re-runs
- **THEN** the provider's page reflects the new entry without any other edit

### Requirement: Provider page content
Each provider page SHALL state the provider's name, its category when the KB records one, its
residency jurisdiction(s) — including an explicit note when residency is region-dependent or
unknown — its sovereignty bloc (including region-level overrides for ring-fenced subsidiaries),
its known endpoint hosts and package names, the data-protection regime names applicable to its
jurisdictions, and the applicable cross-border arrangement references rendered as hyperlinks.

#### Scenario: A mapped provider renders all governance facts
- **WHEN** the page for a provider with a resolved jurisdiction and sovereignty bloc is generated
- **THEN** it states name, residency, sovereignty, endpoints, and packages, names the applicable regimes, and renders arrangement references as hyperlinks

#### Scenario: A region-dependent provider is honest about unknowns
- **WHEN** the page for a region-selectable provider (jurisdiction `unknown`) is generated
- **THEN** the residency is presented as region-dependent rather than as a resolved country

### Requirement: Model-developer page content
Each model-developer page SHALL state the organisation's name, its model-id patterns from the
provenance map, and the provenance bloc(s) those patterns resolve to.

#### Scenario: A developer page renders provenance facts
- **WHEN** the page for a model developer organisation is generated
- **THEN** it states the organisation, its model-id patterns, and their provenance bloc(s)

### Requirement: Discoverability metadata
Every generated page SHALL carry a unique HTML title and meta description that name the provider
or model developer organisation together with the governance dimension it answers (residency,
sovereignty, or provenance), and the site SHALL include the install one-liner on every page.

#### Scenario: Unique page metadata
- **WHEN** any two pages of the generated site are compared
- **THEN** their titles and meta descriptions differ and each names its subject

### Requirement: Automated publication
The site SHALL be rebuilt and republished automatically when the bundled KB or the generator
changes on the default branch and when a release is published, and SHALL be manually triggerable.

#### Scenario: KB change triggers a deploy
- **WHEN** a commit touching the bundled KB lands on the default branch
- **THEN** the publication workflow rebuilds the site from that commit and deploys it

#### Scenario: Release triggers a deploy
- **WHEN** a release is published
- **THEN** the publication workflow rebuilds and deploys the site

#### Scenario: Manual dispatch
- **WHEN** a maintainer triggers the workflow manually
- **THEN** the site is rebuilt and deployed

### Requirement: No runtime impact
Generating and publishing the site SHALL NOT change the shipped package: no new runtime files,
dependencies, or CLI behavior.

#### Scenario: Package unaffected
- **WHEN** the package is built after this change
- **THEN** its contents and dependencies are identical to before, and site tooling lives outside the package
