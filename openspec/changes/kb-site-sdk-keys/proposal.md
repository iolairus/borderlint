# kb-site-sdk-keys

## Why

The KB gained per-language SDK keys in two steps — `jvm` in #68 (Java/Kotlin detection) and `dotnet` in #78 (C# detection) — and agents curated real package data for them (e.g. `aws_bedrock` carries `software.amazon.awssdk.services.bedrockruntime`, `aws.sdk.kotlin.services.bedrockruntime`, `Amazon.BedrockRuntime` today). None of it is visible where users look: the published KB site renders only Python and npm packages, so [the Bedrock page](https://iolairus.github.io/borderlint/providers/aws_bedrock.html) shows just two npm packages. Three compounding causes:

1. **The site generator never learned the new keys** — `scripts/kb_site.py` builds the Packages row from `sdks` + `npm` only; `jvm`/`dotnet` are dropped silently. The pages workflow regenerates faithfully on every KB change — from an incomplete projection.
2. **The weekly freshness check has no SDK-coverage axis** — `kb_drift.py` reports provider/model/sovereignty/staleness gaps, but nothing that would ever surface "this provider ships official Java/.NET SDKs but has no `jvm`/`dotnet` keys", so the omission had no process to catch it.
3. **The documented schema enumeration went stale** — the kb-freshness spec's "KB entry schema is documented" scenario still enumerates the pre-`jvm`/`dotnet` field list, the same oversight class as the generator.

## What Changes

- **KB site**: provider pages render every package key the KB records — Python `sdks`, `npm`, `jvm` (Java), `dotnet` (.NET) — each labeled by language. Pure projection change; `aws_bedrock`'s page gains its Java/Kotlin/.NET packages with no KB edit.
- **Freshness check**: new SDK-coverage section in the drift report — bundled providers carrying package keys in some languages but missing `jvm`/`dotnet` surface for review, with a curated, reasoned exemption list (same suppression mechanics as aliases/residue) so providers with no official Java/.NET SDK don't recur as noise. Keys are never auto-assigned.
- **One-time KB refresh**: audit every bundled provider missing `jvm`/`dotnet`, add registry-verified official SDK keys where they exist (verify-before-add, Huawei precedent), and record reasoned exemptions for the rest.
- **Spec hygiene**: the "KB entry schema is documented" scenario is updated to enumerate `jvm`, `dotnet`, and `category`.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `kb-website`: MODIFIED "Provider page content" — the package-names clause now covers all per-language SDK keys the KB records, labeled by language; one new scenario (multi-language provider renders all keys).
- `kb-freshness`: ADDED "SDK coverage check" — the scheduled check surfaces SDK-key gaps with reasoned exemptions, offline and non-assigning, consistent with "Human-assigned jurisdictions". MODIFIED "Community contribution workflow" — the documented-schema scenario enumerates `jvm`, `dotnet`, `category`.

## Impact

- `scripts/kb_site.py`: Packages row gains `jvm`/`dotnet`.
- `scripts/kb_drift.py`: SDK-coverage section + exemption list in `scripts/kb_drift_aliases.json`.
- `borderlint/data/providers.json`: verified `jvm`/`dotnet` additions where official SDKs exist.
- `tests/`: site-rendering and drift-section fixtures. Zero new dependencies; scanner untouched.

## Non-goals

- No scanner/detection changes — `jvm`/`dotnet` matching already works; this is projection + freshness.
- No auto-population of SDK keys from any upstream feed — curation stays human and registry-verified.
- No model-developer page changes.
