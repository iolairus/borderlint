"""Render findings as text, JSON, or a Mermaid flow map (grouped by jurisdiction)."""

from __future__ import annotations

import json
import os

JURIS = {"us": "United States", "eu": "European Union", "cn": "Mainland China", "hk": "Hong Kong",
         "sg": "Singapore", "gb": "United Kingdom", "mo": "Macao", "my": "Malaysia",
         "CN-GBA": "Mainland GBA", "GBA": "Greater Bay Area", "unknown": "Unknown (region-dependent)"}
REASON = {"denied_provider": "provider denied by policy",
          "residency": "jurisdiction outside the allow-list for this data class",
          "unknown": "jurisdiction could not be determined"}
_RANK = {"ok": 0, "waived": 1, "warn": 2, "fail": 3}

with open(os.path.join(os.path.dirname(__file__), "data", "arrangements.json"), encoding="utf-8") as _fh:
    _ARRANGEMENTS = {a["id"]: a for a in json.load(_fh)["arrangements"]}
# EU/EEA jurisdictions that trigger the GDPR reference (the `eu` token + member country codes).
_EU = frozenset("eu at be bg hr cy cz dk ee fi fr de gr hu ie it lv lt lu mt nl pl pt ro sk si es se is li no".split())


def juris(j: str) -> str:
    return JURIS.get(j, j)


def _ref(aid: str) -> str:
    a = _ARRANGEMENTS[aid]
    return f"{a['name']} — {a['summary']} {a['url']}"


def _arrangements(findings, policy) -> list[str]:
    """Cross-border arrangement reference(s) for flagged flows — context only, never adjudicated."""
    regime = (policy or {}).get("home_regime")
    dests = {f.detection.jurisdiction for f in findings if f.severity != "ok"}
    out = []
    if "CN-GBA" in dests and regime in ("pdpo", "pipl"):  # HK <-> nine GBA cities, not plain cn
        out.append(_ref("gba"))
    if "cn" in dests or (regime == "pipl" and dests - {"cn", "CN-GBA", "hk"}):
        out.append(_ref("pipl"))
    if dests & _EU:
        out.append(_ref("gdpr"))
    return out


def _regimes(findings, policy) -> list[str]:
    """Data-protection regime tag(s) implicated by a flagged flow — set {PDPO, PIPL}, informational."""
    dests = {f.detection.jurisdiction for f in findings if f.severity != "ok"}
    if not dests:
        return []
    regime = (policy or {}).get("home_regime")
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
        lines.append(f"[{mark}] {kb.name(pid)} -> {js}")
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
                      "jurisdiction": f.detection.jurisdiction, "severity": f.severity, "reasons": f.reasons,
                      "kind": f.detection.kind, "evidence": f.detection.evidence,
                      "file": f.detection.file, "line": f.detection.line,
                      "waiver": f.detection.waiver} for f in findings],
        "regimes": _regimes(findings, policy),
        "references": _arrangements(findings, policy),
    }, indent=2)


def mermaid(findings, kb, policy=None) -> str:
    by_j = {}
    for f in findings:
        by_j.setdefault(f.detection.jurisdiction, set()).add(f.detection.provider_id)
    lines = ["flowchart LR", "  app([Your application])"]
    for j, pids in by_j.items():
        jid = "j_" + j.replace("-", "_")
        lines.append(f"  subgraph {jid}[{juris(j)}]")
        for pid in sorted(pids):
            lines.append(f"    {pid}[{kb.name(pid)}]")
        lines.append("  end")
        for pid in sorted(pids):
            lines.append(f"  app --> {pid}")
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
            "message": {"text": f"{kb.name(d.provider_id)} -> {juris(d.jurisdiction)}: {detail}"},
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
              "jurisdiction": d.jurisdiction} for d in ds),
            key=lambda s: (s["file"], s["line"], s["kind"], s["evidence"]))
        components.append({"provider": pid, "name": kb.name(pid),
                           "jurisdictions": sorted({d.jurisdiction for d in ds}), "sites": sites})
    return json.dumps({
        "schema": "borderlint.ai-dataflow-sbom/1",
        "borderlint": __version__,
        "kb_updated": kb.updated,
        "components": components,
    }, indent=2, sort_keys=True)
