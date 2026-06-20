#!/usr/bin/env python3
"""Weekly KB drift check: which upstream (litellm) providers does borderlint not yet cover?

The pure functions (coverage_gap / known_providers / upstream_providers) are unit-tested offline.
main() fetches the upstream and prints the uncovered provider names — one per line, with NO
jurisdiction or endpoint assigned (that mapping is human judgment).
"""

from __future__ import annotations

import json
import sys
import urllib.request

UPSTREAM = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"


def _norm(s: str) -> str:
    return "".join(c for c in s.lower() if c.isalnum())


def known_providers(kb: dict) -> set[str]:
    out: set[str] = set()
    for p in kb.get("providers", []):
        out.add(_norm(p["id"]))
        out.add(_norm(p["name"]))
        for s in p.get("sdks", []):
            out.add(_norm(s))
    return out


def upstream_providers(prices: dict) -> set[str]:
    return {e["litellm_provider"] for e in prices.values()
            if isinstance(e, dict) and e.get("litellm_provider")}


def coverage_gap(upstream: set[str], known: set[str]) -> list[str]:
    """Upstream provider names not represented in the bundled KB — names only, sorted."""
    return sorted({u for u in upstream if _norm(u) not in known})


def main() -> int:
    with open("borderlint/data/providers.json", encoding="utf-8") as fh:
        kb = json.load(fh)
    prices = json.loads(urllib.request.urlopen(UPSTREAM, timeout=30).read())
    for name in coverage_gap(upstream_providers(prices), known_providers(kb)):
        print(name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
