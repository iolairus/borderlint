## 1. Waivers

- [ ] 1.1 Scan source for `borderlint: allow <reason>` comments (the flagged line or the line above), mapping `file:line` → justification
- [ ] 1.2 Mark a finding whose line carries a justified waiver as `waived` (not a violation); ignore a waiver with no reason

## 2. SARIF

- [ ] 2.1 Add a `sarif` output format emitting minimal valid SARIF 2.1.0 (`runs` → `results` → `locations`, with rule id, level, message)

## 3. Reporting

- [ ] 3.1 Render waived findings distinctly in text/JSON/SARIF and exclude them from the failure exit code

## 4. Tests

- [ ] 4.1 Tests: a justified inline waiver downgrades a violation to `waived` (exit 0); an unjustified waiver does not; SARIF output is valid JSON with one result per finding and a `file:line` location; waived findings appear but never fail
