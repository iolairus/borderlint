## 1. CLI scaffolding

- [x] 1.1 Add `init` subparser in `cli.py` beside `scan`/`diff` (lines 47–57) with `--home`, `--classes`, `--output` (default `./residency.json`), and `--force` options
- [x] 1.2 Add `init` dispatch branch in the `if`-ladder (lines 64–66) calling a new `_run_init(a)` handler
- [x] 1.3 Verify `borderlint --help` lists `init` alongside `scan` and `diff`

## 2. Wizard core (`borderlint/init.py`)

- [x] 2.1 Create `borderlint/init.py` with an `run_init(args, input_fn=input)` entry point that accepts an injectable input source for testability
- [x] 2.2 Implement home-base interview: prompt from supported seats (`hk`, `mo`, `CN-GBA`, `jp`, `kr`, `sg`, `au`, `uk`, `eu`, `my`), default `hk`, re-prompt on invalid token (reuse `_valid_home` vocabulary)
- [x] 2.3 Implement data-class interview: prompt for `non-pii`/`employee-pii`/`customer-pii` (+ extras), default to all three on empty input
- [x] 2.4 Run `scan(path, kb)` in inventory mode and collect the set of observed resolved jurisdictions
- [x] 2.5 Implement per-jurisdiction walk: for each observed jurisdiction × each handled class, prompt keep/drop; pre-seed the home base into every class allow-list
- [x] 2.6 Build the policy dict: `home_location`, `classifications` map, `on_unknown: "warn"`, `fail_on: ["residency","denied_provider","sovereignty"]`

## 3. Output and overwrite guard

- [x] 3.1 Implement overwrite protection: if output exists and `--force` is not set, print error to stderr and exit 2; `--force` overwrites
- [x] 3.2 Write the policy JSON to the resolved output path (default `./residency.json`, overridable via `-o/--output`)
- [x] 3.3 Implement non-interactive path: when both `--home` and `--classes` are given, skip prompts, seed home into every class, add every observed jurisdiction to every class, and write directly

## 4. Tests

- [x] 4.1 Add a test that monkeypatches `stdin` (via injected `input_fn`) and asserts the written `residency.json` contains the expected `home_location` and `classifications`
- [x] 4.2 Add a test for the overwrite-refusal case: existing file + no `--force` exits non-zero and leaves the file unchanged; with `--force` it is overwritten
- [x] 4.3 Add a test for non-interactive mode (`--home` + `--classes`) producing a loadable policy with no prompts
- [x] 4.4 Run the full suite (`pytest`) and confirm green

## 5. Docs

- [x] 5.1 Document `borderlint init` (interactive + `--home`/`--classes`/`--force`) in `README.md`
