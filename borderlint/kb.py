"""Provider knowledge base: load and resolve a provider/endpoint to a jurisdiction."""

from __future__ import annotations

import json
import re
from importlib.resources import files

# Region-coded endpoints (the host carries the region) → ccTLD jurisdiction.
_AWS_RE = re.compile(r"\b([a-z]{2}(?:-gov)?-[a-z]+-\d)\b")
_AWS_REGION = {
    "ap-east-1": "hk", "ap-east-2": "hk", "cn-north-1": "cn", "cn-northwest-1": "cn",
    "ap-southeast-1": "sg", "ap-southeast-2": "au", "ap-southeast-3": "id",
    "ap-southeast-5": "my", "ap-southeast-7": "th", "ap-south-1": "in", "ap-south-2": "in",
    "ap-northeast-1": "jp", "ap-northeast-2": "kr", "ap-northeast-3": "jp",
    "eu-west-1": "ie", "eu-west-2": "gb", "eu-west-3": "fr", "eu-central-1": "de",
    "eu-central-2": "ch", "eu-north-1": "se", "eu-south-1": "it", "eu-south-2": "es",
    "me-south-1": "bh", "me-central-1": "ae", "af-south-1": "za", "il-central-1": "il",
}
_AZURE_RE = re.compile(
    r"\b(eastus2?|westus[123]?|centralus|southcentralus|northcentralus|canadacentral|canadaeast|"
    r"brazilsouth|northeurope|westeurope|uksouth|ukwest|francecentral|germanywestcentral|"
    r"switzerlandnorth|swedencentral|norwayeast|polandcentral|italynorth|spaincentral|eastasia|"
    r"southeastasia|japaneast|japanwest|koreacentral|australiaeast|australiasoutheast|centralindia|"
    r"southindia|uaenorth|qatarcentral|southafricanorth|israelcentral|chinaeast2?|chinanorth[23]?)\b")
_AZURE_REGION = {
    "eastus": "us", "eastus2": "us", "westus": "us", "westus2": "us", "westus3": "us",
    "centralus": "us", "southcentralus": "us", "northcentralus": "us", "canadacentral": "ca",
    "canadaeast": "ca", "brazilsouth": "br", "northeurope": "ie", "westeurope": "nl",
    "uksouth": "gb", "ukwest": "gb", "francecentral": "fr", "germanywestcentral": "de",
    "switzerlandnorth": "ch", "swedencentral": "se", "norwayeast": "no", "polandcentral": "pl",
    "italynorth": "it", "spaincentral": "es", "eastasia": "hk", "southeastasia": "sg",
    "japaneast": "jp", "japanwest": "jp", "koreacentral": "kr", "australiaeast": "au",
    "australiasoutheast": "au", "centralindia": "in", "southindia": "in", "uaenorth": "ae",
    "qatarcentral": "qa", "southafricanorth": "za", "israelcentral": "il",
    "chinaeast": "cn", "chinaeast2": "cn", "chinanorth": "cn", "chinanorth2": "cn", "chinanorth3": "cn",
}


def _region_jurisdiction(text: str, scheme: str):
    if scheme == "aws":
        m = _AWS_RE.search(text)
        if not m:
            return None
        r = m.group(1)
        return _AWS_REGION.get(r) or {"us": "us", "ca": "ca", "sa": "br", "cn": "cn"}.get(r.split("-")[0])
    if scheme == "azure":
        m = _AZURE_RE.search(text)
        return _AZURE_REGION.get(m.group(1)) if m else None
    return None


def load_kb(path: str | None = None) -> "KB":
    if path:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        data = json.loads(files("borderlint").joinpath("data/providers.json").read_text("utf-8"))
    return KB(data.get("providers", []))


class KB:
    def __init__(self, providers: list[dict]):
        self.by_id = {p["id"]: p for p in providers}
        sdks, eps = [], []
        for p in providers:
            for s in p.get("sdks", []):
                sdks.append((s, p["id"]))
            ej = p.get("endpoint_jurisdictions", {})
            for h in p.get("endpoints", []):
                eps.append((h, p["id"], ej.get(h, p.get("jurisdiction", "unknown"))))
        # Longest match first so specific SDKs/hosts win over shorter ones.
        self._sdks = sorted(sdks, key=lambda x: -len(x[0]))
        self._eps = sorted(eps, key=lambda x: -len(x[0]))
        self.region_scheme = {p["id"]: p["region_scheme"] for p in providers if p.get("region_scheme")}

    def name(self, pid: str) -> str:
        return self.by_id.get(pid, {}).get("name", pid)

    def default_jurisdiction(self, pid: str) -> str:
        return self.by_id.get(pid, {}).get("jurisdiction", "unknown")

    def match_sdk(self, module: str) -> str | None:
        for s, pid in self._sdks:
            if module == s or module.startswith(s + "."):
                return pid
        return None

    def match_endpoint(self, text: str):
        for h, pid, juris in self._eps:
            if h in text:
                scheme = self.region_scheme.get(pid)
                if scheme:
                    juris = _region_jurisdiction(text, scheme) or juris
                return pid, h, juris
        return None
