## Context

borderlint resolves endpoints via the bundled KB and supports `--providers`, but that file currently
replaces the bundled KB and requires full provider entries. Internal multi-region routing governance
needs additive, lightweight host→jurisdiction definitions.

## Goals / Non-Goals

**Goals:** additive merge of a user KB; a simple endpoints map; the wrong-endpoint guard via the
existing policy.

**Non-Goals:** refreshing the public provider registry; new flags or policy mechanisms.

## Decisions

- **Merge the user KB onto the bundled one, user precedence on conflict.** Alternative: keep replace
  and make users re-list every public provider. Rejected — error-prone and silently drops coverage.
- **Support a flat `endpoints: { host: jurisdiction }` map.** Alternative: require full provider
  objects for each internal host. Rejected — too heavy for "these hosts are in these jurisdictions."
- **Reuse `--providers`; no new flag.** The file may contain `providers` and/or `endpoints`; both
  merge additively onto the bundled KB.

## Risks / Trade-offs

- A user `endpoints` entry that overrides a bundled host masks the bundled jurisdiction — this is the
  intended override semantics (your network knows best); document it.
- Longest-match endpoint resolution still applies, so a specific internal host wins over a shorter
  bundled substring.
