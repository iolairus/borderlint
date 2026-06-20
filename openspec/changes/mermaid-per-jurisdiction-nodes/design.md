## Context

`report.mermaid()` groups providers into per-jurisdiction subgraphs but declares each provider node by
a bare `pid`. Mermaid de-dups node ids globally, so a provider in N jurisdictions renders once (under
whichever zone declared it first) and the other N-1 zones show empty. Subgraph titles use
`juris(j)`, which only names a curated subset of codes — the rest fall back to the bare code.

## Goals / Non-Goals

**Goals:** a multi-jurisdiction provider visible in every zone; consistent zone titles.
**Non-Goals:** changing jurisdiction names in other output formats; naming every ccTLD.

## Decisions

- **One node per (provider, jurisdiction): id `f"{pid}__{j.replace('-','_')}"`.** Mermaid de-dups by
  id, so the only way a provider can appear in two zones is two distinct ids. The node *label* stays the
  provider name (so both nodes read e.g. `AWS Bedrock`); the app edge points at each id.
- **Subgraph title = the jurisdiction code `j`, not `juris(j)`.** Only us/eu/cn/hk/sg/gb/mo/my/CN-GBA/GBA/
  unknown have display names; Bedrock/Azure-resolved codes (`fr`/`de`/`ie`) and `local` don't, so titles
  were inconsistent (`Singapore` vs `fr`). The code is the policy's own vocabulary — consistent and
  unambiguous. Provider node labels still carry the readable names.
- **`juris()` is untouched.** Text/JSON/SARIF/diff keep the display names (`OpenAI -> United States`).
  Only the Mermaid subgraph title stops calling it.

## Risks / Trade-offs

- Zone titles lose the descriptive `Unknown (region-dependent)` / `Mainland China` wording → acceptable;
  codes match what the user writes in the policy, and provider labels remain readable. Other formats
  keep the prose.
