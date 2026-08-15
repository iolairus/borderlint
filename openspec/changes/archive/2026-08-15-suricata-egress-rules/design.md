## Context

The KB holds every provider's endpoint hosts (`_eps`: host, provider id, jurisdiction, plus per-provider region schemes). The policy names the allowed jurisdictions per classification. Compiling the two into Suricata rules turns the advisory scanner into runtime detection: any AI egress the code scan missed still trips an alert at the network boundary. Suricata is detection, not enforcement — that framing keeps the artifact honest.

## Goals / Non-Goals

**Goals:**
- Deterministic, loadable Suricata ruleset from KB + policy; byte-identical across runs on the same inputs.
- Alert posture with provider/jurisdiction context in every rule (`msg` + `metadata`); per-host selection with explicit unknown-jurisdiction coverage.
- Validated against a real Suricata (`suricata -T`) before merge.

**Non-Goals:**
- Enforcement (drop) semantics by default; QUIC/http.host variants; per-region host expansion.

## Decisions

- **KB+policy driven, not findings driven**: the renderer keeps the standard `(findings, kb, policy)` signature but reads only `kb`/`policy` — the ruleset must cover providers the codebase does not use yet; that is the point.
- **TLS SNI matching** (`tls.sni; content:"<host>"; nocase`): AI provider APIs are effectively all TLS. Host entries are used as-is — the KB's prefix-style entries (`bedrock-runtime`, `polly.`) work as substring content matches, mirroring `match_endpoint`'s `h in text` semantics. Rejected http.host duplicates (rule-count doubling for a vanishing plaintext case).
- **Unknown-jurisdiction hosts alert** under any policy not allowing `unknown` — matches the scanner's posture; endpoint-bearing aggregators (OpenRouter, HF, Vercel Gateway, AI/ML API) are covered by exactly this path, and SDK-only aggregators have no endpoints to rule on. Region-scheme providers' hosts always alert with a `region-dependent` msg marker regardless of policy — a static host pattern cannot express "us region yes, eu region no"; coarse-but-loud beats silently wrong. `ponytail: per-region host expansion if a real deployment needs finer than provider-prefix granularity.`
- **Per-host selection**: a host alerts iff its per-host jurisdiction from the KB endpoint table (`endpoint_jurisdictions` override or provider default) is outside the policy's expanded allow-list (`_allowed`: `uk`→`gb`, `GBA`→`hk`+`CN-GBA`). Rejected provider-level selection — six KB providers have hosts in different jurisdictions today (dashscope cn+sg, BFL de/eu/us, …), and a provider-level rule would silently pass the disallowed host.
- **Deterministic sids**: hosts sorted, sid = 1900000 + index, rev fixed at 1 (implementation detail). Regenerating after a KB change shifts sids — the file header states it is generated wholesale and must not be hand-edited or merged by sid.
- **Alert only, drop documented**: the header comment shows the `sed` to convert to drop for inline IPS. Advisory-first matches everything else borderlint emits.
- **Export semantics**: joins the non-gating export list (exit 0), since the artifact is configuration, not a verdict.

## Risks / Trade-offs

- [Risk] Substring SNI matches can overmatch (e.g. a lookalike domain containing a KB host string) → Mitigation: acceptable for alert posture; noted in header.
- [Risk] sid shifts across KB versions break external sid-based suppressions → Mitigation: header documents wholesale regeneration; users pin borderlint versions per ruleset.
- [Risk] QUIC-transported traffic (HTTP/3) bypasses tls.sni rules → Mitigation: documented limitation; quic.sni variant is a follow-up if demand appears.

## Real-world validation (gate before merge)

Generated rulesets (policy and inventory modes) must load clean in a real Suricata via `suricata -T` (docker `jasonish/suricata`) before the PR merges.
