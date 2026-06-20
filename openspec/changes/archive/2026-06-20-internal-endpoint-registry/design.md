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
- **The wrong-endpoint guard reuses existing policy.** An endpoints-resolved jurisdiction outside the
  active allow-list is caught by `residency-policy`'s existing deny-by-default evaluation — this
  change adds no new policy mechanism.
- **Endpoints-map values are validated against the recognised token set.** An unrecognised token is
  an error, not a silent pass — a typo'd jurisdiction must not quietly change a CI verdict.

## Risks / Trade-offs

- A user `endpoints` entry that overrides a bundled host masks the bundled jurisdiction — this is the
  intended override semantics (your network knows best); document it.
- User-supplied hosts are resolved in preference to bundled hosts; longest-match only breaks ties
  within a single source (user, or bundled).
