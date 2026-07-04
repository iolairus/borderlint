## Context

`kb-refresh.yml` runs Mondays 06:00 UTC: `scripts/kb_drift.py` fetches the litellm price list,
diffs its `litellm_provider` values against `providers.json`, and opens an issue for uncovered
provider names. The upstream file's **keys are model identifiers** (`deepseek/deepseek-r1`,
`anthropic.claude-…`) and are currently discarded — exactly the data a provenance coverage
check needs. Sovereignty lives in a separate bundled map (`sovereignty.json`: provider id →
bloc), so a provider can silently lack a sovereignty assignment, and the `updated` dates on the
bundled KBs are never read. The pure-function/offline-test
pattern in `kb_drift.py` (`coverage_gap`, `known_providers`, `upstream_providers`) is the
template every new check follows.

## Goals / Non-Goals

**Goals:**
- Provenance model-coverage drift, sovereignty completeness, and KB staleness in the same
  weekly report, from the same single upstream fetch.
- Every new check is a pure, offline-testable function; network stays in `main()` only.
- The weekly issue stays readable: aggregated families, capped sections, empty sections omitted.

**Non-Goals:**
- HF Hub top-N/trending sweep (separate upstream, auth, churn profile — future change).
- Auto-assigning any jurisdiction or bloc; scan-path changes of any kind.

## Decisions

### D1 — Reuse the litellm fetch; match its keys through the real matcher
**Decision:** The provenance check runs each upstream model key through `load_kb().match_model`
— the same code path the scanner uses (passthrough stripping, `.gguf` basenames, stoplist,
anchored prefixes). A key counts as covered if either the full key or its post-`/` remainder
matches (litellm keys are often provider-qualified: `bedrock/anthropic.claude-…`).
**Alternatives rejected:**
- *Reimplement matching in the script.* Rejected: two matchers drift; the check must answer
  "what would the scanner resolve", not "what does a lookalike regex resolve".
- *HF Hub API as the model upstream.* Rejected here: new upstream, auth and pagination, very
  different churn; deferred to its own change.

### D2 — Aggregate uncovered models by family stem, cap the section
**Decision:** Uncovered keys are grouped by a deterministic family stem (basename after the last
`/`, leading alphabetic run, lowercased — `grok-4-fast` → `grok`), reported as
`stem — N models, e.g. <example>`, sorted by count descending, capped at 50 rows with a
`… and N more families` line.
**Rationale:** The upstream has thousands of keys; a raw list is an unreadable issue nobody
triages. Families are the unit a human assigns a bloc to.
**Alternatives rejected:**
- *List every uncovered model ID.* Rejected: first run would produce a four-digit line count.
- *LLM-assisted clustering.* Rejected: deterministic core; a leading-alpha stem is 95% as good.

### D3 — Sovereignty completeness joins provider ids against the sovereignty map
**Decision:** A pure function takes the provider ids from `providers.json` and the bundled
sovereignty map from `sovereignty.json`, and reports ids with no mapping or a bloc outside the
sovereignty vocabulary. The vocabulary is imported from `borderlint.kb` — one source of truth;
the constant is module-private (`_SOVEREIGNTY_BLOCS`) and the private import is deliberate: a
dev script in the same repo does not justify new public API surface. The new-provider section's
prompt text now asks for endpoint(s), jurisdiction, **and sovereignty bloc**.
**Alternatives rejected:**
- *Audit a `sovereignty` field on provider entries.* Rejected: no such field exists — the bloc
  map is a separate file; auditing the entries would flag every provider on the first run.
- *Duplicate the bloc list in the script.* Rejected: vocabularies drift silently; the import is
  free (script already runs from the repo root with the package importable).

### D4 — Staleness from the `updated` fields, 90-day interval, all bundled KBs
**Decision:** The check scans every JSON file in `borderlint/data/` with a top-level `updated`
date (today: providers, provenance, sovereignty, regimes, arrangements) and warns when the date
is older than 90 days (file, date, age in days). Threshold is a script constant; the
reference date is a function parameter, keeping the check pure.
**Rationale:** 90 days matches a quarterly review cadence; scanning the data directory means a
future KB is covered the day it lands, without touching the script.
**Alternatives rejected:**
- *Enumerate the two dimension KBs only.* Rejected: auditing sovereignty completeness while
  ignoring `sovereignty.json`'s own staleness is incoherent; the enumeration also rots.

### D5 — Script emits the finished markdown issue body
**Decision:** `kb_drift.py` prints a sectioned markdown report (`### New providers`,
`### Uncovered model families`, `### Sovereignty gaps`, `### Stale knowledge bases`), empty
sections omitted, nothing printed when all are empty. The workflow's logic: output non-empty →
look for an open issue with the exact title `KB freshness: items to review`; **update its body
if found, create it otherwise** — staleness is a persistent condition, and create-always would
open a duplicate issue every Monday until a human bumps a date. The code fence is dropped (the
body is markdown now).
**Alternatives rejected:**
- *Script emits JSON; workflow assembles markdown in github-script.* Rejected: moves
  presentation into untested inline JS; the script's output is directly unit-testable.
- *Always create a new issue.* Rejected: weekly duplicates for any condition that persists;
  update-in-place keeps one live review item with the freshest state.

## Risks / Trade-offs

- **[First-run flood]** The initial provenance section will be long (every family without an
  entry). → Aggregation + cap keeps it readable; triage adds entries, passthrough orgs, or
  consciously accepts `unknown`.
- **[Provider-qualified prefixes]** litellm's `azure/`, `bedrock/` qualifiers are not hub orgs;
  stripping only the first segment may occasionally mask a real org. → Matching both the full
  key and the remainder bounds the error to false-covered, never false-alarm.
- **[Import coupling]** The script now imports `borderlint.kb`; a broken package import breaks
  the weekly job. → CI runs the same import on every push; the failure mode is loud, not silent.

## Migration Plan

1. Extend `scripts/kb_drift.py` (new pure functions + sectioned `main`).
2. Update `kb-refresh.yml` (body passthrough, new title).
3. Offline unit tests per pure function.
4. No data migration; rollback is a revert — the workflow shape is unchanged.

## Open Questions

- Should provider-qualified aggregator prefixes (`azure/`, `bedrock/`) become scanner
  passthroughs too? Out of scope here; candidate for a provenance follow-up.
