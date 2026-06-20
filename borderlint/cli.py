"""borderlint command-line interface."""

from __future__ import annotations

import argparse
import sys

from . import report
from .detect import scan
from .kb import load_kb
from .policy import Finding, evaluate, load_policy


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="borderlint", description="Map and govern where your AI data flows.")
    ap.add_argument("--version", action="store_true", help="print version and KB last-reviewed date")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("scan", help="Scan a path for AI data flows and check a residency policy.")
    s.add_argument("path", nargs="?", default=".")
    s.add_argument("-p", "--policy", help="residency policy JSON (omit for inventory mode)")
    s.add_argument("-c", "--classification", help="data class on the scanned path (required with --policy)")
    s.add_argument("-f", "--format", choices=["text", "json", "mermaid", "sarif", "sbom"], default="text")
    s.add_argument("--providers", help="custom provider knowledge base JSON")
    a = ap.parse_args(argv)

    if a.version:
        from . import __version__
        print(f"borderlint {__version__} (KB last reviewed {load_kb().updated})")
        return 0
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

    renderers = {"text": report.text, "json": report.as_json, "mermaid": report.mermaid,
                 "sarif": report.sarif, "sbom": report.sbom}
    print(renderers[a.format](findings, kb, policy))
    if a.format == "sbom":  # an export is an artifact, not a gate
        return 0
    return 1 if any(f.severity == "fail" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
