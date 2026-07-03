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

# GCP regions in a Vertex AI host: <region>-aiplatform.googleapis.com ; multi-region aiplatform.<us|eu>.rep...
_GCP_RE = re.compile(r"\b([a-z]+-[a-z]+\d+)-aiplatform\.googleapis\.com")
_GCP_MULTI_RE = re.compile(r"\baiplatform\.(us|eu)\.rep\.googleapis\.com")
_GCP_REGION = {
    "us-central1": "us", "us-east1": "us", "us-east4": "us", "us-east5": "us", "us-west1": "us",
    "us-west4": "us", "us-south1": "us", "northamerica-northeast1": "ca", "northamerica-northeast2": "ca",
    "southamerica-east1": "br", "southamerica-west1": "cl", "europe-west1": "be", "europe-west2": "gb",
    "europe-west3": "de", "europe-west4": "nl", "europe-west6": "ch", "europe-west8": "it",
    "europe-west9": "fr", "europe-west12": "it", "europe-central2": "pl", "europe-north1": "fi",
    "europe-southwest1": "es", "asia-east1": "tw", "asia-east2": "hk", "asia-northeast1": "jp",
    "asia-northeast2": "jp", "asia-northeast3": "kr", "asia-south1": "in", "asia-south2": "in",
    "asia-southeast1": "sg", "asia-southeast2": "id", "australia-southeast1": "au",
    "australia-southeast2": "au", "me-west1": "il", "me-central1": "qa", "me-central2": "sa",
    "africa-south1": "za",
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
    if scheme == "gcp":
        m = _GCP_RE.search(text)
        if m:
            return _GCP_REGION.get(m.group(1))
        mr = _GCP_MULTI_RE.search(text)
        return mr.group(1) if mr else None  # global aiplatform.googleapis.com -> None -> default unknown
    return None


_SPECIAL_TOKENS = {"CN-GBA", "GBA", "local", "unknown"}


def _valid_jurisdiction(token: str) -> bool:
    return token in _SPECIAL_TOKENS or (len(token) == 2 and token.isalpha() and token.islower())


# --- Sovereignty dimension ----------------------------------------------------
# Sovereignty blocs: which government can compel disclosure of a flow's data, derived from the
# provider's home legal regime (not the endpoint region). Distinct from residency.
_SOVEREIGNTY_BLOCS = frozenset({"us", "eu", "cn", "uk", "ru", "in", "il", "ca", "local", "unknown"})


def _valid_sovereignty(token: str) -> bool:
    """A sovereignty bloc must be one of the fixed vocabulary."""
    return token in _SOVEREIGNTY_BLOCS


def _load_sovereignty_map() -> dict:
    """Bundled provider id → sovereignty bloc map (advisory; never adjudicates legality)."""
    return json.loads(files("borderlint").joinpath("data/sovereignty.json").read_text("utf-8"))


_LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}


def _is_loopback_evidence(evidence: str) -> bool:
    """True if the evidence string references a loopback host (self-hosted → local sovereignty)."""
    low = evidence.lower()
    return any(h in low for h in _LOOPBACK_HOSTS) or ".localhost" in low


# --- Provenance dimension -----------------------------------------------------
# Provenance blocs: the legal regime of the model's developer (whose weights), derived from model
# references found statically in code. The sovereignty vocabulary minus `local` — weights always
# have a developer. Distinct from residency and sovereignty.
_PROVENANCE_BLOCS = frozenset({"us", "eu", "cn", "uk", "ru", "in", "il", "ca", "unknown"})

# A model identifier: no spaces, model-id punctuation only. Anchors prefix matching so prose
# strings that merely start with a model name ("gpt-4 is great") are never flagged.
_MODEL_ID = re.compile(r"^[A-Za-z0-9._/:-]{3,100}$")


def _valid_provenance(token: str) -> bool:
    """A provenance bloc must be one of the fixed vocabulary."""
    return token in _PROVENANCE_BLOCS


def _load_provenance_map() -> dict:
    """Bundled model-ID prefix → bloc map + first-party provider defaults (advisory)."""
    return json.loads(files("borderlint").joinpath("data/provenance.json").read_text("utf-8"))


def _endpoints_provider(endpoints: dict) -> dict:
    for host, juris in endpoints.items():
        if not _valid_jurisdiction(juris):
            raise ValueError(
                f"invalid jurisdiction '{juris}' for endpoint '{host}' "
                "(use a ccTLD/ISO code or one of CN-GBA, GBA, local, unknown)")
    return {"id": "internal_endpoint", "name": "Internal endpoint", "_user": True,
            "sdks": [], "npm": [], "endpoints": list(endpoints), "jurisdiction": "unknown",
            "endpoint_jurisdictions": dict(endpoints)}


def load_kb(path: str | None = None) -> "KB":
    """Load the bundled KB; if a user file is given, merge it on top (user entries win)."""
    bundled = json.loads(files("borderlint").joinpath("data/providers.json").read_text("utf-8"))
    providers = list(bundled.get("providers", []))
    sov_doc = _load_sovereignty_map()
    sov_map = dict(sov_doc.get("providers", {}))  # bundled provider id → bloc (copy; user merges in)
    prov_doc = _load_provenance_map()
    prov_patterns = {pat.lower(): entry["bloc"] for pat, entry in prov_doc.get("patterns", {}).items()}
    if path:
        with open(path, encoding="utf-8") as fh:
            user = json.load(fh)
        user_providers = [dict(p, _user=True) for p in user.get("providers", [])]
        if user.get("endpoints"):
            user_providers.append(_endpoints_provider(user["endpoints"]))
        providers = user_providers + providers  # user first → precedence
        # User sovereignty overrides: a top-level "sovereignty" map (provider id → bloc) takes
        # precedence over the bundled map; validated against the bloc vocabulary.
        user_sov = user.get("sovereignty", {})
        if isinstance(user_sov, dict):
            for pid, bloc in user_sov.items():
                if not _valid_sovereignty(bloc):
                    raise ValueError(
                        f"invalid sovereignty bloc '{bloc}' for provider '{pid}' "
                        "(use one of us, eu, cn, uk, ru, in, il, ca, local, unknown)")
                sov_map[pid] = bloc  # user wins
        # User provenance overrides: a top-level "provenance" map (model-ID prefix → bloc) takes
        # precedence over the bundled patterns; validated against the bloc vocabulary.
        user_prov = user.get("provenance", {})
        if isinstance(user_prov, dict):
            for pat, bloc in user_prov.items():
                if not _valid_provenance(bloc):
                    raise ValueError(
                        f"invalid provenance bloc '{bloc}' for model pattern '{pat}' "
                        "(use one of us, eu, cn, uk, ru, in, il, ca, unknown)")
                prov_patterns[pat.lower()] = bloc  # user wins
    kb = KB(providers)
    kb.updated = bundled.get("updated")
    kb.sovereignty_map = sov_map
    kb.sovereignty_updated = sov_doc.get("updated")
    kb.provenance_defaults = dict(prov_doc.get("provider_defaults", {}))
    kb.provenance_updated = prov_doc.get("updated")
    kb.set_provenance_patterns(prov_patterns)
    return kb


class KB:
    def __init__(self, providers: list[dict]):
        self.by_id = {}
        for p in providers:
            self.by_id.setdefault(p["id"], p)  # first wins; user providers are passed first
        sdks, npm, eps = [], [], []
        for p in providers:
            prio = 0 if p.get("_user") else 1  # user-supplied entries resolve in preference
            for s in p.get("sdks", []):
                sdks.append((prio, s, p["id"]))
            for n in p.get("npm", []):
                npm.append((prio, n, p["id"]))
            ej = p.get("endpoint_jurisdictions", {})
            for h in p.get("endpoints", []):
                eps.append((prio, h, p["id"], ej.get(h, p.get("jurisdiction", "unknown"))))
        # User entries first; within a source, longest match wins.
        self._sdks = sorted(sdks, key=lambda x: (x[0], -len(x[1])))
        self._npm = sorted(npm, key=lambda x: (x[0], -len(x[1])))
        self._eps = sorted(eps, key=lambda x: (x[0], -len(x[1])))
        self.region_scheme = {p["id"]: p["region_scheme"] for p in providers if p.get("region_scheme")}
        self.updated: str | None = None  # KB last-reviewed date, set by load_kb
        self.sovereignty_map: dict = {}  # provider id → sovereignty bloc, set by load_kb
        self.sovereignty_updated: str | None = None  # sovereignty map last-reviewed date
        self.provenance_defaults: dict = {}  # provider id → bloc for first-party-only providers
        self.provenance_updated: str | None = None  # provenance map last-reviewed date
        self._prov_prefixes: list = []  # (prefix, bloc), longest first, set via set_provenance_patterns

    def set_provenance_patterns(self, patterns: dict) -> None:
        """Install the (merged) model-ID prefix → bloc map; longest prefix wins."""
        self._prov_prefixes = sorted(patterns.items(), key=lambda x: -len(x[0]))

    def name(self, pid: str) -> str:
        return self.by_id.get(pid, {}).get("name", pid)

    def default_jurisdiction(self, pid: str) -> str:
        return self.by_id.get(pid, {}).get("jurisdiction", "unknown")

    def default_sovereignty(self, pid: str) -> str:
        """Provider-level sovereignty bloc from the (merged) sovereignty map; 'unknown' if unmapped."""
        return self.sovereignty_map.get(pid, "unknown")

    def resolve_sovereignty(self, provider_id: str, evidence: str = "", jurisdiction: str = "") -> str:
        """Resolve a flow's sovereignty bloc.

        Precedence: host/region-level override on the provider KB entry → provider-level value
        from the sovereignty map → 'unknown'. Loopback evidence → 'local'. Region-in-endpoint
        providers (Bedrock, Azure OpenAI, Vertex) inherit the provider sovereignty regardless of
        the resolved residency (D3): the endpoint region determines residency, not sovereignty.
        A host-level override keys off the resolved jurisdiction (e.g. AWS China regions resolve
        to jurisdiction 'cn', which maps to sovereignty 'cn' via the Sinnet ring-fence override).
        """
        if evidence and _is_loopback_evidence(evidence):
            return "local"
        entry = self.by_id.get(provider_id, {})
        # Region-level override keyed off the resolved jurisdiction (e.g. AWS China regions,
        # operated by Sinnet/NWCD, resolve to jurisdiction 'cn' → sovereignty 'cn'). The region
        # is already encoded in the jurisdiction for region-in-endpoint providers, so an exact
        # jurisdiction lookup is enough — no substring matching against raw evidence.
        overrides = entry.get("sovereignty_overrides", {})
        if jurisdiction and jurisdiction in overrides:
            return overrides[jurisdiction]
        return self.default_sovereignty(provider_id)

    def match_model(self, literal: str) -> tuple[str, str] | None:
        """Match a string literal against the model-ID prefix map → (identifier, bloc) or None.

        Anchored: the whole literal must look like a model identifier (no spaces, model-id
        charset) and start with a known prefix. Longest prefix wins.
        """
        s = literal.strip()
        if not _MODEL_ID.match(s):
            return None
        low = s.lower()
        for prefix, bloc in self._prov_prefixes:
            if low.startswith(prefix):
                return s, bloc
        return None

    def default_provenance(self, pid: str) -> str:
        """Tier-2 provenance: the org's bloc for providers that serve only their own models."""
        return self.provenance_defaults.get(pid, "unknown")

    def category(self, pid: str) -> str:
        """Provider category: 'inference' (default), 'vector_store', or 'aggregator'."""
        return self.by_id.get(pid, {}).get("category", "inference")

    def match_sdk(self, module: str) -> str | None:
        for _prio, s, pid in self._sdks:
            if module == s or module.startswith(s + "."):
                return pid
        return None

    def match_npm(self, pkg: str) -> str | None:
        for _prio, name, pid in self._npm:
            if pkg == name or pkg.startswith(name + "/"):
                return pid
        return None

    def match_endpoint(self, text: str):
        for _prio, h, pid, juris in self._eps:
            if h in text:
                scheme = self.region_scheme.get(pid)
                if scheme:
                    juris = _region_jurisdiction(text, scheme) or juris
                return pid, h, juris
        return None
