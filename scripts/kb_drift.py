#!/usr/bin/env python3
"""Weekly KB freshness check: what has drifted since the bundled knowledge bases were reviewed?

Sections: upstream (litellm) providers not covered by providers.json; upstream model identifiers
the provenance map does not resolve (grouped by family); provider ids without a sovereignty
mapping; bundled KBs whose `updated` date is older than the review interval. The pure functions
are unit-tested offline; main() fetches the upstream once and prints a markdown report — empty
when there is nothing to review. No jurisdiction or bloc is ever auto-assigned.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from borderlint.kb import _SOVEREIGNTY_BLOCS, load_kb  # noqa: E402  deliberate private import (design D3)

UPSTREAM = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
DATA_DIR = REPO_ROOT / "borderlint" / "data"
STALE_DAYS = 90
FAMILY_CAP = 50


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


def upstream_models(prices: dict) -> list[str]:
    """The upstream file's keys are model identifiers — the provenance check's input."""
    return sorted(k for k, e in prices.items()
                  if isinstance(e, dict) and e.get("litellm_provider"))


def coverage_gap(upstream: set[str], known: set[str]) -> list[str]:
    """Upstream provider names not represented in the bundled KB — names only, sorted."""
    return sorted({u for u in upstream if _norm(u) not in known})


def model_coverage_gap(model_ids: list[str], kb) -> list[str]:
    """Upstream model identifiers the provenance map does not resolve, sorted.

    Covered when the key or any of its `/`-suffixes matches — litellm keys carry
    provider/region qualifiers of varying depth (`bedrock/ap-northeast-1/qwen.qwen3`),
    and the qualifiers are not hub orgs.
    """
    out = []
    for mid in sorted(set(model_ids)):
        parts = mid.split("/")
        if any(kb.match_model("/".join(parts[i:])) for i in range(len(parts))):
            continue
        out.append(mid)
    return out


def family_stems(uncovered: list[str]) -> list[tuple[str, int, str]]:
    """Group uncovered identifiers by family stem → (stem, count, example), most models first.

    Stem = leading alphabetic run of the basename, lowercased (`grok-4-fast` → `grok`).
    """
    groups: dict[str, list[str]] = {}
    for mid in uncovered:
        base = mid.rsplit("/", 1)[-1].lower()
        alpha = ""
        for c in base:
            if not c.isalpha():
                break
            alpha += c
        groups.setdefault(alpha or base, []).append(mid)
    return sorted(((s, len(v), sorted(v)[0]) for s, v in groups.items()),
                  key=lambda x: (-x[1], x[0]))


def sovereignty_gaps(provider_ids: list[str], sov_map: dict) -> list[tuple[str, str | None]]:
    """Provider ids with no sovereignty mapping or a bloc outside the vocabulary, sorted."""
    return sorted((pid, sov_map.get(pid)) for pid in set(provider_ids)
                  if sov_map.get(pid) not in _SOVEREIGNTY_BLOCS)


def stale_kbs(kb_dates: dict, today: dt.date,
              interval_days: int = STALE_DAYS) -> list[tuple[str, str, int]]:
    """(name, updated, age_days) for KBs whose `updated` date is older than the interval."""
    out = []
    for name, date_str in sorted(kb_dates.items()):
        age = (today - dt.date.fromisoformat(date_str)).days
        if age > interval_days:
            out.append((name, date_str, age))
    return out


def render_report(providers_gap: list[str], families: list[tuple[str, int, str]],
                  sov_gaps: list[tuple[str, str | None]], stale: list[tuple[str, str, int]],
                  family_cap: int = FAMILY_CAP) -> str:
    """Markdown issue body: empty sections omitted; empty report is the empty string."""
    parts = []
    if providers_gap:
        parts.append(
            "### New providers\n\n"
            "Upstream providers not yet covered by the borderlint KB. Assign endpoint host(s), "
            "a jurisdiction, and a sovereignty bloc **by hand** — do not auto-merge.\n\n"
            + "\n".join(f"- {p}" for p in providers_gap))
    if families:
        lines = [f"- `{stem}` — {n} model{'s' if n > 1 else ''}, e.g. `{ex}`"
                 for stem, n, ex in families[:family_cap]]
        if len(families) > family_cap:
            lines.append(f"- … and {len(families) - family_cap} more families")
        parts.append(
            "### Uncovered model families\n\n"
            "Upstream model identifiers the provenance map does not resolve, grouped by family. "
            "Assign a provenance bloc **by hand**, add a passthrough org, or accept `unknown`.\n\n"
            + "\n".join(lines))
    if sov_gaps:
        parts.append(
            "### Sovereignty gaps\n\n"
            "Bundled providers with no sovereignty bloc or an invalid one. Assign **by hand**.\n\n"
            + "\n".join(f"- `{pid}` — " + (f"invalid bloc `{bloc}`" if bloc else "no mapping")
                        for pid, bloc in sov_gaps))
    if stale:
        parts.append(
            f"### Stale knowledge bases\n\n"
            f"Last reviewed more than {STALE_DAYS} days ago — review and bump `updated`.\n\n"
            + "\n".join(f"- `{name}` — updated {date}, {age} days ago"
                        for name, date, age in stale))
    return "\n\n".join(parts)


def main() -> int:
    with open(DATA_DIR / "providers.json", encoding="utf-8") as fh:
        providers_doc = json.load(fh)
    kb = load_kb()
    prices = json.loads(urllib.request.urlopen(UPSTREAM, timeout=30).read())

    providers_gap = coverage_gap(upstream_providers(prices), known_providers(providers_doc))
    families = family_stems(model_coverage_gap(upstream_models(prices), kb))
    sov_gaps = sovereignty_gaps([p["id"] for p in providers_doc["providers"]], kb.sovereignty_map)
    kb_dates = {f.name: json.loads(f.read_text(encoding="utf-8")).get("updated")
                for f in sorted(DATA_DIR.glob("*.json"))}
    stale = stale_kbs({k: v for k, v in kb_dates.items() if v}, dt.date.today())

    report = render_report(providers_gap, families, sov_gaps, stale)
    if report:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
