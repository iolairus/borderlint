## ADDED Requirements

### Requirement: Exclude oversized files

borderlint SHALL skip any file whose size exceeds a fixed threshold (5 MB) before reading it, so a
very large file is excluded from scanning rather than read into memory. Skipping an oversized file
MUST NOT fail the scan.

#### Scenario: An oversized file is skipped
- **WHEN** a file with a scanned extension exceeds the size threshold
- **THEN** it is excluded from detection and the scan continues without error

#### Scenario: A normal-sized file is still scanned
- **WHEN** a file is at or under the threshold
- **THEN** it is scanned as usual
