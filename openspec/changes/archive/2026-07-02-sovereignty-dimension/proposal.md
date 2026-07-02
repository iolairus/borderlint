## Why

borderlint models **residency** — where an endpoint physically sits — but residency is necessary,
not sufficient. A US-headquartered provider (AWS, Azure, GCP, OpenAI, Anthropic) is subject to US
compelled-disclosure law (CLOUD Act, FISA 702, Patriot Act §215) regardless of where the endpoint
is hosted. A flow to AWS Bedrock `ap-east-1` resolves to residency `hk` yet remains under **US
sovereignty** for disclosure purposes. Today a policy that allows `hk` silently approves that
exposure. We need an orthogonal **sovereignty** dimension: *which government can compel disclosure
of this flow's data*, evaluated independently of where the bytes rest.

## What Changes

- Introduce a **sovereignty** attribute on each resolved flow, distinct from jurisdiction
  (residency). Sovereignty reflects the provider's home legal regime for compelled disclosure,
  not the endpoint region.
- Add a bundled **sovereignty map** keyed by provider id (and, where relevant, by endpoint host),
  covering the blocs that are practically distinct for compelled disclosure: `us`, `eu`, `cn`,
  `uk`, `ru`, `in`, `il`, plus `local` (no external sovereign — self-hosted) and `unknown`.
- Extend the policy schema with an optional `sovereignty` block: per-classification allow-lists of
  sovereignty blocs, plus `on_unknown` and inclusion in `fail_on`. Default behaviour is unchanged
  when the block is absent (sovereignty is opt-in and never breaks existing policies).
- Add a `sovereignty` finding reason, reported alongside `residency` / `denied_provider` /
  `unknown`. A flow fails only if its sovereignty is outside the declared allow-list **and**
  `sovereignty` is in `fail_on`.
- Surface sovereignty in the text, JSON, and Mermaid reports as an additional column/label, never
  replacing residency.

## Capabilities

### New Capabilities
- `sovereignty`: model which government can compel disclosure of a flow's data, as a dimension
  orthogonal to residency; map providers to sovereignty blocs; evaluate against an optional
  per-classification sovereignty allow-list.

### Modified Capabilities
- `jurisdiction-classification`: each resolved flow additionally carries a sovereignty bloc;
  provider KB entries gain an optional `sovereignty` field; loopback/self-hosted flows resolve to
  sovereignty `local`.
- `residency-policy`: policy schema gains an optional `sovereignty` block; evaluation produces a
  new `sovereignty` reason; `fail_on` accepts `sovereignty`.
- `cli-and-reporting`: text/JSON/Mermaid reports surface the sovereignty bloc per flow and a
  sovereignty summary; CLI adds no new required flags (policy-driven).

## Non-goals

- **Not adjudicating legality.** borderlint surfaces the sovereignty bloc and the policy decides;
  it does not opine on whether a given compelled-disclosure statute actually applies.
- **Not modelling data-protection adequacy** (e.g. EU-US Data Privacy Framework status). That is
  a transfer-mechanism concern, separate from compelled-disclosure exposure.
- **Not open-weights provenance.** Downloaded weights (Llama, Mistral, Qwen, DeepSeek) carry an
  export-control / supply-chain provenance concern distinct from runtime sovereignty; deferred to a
  later change.
- **Not a full country-by-country sovereign map.** We model blocs (`us`, `eu`, `cn`, `uk`, `ru`,
  `in`, `il`, `local`, `unknown`), not every state on earth.
- **No breaking changes.** Sovereignty is opt-in; absent the policy block, behaviour is identical
  to today.

## Impact

- `borderlint/data/`: new `sovereignty.json` map; `providers.json` gains optional `sovereignty`
  per entry.
- `borderlint/kb.py`, `borderlint/policy.py`, `borderlint/report.py`: resolve, evaluate, and
  render the new dimension.
- `tests/test_borderlint.py`: sovereignty resolution, evaluation, and reporting cases.
- `examples/residency.json`: an annotated example showing the optional `sovereignty` block.
- Docs: `CAPABILITIES.md` and `README.md` gain a sovereignty subsection.
