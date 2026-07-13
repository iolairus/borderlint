# add-html-report-format

## Why

Scan results today are consumable only by people who live in terminals or CI (text/JSON/SARIF) — but the audience that must act on a cross-border finding is a privacy or compliance reviewer who works in documents. Evidence that the sign-off audience cannot open never reaches the review; a single shareable file closes the gap between the engineer who runs the scan and the reviewer who adjudicates the flow.

## What Changes

- New `--format html` on `borderlint scan`: renders the scan result as **one self-contained HTML file** written to stdout (redirect to save), suitable for email/attachment and offline/air-gapped viewing.
- Content: scan metadata header (scanned path, git commit, policy SHA-256 when a policy is supplied, KB last-reviewed dates — reusing the existing evidence envelope helpers), findings grouped by jurisdiction with residency / sovereignty / provenance shown side by side per flow, severity chips (fail / warn / waived / ok), regime tags and cross-border arrangement references (as hyperlinks, matching other formats), and a waiver register section when waivers exist.
- Strictly self-contained: inline CSS only, no external scripts, stylesheets, fonts, or images — no network request of any kind when opened.
- Export semantics identical to `sbom`/`evidence`: an artifact, not a gate — **exits 0** regardless of findings (config errors still exit 2).
- Works in both inventory mode (no policy: flows + jurisdictions listed, no severities) and policy mode.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `cli-and-reporting`: the accepted `--format` set gains `html`; requirements added for the HTML document's required sections, self-containment, and export (non-gating) exit-code semantics.

## Impact

- `borderlint/report.py`: new `html(findings, kb, policy=...)` renderer following the existing one-function-per-format pattern; reuses envelope/regime helpers already used by `evidence`.
- `borderlint/cli.py`: `html` added to the `--format` choices and the renderers dict; added to the export set that forces exit 0.
- `tests/test_borderlint.py`: renderer tests (substring asserts per house style) + CLI exit-code test.
- `README.md` / `CAPABILITIES.md`: document the new format.
- No new dependencies (stdlib string rendering; `html.escape` for content safety). No changes to detection, policy evaluation, or other formats.

## Non-goals

- **Not an evidence/filing format.** The evidence pack deliberately rejected HTML for regulatory filing (`2026-07-08-evidence-pack/design.md`) — markdown remains the filing artifact. This format is a human-readable report for review conversations; that decision is not reopened.
- No charts/JS interactivity, no mermaid.js embedding, no PDF export.
- No multi-scan aggregation or historical comparison (SBOM `diff` covers deltas).
- No styling configurability (themes, logos).
