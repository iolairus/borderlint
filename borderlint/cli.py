"""borderlint command-line interface."""

from __future__ import annotations

import argparse
import json
import sys

from . import report
from .detect import scan
from .kb import load_kb
from .policy import Finding, evaluate, load_policy


def _envelope(a, kb) -> dict:
    """Audit envelope for the evidence pack. Local-only resolution; absent fields stay None
    so the renderer prints 'unavailable' — an auditor must see absence, not silence."""
    import datetime as dt
    import hashlib
    import os
    import subprocess
    from . import __version__
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    ts = (dt.datetime.fromtimestamp(int(epoch), dt.timezone.utc) if epoch
          else dt.datetime.now(dt.timezone.utc))
    commit = None
    try:
        root = a.path if os.path.isdir(a.path) else (os.path.dirname(a.path) or ".")
        r = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=2)
        commit = r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None
    except (OSError, subprocess.SubprocessError):
        commit = None
    digest = None
    if a.policy:
        with open(a.policy, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
    return {"version": __version__, "kb_providers": kb.updated,
            "kb_sovereignty": kb.sovereignty_updated, "kb_provenance": kb.provenance_updated,
            "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ"), "path": a.path,
            "commit": commit, "policy_digest": digest, "classification": a.classification}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="borderlint", description="Map and govern where your AI data flows.")
    ap.add_argument("--version", action="store_true", help="print version and KB last-reviewed date")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("scan", help="Scan a path for AI data flows and check a residency policy.")
    s.add_argument("path", nargs="?", default=".")
    s.add_argument("-p", "--policy", help="residency policy JSON (omit for inventory mode)")
    s.add_argument("-c", "--classification", help="data class on the scanned path (required with --policy)")
    s.add_argument("-f", "--format", choices=["text", "json", "mermaid", "sarif", "sbom", "evidence", "html"], default="text")
    s.add_argument("--providers", help="custom provider knowledge base JSON")
    dp = sub.add_parser("diff", help="Compare two AI data-flow SBOMs (baseline vs current).")
    dp.add_argument("baseline")
    dp.add_argument("current")
    dp.add_argument("-f", "--format", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)

    if a.version:
        from . import __version__
        print(f"borderlint {__version__} (KB last reviewed {load_kb().updated})")
        return 0
    if a.cmd == "diff":
        return _run_diff(a)
    if a.cmd != "scan":
        ap.print_help()
        return 0

    try:
        kb = load_kb(a.providers)
    except (ValueError, OSError) as e:  # bad jurisdiction token / unreadable file (JSONDecodeError is a ValueError)
        print(f"error: {e}", file=sys.stderr)
        return 2
    detections = scan(a.path, kb)

    policy = None
    if a.policy:
        if not a.classification:
            print("error: --classification is required when --policy is given", file=sys.stderr)
            return 2
        policy = load_policy(a.policy)
        try:
            findings = evaluate(detections, policy, a.classification, kb)
        except KeyError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
    else:
        findings = [Finding(d, "ok", []) for d in detections]  # inventory mode

    envelope = _envelope(a, kb) if a.format in ("evidence", "html") else None
    renderers = {"text": report.text, "json": report.as_json,
                 "mermaid": lambda f, k, p: report.mermaid(f, k, p, report.project_label(a.path)),
                 "sarif": report.sarif, "sbom": report.sbom,
                 "evidence": lambda f, k, p: report.evidence(f, k, p, envelope),
                 "html": lambda f, k, p: report.html(f, k, p, envelope)}
    print(renderers[a.format](findings, kb, policy))
    if a.format in ("sbom", "evidence", "html"):  # an export is an artifact, not a gate
        return 0
    return 1 if any(f.severity == "fail" for f in findings) else 0


def _run_diff(a) -> int:
    docs = []
    for path in (a.baseline, a.current):
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except (OSError, ValueError) as e:  # unreadable / not JSON
            print(f"error: {e}", file=sys.stderr)
            return 2
        if not isinstance(doc, dict) or doc.get("schema") != "borderlint.ai-dataflow-sbom/1":
            print(f"error: {path} is not a borderlint AI data-flow SBOM", file=sys.stderr)
            return 2
        docs.append(doc)
    delta = report.diff_flows(docs[0], docs[1])
    print(report.diff_json(delta) if a.format == "json" else report.diff_text(delta))
    return 1 if any(f["jurisdiction"] != "local" for f in delta["added"]) else 0  # new non-local egress gates


if __name__ == "__main__":
    raise SystemExit(main())
