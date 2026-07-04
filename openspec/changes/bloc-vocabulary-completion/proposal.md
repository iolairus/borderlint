## Why

The sovereignty and provenance vocabularies stop at nine blocs, so model families from Japan,
South Korea, Singapore, Australia, and the UAE cannot be expressed at all — Falcon (TII),
EXAONE (LG), Solar (Upstage), and SEA-LION (AI Singapore) were deliberately left out of the
provenance map for exactly this reason, and freshness issue #39 now surfaces them as uncovered
families every week. A user KB cannot even override them: the tokens are rejected at load time.

## What Changes

- Both bloc vocabularies gain `jp`, `kr`, `sg`, `au`, `ae` (sovereignty and provenance; `local`
  stays sovereignty-only). Policy validation, user-KB validation, and report display names
  accept and render the new blocs.
- `sovereignty.json` gains a legal-source note per new bloc (APPI; PIPA; PDPA/CPC; TOLA 2018;
  UAE PDPL) — no provider re-mappings: no bundled provider is headquartered in these blocs.
- `provenance.json` gains anchored entries for the deferred families and their hub orgs:
  Falcon/TII → `ae`; EXAONE/LG, Solar/Upstage, HyperCLOVA/Naver → `kr`; PLaMo/Preferred
  Networks, Sarashina/SoftBank, ELYZA, Swallow/Tokyo Tech (org-anchored) → `jp`;
  SEA-LION/AI Singapore → `sg`. `au` ships as vocabulary only — no notable open-weights family
  today; the token exists for user KBs and future entries.
- Docs (README, CAPABILITIES) list the extended vocabularies.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `sovereignty`: the bloc vocabulary requirement extends to the five new blocs.
- `model-provenance`: the bloc vocabulary requirement extends identically (still minus `local`);
  the bundled map covers the previously deferred families.

## Impact

- `borderlint/kb.py`, `borderlint/policy.py` — the two vocabulary frozensets and their mirrors.
- `borderlint/report.py` — display names for the five blocs.
- `borderlint/data/sovereignty.json` (sources), `borderlint/data/provenance.json` (family and
  org patterns), both with `updated` bumped.
- `tests/` — vocabulary acceptance, family resolution per new bloc.
- Freshness issue #39 shrinks: the deferred families leave the uncovered list on the next run.

## Non-goals

- No new providers: no bundled provider is homed in these blocs, so `providers.json` and the
  sovereignty provider map are untouched.
- No exhaustive per-country expansion beyond these five (the drift check surfaces the next
  candidates when they matter).
- No change to resolution mechanics — patterns stay anchored, longest-match, user-first.
