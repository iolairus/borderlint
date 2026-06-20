## 1. Arrangements list

- [ ] 1.1 Bundle an `arrangements.json` (GBA Standard Contract; PIPL cross-border transfer; GDPR Chapter V / SCCs) with name, URL, one-line summary, and applicability (jurisdictions + home regime)
- [ ] 1.2 Select the matching arrangement(s) per flagged flow from the list, replacing the single hardcoded GBA reference

## 2. Regime tags

- [ ] 2.1 Compute the implicated regime(s) for a flagged flow from the home regime + destination jurisdiction (PDPO / PIPL / GBA / GDPR)

## 3. Reporting

- [ ] 3.1 Render regime tags and arrangement references in text and JSON output for flagged flows (reference-only; no severity/exit change)

## 4. Tests

- [ ] 4.1 Tests: a GBA (`hk`↔`cn`) flow surfaces the GBA reference; an EU-destination flow surfaces the GDPR reference; a `pdpo`-home `cn` flow is tagged PDPO + PIPL; tags/references never change severity or exit code
