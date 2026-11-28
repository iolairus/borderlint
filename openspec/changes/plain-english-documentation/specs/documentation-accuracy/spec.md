# documentation-accuracy Delta

## ADDED Requirements

### Requirement: Documentation uses direct, reader-focused language

Current user, contributor, and integration documentation SHALL use active verbs when the actor is
known and imperative verbs for instructions. Narrative prose MUST NOT use “gate” as a verb,
“surface” as a verb, “seat” for a configured home location, “scaffold” as a verb, “eval-set” for
the policy, or “orthogonal axes” for the three checks. It SHALL use the corresponding direct terms:
“fail” or “block,” “show,” “report,” or “link to,” “home location,” “create” or “generate,”
“policy,” and “separate checks.” Exact commands, policy fields, output values, and necessary
technical or legal terms MUST remain unchanged.

#### Scenario: Reader learns how policy enforcement works

- **WHEN** the reader encounters a description of a policy violation during a policy-enforcement
  scan that uses a gating output format
- **THEN** the documentation says directly that borderlint returns a non-zero exit code or fails
  the build, rather than saying that the command “gates” CI

#### Scenario: Reader chooses an export format

- **WHEN** the reader encounters documentation for SBOM, evidence, HTML, badge, or Suricata exports
- **THEN** the documentation states that these exports return zero rather than implying that every
  policy violation fails the build

#### Scenario: Documentation describes product behavior

- **WHEN** a reviewer searches narrative prose for the unclear terms named in this requirement
- **THEN** each occurrence is replaced with its direct equivalent or is a literal command, policy
  field, output value, or proper name whose spelling must remain unchanged

### Requirement: Documentation is structured around reader tasks

The README SHALL place its quick start before detailed capability and reference sections. The quick
start SHALL show, in order, installation, an inventory scan, policy creation, and a policy-enforcement
scan, and SHALL explain the resulting CI behavior. Ordered installation and contribution procedures
SHALL use numbered steps with imperative verbs. Each current document SHALL explain residency,
sovereignty, provenance, software bill of materials (SBOM), and Model Context Protocol (MCP) at its
first use of those concepts, or link directly to that explanation in the same document.

#### Scenario: New user follows the README

- **WHEN** a reviewer inspects the README quick start
- **THEN** it presents `pip install borderlint`, `borderlint scan .`, `borderlint init .`, and a
  policy-enforcement scan in that order before the detailed capability sections

#### Scenario: User follows integration instructions

- **WHEN** a reviewer inspects the Claude Code or Cursor instructions
- **THEN** numbered, imperative steps cover installation, the pre-addition scan, the accepted-flow
  waiver, and the SBOM-diff enforcement behavior

#### Scenario: Reader encounters a complex concept

- **WHEN** a reviewer locates the first use of residency, sovereignty, provenance, SBOM, or MCP in
  an included document
- **THEN** the document provides a plain-language explanation at that point or a direct link to an
  explanation in the same document

### Requirement: Clarity edits preserve meaning and consistent terminology

Clarity edits SHALL preserve all material capabilities, defaults, limitations, citations, and
safeguards. Current documentation SHALL use consistent terms for the same action or concept and
MUST NOT remove or weaken a limitation to make prose shorter.

#### Scenario: Reviewer compares old and new technical content

- **WHEN** a reviewer checks an edited file against its preservation checklist and current behavior
- **THEN** commands, defaults, exit codes, policy semantics, static-analysis limits, legal
  disclaimers, citations, and integration safeguards are marked verified with no material omission

#### Scenario: Reader moves between documentation surfaces

- **WHEN** a reviewer compares terminology in the README, capability, contributor, and integration
  documentation
- **THEN** core concepts and actions use the direct terms required by this specification, with no
  contradictory instructions

#### Scenario: Rewrite removes repeated detail

- **WHEN** repeated material is shortened or replaced with a link
- **THEN** the destination retains the material information and the link leads to the relevant
  current documentation
