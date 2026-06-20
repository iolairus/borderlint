## Context

borderlint reports text/JSON/Mermaid and fails on violations. For CI adoption it needs SARIF (the
code-scanning UI) and a reviewed suppression path (waivers) — both without weakening the
deny-by-default core.

## Goals / Non-Goals

**Goals:** SARIF emission; inline justified waivers that downgrade a finding to *waived* (reported,
not failed).

**Non-Goals:** policy-file/global waivers; hiding findings; waiver expiry or approval flows.

## Decisions

- **Inline `borderlint: allow <reason>` comment, justification required.** Alternative: a bare
  disable comment. Rejected — a residency waiver must be auditable; no reason ⇒ ignored, so a flow
  cannot be silently disabled.
- **Match a waiver on the flagged line or the line immediately above it.** Covers both
  `client(base_url=...)  # borderlint: allow …` and a preceding-line comment.
- **Waived findings are still emitted (text/JSON/SARIF), marked waived, and excluded from the exit
  code.** Alternative: drop them. Rejected — auditability; a reviewer must see what was waived and why.
- **SARIF is plain JSON, pinned to 2.1.0.** Zero-dep; emit the minimal valid structure
  (`runs` → `results` → `locations`) that GitHub code-scanning requires.

## Risks / Trade-offs

- A line-scoped waiver could be over-broad → acceptable; it is visible in the report and the diff.
- SARIF schema drift → pin to 2.1.0 and emit only the required fields.
