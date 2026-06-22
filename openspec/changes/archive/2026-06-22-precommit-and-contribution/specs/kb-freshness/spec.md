## ADDED Requirements

### Requirement: Community contribution workflow

The project SHALL document how to contribute a provider to the bundled knowledge base, covering
the KB entry schema and the rule that jurisdictions are human-assigned via pull request. The
documentation MUST stay consistent with the existing "Human-assigned jurisdictions" requirement
(no auto-merge from an upstream feed).

#### Scenario: KB entry schema is documented
- **WHEN** a contributor consults the contribution guide
- **THEN** it documents each KB entry field (`id`, `name`, `sdks`, `npm`, `endpoints`,
  `jurisdiction`, `region_scheme`, `endpoint_jurisdictions`), marks which are required versus
  optional, and lists the valid jurisdiction tokens (ccTLD/ISO codes plus `CN-GBA`, `GBA`,
  `local`, `unknown`)

#### Scenario: Jurisdictions stay human-assigned
- **WHEN** a new provider is contributed via pull request
- **THEN** the guide requires its jurisdiction to be assigned by a human reviewer, never
  auto-merged from the drift check's output
