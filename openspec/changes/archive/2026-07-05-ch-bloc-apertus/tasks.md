## 1. Vocabulary

- [x] 1.1 Add `ch` to both frozensets in `borderlint/kb.py`, both `borderlint/policy.py` mirrors, the `report.py` display map ("Switzerland"), and the four "(use one of …)" error messages (D1, both vocabulary requirements)

## 2. Data

- [x] 2.1 `sovereignty.json`: `ch` source note (revised FADP 2023 + BÜPF); bump `updated` (D1)
- [x] 2.2 `provenance.json`: `apertus`→ch, `swiss-ai/`→ch; bump `updated` (D1)

## 3. Tests & docs

- [x] 3.1 Tests: `ch` accepted in policy blocks and user KBs; `swiss-ai/Apertus-70B-Instruct` and `apertus-70b-instruct` → ch; assert the rejection error text names `ch`; sources/display completeness auto-guards cover the rest
- [x] 3.2 README + CAPABILITIES bloc lists

## 4. Validation

- [x] 4.1 Full suite + `openspec validate ch-bloc-apertus --strict`
