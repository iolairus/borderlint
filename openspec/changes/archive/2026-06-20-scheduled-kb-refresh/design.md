## Context

The bundled provider KB is curated data. There is no canonical "provider → endpoint → jurisdiction"
registry, but maintained upstreams (e.g. litellm's model/provider data) list providers and can
reveal ones borderlint doesn't yet cover. Jurisdiction and endpoint-host assignment remains human
judgment. This change adds a discovery loop, not an auto-updater.

## Goals / Non-Goals

**Goals:** detect provider-coverage drift weekly and surface it for review; stamp KB provenance;
keep scans offline and deterministic.

**Non-Goals:** auto-assigning jurisdictions/hosts; runtime registry fetch; permanent upstream lock-in.

## Decisions

- **Discover, then a human assigns.** Alternative: auto-pull endpoints + guess jurisdictions.
  Rejected — host/jurisdiction mapping is judgment; a wrong auto-assignment silently changes CI
  verdicts. The job opens a PR/issue listing uncovered providers; a person curates.
- **Scheduled GitHub Action (weekly cron), not a runtime fetch.** Scans use the pinned bundled KB
  with no network — freshness arrives as a stream of small reviewed PRs, keeping CI reproducible.
- **Upstream is a maintained provider list (litellm to start).** Alternative: scrape provider docs.
  Rejected — not machine-readable. The script isolates the upstream so it can be swapped.

## Risks / Trade-offs

- Upstream format/availability changes → the script is isolated and dev/CI-only; a failure opens no
  PR and never affects scans.
- Discovery is coarse (provider names, not always endpoint hosts) → acceptable; it flags *what* to
  curate, the human supplies the hosts and jurisdiction.
