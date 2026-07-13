"""Render findings as text, JSON, or a Mermaid flow map (grouped by jurisdiction)."""

from __future__ import annotations

import json
import os
import re
import subprocess
from html import escape as _escape

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
          "sovereignty_unknown": "sovereignty could not be determined",
          "provenance": "model provenance outside the allow-list for this data class",
          "provenance_unknown": "model provenance could not be determined",
          "model_denied": "model family is on the policy deny list"}
SOVEREIGNTY = {"us": "United States", "eu": "European Union", "cn": "Mainland China",
               "uk": "United Kingdom", "ru": "Russia", "in": "India", "il": "Israel",
               "ca": "Canada", "jp": "Japan", "kr": "South Korea", "sg": "Singapore",
               "au": "Australia", "ae": "UAE", "ch": "Switzerland", "local": "Local", "unknown": "Unknown"}
_RANK = {"ok": 0, "waived": 1, "warn": 2, "fail": 3}

with open(os.path.join(os.path.dirname(__file__), "data", "arrangements.json"), encoding="utf-8") as _fh:
    _ARRANGEMENTS = {a["id"]: a for a in json.load(_fh)["arrangements"]}
with open(os.path.join(os.path.dirname(__file__), "data", "regimes.json"), encoding="utf-8") as _fh:
    _REGIMES = json.load(_fh)["regimes"]  # jurisdiction -> {regime, arrangements[]}
with open(os.path.join(os.path.dirname(__file__), "data", "evidence_regimes.json"), encoding="utf-8") as _fh:
    _EVIDENCE = json.load(_fh)  # regime display string -> filing expectations (advisory)
# EU/EEA jurisdictions that trigger the GDPR reference (the `eu` token + member country codes).
_EU = frozenset("eu at be bg hr cy cz dk ee fi fr de gr hu ie it lv lt lu mt nl pl pt ro sk si es se is li no".split())


def juris(j: str) -> str:
    return JURIS.get(j, j)


def sov(b: str) -> str:
    """Display label for a sovereignty or provenance bloc (shared vocabulary)."""
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


def _arrangement_ids(findings, policy) -> list[str]:
    """Cross-border arrangement id(s) for flagged flows — context only, never adjudicated."""
    policy = policy or {}
    dests = _flagged_dests(findings)
    loc = _alias(policy.get("home_location")) if policy.get("home_location") else None
    if loc:  # home-location path: GBA span + destination specials, then home-driven refs from the map
        span = {loc} | dests
        out = []
        if {"hk", "CN-GBA"} <= span:
            out.append("gba")
        if {"mo", "CN-GBA"} <= span:
            out.append("gba_mo")
        if "cn" in dests or (loc == "CN-GBA" and dests - {"cn", "CN-GBA", "hk", "mo"}):
            out.append("pipl")
        if dests & _EU:
            out.append("gdpr")
        for aid in _REGIMES.get(loc, {}).get("arrangements", []):  # seeded empty for hk/mo/cn/CN-GBA
            if aid not in out:
                out.append(aid)
        return out
    # legacy home_regime path — unchanged
    regime = policy.get("home_regime")
    out = []
    if "CN-GBA" in dests and regime in ("pdpo", "pipl"):  # HK <-> nine GBA cities, not plain cn
        out.append("gba")
    if "cn" in dests or (regime == "pipl" and dests - {"cn", "CN-GBA", "hk"}):
        out.append("pipl")
    if dests & _EU:
        out.append("gdpr")
    return out


def _arrangements(findings, policy) -> list[str]:
    """Cross-border arrangement reference(s) for flagged flows — context only, never adjudicated."""
    return [_ref(aid) for aid in _arrangement_ids(findings, policy)]


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
        provs = ", ".join(sov(x) for x in sorted({getattr(f.detection, "provenance", "unknown") for f in fs}))
        lines.append(f"[{mark}] {kb.name(pid)}{tag} -> {js} | sovereignty: {sovs} | weights: {provs}")
        for f in fs:
            d = f.detection
            model = getattr(d, "model", None)
            org = getattr(d, "model_org", None)
            label = f"{model} — {org}" if model and org else model
            suffix = f" [model: {label}]" if model and d.kind != "model_reference" else ""
            lines.append(f"        {d.file}:{d.line} ({d.kind}: {d.evidence}){suffix}")
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
                      "provenance": getattr(f.detection, "provenance", "unknown"),
                      "model": getattr(f.detection, "model", None),
                      "model_org": getattr(f.detection, "model_org", None),
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
    prov_by_pj = {}  # (provider, jurisdiction) → provenance bloc, shown when it differs
    for f in findings:
        by_j.setdefault(f.detection.jurisdiction, set()).add(f.detection.provider_id)
        sov_by_pj[(f.detection.provider_id, f.detection.jurisdiction)] = getattr(
            f.detection, "sovereignty", "unknown")
        prov_by_pj[(f.detection.provider_id, f.detection.jurisdiction)] = getattr(
            f.detection, "provenance", "unknown")
    lines = ["flowchart LR", f"  app([{_mlabel(app_label)}])"]
    for j, pids in by_j.items():
        js = j.replace("-", "_")
        lines.append(f"  subgraph j_{js}[{_mlabel(j)}]")  # zone titled by the jurisdiction code
        for pid in sorted(pids):
            bloc = sov_by_pj.get((pid, j), "unknown")
            pb = prov_by_pj.get((pid, j), "unknown")
            # provenance appended only when it diverges from sovereignty — the interesting case
            label = f"{kb.name(pid)} ({sov(bloc)}, weights {sov(pb)})" if pb not in (bloc, "unknown") \
                else f"{kb.name(pid)} ({sov(bloc)})"
            lines.append(f"    {pid}__{js}[{_mlabel(label)}]")
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
            "message": {"text": f"{kb.name(d.provider_id)} -> {juris(d.jurisdiction)} (sovereignty {sov(getattr(d, 'sovereignty', 'unknown'))}, weights {sov(getattr(d, 'provenance', 'unknown'))}): {detail}"},
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
              "sovereignty": getattr(d, "sovereignty", "unknown"),
              "provenance": getattr(d, "provenance", "unknown"),
              "model": getattr(d, "model", None),
              "model_org": getattr(d, "model_org", None)} for d in ds),
            key=lambda s: (s["file"], s["line"], s["kind"], s["evidence"]))
        components.append({"provider": pid, "name": kb.name(pid), "category": kb.category(pid),
                           "jurisdictions": sorted({d.jurisdiction for d in ds}),
                           "sovereignties": sorted({getattr(d, "sovereignty", "unknown") for d in ds}),
                           "provenances": sorted({getattr(d, "provenance", "unknown") for d in ds}),
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


_HTML_STYLE = """\
body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;margin:2rem auto;max-width:62rem;padding:0 1rem;color:#1a1a1a}
h1{font-size:1.4rem}h2{font-size:1.1rem;margin-top:1.6rem}
table{border-collapse:collapse;width:100%;font-size:.9rem;margin:.4rem 0}
th,td{border:1px solid #ccc;padding:.35rem .5rem;text-align:left;vertical-align:top}
th{background:#f5f5f5}
table.meta{width:auto}
code{font-family:ui-monospace,monospace;font-size:.85em}
.chip{padding:.1rem .45rem;border-radius:.6rem;font-weight:600;font-size:.8rem}
.chip.fail{background:#fdd;color:#900}.chip.warn{background:#fe9;color:#850}
.chip.waived{background:#eee;color:#555}.chip.ok{background:#dfd;color:#060}
tr.reasons td{border-top:0;color:#900;font-size:.85rem}"""


def html(findings, kb, policy=None, envelope=None) -> str:
    """Self-contained HTML report for review conversations — fetches nothing, runs nothing.

    An artifact, not a gate (paired with exit 0 in the CLI). Every repo/KB-derived string is
    escaped: scanned source must not be able to inject markup into the report. Not a filing
    format — the markdown evidence pack remains the filing artifact.
    """
    env = envelope or {}
    pol = policy or {}
    has_policy = bool(pol)
    e = lambda v: _escape(str(v), quote=True)
    ua = lambda v: e(v) if v else "unavailable"
    title = "borderlint — AI data-flow &amp; residency report"
    out = ["<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           f"<title>{title}</title>", "<style>", _HTML_STYLE, "</style>", "</head>", "<body>",
           f"<h1>{title}</h1>"]

    rows = [("Tool", "borderlint " + ua(env.get("version"))),
            ("KB last reviewed", "providers " + ua(env.get("kb_providers"))
             + " / sovereignty " + ua(env.get("kb_sovereignty"))
             + " / provenance " + ua(env.get("kb_provenance"))),
            ("Scan timestamp (UTC)", ua(env.get("timestamp"))),
            ("Scanned path", ua(env.get("path"))),
            ("Git commit", ua(env.get("commit")))]
    if has_policy:
        rows += [("Policy SHA-256", ua(env.get("policy_digest"))),
                 ("Classification", ua(env.get("classification"))),
                 ("Home location", ua(pol.get("home_location")))]
    out.append('<table class="meta">')
    out += [f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows]  # values escaped above
    out.append("</table>")

    if not findings:
        out.append("<p>No AI provider usage detected.</p>")
    else:
        by = {}
        for f in findings:
            by.setdefault(f.detection.jurisdiction, []).append(f)
        ncols = 8 if has_policy else 7
        for j in sorted(by):
            out.append(f"<h2>{e(juris(j))} <code>{e(j)}</code></h2>")
            out.append("<table>")
            head = "<th>Provider</th><th>Residency</th><th>Sovereignty</th><th>Weights</th><th>Model</th><th>Location</th><th>Evidence</th>"
            out.append("<tr>" + ("<th>Severity</th>" if has_policy else "") + head + "</tr>")
            for f in by[j]:
                d = f.detection
                model = getattr(d, "model", None)
                org = getattr(d, "model_org", None)
                mlabel = (f"{model} — {org}" if org else model) if model else "—"
                cat = kb.category(d.provider_id)
                plabel = f"{kb.name(d.provider_id)} ({cat})" if cat else kb.name(d.provider_id)
                cells = [f'<td><span class="chip {e(f.severity)}">{e(f.severity)}</span></td>'] if has_policy else []
                cells += [f"<td>{e(plabel)}</td>", f"<td>{e(juris(d.jurisdiction))}</td>",
                          f"<td>{e(sov(getattr(d, 'sovereignty', 'unknown')))}</td>",
                          f"<td>{e(sov(getattr(d, 'provenance', 'unknown')))}</td>",
                          f"<td>{e(mlabel)}</td>",
                          f"<td><code>{e(d.file)}:{d.line}</code></td>",
                          f"<td><code>{e(d.kind)}: {e(d.evidence)}</code></td>"]
                out.append("<tr>" + "".join(cells) + "</tr>")
                if f.reasons:
                    reasons = "; ".join(e(REASON.get(r, r)) for r in f.reasons)
                    out.append(f'<tr class="reasons"><td colspan="{ncols}">! {reasons}</td></tr>')
            out.append("</table>")

    waived = [f for f in findings if f.severity == "waived"]
    if waived:
        out.append("<h2>Waiver register</h2>")
        out.append("<ul>")
        for f in waived:
            d = f.detection
            out.append(f"<li><code>{e(d.file)}:{d.line}</code> ({e(kb.name(d.provider_id))}) — {e(d.waiver)}</li>")
        out.append("</ul>")

    regs = _regimes(findings, pol)
    aids = _arrangement_ids(findings, pol)
    if regs or aids:
        out.append("<h2>Cross-border context (references only)</h2>")
        if regs:
            out.append(f"<p>Regimes implicated: {e(', '.join(regs))}</p>")
        if aids:
            out.append("<ul>")
            for aid in aids:
                a = _ARRANGEMENTS[aid]
                out.append(f'<li><a href="{e(a["url"])}">{e(a["name"])}</a> — {e(a["summary"])}</li>')
            out.append("</ul>")

    if has_policy and findings:
        fails = sum(f.severity == "fail" for f in findings)
        warns = sum(f.severity == "warn" for f in findings)
        n_waived = len(waived)
        oks = len(findings) - fails - warns - n_waived
        out.append(f"<p>Summary: {fails} fail, {warns} warn, {n_waived} waived, {oks} ok</p>")

    out += ["</body>", "</html>"]
    return "\n".join(out)


def evidence(findings, kb, policy=None, envelope=None) -> str:
    """Markdown evidence pack: audit envelope, transfer inventory, waiver register, regime annex.

    An artifact, not a gate (always paired with exit 0 in the CLI). Unresolvable envelope
    fields render as 'unavailable' — an auditor must be able to tell absent from forgotten.
    """
    env = envelope or {}
    pol = policy or {}
    ua = lambda v: v if v else "unavailable"
    has_policy = bool(pol)
    out = ["# AI data-flow evidence pack", "", "## Audit envelope", ""]
    out += [f"- Tool: borderlint {ua(env.get('version'))}",
            "- KB last reviewed: providers " + ua(env.get("kb_providers"))
            + " / sovereignty " + ua(env.get("kb_sovereignty"))
            + " / provenance " + ua(env.get("kb_provenance")),
            f"- Scan timestamp (UTC): {ua(env.get('timestamp'))}",
            f"- Scanned path: {ua(env.get('path'))}",
            f"- Git commit: {ua(env.get('commit'))}",
            f"- Policy SHA-256: {ua(env.get('policy_digest'))}",
            f"- Classification: {ua(env.get('classification'))}",
            f"- Home location: {ua(pol.get('home_location'))}", ""]

    out += ["## Transfer inventory", ""]
    if not findings:
        out += ["No AI data flows detected.", ""]
    else:
        head = "| # | Provider (category) | Residency | Sovereignty | Weights | Model | Verdict |"
        if not has_policy:
            head = head.replace(" Verdict |", " — |")
        out += [head, "|---|---|---|---|---|---|---|"]
        for i, f in enumerate(findings, 1):
            d = f.detection
            model = d.model or "—"
            if d.model and getattr(d, "model_org", None):
                model = f"{d.model} ({d.model_org})"
            verdict = f.severity if has_policy else "—"
            out.append(f"| {i} | {kb.name(d.provider_id)} ({kb.category(d.provider_id)}) "
                       f"| {juris(d.jurisdiction)} | {sov(d.sovereignty)} | {sov(d.provenance)} "
                       f"| {model} | {verdict} |")
        out += ["", "### Code locations", ""]
        for i, f in enumerate(findings, 1):
            d = f.detection
            reasons = ("; ".join(REASON.get(r, r) for r in f.reasons)) if f.reasons else ""
            out.append(f"{i}. `{d.file}:{d.line}` ({d.kind}: {d.evidence})"
                       + (f" — {reasons}" if reasons else ""))
        out.append("")

    waived = [f for f in findings if f.severity == "waived"]
    out += ["## Waiver register", ""]
    if waived:
        for f in waived:
            d = f.detection
            out.append(f"- `{d.file}:{d.line}` ({kb.name(d.provider_id)}) — {d.waiver}")
    else:
        out.append("No active waivers.")
    out.append("")

    if has_policy:
        counts = {}
        for f in findings:
            counts[f.severity] = counts.get(f.severity, 0) + 1
        out += ["## Summary", "",
                " / ".join(f"{counts.get(k, 0)} {k}" for k in ("ok", "warn", "fail", "waived")), ""]
        refs = _arrangements(findings, pol)
        regs = _regimes(findings, pol)
        if regs or refs:
            out += ["## Cross-border context (references only)", ""]
            out += [f"- Regimes in play: {', '.join(regs)}"] if regs else []
            out += [f"- {r}" for r in refs] + [""]

    loc = _alias(pol["home_location"]) if pol.get("home_location") else None
    if loc:
        regime = regime_of(loc)
        entry = _EVIDENCE["regimes"].get(regime or "")
        if entry:
            out += [f"## Regime annex — {entry['heading']}", "",
                    f"_Expectations data last reviewed {_EVIDENCE.get('updated', 'unavailable')}."
                    " References only; this annex never adjudicates filing sufficiency._", "",
                    "**Citations**", ""]
            out += [f"- {c}" for c in entry["citations"]]
            out += ["", "**Filled from this scan (static)**", ""]
            dests = sorted({f.detection.jurisdiction for f in findings})
            sovs = sorted({f.detection.sovereignty for f in findings})
            provs = sorted({f.detection.provenance for f in findings})
            orgs = sorted({f.detection.model_org for f in findings if getattr(f.detection, "model_org", None)})
            filled = {"destination jurisdictions": ", ".join(juris(d) for d in dests) or "none",
                      "compelled-disclosure (sovereignty) blocs": ", ".join(sov(b) for b in sovs) or "none",
                      "model provenance blocs and developer organisations":
                          (", ".join(sov(b) for b in provs) or "none")
                          + (f" — orgs: {', '.join(orgs)}" if orgs else ""),
                      "transfer mechanism references": "see Cross-border context above",
                      "code locations": "see Transfer inventory above"}
            for field in entry["static"]:
                if field.startswith("data classification"):
                    out.append(f"- {field}: {env.get('classification') or 'unavailable'}")
                else:
                    out.append(f"- {field}: {filled.get(field, 'see Transfer inventory above')}")
            out += ["", "**To be completed by the organisation**", ""]
            out += [f"- [ ] {field}: ________" for field in entry["org"]]
            out.append("")
        else:
            out += ["## Regime annex", "",
                    f"No annex is available for regime {regime or 'unknown'}; the inventory above stands alone.", ""]
    return "\n".join(out)
