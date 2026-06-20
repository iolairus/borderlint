## 1. Arrangements list

- [ ] 1.1 Bundle `arrangements.json` (GBA Standard Contract; PIPL cross-border transfer; GDPR Chapter V / SCCs) with name, URL, one-line summary, and applicability
- [ ] 1.2 Select the matching arrangement(s) per flagged flow — GBA ⇐ `hk`↔`CN-GBA`; PIPL ⇐ `cn` destination (or `pipl` home → outside); GDPR ⇐ EU/EEA destination — replacing the single hardcoded GBA reference (which currently also fires on plain `cn`)

## 2. Regime tags

- [ ] 2.1 Compute the implicated regime tag(s) from {PDPO, PIPL} via the home regime + destination (GDPR stays a reference, not a tag)

## 3. Reporting

- [ ] 3.1 Render regime tags + arrangement references in text and JSON for flagged flows; do NOT add them to SARIF results or change SARIF levels

## 4. Tests

- [ ] 4.1 Tests: `hk`↔`CN-GBA` → GBA ref (NOT plain `cn`); `cn` → PIPL ref; an EU member code → GDPR ref; a `pdpo`-home `cn` flow tagged PDPO + PIPL; tags/references never change severity, exit code, or SARIF results/levels
