# provider-data-practices Delta

## ADDED Requirements

### Requirement: Xiaomi MiMo curated facts
The bundled data-practice knowledge base SHALL carry a curated entry for `xiaomi_mimo` stating
the training default (`no`), the retention posture, and the storage-region note, each fact
carrying its source citation; undocumented facts (subprocessors) SHALL be recorded as null.

#### Scenario: Facts render with citations
- **WHEN** the evidence pack or KB website renders data practices for `xiaomi_mimo`
- **THEN** the training default cites the privacy policy statement that submitted content will
  not be used for model training, and the storage note cites the service agreement's EU +
  Singapore storage disclosure
