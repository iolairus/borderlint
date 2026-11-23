## ADDED Requirements

### Requirement: HKMA profile follows current superseding guidance

The HKMA profile SHALL cite the 15 October 2026 Supervisory Guidance for Responsible Adoption of
Artificial Intelligence rather than the superseded 2019 High-level Principles. Every handled class
SHALL start with only `hk`; the former `CN-GBA` non-PII seed and its incorrect GBA Standard
Contract rationale SHALL be removed. Notes SHALL describe onshore defaults as conservative,
operator-editable product policy rather than a regulatory localisation mandate, and SHALL NOT use
the obsolete Sandbox rationale or the Korean `PIPC` regulator name.

#### Scenario: HKMA seeds only Hong Kong after review
- **WHEN** init uses the `hkma` profile for non-PII, employee-PII, or customer-PII data
- **THEN** each class starts with only `hk` unless the operator deliberately adds destinations

#### Scenario: Current guidance and limits are visible
- **WHEN** the HKMA profile is loaded or rendered
- **THEN** it cites the 2026 ART guidance and explains that the guidance does not itself mandate
  onshore processing

### Requirement: MAS profile records guidance transition without changing seeds

The MAS profile SHALL retain its 5 December 2024 information-paper citation and Singapore-only
defaults while noting the final AI Risk Management Guidelines issued 7 October 2026, effective
7 October 2027, with Sections 5–6 to be met by 7 October 2028. Notes SHALL describe the seeds as
product policy and SHALL NOT assert an onshore-only regulatory requirement or imply that the future
Guidelines are already effective.

#### Scenario: MAS defaults remain stable during transition
- **WHEN** init uses the `mas` profile
- **THEN** all handled classes still start with only `sg`, and the provenance note identifies both
  the current 2024 paper and the 2026 Guidelines' future dates
