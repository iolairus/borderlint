"""Provider knowledge base: load and resolve a provider/endpoint to a jurisdiction."""

from __future__ import annotations

import json
from importlib.resources import files


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
                return pid, h, juris
        return None
