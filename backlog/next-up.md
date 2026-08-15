# Next up — candidate directions (2026-08-13)

Ranked ideas from the "how else can borderlint help people use AI safely"
discussion. `mcp-config-scanning` (rank 1) is already proposed as an
OpenSpec change; these are the rest, in order. Each becomes a change via
`/opsx:propose` when picked up.

## 1. Egress allowlist output — policy as enforcement (PROPOSED 2026-08-13 as suricata-egress-rules — detection posture, Suricata TLS-SNI alert rules)

A new renderer that derives an egress allowlist (FQDNs) from the policy's
allowed flows, using the endpoint data already in the provider KB.
Consumable as a NetworkPolicy, firewall list, or proxy config. Converts the
advisory scanner into a network control: the scanner says what may flow,
the network enforces it. Mostly a new output format over existing data —
no new detection machinery.

Open questions: output shape(s) to support first (plain FQDN list vs
Kubernetes NetworkPolicy vs squid/proxy ACL); how regional endpoints
expand (allow only the policy-permitted regions' hosts).

## 2. Provider data-practice facts in the KB

Per-provider, hand-curated, drift-checked facts privacy reviewers ask
first and currently dig out of scattered ToS pages: trains on your API
data by default (yes/no/opt-out), retention window, subprocessor list
link, whether an enterprise tier changes the answer. Surfaces on the KB
site and in the evidence pack. Extends the moat — residency/sovereignty
curation is why borderlint is trusted; these are the adjacent facts with
the same curation-is-the-value property.

Open questions: sourcing discipline (cite the ToS section + retrieval
date per fact); how to keep claims review-dated without implying legal
advice.

## 3. Regulator-mapped policy profiles

`borderlint init --profile hkma` (also MAS, EU-AI-Act, PDPO) seeding the
policy interview from a regulator's published guidance instead of a blank
slate. Pure data addition over the existing init wizard. Directly answers
the Post 4b teaser question (turning a standards PDF into an automated
guardrail).

Open questions: which profile first (HKMA GenAI guidance is the home-turf
credibility play); how profiles version as guidance updates.

## Deliberately not doing

- Prompt-content DLP — crowded, hard, off-thesis (borderlint's identity
  is *where*, not *what*).
- Runtime AI gateway — a funded product category, not a scanner feature.
