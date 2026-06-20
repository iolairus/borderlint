"""Load a residency policy and evaluate detections (deny-by-default)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field


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
    return data


def _allowed(allow: list[str]) -> set[str]:
    s = set(allow)
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
        findings.append(Finding(d, _severity(reasons, fail_on, on_unknown), reasons))
    return findings


def _severity(reasons: list[str], fail_on: set[str], on_unknown: str) -> str:
    if not reasons:
        return "ok"
    fail = (("denied_provider" in reasons and "denied_provider" in fail_on)
            or ("residency" in reasons and "residency" in fail_on)
            or ("unknown" in reasons and on_unknown == "fail"))
    return "fail" if fail else "warn"
