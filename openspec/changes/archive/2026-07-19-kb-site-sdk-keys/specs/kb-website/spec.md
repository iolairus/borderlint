# kb-website — delta for kb-site-sdk-keys

## MODIFIED Requirements

### Requirement: Provider page content
Each provider page SHALL state the provider's name, its category when the KB records one, its
residency jurisdiction(s) — including an explicit note when residency is region-dependent or
unknown — its sovereignty bloc (including region-level overrides for ring-fenced subsidiaries),
its known endpoint hosts and all recorded package names per language (Python `sdks`, npm,
JVM `jvm`, .NET `dotnet`), labeled by language, the data-protection regime names applicable to its
jurisdictions, and the applicable cross-border arrangement references rendered as hyperlinks.

#### Scenario: A mapped provider renders all governance facts
- **WHEN** the page for a provider with a resolved jurisdiction and sovereignty bloc is generated
- **THEN** it states name, residency, sovereignty, endpoints, and packages, names the applicable regimes, and renders arrangement references as hyperlinks

#### Scenario: A region-dependent provider is honest about unknowns
- **WHEN** the page for a region-selectable provider (jurisdiction `unknown`) is generated
- **THEN** the residency is presented as region-dependent rather than as a resolved country

#### Scenario: Multi-language SDK keys render per language
- **WHEN** the page for a provider carrying `jvm` and `dotnet` keys (for example `aws_bedrock`) is generated
- **THEN** its packages list includes the JVM and .NET package names labeled by language alongside any Python and npm packages
