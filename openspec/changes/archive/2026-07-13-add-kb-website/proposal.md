# add-kb-website

## Why

The people who search for "is DeepSeek PIPL-compliant" or "Bedrock data residency Hong Kong" are privacy and compliance practitioners — and nothing in this project is visible where they search. The knowledge base already answers those questions (90 providers, ~211 model-family patterns, regime and arrangement references, all hand-curated with review dates) but only as JSON inside a Python package. Publishing it as a browsable site turns the KB into the project's discovery surface at zero ongoing cost.

## What Changes

- New dev-side generator `scripts/kb_site.py` (stdlib-only) that renders the bundled KB (`borderlint/data/*.json`) into a static site: an index, one page per provider, and one page per model developer organisation (aggregated from the provenance patterns).
- Provider pages state: name, category where recorded, residency jurisdiction(s) including region-dependent resolution notes, sovereignty bloc (with region-level ring-fenced-subsidiary overrides), known endpoint hosts, SDK/npm package names, the applicable regime names, and arrangement references as hyperlinks.
- Model-developer pages state: the organisation, its model-id patterns, and their provenance bloc(s).
- Every page carries a unique title and meta description naming the provider/organisation and governance axis (long-tail search), the KB last-reviewed dates, a link back to the repo, and the install one-liner.
- Index page leads with the flagship three-axis example (Bedrock `ap-east-1` serving DeepSeek-R1 → residency `hk`, sovereignty `us`, provenance `cn`).
- New `.github/workflows/pages.yml`: rebuilds and deploys to GitHub Pages on pushes to `main` touching `borderlint/data/**` or the generator, on release, and manually.
- Generator smoke test in the existing test suite.

## Capabilities

### New Capabilities

- `kb-website`: generation and publication of a browsable static site from the bundled knowledge base.

### Modified Capabilities

(none — CLI behavior, KB content, and the shipped package are untouched)

## Impact

- New: `scripts/kb_site.py`, `.github/workflows/pages.yml`, `tests` addition; README link to the site.
- No runtime impact: the pip-installed package gains no files, dependencies, or behavior. Zero-runtime-dependency constraint untouched (the generator itself is also stdlib-only, matching `scripts/kb_drift.py`).
- Requires GitHub Pages enabled for the repository (one-time setting; workflow uses the standard Pages actions).

## Non-goals

- No hosted scanning, search box, or any dynamic behavior — plain static pages, no JavaScript.
- No separate content beyond what the KB already contains — the site is a projection of the JSON, never hand-edited (corrections go to the KB via the existing contribution flow).
- No custom domain, analytics, or theming beyond minimal shared CSS.
- No per-model pages for all 211 patterns — one page per developer organisation; thin near-duplicate pages hurt search and readers alike.
