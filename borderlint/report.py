"""Render findings as text, JSON, or a Mermaid flow map (grouped by jurisdiction)."""

from __future__ import annotations

import json
import os
import re
import subprocess

from .policy import _alias

JURIS = {"us": "United States", "eu": "European Union", "cn": "Mainland China", "hk": "Hong Kong",
         "sg": "Singapore", "gb": "United Kingdom", "mo": "Macao", "my": "Malaysia",
         "ru": "Russia", "in": "India", "fr": "France", "nl": "Netherlands", "de": "Germany",
         "be": "Belgium", "ch": "Switzerland", "it": "Italy", "es": "Spain", "fi": "Finland",
         "pl": "Poland", "se": "Sweden", "no": "Norway", "ie": "Ireland", "jp": "Japan",
         "kr": "South Korea", "tw": "Taiwan", "au": "Australia", "ca": "Canada", "br": "Brazil",
         "cl": "Chile", "id": "Indonesia", "th": "Thailand", "il": "Israel", "ae": "UAE",
         "qa": "Qatar", "sa": "Saudi Arabia", "za": "South Africa",
         "CN-GBA": "Mainland GBA", "GBA": "Greater Bay Area", "local": "Local",
         "unknown": "Unknown (region-dependent)"}
REASON = {"denied_provider": "provider denied by policy",
          "residency": "jurisdiction outside the allow-list for this data class",
          "unknown": "jurisdiction could not be determined",
          "sovereignty": "sovereignty outside the allow-list for this data class",
          "sovereignty_unknown": "sovereignty could not be determined"}
SOVEREIGNTY = {"us": "United States", "eu": "European Union", "cn": "Mainland China",
               "uk": "United Kingdom", "ru": "Russia", "in": "India", "il": "Israel",
               "ca": "Canada", "local": "Local", "unknown": "Unknown"}
_RANK = {"ok": 0, "waived": 1, "warn": 2, "fail": 3}

with open(os.path.join(os.path.dirname(__file__), "data", "arrangements.json"), encoding="utf-8") as _fh:
    _ARRANGEMENTS = {a["id"]: a for a in json.load(_fh)["arrangements"]}
with open(os.path.join(os.path.dirname(__file__), "data", "regimes.json"), encoding="utf-8") as _fh:
    _REGIMES = json.load(_fh)["regimes"]  # jurisdiction -> {regime, arrangements[]}
# EU/EEA jurisdictions that trigger the GDPR reference (the `eu` token + member country codes).
_EU = frozenset("eu at be bg hr cy cz dk ee fi fr de gr hu ie it lv lt lu mt nl pl pt ro sk si es se is li no".split())


def juris(j: str) -> str:
    return JURIS.get(j, j)


def sov(b: str) -> str:
    """Display label for a sovereignty bloc."""
    return SOVEREIGNTY.get(b, b)


def _ref(aid: str) -> str:
    a = _ARRANGEMENTS[aid]
    return f"{a['name']} — {a['summary']} {a['url']}"


def regime_of(j: str):
    """Data-protection regime tag for a jurisdiction, or None if the KB maps none."""
    entry = _REGIMES.get(j)
    return entry.get("regime") if entry else None


def _flagged_dests(findings) -> set:
    return {f.detection.jurisdiction for f in findings if f.severity != "ok"}


def _arrangements(findings, policy) -> list[str]:
    """Cross-border arrangement reference(s) for flagged flows — context only, never adjudicated."""
    policy = policy or {}
    dests = _flagged_dests(findings)
    loc = _alias(policy.get("home_location")) if policy.get("home_location") else None
    if loc:  # home-location path: GBA span + destination specials, then home-driven refs from the map
        span = {loc} | dests
        out = []
        if {"hk", "CN-GBA"} <= span:
            out.append(_ref("gba"))
        if {"mo", "CN-GBA"} <= span:
            out.append(_ref("gba_mo"))
        if "cn" in dests or (loc == "CN-GBA" and dests - {"cn", "CN-GBA", "hk", "mo"}):
            out.append(_ref("pipl"))
        if dests & _EU:
            out.append(_ref("gdpr"))
        for aid in _REGIMES.get(loc, {}).get("arrangements", []):  # seeded empty for hk/mo/cn/CN-GBA
            ref = _ref(aid)
            if ref not in out:
                out.append(ref)
        return out
    # legacy home_regime path — unchanged
    regime = policy.get("home_regime")
    out = []
    if "CN-GBA" in dests and regime in ("pdpo", "pipl"):  # HK <-> nine GBA cities, not plain cn
        out.append(_ref("gba"))
    if "cn" in dests or (regime == "pipl" and dests - {"cn", "CN-GBA", "hk"}):
        out.append(_ref("pipl"))
    if dests & _EU:
        out.append(_ref("gdpr"))
    return out


def _regimes(findings, policy) -> list[str]:
    """Regime tag(s) implicated by a flagged flow — {PDPO, PIPL, Macao PDPA}, informational."""
    policy = policy or {}
    dests = _flagged_dests(findings)
    if not dests:
        return []
    loc = _alias(policy.get("home_location")) if policy.get("home_location") else None
    if loc:  # home-location path: regime of the home + each destination, from the map
        tags = {regime_of(loc)} | {regime_of(d) for d in dests}
        tags.discard(None)
        return sorted(tags)
    # legacy home_regime path — unchanged
    regime = policy.get("home_regime")
    tags = set()
    if regime == "pdpo":
        tags.add("PDPO")
    if regime == "pipl" or dests & {"cn", "CN-GBA"}:
        tags.add("PIPL")
    return sorted(tags)


def text(findings, kb, policy=None) -> str:
    if not findings:
        return "borderlint: no AI provider usage detected."
    lines = ["borderlint — AI data-flow & residency report", "=" * 46]
    by = {}
    for f in findings:
        by.setdefault(f.detection.provider_id, []).append(f)
    for pid in sorted(by):
        fs = by[pid]
        worst = max((f.severity for f in fs), key=lambda s: _RANK[s])
        mark = {"ok": " OK ", "waived": "WAIV", "warn": "WARN", "fail": "FAIL"}[worst]
        js = ", ".join(juris(x) for x in sorted({f.detection.jurisdiction for f in fs}))
        tag = " (vector store)" if kb.category(pid) == "vector_store" else ""
        sovs = ", ".join(sov(x) for x in sorted({getattr(f.detection, "sovereignty", "unknown") for f in fs}))
        lines.append(f"[{mark}] {kb.name(pid)}{tag} -> {js} | sovereignty: {sovs}")
        for f in fs:
            d = f.detection
            lines.append(f"        {d.file}:{d.line} ({d.kind}: {d.evidence})")
            for r in f.reasons:
                lines.append(f"           ! {REASON.get(r, r)}")
            if f.severity == "waived":
                lines.append(f"           ~ waived: {d.waiver}")
    fails = sum(f.severity == "fail" for f in findings)
    warns = sum(f.severity == "warn" for f in findings)
    waived = sum(f.severity == "waived" for f in findings)
    lines.append("")
    tags = _regimes(findings, policy)
    if tags:
        lines.append(f"Regimes implicated: {', '.join(tags)}")
    for r in _arrangements(findings, policy):
        lines.append(f"Reference: {r}")
    lines.append(f"Summary: {fails} fail, {warns} warn, {waived} waived, {len(findings) - fails - warns - waived} ok")
    return "\n".join(lines)


def as_json(findings, kb, policy=None) -> str:
    return json.dumps({
        "findings": [{"provider": f.detection.provider_id, "name": kb.name(f.detection.provider_id),
                      "category": kb.category(f.detection.provider_id),
                      "jurisdiction": f.detection.jurisdiction,
                      "sovereignty": getattr(f.detection, "sovereignty", "unknown"),
                      "severity": f.severity, "reasons": f.reasons,
                      "kind": f.detection.kind, "evidence": f.detection.evidence,
                      "file": f.detection.file, "line": f.detection.line,
                      "waiver": f.detection.waiver} for f in findings],
        "regimes": _regimes(findings, policy),
        "references": _arrangements(findings, policy),
    }, indent=2)


def _mlabel(s: str) -> str:
    """A Mermaid label: double-quoted and entity-escaped (# before ", as the quote escape adds a #)."""
    return '"' + s.replace("#", "#35;").replace('"', "#quot;") + '"'


def _pyproject_nv(path: str):
    """(name, version) from a PEP 621 pyproject `[project]` table — tomllib if present, else a regex."""
    try:
        import tomllib
        with open(path, "rb") as fh:
            proj = tomllib.load(fh).get("project", {})
        return proj.get("name"), proj.get("version")
    except ModuleNotFoundError:
        pass  # Python 3.10 — fall back to the regex below
    except (OSError, ValueError):
        return None, None
    try:
        src = open(path, encoding="utf-8").read()
    except OSError:
        return None, None
    m = re.search(r"(?ms)^\[project\](.*?)(?=^\[|\Z)", src)
    if not m:
        return None, None
    block = m.group(1)
    def field(k):
        fm = re.search(rf'(?m)^[ \t]*{k}[ \t]*=[ \t]*["\']([^"\']+)["\']', block)
        return fm.group(1) if fm else None
    return field("name"), field("version")


def _manifest(root: str):
    """(name, version) from the scan root's pyproject `[project]` or package.json; same manifest for both."""
    py = os.path.join(root, "pyproject.toml")
    if os.path.isfile(py):
        n, v = _pyproject_nv(py)
        if n or v:
            return n, v
    pj = os.path.join(root, "package.json")
    if os.path.isfile(pj):
        try:
            with open(pj, encoding="utf-8") as fh:
                d = json.load(fh)
            if isinstance(d, dict):
                return d.get("name"), d.get("version")
        except (OSError, ValueError):
            pass
    return None, None


def _git_tag(root: str):
    try:  # best-effort: git absent / not a repo / no tags / timeout -> None, never fails the scan
        # The scanned repo may be untrusted; -c overrides neutralise its .git/config (a malicious
        # core.fsmonitor / hooksPath is an RCE vector). GIT_OPTIONAL_LOCKS=0 avoids index writes.
        r = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null",
             "-C", root, "describe", "--tags", "--abbrev=0"],
            capture_output=True, text=True, timeout=2,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
        out = r.stdout.strip()
        return out if r.returncode == 0 and out else None
    except Exception:
        return None


def project_label(root) -> str:
    """Codebase label for the Mermaid root node: name@version where determinable, else the directory name."""
    base = os.path.abspath(str(root))
    if not os.path.isdir(base):
        base = os.path.dirname(base)
    name, mver = _manifest(base)
    if not name:
        name = os.path.basename(base) or None
    if not name:
        return "Your application"
    ver = _git_tag(base) or mver
    label = f"{name}@{ver}" if ver else str(name)
    return " ".join(label.split())  # collapse to a single line


def mermaid(findings, kb, policy=None, app_label="Your application") -> str:
    by_j = {}
    sov_by_pj = {}  # (provider, jurisdiction) → sovereignty bloc, for the node label
    for f in findings:
        by_j.setdefault(f.detection.jurisdiction, set()).add(f.detection.provider_id)
        sov_by_pj[(f.detection.provider_id, f.detection.jurisdiction)] = getattr(
            f.detection, "sovereignty", "unknown")
    lines = ["flowchart LR", f"  app([{_mlabel(app_label)}])"]
    for j, pids in by_j.items():
        js = j.replace("-", "_")
        lines.append(f"  subgraph j_{js}[{_mlabel(j)}]")  # zone titled by the jurisdiction code
        for pid in sorted(pids):
            bloc = sov_by_pj.get((pid, j), "unknown")
            lines.append(f"    {pid}__{js}[{_mlabel(f'{kb.name(pid)} ({sov(bloc)})')}]")  # sovereignty appended
        lines.append("  end")
        for pid in sorted(pids):
            lines.append(f"  app --> {pid}__{js}")
    return "\n".join(lines)


_SARIF_LEVEL = {"fail": "error", "warn": "warning", "waived": "note", "ok": "note"}


def sarif(findings, kb, policy=None) -> str:
    """SARIF 2.1.0 — one result per finding; waived results are note + suppressed."""
    results = []
    for f in findings:
        d = f.detection
        detail = REASON.get(f.reasons[0], "") if f.reasons else "allowed"
        result = {
            "ruleId": f.reasons[0] if f.reasons else "ai-data-flow",
            "level": _SARIF_LEVEL[f.severity],
            "message": {"text": f"{kb.name(d.provider_id)} -> {juris(d.jurisdiction)} (sovereignty {sov(getattr(d, 'sovereignty', 'unknown'))}): {detail}"},
            "locations": [{"physicalLocation": {
                "artifactLocation": {"uri": d.file},
                "region": {"startLine": d.line}}}],
        }
        if f.severity == "waived":
            result["suppressions"] = [{"kind": "inSource", "justification": d.waiver or ""}]
        results.append(result)
    return json.dumps({
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "borderlint",
                                "informationUri": "https://github.com/iolairus/borderlint"}},
            "results": results,
        }],
    }, indent=2)


def sbom(findings, kb, policy=None) -> str:
    """Deterministic, policy-independent AI data-flow inventory — severity-free; basis for diff (D6)."""
    from . import __version__
    by = {}
    for f in findings:
        by.setdefault(f.detection.provider_id, []).append(f.detection)
    components = []
    for pid in sorted(by):
        ds = by[pid]
        sites = sorted(
            ({"file": d.file, "line": d.line, "kind": d.kind, "evidence": d.evidence,
              "jurisdiction": d.jurisdiction,
              "sovereignty": getattr(d, "sovereignty", "unknown")} for d in ds),
            key=lambda s: (s["file"], s["line"], s["kind"], s["evidence"]))
        components.append({"provider": pid, "name": kb.name(pid), "category": kb.category(pid),
                           "jurisdictions": sorted({d.jurisdiction for d in ds}),
                           "sovereignties": sorted({getattr(d, "sovereignty", "unknown") for d in ds}),
                           "sites": sites})
    return json.dumps({
        "schema": "borderlint.ai-dataflow-sbom/1",
        "borderlint": __version__,
        "kb_updated": kb.updated,
        "components": components,
    }, indent=2, sort_keys=True)


def _flows(doc) -> dict:
    """{(provider id, jurisdiction): display name} for every flow in an SBOM document."""
    out = {}
    for c in doc.get("components", []):
        for j in c.get("jurisdictions", []):
            out[(c["provider"], j)] = c.get("name", c["provider"])
    return out


def diff_flows(old: dict, new: dict) -> dict:
    """Flows added/removed between two AI data-flow SBOMs, at (provider id, jurisdiction) granularity."""
    o, n = _flows(old), _flows(new)
    rows = lambda keys, names: [{"provider": p, "jurisdiction": j, "name": names[(p, j)]}
                                for p, j in sorted(keys)]
    return {"added": rows(set(n) - set(o), n), "removed": rows(set(o) - set(n), o)}


def diff_text(delta: dict) -> str:
    a, r = delta["added"], delta["removed"]
    if not a and not r:
        return "borderlint diff: no AI data-flow changes."
    lines = ["borderlint diff — AI data-flow changes", "=" * 38]
    lines += [f"  + added:   {f['name']} -> {juris(f['jurisdiction'])}" for f in a]
    lines += [f"  - removed: {f['name']} -> {juris(f['jurisdiction'])}" for f in r]
    lines.append(f"Summary: {len(a)} added, {len(r)} removed")
    return "\n".join(lines)


def diff_json(delta: dict) -> str:
    return json.dumps(delta, indent=2, sort_keys=True)
