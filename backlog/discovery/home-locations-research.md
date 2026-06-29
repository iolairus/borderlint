---
type: discovery
created: 2026-06-29
tags: [borderlint, home-locations, data-residency, legal-research]
---

# Home-locations research — regimes & cross-border references

**Purpose.** Verified, cited inputs for wiring ten new `home_location` values into borderlint's
context layer: `jp, sg, my, id, uk(=gb), eu, ae, in, kr, au`. Feeds change 3
(`/opsx:propose home-locations-apec-emea`). This is the accuracy gate — change 1
(`home-jurisdiction-engine`) already shipped the data-driven engine; this doc supplies the data.

**Framing.** borderlint **never adjudicates** whether a transfer is lawful — it only surfaces a
*reference link* to the relevant regime + cross-border mechanism for a flagged flow. So a mechanism
that is enacted-but-not-yet-operational (IN, AE, ID) is still a valid reference; the "Status" column
records the nuance, it does not block inclusion.

**Confidence.** Regime *names* are all **high** (well-established statutes). Cross-border *mechanism*
detail is high except where a column says otherwise.

## Findings

| Home | Regime tag | Cross-border mechanism (reference) | Status (as of 2026-06) | Conf. |
|---|---|---|---|---|
| `jp` | APPI | Art. 28 — prior consent, **or** a PPC-designated equivalent country (EU, UK), **or** recipient with equivalent safeguards / APEC CBPR | In force | high |
| `kr` | PIPA | Art. 28-8 — consent, law/treaty, contract-necessity with notice, **or** PIPC-recognised certification | In force (2023 amendment) | high |
| `sg` | PDPA (SG) | s.26 Transfer Limitation Obligation + PDP Regs 2021 — comparable standard via enforceable contract / BCR / certification (APEC CBPR) | In force | high |
| `au` | Privacy Act / APPs | APP 8 + s.16C — accountability; exempt where recipient bound by **substantially similar** law + enforceable mechanism (OAIC keeps **no** country list) | In force | high |
| `uk` (=`gb`) | UK GDPR / DPA 2018 | Chapter V / Art. 46 — adequacy regulations **or** appropriate safeguards: **UK IDTA** or the **UK Addendum** to the EU SCCs | In force (IDTA 21 Mar 2022) | high |
| `eu` | GDPR | Chapter V — adequacy decision **or** SCCs / BCRs / derogations *(already in KB as `gdpr`)* | In force | high |
| `my` | PDPA (MY) | Amended **s.129** — destination with "substantially similar" law **or** "adequate level of protection"; CBPDT Guidelines | In force **1 Apr 2025**; whitelist abolished | high |
| `in` | DPDP Act 2023 | **s.16** + Rule 15 — negative-list: transfer to **any** country except those the Central Government restricts | Rules notified Nov 2025; **no restricted list yet**; s.16 operational **~May 2027** | high (model) |
| `ae` | PDPL (UAE) | Art. 22-23 — adequacy (UAE Data Office approval) **or** appropriate safeguards (SCCs/contract/consent) | Law in force; **Executive Regulations unpublished**; compliance by 1 Jan 2027; free zones differ | moderate |
| `id` | UU PDP | Art. 56 — destination with equal/higher protection, **or** adequate & binding safeguards, **or** consent | Law in force; **implementing regulation pending** | high (law) / moderate (instrument) |

## Proposed `regimes.json` additions (for change 3)

Each maps the home jurisdiction → its regime tag + the home-driven arrangement id(s) the engine
surfaces for any flagged cross-border flow. `gb` doubles as `uk` via the existing alias.

```json
"jp": { "regime": "APPI", "arrangements": ["appi_xborder"] },
"kr": { "regime": "PIPA", "arrangements": ["pipa_xborder"] },
"sg": { "regime": "PDPA (SG)", "arrangements": ["sg_pdpa_transfer"] },
"au": { "regime": "Privacy Act / APPs", "arrangements": ["au_app8"] },
"gb": { "regime": "UK GDPR / DPA 2018", "arrangements": ["uk_idta"] },
"eu": { "regime": "GDPR", "arrangements": ["gdpr"] },
"my": { "regime": "PDPA (MY)", "arrangements": ["my_pdpa_xborder"] },
"in": { "regime": "DPDP Act", "arrangements": ["in_dpdp_s16"] },
"ae": { "regime": "PDPL (UAE)", "arrangements": ["ae_pdpl_xborder"] },
"id": { "regime": "UU PDP", "arrangements": ["id_uupdp_xborder"] }
```

## Proposed `arrangements.json` additions (for change 3)

`gdpr` already exists. Eight new entries (`eu` reuses `gdpr`):

```json
{ "id": "appi_xborder", "name": "APPI cross-border transfer (Art. 28)",
  "summary": "Japan APPI: prior consent, a PPC-designated equivalent country (EU, UK), or a recipient with equivalent safeguards / APEC CBPR.",
  "url": "https://www.ppc.go.jp/en/" },
{ "id": "pipa_xborder", "name": "PIPA overseas transfer (Art. 28-8)",
  "summary": "Korea PIPA: consent, law/treaty, contract-necessity with notice, or a PIPC-recognised certification.",
  "url": "https://www.pipc.go.kr/eng/" },
{ "id": "sg_pdpa_transfer", "name": "PDPA Transfer Limitation Obligation (s.26)",
  "summary": "Singapore PDPA: ensure the recipient provides a standard of protection comparable to the PDPA via enforceable contract, BCR, or certification.",
  "url": "https://www.pdpc.gov.sg/" },
{ "id": "au_app8", "name": "Australian Privacy Principle 8 (cross-border disclosure)",
  "summary": "Australia Privacy Act: the disclosing entity stays accountable (s.16C) unless the recipient is bound by a substantially similar law with enforceable mechanisms.",
  "url": "https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-8-app-8-cross-border-disclosure-of-personal-information" },
{ "id": "uk_idta", "name": "UK international data transfer (IDTA / Addendum)",
  "summary": "UK GDPR Chapter V: an adequacy regulation, or appropriate safeguards via the UK IDTA or the UK Addendum to the EU SCCs.",
  "url": "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/" },
{ "id": "my_pdpa_xborder", "name": "Malaysia PDPA cross-border transfer (s.129)",
  "summary": "Malaysia PDPA (amended, in force 1 Apr 2025): a destination with substantially similar law or an adequate level of protection; see the CBPDT Guidelines.",
  "url": "https://www.pdp.gov.my/" },
{ "id": "in_dpdp_s16", "name": "DPDP Act cross-border transfer (s.16)",
  "summary": "India DPDP Act 2023 + Rule 15: transfer permitted to any country except those restricted by the Central Government (no restricted list issued yet; s.16 operational ~May 2027).",
  "url": "https://www.meity.gov.in/data-protection-framework" },
{ "id": "ae_pdpl_xborder", "name": "UAE PDPL cross-border transfer (Art. 22-23)",
  "summary": "UAE PDPL: transfer to an adequate jurisdiction (UAE Data Office) or under appropriate safeguards; Executive Regulations not yet published. DIFC and ADGM free zones have separate regimes.",
  "url": "https://uaelegislation.gov.ae/en/legislations/1972" },
{ "id": "id_uupdp_xborder", "name": "Indonesia UU PDP cross-border transfer (Art. 56)",
  "summary": "Indonesia PDP Law (Law 27/2022): destination with equal/higher protection, adequate & binding safeguards, or data-subject consent; implementing regulation pending.",
  "url": "https://www.dlapiperdataprotection.com/?t=transfer&c=ID" }
```

## Open questions / nuances (carry into change 3 design)

- **UAE free zones.** DIFC (DP Law 2020) and ADGM (DP Regs 2021) run **separate** regimes from the
  federal PDPL. The `ae` entry's note must say "federal PDPL; DIFC/ADGM differ" rather than imply one.
- **`eu` is coarse.** One token ignores member-state specifics; acceptable for reference-only output.
  GDPR is EU-wide so the regime tag holds.
- **Not-yet-operational mechanisms** (IN s.16 ~2027, AE Executive Regs, ID implementing reg): cite the
  framework; the summary records the status. Revisit when the instruments land.
- **`uk` vs `gb`.** Map under `gb`; the shipped `uk`→`gb` alias makes `home_location: uk` resolve here.
- **Regime tag collisions.** "PDPA" is disambiguated as `PDPA (SG)` / `PDPA (MY)` vs the existing
  `Macao PDPA` / `PDPO`.
- **Official-source upgrade.** `in_dpdp_s16` and `id_uupdp_xborder` cite a ministry page / DLA Piper;
  swap for a more permanent gov URL during change 3 if one is stable.

## Sources

- Japan APPI — [PPC](https://www.ppc.go.jp/en/), [DLA Piper JP](https://www.dlapiperdataprotection.com/?t=transfer&c=JP)
- Korea PIPA — [PIPC](https://www.pipc.go.kr/eng/), [Law.asia](https://law.asia/doing-business-in-korea-data-privacy-compliance/)
- Singapore PDPA — [PDPC s.26 guideline](https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/advisory-guidelines/the-transfer-limitation-obligation---ch-19-(270717).pdf)
- Australia APP 8 — [OAIC Chapter 8](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-8-app-8-cross-border-disclosure-of-personal-information)
- UK IDTA — [ICO international transfers](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/)
- Malaysia PDPA — [PDP CBPDT Guidelines (3/2025)](https://www.pdp.gov.my/ppdpv1/wp-content/uploads/2025/08/GP_CBPDT_EN-1.pdf), [Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2025/07/from-legislative-reform-to-practical-guidance-key-amendments-to-malaysias-pdpa-and-the-launch-of-cross-border-transfer-guidelines)
- India DPDP — [Rule 15 (DPDPA.com)](https://www.dpdpa.com/dpdparules/rule15.html), [MediaNama](https://www.medianama.com/2025/11/223-dpdp-rules-cross-border-data-transfers/)
- UAE PDPL — [Federal Decree-Law 45/2021](https://uaelegislation.gov.ae/en/legislations/1972/download), [Pinsent Masons](https://www.pinsentmasons.com/out-law/guides/business-in-the-uae-navigating-data-protection-regime)
- Indonesia UU PDP — [Makarim & Taira](https://www.makarim.com/news/personal-data-protection-law-cross-border-transfer-requirements), [DLA Piper ID](https://www.dlapiperdataprotection.com/?t=transfer&c=ID)
