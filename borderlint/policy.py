"""Load a residency policy and evaluate detections (deny-by-default)."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field

_JURIS_ALIAS = {"uk": "gb"}  # `.uk` is the ccTLD for ISO-3166 `GB`


def _alias(j):
    """Normalise a jurisdiction token (currently only uk -> gb)."""
    return _JURIS_ALIAS.get(j, j)


def _valid_home(j: str) -> bool:
    """Format check for a home_location: a recognised special token or a ccTLD/ISO code."""
    return j in ("CN-GBA", "GBA") or (len(j) == 2 and j.isalpha() and j.islower())


@dataclass
class Finding:
    detection: object
    severity: str  # "ok" | "warn" | "fail"
    reasons: list = field(default_factory=list)


def load_policy(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    # Shorthand: a bare {classification: [jurisdictions]} map is the classifications block.
    if "classifications" not in data and data and all(isinstance(v, list) for v in data.values()):
        data = {"classifications": data}
    loc = data.get("home_location")
    if loc is not None:  # normalise + format-check; never fails (home_location is informational only)
        loc = _alias(loc)
        data["home_location"] = loc
        if not _valid_home(loc):
            print(f"warning: home_location '{loc}' is not a recognised jurisdiction code; "
                  "regime tags and arrangement references will be omitted", file=sys.stderr)
    return data


def _allowed(allow: list[str]) -> set[str]:
    s = {_alias(x) for x in allow}  # uk -> gb so a `uk` allow-list entry matches a `gb` flow
    if "GBA" in s:  # GBA alias = hk + the nine Mainland GBA cities
        s.update({"hk", "CN-GBA"})
    return s


def evaluate(detections, policy: dict, classification: str, kb=None) -> list[Finding]:
    classes = policy.get("classifications", {})
    if classification not in classes:
        raise KeyError(f"classification '{classification}' not defined in policy")
    allow = _allowed(classes[classification])
    deny = set(policy.get("providers", {}).get("deny", []))
    prov_allow = set(policy.get("providers", {}).get("allow", []))
    on_unknown = policy.get("on_unknown", "warn")
    fail_on = set(policy.get("fail_on", ["residency", "denied_provider"]))

    findings = []
    for d in detections:
        reasons = []
        if d.provider_id in deny or (prov_allow and d.provider_id not in prov_allow):
            reasons.append("denied_provider")
        if d.jurisdiction == "unknown":
            reasons.append("unknown")
        elif d.jurisdiction == "local":
            pass  # local inference is not a cross-border transfer; never a residency violation
        elif d.jurisdiction not in allow:
            reasons.append("residency")
        sev = _severity(reasons, fail_on, on_unknown)
        if sev == "fail" and d.waiver:  # a justified waiver downgrades a residency/unknown failure
            blocking = "denied_provider" in reasons and "denied_provider" in fail_on
            if not blocking:  # ...but never an explicit provider deny
                sev = "waived"
        findings.append(Finding(d, sev, reasons))
    return findings


def _severity(reasons: list[str], fail_on: set[str], on_unknown: str) -> str:
    if not reasons:
        return "ok"
    fail = (("denied_provider" in reasons and "denied_provider" in fail_on)
            or ("residency" in reasons and "residency" in fail_on)
            or ("unknown" in reasons and on_unknown == "fail"))
    return "fail" if fail else "warn"
