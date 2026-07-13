# add-kb-website — tasks

## 1. Generator

- [x] 1.1 `scripts/kb_site.py`: load the KB JSONs (providers, sovereignty, provenance, regimes, arrangements), aggregate provenance patterns by developer organisation (normalised unique slugs, deterministic collision suffix) — spec: Site generation, Model-developer page content; design decision 3
- [x] 1.2 Page templates (shared inline CSS, escaped content): provider page with name / category-when-recorded / residency (region-dependent note for `unknown`) / sovereignty incl. region-level overrides / endpoints / packages + regime names and arrangement hyperlinks from the KB mappings — spec: Provider page content
- [x] 1.3 Model-developer pages (org, patterns, provenance blocs) and index with the flagship Bedrock/DeepSeek-R1 example and links to all pages — spec: Model-developer page content, Site generation
- [x] 1.4 Per-page unique `<title>`/meta description naming subject + governance dimension; KB review dates, repo link, and install one-liner on every page — spec: Discoverability metadata
- [x] 1.5 Add `site/` to `.gitignore` — design decision 2

## 2. Publication

- [x] 2.1 `.github/workflows/pages.yml`: build via `python scripts/kb_site.py`, deploy with `actions/upload-pages-artifact` + `actions/deploy-pages`; triggers: push to `main` (paths `borderlint/data/**`, `scripts/kb_site.py`), `release: published`, `workflow_dispatch` — spec: Automated publication
- [x] 2.2 Enable GitHub Pages for the repo (source: GitHub Actions) via `gh api` — design risk 1

## 3. Tests

- [x] 3.1 Smoke test: generator runs against the bundled KB, emits index + one page per provider + one page per developer org; slugs unique; unknown-jurisdiction provider page says region-dependent; spot-check title/meta uniqueness on two pages — spec: all
- [x] 3.2 Package-unchanged check: site tooling not in the wheel (assert generator path outside `borderlint/`) — spec: No runtime impact

## 4. Docs

- [x] 4.1 README: link the browsable KB site from the "Keeping the KB fresh" section — proposal Impact (doc-only)
