## 1. Per-jurisdiction Mermaid nodes

- [x] 1.1 In `report.mermaid()`, emit a distinct node per (provider, jurisdiction) with id `<provider>__<juris>` (the `juris` segment with `-`→`_`), labelled by the provider name, and an `app -->` edge to each
- [x] 1.2 Title each jurisdiction subgraph by its code (`j`), not the `juris(j)` display name; leave `juris()` untouched for the other output formats

## 2. Tests

- [x] 2.1 Tests: a finding set where one provider resolves to two jurisdictions yields a distinct node under each zone (two nodes, two `app -->` edges); subgraph titles are the codes (`sg`, `fr`, `cn`); a single-jurisdiction provider still renders one node
