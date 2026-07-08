## Why

The artifact a DPO actually files is a transfer inventory — a RoPA appendix or PIA annex — and
borderlint stops short of it: the JSON has the flows but no audit framing (who scanned what,
when, under which policy version), so every filing means hand-assembling context around CI
output. Roadmap P1-3; all three axes plus developer orgs are now on findings.

## What Changes

- `--format evidence`: a self-contained markdown transfer-inventory document, four parts:
  1. **Audit envelope** — tool version, the three KB last-reviewed dates, scan timestamp (UTC),
     the scanned path's git commit when resolvable, the policy file's SHA-256 digest, declared
     classification and home location. Unresolvable fields say "unavailable", never vanish.
  2. **Transfer inventory** — per flow: provider and category, residency, sovereignty,
     provenance (with developer org and model identifier when known), applicable cross-border
     arrangement references, verdict with reasons, and code locations.
  3. **Waiver register** — every active waiver with location and justification, plus summary
     counts by verdict.
  4. **Regime-aligned annex** — when the declared `home_location` falls under a covered regime,
     an annex maps the inventory to that regime's documented filing expectations with
     citations: **PDPO/PCPD cross-border guidance (hk)**, **PIPL PIA and transfer-route
     framing incl. the GBA Standard Contract (cn, CN-GBA)**, **Macao PDPA with the Macao GBA SC
     variant (mo)**, and **PDPA s.26 / PDPC transfer documentation (sg)** ship first. Fields a static scan cannot know — purpose,
     data-subject scale, recipient legal entities — render as clearly marked org-supplied
     blanks, so the pack is a pre-filled template, not a false claim of completeness.
     Uncovered home locations get the generic pack with no fake annex. Annex expectations are
     bundled, human-curated data with the same advisory posture as arrangements: references,
     never adjudication; the annex states that data's own last-reviewed date.
- Artifact semantics: always exits 0, like the SBOM — the gating run sits beside it.
- Without a policy, the evidence pack renders in inventory framing (flows and axes, no
  verdicts), so it works before an org has written its first policy.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cli-and-reporting`: new requirements for the evidence format, its audit envelope, and its
  artifact exit semantics.

## Impact

- `borderlint/report.py` — `evidence()` renderer reusing the regimes/arrangements machinery.
- `borderlint/cli.py` — format choice, policy-path and scan-root threading for digest/commit.
- `borderlint/data/` — a small regime-expectations data file (citations + expected fields
  per covered regime), dated like every KB.
- `README.md`, `CAPABILITIES.md` (P1-3 row), tests.
- Deterministic core preserved: only timestamp and commit come from the environment; no
  network; git via local subprocess, absent gracefully.

## Non-goals

- No PDF/HTML rendering (markdown files cleanly and converts anywhere).
- No international-framework annexes in this change; the accepted phase-2 order (RoPA → NIST
  AI RMF → ISO/IEC 42001, 27701 riding on RoPA, COBIT deliberately excluded) is recorded in the
  roadmap.
- No new required CLI flags; no legal adjudication — arrangements stay reference links.
- No changes to any existing format; the JSON keeps its shape.
