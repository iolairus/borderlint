# kb-site-sdk-keys — tasks

## 1. Site generator

- [x] 1.1 kb_site.py: extend the Packages row to append `jvm` entries labeled `(Java)` and `dotnet` entries labeled `(.NET)` after the Python/npm entries — kb-website spec: multi-language scenario; design decision 1

## 2. Freshness check

- [x] 2.1 kb_drift.py: SDK-coverage section — report bundled providers with `sdks`/`npm` but missing `jvm`/`dotnet`, unless exempt; render provider id + missing keys; omit section when empty; SDK-gap count joins the leading actionable-summary line — kb-freshness spec: SDK coverage check (all scenarios) + MODIFIED summary requirement; design decision 2
- [x] 2.2 kb_drift_aliases.json: add `sdk_exempt` map (provider id → reason); loud failure on empty reason or id absent from the KB — spec: exemption scenarios; design decision 2

## 3. KB curation (verify-before-add)

- [x] 3.1 Audit every provider the new section flags; for each, check Maven Central / NuGet / vendor docs for an official Java or .NET SDK and add the confirmed `jvm`/`dotnet` key — design decision 3
- [x] 3.2 Record a reasoned `sdk_exempt` entry for each flagged provider with no official Java/.NET SDK — design decision 3

## 4. Tests

- [x] 4.1 Site fixture: a provider carrying all four package keys renders Python, npm, Java, and .NET entries labeled per language — kb-website spec: multi-language scenario
- [x] 4.2 Drift fixtures: gap provider surfaces with missing keys; reasoned exemption suppressed; empty reason and unknown-id exemptions fail loudly; empty section omitted; summary head counts SDK gaps; KB load/scan unaffected by `sdk_exempt` — kb-freshness spec: all SDK-coverage + summary scenarios
- [x] 4.3 Full suite green

## 5. Real-world validation (before merge)

- [x] 5.1 Regenerate the site locally and confirm `aws_bedrock` shows its Java/Kotlin/.NET packages alongside npm; spot-check two other multi-language providers — proposal What Changes
- [x] 5.2 Run the drift script and confirm the SDK-coverage section matches the post-curation state (near-empty) — design risk 1

## 6. Deploy

- [ ] 6.1 After merge, confirm the pages workflow republishes (push trigger covers `scripts/kb_site.py` and `borderlint/data/**`); trigger `workflow_dispatch` if the curation landed without touching those paths — kb-website spec: Automated publication
