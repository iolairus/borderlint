## 1. Waivers

- [ ] 1.1 Scan source for `borderlint: allow <reason>` comments (the flagged line or the line above), capturing the justification per line — one waiver covers every flow on that line
- [ ] 1.2 Change a residency or unknown-jurisdiction **failure** carrying a justified waiver into the `waived` state (excluded from the exit code, regardless of `fail_on`); never clear a provider-deny violation; ignore a waiver with no reason

## 2. SARIF

- [ ] 2.1 Add a `sarif` output format emitting SARIF 2.1.0 (`version`, `$schema`, `runs[].tool.driver.name` = `borderlint`, one `results` entry per finding with `ruleId`/`level`/`message`/`file:line` location); a waived result carries `level` `note` + a `suppressions` entry

## 3. Reporting

- [ ] 3.1 Render waived findings distinctly in text/JSON/SARIF and exclude them from the failure exit code

## 4. Tests

- [ ] 4.1 Tests: a justified inline waiver turns a residency failure into `waived` (exit 0); a waiver does NOT clear a provider-deny violation; an unjustified waiver is ignored; a line with two detections + one waiver waives both; SARIF output has `version` 2.1.0, `tool.driver.name` `borderlint`, one result per finding with a `file:line` location, and a waived result is `level` `note` with a `suppressions` entry
