# borderlint

**Map and govern where your AI data and traffic flow — east-west / APAC lens.**

A static, in-CI check for **HK / GBA entities**: does your AI data stay within the jurisdictions
your PDPO / PIPL policy allows? borderlint statically scans your repo (**Python and
TypeScript/JavaScript**) for AI provider usage, resolves each flow to a jurisdiction (ccTLD codes
plus the `CN-GBA` / `GBA` tokens), and fails the build on any flow outside the allow-list for the
data class you declare. Western and Chinese providers are treated evenly. **Zero runtime dependencies.**

## Use

```bash
python -m borderlint scan ./service --policy residency.json --classification customer-pii
```

- No `--policy` → **inventory mode** (lists flows + jurisdictions, exits 0).
- `--format json|mermaid|sarif|sbom` — machine output, a flow map, **SARIF** for GitHub code-scanning,
  or a deterministic **AI data-flow SBOM** (policy-independent inventory of every flow; an artifact, exits 0).
- `diff <baseline.sbom> <current.sbom>` — compare two SBOMs; **exits 1 when the PR adds a new
  non-`local` flow** (new egress), else 0. Diff the base-branch SBOM against the PR's to gate new AI egress.
- Accept a reviewed flow with an inline `# borderlint: allow <reason>` **waiver** (justification
  required; it's reported as *waived*, not hidden, and can't override an explicit provider `deny`).
- Exit code is non-zero on a violation, so it gates CI.

## Policy (the eval-set)

`residency.json` maps each data class to the jurisdictions you accept:

```json
{
  "home_location": "hk",
  "classifications": {
    "customer-pii": ["hk", "CN-GBA", "sg"],
    "employee-pii": ["hk", "CN-GBA"],
    "non-pii":      ["hk", "CN-GBA", "cn", "mo", "sg", "us", "gb"]
  }
}
```

**Deny-by-default**: a flow to any code not on the list for the declared class fails — so `sg` is
allowed but `my` is not, matching a PDPO agreed-locations EULA. `GBA` is shorthand for `hk` +
`CN-GBA`. Declare your **`home_location`** (`hk`, `mo`, or `CN-GBA`) and a flagged flow is tagged with
the **data-protection regimes** in play (PDPO / **Macao PDPA** / PIPL) and the relevant **cross-border
arrangement** — the matching GBA Standard Contract variant, *(Mainland, Hong Kong)* or *(Mainland,
Macao)*, PIPL cross-border, or GDPR SCCs — as reference links, never adjudicated. (`home_regime`
`pdpo`/`pipl` is still accepted.)

## Capabilities

- **Languages:** Python (AST) and TypeScript/JavaScript (`import` / `require` / dynamic `import()`),
  plus endpoint references in config/text files and **OpenAI-compatible `/v1/chat/completions` calls**
  — even to a runtime-configured host (resolved to `unknown`, so `on_unknown: fail` gates it).
- **Providers:** 13+ across the east-west boundary (OpenAI, Anthropic, Google, Azure, Bedrock,
  Mistral, Cohere + Tencent, Alibaba, DeepSeek, Moonshot, Zhipu, Baidu), with Python and JS/TS
  package names and the **Vercel AI SDK** (`@ai-sdk/*`).
- **Aggregators:** litellm, langchain, LlamaIndex, aisuite, Vercel AI core (`ai`) → `unknown`
  (runtime-routed), so `on_unknown: fail` blocks them for sensitive classes.
- **Jurisdictions:** ccTLD/ISO codes + `CN-GBA` / `GBA`; **AWS/Azure region resolved from the
  endpoint host** where present (e.g. `bedrock-runtime.ap-east-1…` → `hk`).
- **Policy:** classification-keyed JSON eval-set, deny-by-default, provider allow/deny, configurable
  failure set, declared home regime.
- **Regimes & arrangements:** home location `hk`/`mo`/`CN-GBA` → PDPO / Macao PDPA / PIPL tags, linked to
  the matching GBA Standard Contract (HK or Macao), PIPL cross-border, or GDPR SCCs — reference only.
- **Output & CI:** text / JSON / Mermaid / **SARIF** / **SBOM**, an SBOM **`diff`** gate for new
  egress, inline **waivers**, exit codes, GitHub Action + Jenkins.

## Scope

For HK / GBA home bases under PDPO / PIPL / GBA. Not yet: vector-DB / storage residency, CycloneDX /
SPDX SBOM export, and optional LLM enrichment. Per-capability status — shipped vs. next vs. later — is
tracked in [`CAPABILITIES.md`](CAPABILITIES.md).

## Internal endpoints

Map your own regional endpoints to jurisdictions; they **merge** with the bundled provider KB (your
entries win on conflict):

```json
{ "endpoints": { "llm-cn.acme.internal": "cn", "llm-hk.acme.internal": "hk", "llm-sg.acme.internal": "sg" } }
```

```bash
borderlint scan . --providers internal-endpoints.json --policy residency.json --classification customer-pii
```

A configuration wired to the **wrong regional endpoint** — e.g. the CN endpoint for HK/SG-only
customer PII — then fails the build, so you can't ship a service pointed at the wrong region.

A runnable end-to-end example is in [`examples/gba-resident-app/`](examples/gba-resident-app/) — a
GBA-resident app (internal Shenzhen endpoint → `CN-GBA`, plus Mainland / Western / local fallbacks). Run
it under `residency-hk.json` vs `residency-mo.json` and the surfaced **GBA Standard Contract** flips
between the *(Mainland, Hong Kong)* and *(Mainland, Macao)* variant, and the regime tag between PDPO and
Macao PDPA:

```bash
borderlint scan examples/gba-resident-app \
  --providers examples/gba-resident-app/internal-endpoints.json \
  --policy examples/gba-resident-app/residency-hk.json --classification customer-pii
```

## CI

Same command in any pipeline. GitHub Actions (composite action):

```yaml
- uses: iolairus/borderlint@v0.11.0
  with: { path: ., policy: residency.json, classification: customer-pii }
```

Jenkins / anything else: `pip install borderlint && borderlint scan . --policy residency.json --classification customer-pii` — a non-zero exit fails the stage. Full examples in `examples/ci/`.

pre-commit — catch a bad flow before it's committed (`.pre-commit-config.yaml`):

```yaml
- repo: https://github.com/iolairus/borderlint
  rev: v0.11.0
  hooks:
    - id: borderlint
      args: [--policy, residency.json, --classification, customer-pii]
```

The hook runs `borderlint scan` over the repo (the `args` are required for a real gate; without a
policy it runs inventory mode and always passes).

## Keeping the KB fresh

A weekly GitHub Action (`.github/workflows/kb-refresh.yml`) diffs the bundled provider KB against
litellm's registry and opens an issue listing providers we don't yet cover — jurisdictions are
assigned **by hand**, never auto-merged. `borderlint --version` shows the KB's last-reviewed date.
To add or correct a provider, see [`CONTRIBUTING.md`](CONTRIBUTING.md) (KB schema + PR workflow).

## Development

borderlint is built **spec-first** with [OpenSpec](https://github.com/Fission-AI/OpenSpec): every change
is a reviewed proposal (specs + design + tasks) gated by a `spec-reviewer` agent before any code is
written. To bootstrap the same workflow into another repo:

```bash
scripts/opsx-init.sh [--no-jira] /path/to/your/repo
```

It scaffolds `AGENTS.md`, `.claude/` (slash commands + the spec-reviewer gate), an empty `openspec/`, and
`workflow.yaml`. `--no-jira` trims it to the core loop — propose → review → apply → commit → ship.

## License

MIT © 2026 Iolaire McKinnon. Vendor-neutral by design.
