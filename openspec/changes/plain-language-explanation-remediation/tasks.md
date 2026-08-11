## 1. CLI flag

- [x] 1.1 Add `--explain` argument to `scan` parser in `borderlint/cli.py`
- [x] 1.2 Pass `explain` flag through to renderers

## 2. Explanation generation

- [x] 2.1 Add `explain_reason()` helper in `borderlint/report.py` mapping reason codes to templates
- [x] 2.2 Extend `text()` renderer to include explanation lines when explain is True
- [x] 2.3 Extend `as_json()` to include `explanation` field per finding when explain is True

## 3. Tests

- [x] 3.1 Add end-to-end test that `--explain` reaches the renderer through the CLI
- [x] 3.2 Add unit test for explanation text for residency violation
- [x] 3.3 Add unit test for JSON output with explanation field
