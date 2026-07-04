"""Load a residency policy and evaluate detections (deny-by-default)."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field

_JURIS_ALIAS = {"uk": "gb"}  # `.uk` is the ccTLD for ISO-3166 `GB`

# Sovereignty bloc vocabulary (mirrors borderlint.kb._SOVEREIGNTY_BLOCS; duplicated here to
# avoid a circular import — policy must not depend on kb at module load).
_SOVEREIGNTY_BLOCS = frozenset(
    {"us", "eu", "cn", "uk", "ru", "in", "il", "ca", "jp", "kr", "sg", "au", "ae", "local", "unknown"})


def _valid_sovereignty(token: str) -> bool:
    """A sovereignty bloc must be one of the fixed vocabulary."""
    return token in _SOVEREIGNTY_BLOCS


# Provenance bloc vocabulary (mirrors borderlint.kb._PROVENANCE_BLOCS; duplicated for the same
# circular-import reason). The sovereignty vocabulary minus `local` — weights always have a developer.
_PROVENANCE_BLOCS = frozenset(
    {"us", "eu", "cn", "uk", "ru", "in", "il", "ca", "jp", "kr", "sg", "au", "ae", "unknown"})


def _valid_provenance(token: str) -> bool:
    """A provenance bloc must be one of the fixed vocabulary."""
    return token in _PROVENANCE_BLOCS


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
    # Sovereignty block is opt-in. Validate bloc tokens when present; never fails the run on shape.
    sov = data.get("sovereignty")
    if sov and isinstance(sov, dict):
        for cls, blocs in sov.get("classifications", {}).items():
            for b in blocs:
                if not _valid_sovereignty(b):
                    raise ValueError(
                        f"invalid sovereignty bloc '{b}' in classification '{cls}' "
                        "(use one of us, eu, cn, uk, ru, in, il, ca, jp, kr, sg, au, ae, local, unknown)")
    # Provenance block is opt-in. Validate bloc tokens when present, same posture as sovereignty.
    mprov = data.get("provenance")
    if mprov and isinstance(mprov, dict):
        for cls, blocs in mprov.get("classifications", {}).items():
            for b in blocs:
                if not _valid_provenance(b):
                    raise ValueError(
                        f"invalid provenance bloc '{b}' in classification '{cls}' "
                        "(use one of us, eu, cn, uk, ru, in, il, ca, jp, kr, sg, au, ae, unknown)")
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

    # Sovereignty is opt-in: only evaluate when the policy declares a sovereignty block AND a
    # sovereignty allow-list for the active classification. Absent → no sovereignty reason, ever.
    sov_block = policy.get("sovereignty") or {}
    sov_classes = sov_block.get("classifications", {}) if isinstance(sov_block, dict) else {}
    sov_allow = set(sov_classes.get(classification, [])) if classification in sov_classes else None
    sov_on_unknown = sov_block.get("on_unknown", "warn") if isinstance(sov_block, dict) else "warn"

    # Provenance (model weights) is opt-in with the same shape. `mprov` to avoid clashing with the
    # provider allow-list above.
    mprov_block = policy.get("provenance") or {}
    mprov_classes = mprov_block.get("classifications", {}) if isinstance(mprov_block, dict) else {}
    mprov_allow = set(mprov_classes.get(classification, [])) if classification in mprov_classes else None
    mprov_on_unknown = mprov_block.get("on_unknown", "warn") if isinstance(mprov_block, dict) else "warn"

    findings = []
    for d in detections:
        reasons = []
        if d.kind != "model_reference":  # a standalone model reference is a weights signal, not a flow
            if d.provider_id in deny or (prov_allow and d.provider_id not in prov_allow):
                reasons.append("denied_provider")
            if d.jurisdiction == "unknown":
                reasons.append("unknown")
            elif d.jurisdiction == "local":
                pass  # local inference is not a cross-border transfer; never a residency violation
            elif d.jurisdiction not in allow:
                reasons.append("residency")
            # Sovereignty dimension (opt-in): evaluate only when an allow-list is declared for this class.
            if sov_allow is not None:
                sov = getattr(d, "sovereignty", "unknown")
                if sov == "local":
                    pass  # self-hosted → no external sovereign; exempt, mirroring residency `local`
                elif sov == "unknown":
                    reasons.append("sovereignty_unknown")  # governed by sov_on_unknown
                elif sov not in sov_allow:
                    reasons.append("sovereignty")  # an allow-list mismatch
        # Provenance dimension (opt-in): applies to flows and standalone model references alike.
        if mprov_allow is not None:
            mp = getattr(d, "provenance", "unknown")
            if mp == "unknown":
                reasons.append("provenance_unknown")  # governed by mprov_on_unknown
            elif mp not in mprov_allow:
                reasons.append("provenance")  # an allow-list mismatch
        sev = _severity(reasons, fail_on, on_unknown, sov_on_unknown, mprov_on_unknown)
        if sev == "fail" and d.waiver:  # a justified waiver downgrades a residency/unknown/sovereignty failure
            blocking = "denied_provider" in reasons and "denied_provider" in fail_on
            if not blocking:  # ...but never an explicit provider deny
                sev = "waived"
        findings.append(Finding(d, sev, reasons))
    return findings


def _severity(reasons: list[str], fail_on: set[str], on_unknown: str, sov_on_unknown: str = "warn",
              mprov_on_unknown: str = "warn") -> str:
    if not reasons:
        return "ok"
    fail = (("denied_provider" in reasons and "denied_provider" in fail_on)
            or ("residency" in reasons and "residency" in fail_on)
            or ("unknown" in reasons and on_unknown == "fail")
            or ("sovereignty" in reasons and "sovereignty" in fail_on)
            or ("sovereignty_unknown" in reasons and sov_on_unknown == "fail")
            or ("provenance" in reasons and "provenance" in fail_on)
            or ("provenance_unknown" in reasons and mprov_on_unknown == "fail"))
    return "fail" if fail else "warn"
