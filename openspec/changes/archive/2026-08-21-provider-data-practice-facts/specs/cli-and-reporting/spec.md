# cli-and-reporting Delta

## ADDED Requirements

### Requirement: Evidence pack data-practices register
The evidence pack SHALL include a data-practices register listing, for every provider in
the flow inventory that has a curated entry, its training default, retention window,
subprocessor link, and enterprise-tier note, each with source citation and retrieval date.
Providers in the inventory without a curated entry SHALL appear in the register marked as
not curated. The register SHALL carry the advisory disclaimer and SHALL NOT affect verdicts
or summary counts.

#### Scenario: Curated providers are registered with citations
- **WHEN** the evidence pack renders a flow whose provider has a curated data-practices entry
- **THEN** the register lists that provider's facts with citations and retrieval dates

#### Scenario: Uncurated providers stay visible
- **WHEN** the evidence pack renders a flow whose provider has no curated entry
- **THEN** the register marks that provider as not curated rather than omitting it

#### Scenario: The register leaves verdicts untouched
- **WHEN** the same tree and policy are scanned with and without the data-practices knowledge base present
- **THEN** both runs produce identical verdicts, summary counts, and exit codes
