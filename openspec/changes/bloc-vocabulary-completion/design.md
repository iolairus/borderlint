## Context

Both dimensions share one bloc vocabulary (`_SOVEREIGNTY_BLOCS` in `kb.py:85`, provenance =
same minus `local`, `kb.py:111`), mirrored in `policy.py` for load-time validation and given
display names in `report.py`'s `SOVEREIGNTY` map (shared by `sov()` for both dimensions). The
provenance map deliberately omitted Falcon, EXAONE, Solar, and SEA-LION because their
developers' blocs did not exist (`ae`, `kr`, `sg`); the kb-freshness report now nags about them
weekly. No bundled provider is headquartered in the five new blocs (verified against all 84
provider ids), so the sovereignty provider map needs no edits.

## Goals / Non-Goals

**Goals:**
- Five new tokens valid everywhere a bloc is accepted: policy blocks, user KBs, drift audit.
- Bundled provenance entries for the deferred families, anchored per the established rules.
- Legal-source documentation per new sovereignty bloc, same style as the existing nine.

**Non-Goals:**
- New providers or provider re-mappings; resolution-mechanic changes; blocs beyond these five.

## Decisions

### D1 — Extend both vocabularies with the same five tokens
**Decision:** `jp`, `kr`, `sg`, `au`, `ae` join both frozensets (and the `policy.py` mirrors and
the `report.py` display map). `local` remains sovereignty-only.
**Rationale:** One vocabulary, one display map is the shipped invariant; a bloc that exists for
weights but not for sovereignty (or vice versa) would break the shared `sov()` rendering and
the shared mental model.
**Alternatives rejected:**
- *Add only the blocs with bundled families today (`ae`, `kr`, `sg`, `jp`).* Rejected: `au` is
  a meaningful compelled-disclosure regime (TOLA 2018) that user KBs and future provider
  entries need; a vocabulary token costs one word, a second vocabulary-extension change costs
  a full pipeline pass.
- *Free-form bloc tokens (drop validation).* Rejected: validation is what catches `overseas`
  and `mars` typos at load time; the closed vocabulary is a feature.

### D2 — Family entries stay anchored; org prefixes carry the ambiguous names
**Decision:** Distinctive stems get bare-prefix entries (`exaone`, `plamo`, `sarashina`,
`elyza`, `sea-lion`, `hyperclova`); collision-prone stems get pinned forms (`falcon-`,
`falcon2`, `falcon3`, `solar-`); families whose hub ids do not start with the family name are
carried by their org prefix instead (`tiiuae/`, `upstage/`, `lgai-exaone/`,
`naver-hyperclovax/`, `aisingapore/`, `sbintuitions/`, `pfnet/`, `tokyotech-llm/`, `rinna/`,
`elyza/`) — e.g. `tokyotech-llm/Llama-3.1-Swallow-8B` resolves via the org because the
basename starts with the base-family name, not "swallow".
**Rationale:** Same anchoring discipline that keeps `llama_index` out of the match set; org
prefixes are unambiguous and survive family renames.
**Alternatives rejected:**
- *Bare `falcon` / `solar` stems.* Rejected: ordinary words; `solarwinds`-style identifiers and
  `falcon` tooling (CrowdStrike Falcon SDKs) would match.
- *Passthrough-stripping the developer orgs.* Rejected: passthrough is for quantizer/conversion
  hubs that carry no provenance; these orgs ARE the provenance signal.

### D3 — Sources, not mappings, in sovereignty.json
**Decision:** Each new bloc gets a `sources` entry naming its compelled-disclosure regime
(jp: APPI + criminal-procedure access; kr: PIPA + Communications Privacy Act; sg: PDPA +
Criminal Procedure Code; au: TOLA 2018 + Privacy Act 1988; ae: Federal Decree-Law 45/2021 +
state-security access). The provider map is untouched.
**Rationale:** The sources block is the map's documentation contract — every bloc the
vocabulary admits should say what legal regime it stands for, even before a provider uses it.
**Alternatives rejected:**
- *Add sources only when a provider first uses the bloc.* Rejected: the documentation contract
  would lag the vocabulary; a user KB can emit the bloc the day it ships, and the report reader
  deserves the citation then, not after bundled curation catches up.
- *Also update the provenance data's deferred-families note lazily.* Rejected: shipping data
  whose own note declares the new entries absent is a self-contradiction; the note is corrected
  in the same change.

## Risks / Trade-offs

- **[Fine-tune ids that embed family names]** e.g. `elyza` is itself a Llama fine-tune shop;
  its bloc is the fine-tuner's, which is the correct answer under the shipped base-family rule
  read at the derivative level — the map records who produced the weights being pulled.
  → Documented per-entry `org`; user KBs override when a stricter lineage view is wanted.
- **[Display-name politics]** `kr` renders "South Korea", `ae` "UAE" — plain English short
  names, matching the existing JURIS rendering of the same country codes so residency and
  sovereignty never label one code two ways.

## Migration Plan

1. Extend the two frozensets, the two `policy.py` mirrors, and the `report.py` display map.
2. Add `sources` entries (sovereignty.json) and pattern/org entries (provenance.json); bump
   both `updated` dates.
3. Tests: new tokens accepted in policy + user KB; one resolution test per new bloc; drift
   `model_coverage_gap` no longer reports the covered families.
4. Docs. No data migration; rollback is a revert.

## Open Questions

None.
