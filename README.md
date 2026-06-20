# borderlint

**Map and govern where your AI data and traffic flow — east-west / APAC lens.**

A static, in-CI check for **HK / GBA entities**: does your AI data stay within the jurisdictions
your PDPO / PIPL policy allows? borderlint detects AI provider usage in your repo, resolves each
flow to a jurisdiction (ccTLD codes plus the `CN-GBA` / `GBA` tokens), and fails the build on any
flow outside the allow-list for the data class you declare. Western and Chinese providers are
treated evenly. **Zero runtime dependencies.**

## Use

```bash
python -m borderlint scan ./service --policy residency.json --classification customer-pii
```

- No `--policy` → **inventory mode** (lists flows + jurisdictions, exits 0).
- `--format json|mermaid` for machine output or a flow map.
- Exit code is non-zero on a violation, so it gates CI.

## Policy (the eval-set)

`residency.json` maps each data class to the jurisdictions you accept:

```json
{
  "home_regime": "pdpo",
  "classifications": {
    "customer-pii": ["hk", "CN-GBA", "sg"],
    "employee-pii": ["hk", "CN-GBA"],
    "non-pii":      ["hk", "CN-GBA", "cn", "mo", "sg", "us", "gb"]
  }
}
```

**Deny-by-default**: a flow to any code not on the list for the declared class fails — so `sg` is
allowed but `my` is not, matching a PDPO agreed-locations EULA. `GBA` is shorthand for `hk` +
`CN-GBA`. Cross-border arrangements (e.g. the GBA Standard Contract) are surfaced as reference
links, never adjudicated.

## Scope (v1)

For HK / GBA home bases under PDPO / PIPL / GBA. Python scanning today. Not yet: TypeScript, SARIF,
a GitHub Action, container/SCA mode, LLM enrichment. Full scope in `CAPABILITIES.md`.

## License

MIT © 2026 Iolaire McKinnon. Vendor-neutral by design.
