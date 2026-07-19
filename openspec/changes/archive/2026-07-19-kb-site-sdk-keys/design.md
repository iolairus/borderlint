# kb-site-sdk-keys — design

## Context

KB entries carry up to four package keys — `sdks` (Python), `npm`, `jvm` (Java/Kotlin,
since #68), `dotnet` (C#, since #78) — matched by the scanner per language. The site generator
(`scripts/kb_site.py`, Packages row at lines 115-118) predates the two newer keys and renders
only the first two; the weekly drift check (`scripts/kb_drift.py`) has no axis that compares
per-language SDK coverage. Both are offline, deterministic tools driven by the bundled KB plus
the curated suppression file (`scripts/kb_drift_aliases.json`).

## Goals / Non-Goals

**Goals:**
- The published KB site shows every SDK key a provider entry records, per language.
- The weekly freshness issue surfaces providers with SDK-key gaps, without recurring noise from
  providers that legitimately have no official Java/.NET SDK.
- A one-time, registry-verified curation pass closes today's gaps.

**Non-Goals:** scanner changes; auto-assigned SDK keys; model-developer pages; new dependencies.

## Decisions

1. **One Packages row, four languages, labeled.** Extend the existing row construction to append
   `jvm` entries labeled `(Java)` and `dotnet` labeled `(.NET)`, after `(Python)` and `(npm)`.
   Language labels follow the CONTRIBUTING schema table's names. No layout or page-structure
   change; providers without the newer keys render exactly as before. `aws_bedrock` needs no KB
   edit — its entry already carries both keys; the page fixes itself on the next deploy.
2. **SDK-coverage section in the drift report, exemption-backed.** A provider is reported when
   it carries at least one package key (`sdks` or `npm`) but lacks `jvm` or `dotnet`, and is not
   listed under a new `sdk_exempt` map in the suppression file. `sdk_exempt` maps provider id →
   reason (e.g. "Python/JS-only vendor, no official JVM/.NET SDK"), consumed only by the check —
   same mechanics and loud-failure rules as aliases/residue: an empty reason fails the check, an
   exempt id absent from the KB fails loudly. The check stays a pure offline function of bundled
   KB + suppression list (Deterministic coverage diff); it never assigns keys, only reports
   (Human-assigned jurisdictions precedent). Report section lists provider id + which keys are
   missing; the section is omitted when empty like the others, and its count joins the report's
   leading actionable-summary line (MODIFIED summary requirement — otherwise an SDK-only report
   would print "nothing actionable" above a non-empty section).
3. **One-time curation, verify-before-add.** For every provider the new section flags: check
   Maven Central / NuGet / the vendor docs for an official Java or .NET SDK; add the key only
   when the published coordinate/namespace is confirmed (Huawei precedent — a guessed prefix is
   worse than a missing one); otherwise record a reasoned `sdk_exempt` entry. Expected outcome
   for the current 27 npm-only providers: a handful of key additions (cloud/lab vendors with
   real multi-language SDKs), exemptions for the rest. Bedrock is verified-only (keys present).
4. **Spec scenario enumeration catches up.** The kb-freshness "KB entry schema is documented"
   scenario enumerates the entry fields; it is updated to include `jvm`, `dotnet`, and
   `category` so the documented schema can no longer silently drift from the real one.

## Risks / Trade-offs

- [The new drift section could nag weekly about legitimately single-language vendors] → the
  `sdk_exempt` reasoned list suppresses them permanently; first run after this change ships
  should land with the curation pass already done, so the section opens near-empty.
- [Language label choice ((Java) vs (JVM)) could confuse Kotlin users] → the KB key is `jvm`
  and Kotlin packages render under it; the label says (Java) per CONTRIBUTING's
  "Java/Kotlin import-package prefixes" wording — noted in the row via the label alone.
- [Curation could over-add third-party/community SDKs] → official-vendor coordinates only,
  registry-verified in the same pass, matching the verify-before-add rule used for Huawei.

## Open Questions

None.
