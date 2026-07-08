## MODIFIED Requirements

### Requirement: Exclude non-source locations
The system SHALL exclude version-control, dependency, and build directories from scanning so that
vendored or generated code does not produce detections: name-based exclusions (`.git`,
`node_modules`, `__pycache__`, `.venv`, `venv`, `site-packages`, cache and build output) and
marker-based exclusions — any directory containing a `pyvenv.cfg` file or a `conda-meta`
subdirectory SHALL be skipped as a whole subtree, regardless of the directory's name.
Application code outside such directories SHALL be scanned as usual.

#### Scenario: Match inside an excluded directory
- **WHEN** a provider endpoint host appears in an excluded directory (for example `node_modules`)
- **THEN** no detection is recorded for that location

#### Scenario: A nonstandard-named virtualenv is excluded by its marker
- **WHEN** the scanned path contains `.venv-cuda/` with a `pyvenv.cfg` and site-packages full of AI libraries
- **THEN** no detections are recorded from inside it

#### Scenario: A conda environment is excluded
- **WHEN** the scanned path contains an environment directory with a `conda-meta` subdirectory
- **THEN** no detections are recorded from inside it

#### Scenario: A bare site-packages directory is excluded by name
- **WHEN** the scanned path contains a `site-packages/` directory with no environment marker
- **THEN** no detections are recorded from inside it

#### Scenario: Application code beside an environment is still scanned
- **WHEN** the scanned path contains both an environment directory and application source files
- **THEN** the application files' flows are detected as usual
