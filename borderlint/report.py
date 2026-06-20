"""Render findings as text, JSON, or a Mermaid flow map (grouped by jurisdiction)."""

from __future__ import annotations

import json

JURIS = {"us": "United States", "eu": "European Union", "cn": "Mainland China", "hk": "Hong Kong",
         "sg": "Singapore", "gb": "United Kingdom", "mo": "Macao", "my": "Malaysia",
         "CN-GBA": "Mainland GBA", "GBA": "Greater Bay Area", "unknown": "Unknown (region-dependent)"}
REASON = {"denied_provider": "provider denied by policy",
          "residency": "jurisdiction outside the allow-list for this data class",
          "unknown": "jurisdiction could not be determined"}
GBA_REF = ("GBA Standard Contract — https://www.digitalpolicy.gov.hk/en/our_work/"
           "digital_infrastructure/mainland/gbacbdf/cross-boundary_data_flow/index.html")
_RANK = {"ok": 0, "warn": 1, "fail": 2}


def juris(j: str) -> str:
    return JURIS.get(j, j)


def _arrangements(findings, policy) -> list[str]:
    regime = (policy or {}).get("home_regime")
    flagged_china = any(f.severity != "ok" and f.detection.jurisdiction in ("cn", "CN-GBA") for f in findings)
    if regime in ("pdpo", "pipl") and flagged_china:
        return [f"Reference ({regime}): {GBA_REF}"]
    return []


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
        mark = {"ok": " OK ", "warn": "WARN", "fail": "FAIL"}[worst]
        js = ", ".join(juris(x) for x in sorted({f.detection.jurisdiction for f in fs}))
        lines.append(f"[{mark}] {kb.name(pid)} -> {js}")
        for f in fs:
            d = f.detection
            lines.append(f"        {d.file}:{d.line} ({d.kind}: {d.evidence})")
            for r in f.reasons:
                lines.append(f"           ! {REASON.get(r, r)}")
    fails = sum(f.severity == "fail" for f in findings)
    warns = sum(f.severity == "warn" for f in findings)
    lines.append("")
    lines += _arrangements(findings, policy)
    lines.append(f"Summary: {fails} fail, {warns} warn, {len(findings) - fails - warns} ok")
    return "\n".join(lines)


def as_json(findings, kb, policy=None) -> str:
    return json.dumps({
        "findings": [{"provider": f.detection.provider_id, "name": kb.name(f.detection.provider_id),
                      "jurisdiction": f.detection.jurisdiction, "severity": f.severity, "reasons": f.reasons,
                      "kind": f.detection.kind, "evidence": f.detection.evidence,
                      "file": f.detection.file, "line": f.detection.line} for f in findings],
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
