"""Scan a path for AI provider usage (SDK imports + endpoint references)."""

from __future__ import annotations

import ast
import os
import re
import warnings
from dataclasses import dataclass, replace
from pathlib import Path

IGNORE = {".git", "node_modules", "__pycache__", ".venv", "venv", "site-packages", "build",
          "dist", ".mypy_cache", ".pytest_cache", ".tox", ".ruff_cache"}
TEXT_EXT = {".env", ".ts", ".tsx", ".js", ".jsx", ".yaml", ".yml", ".toml", ".json", ".ini", ".cfg", ".sh"}
JS_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
JVM_EXT = {".java", ".kt", ".kts"}
MAX_FILE_BYTES = 5 * 1024 * 1024  # skip files larger than this; no source file is this big

# AI endpoint declared via a config key or a base_url kwarg — anchored on the key, not the URL,
# so arbitrary URLs are not flagged. Works across YAML/JSON/TOML and Python/JS code.
_ENDPOINT_KEY = re.compile(
    r"""(?i)\b(base_?url|api_base|openai_api_base|azure_endpoint|api_endpoint|inference_endpoint)\b['"]?\s*[:=]\s*['"]?\s*([^\s'"#,}\]]+)""")
_LOOPBACK = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}

# Env-style endpoint keys: TELLMEWHY_LLM_SERVER_URL=... — segment-matched so EMAIL_URL's "AI"
# substring never qualifies. The stem list is deliberately curated (no bare MODEL/API).
_ENV_KEY = re.compile(r"""(?im)^[ \t]*-?[ \t]*([A-Za-z][A-Za-z0-9_]*)[ \t]*[:=][ \t]*['"]?[ \t]*([^\s'"#,}\]]+)""")
_ENV_STEMS = frozenset({"llm", "openai", "anthropic", "gpt", "claude", "gemini", "mistral",
                        "deepseek", "qwen", "ollama", "vllm", "inference",
                        "completion", "completions", "embedding", "embeddings"})
_ENV_SUFFIXES = frozenset({"url", "endpoint", "base", "host"})


def _env_key_matches(key: str) -> bool:
    segs = key.lower().split("_")
    return len(segs) >= 2 and segs[-1] in _ENV_SUFFIXES and any(x in _ENV_STEMS for x in segs)

# Inline waiver: `borderlint: allow <reason>` in any comment. The reason (justification) is required.
_WAIVER = re.compile(r"borderlint:\s*allow\b[ \t]*(.*)", re.I)

# Capture the module specifier from: `import X from "pkg"`, `import "pkg"`, `export ... from "pkg"`,
# `require("pkg")`, dynamic `import("pkg")`. Regex over tree-sitter keeps borderlint zero-dependency.
_JS_IMPORT = re.compile(
    r'''(?:^[ \t]*import\b[^'"\n]*?\bfrom[ \t]*|^[ \t]*import[ \t]*|^[ \t]*export\b[^'"\n]*?\bfrom[ \t]*|\brequire[ \t]*\([ \t]*|\bimport[ \t]*\([ \t]*)['"]([^'"]+)['"]''',
    re.M)

# OpenAI-compatible API call by its request-path signature. A static host is resolved only when its
# `scheme://host` sits in the same literal directly before the path; otherwise the host is dynamic.
_API_PATH = re.compile(
    r"""(?:https?://(?P<host>[^\s'"`/]+))?(?P<path>/v1/(?:chat/completions|completions|responses|embeddings))\b""")

# Quoted string literals, any language — candidates for model-reference matching. The KB does the
# anchoring (model-id charset + known prefix), so this can stay permissive.
_STR_LITERAL = re.compile(r"""['"]([^'"\n]{3,100})['"]""")


@dataclass(frozen=True)
class Detection:
    provider_id: str
    kind: str  # "sdk_import" | "endpoint_reference" | "config_endpoint" | "api_call" | "model_reference"
    evidence: str
    file: str
    line: int
    jurisdiction: str
    waiver: str | None = None  # justification, if an inline `borderlint: allow` waiver applies
    sovereignty: str = "unknown"  # compelled-disclosure bloc; resolved in scan() from the provider KB
    provenance: str = "unknown"  # model-weights bloc; bound model reference or first-party default
    model: str | None = None  # the bound model identifier, when one resolved the provenance
    model_org: str | None = None  # the matched pattern's developer organisation, when known


def _scan_py(path: str, src: str, kb) -> list[Detection]:
    out: list[Detection] = []
    try:
        with warnings.catch_warnings():  # ponytail: hush the scanned file's own warnings, not ours
            warnings.simplefilter("ignore")
            tree = ast.parse(src)
    except SyntaxError:
        return out  # resilient: skip unparseable files
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                pid = kb.match_sdk(a.name)
                if pid:
                    out.append(Detection(pid, "sdk_import", a.name, path, n.lineno, kb.default_jurisdiction(pid)))
        elif isinstance(n, ast.ImportFrom):
            pid = kb.match_sdk(n.module or "")
            if pid:
                out.append(Detection(pid, "sdk_import", n.module, path, n.lineno, kb.default_jurisdiction(pid)))
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            m = kb.match_endpoint(n.value)
            if m:
                out.append(Detection(m[0], "endpoint_reference", m[1], path, n.lineno, m[2]))
    return out


def _scan_text(path: str, src: str, kb) -> list[Detection]:
    out: list[Detection] = []
    for i, line in enumerate(src.splitlines(), 1):
        m = kb.match_endpoint(line)
        if m:
            out.append(Detection(m[0], "endpoint_reference", m[1], path, i, m[2]))
    return out


def _scan_js(path: str, src: str, kb) -> list[Detection]:
    out: list[Detection] = []
    for m in _JS_IMPORT.finditer(src):
        pid = kb.match_npm(m.group(1))
        if pid:
            line = src.count("\n", 0, m.start()) + 1
            out.append(Detection(pid, "sdk_import", m.group(1), path, line, kb.default_jurisdiction(pid)))
    return out


_JVM_IMPORT = re.compile(r"^\s*import\s+(?:static\s+)?([\w.]+)", re.M)  # Java `;` and Kotlin bare forms


def _scan_jvm(path: str, src: str, kb) -> list[Detection]:
    out: list[Detection] = []
    for m in _JVM_IMPORT.finditer(src):
        pid = kb.match_jvm(m.group(1))
        if pid:
            line = src.count("\n", 0, m.start()) + 1
            out.append(Detection(pid, "sdk_import", m.group(1), path, line, kb.default_jurisdiction(pid)))
    return out


def _host_of(value: str) -> str | None:
    v = value.strip().strip("'\"")
    if "://" in v:
        v = v.split("://", 1)[1]
    v = v.split("/", 1)[0].rsplit("@", 1)[-1]
    if v.startswith("["):  # ipv6 literal, e.g. [::1]:8080
        return v.split("]", 1)[0].lstrip("[") or None
    return v.split(":", 1)[0] or None


def _scan_config_endpoints(path: str, src: str, kb) -> list[Detection]:
    """Endpoints declared behind an AI-endpoint key (config, base_url kwarg, or env-style key)."""
    out: list[Detection] = []
    matches = list(_ENDPOINT_KEY.finditer(src))
    seen_spans = {m.span(2) for m in matches}
    for m in _ENV_KEY.finditer(src):
        if _env_key_matches(m.group(1)) and m.span(2) not in seen_spans:
            matches.append(m)
    for m in matches:
        raw = m.group(2)
        if "(" in raw or ")" in raw:
            continue  # environment getter / code call: runtime-resolved, the .env is the source
        host = _host_of(raw)
        if not host:
            continue
        low = host.lower()
        is_loop = low in _LOOPBACK or low.endswith(".localhost")
        host_shaped = re.search(r"[A-Za-z0-9]\.[A-Za-z0-9]", host) or "://" in raw
        if not is_loop and not host_shaped:
            continue  # not host-shaped: bare enums, "." / "./src" (e.g. tsconfig baseUrl), skip
        line = src.count("\n", 0, m.start()) + 1
        if is_loop:
            out.append(Detection("local", "config_endpoint", host, path, line, "local"))
        else:
            hit = kb.match_endpoint(host)
            if hit:  # known provider host (incl. region resolution)
                out.append(Detection(hit[0], "config_endpoint", hit[1], path, line, hit[2]))
            else:  # custom / OpenAI-compatible host we can't place — surface for assertion
                out.append(Detection("custom_endpoint", "config_endpoint", host, path, line, "unknown"))
    return out


def _scan_api_calls(path: str, src: str, kb) -> list[Detection]:
    """OpenAI-compatible calls by request-path signature; host resolved only if static in the literal."""
    out: list[Detection] = []
    for m in _API_PATH.finditer(src):
        line = src.count("\n", 0, m.start()) + 1
        host = _host_of(m.group("host")) if m.group("host") else None
        if host:
            low = host.lower()
            if low in _LOOPBACK or low.endswith(".localhost"):
                out.append(Detection("local", "api_call", host, path, line, "local"))
                continue
            hit = kb.match_endpoint(host)
            if hit:  # known provider host (incl. region resolution)
                out.append(Detection(hit[0], "api_call", hit[1], path, line, hit[2]))
                continue
            out.append(Detection("custom_endpoint", "api_call", host, path, line, "unknown"))
        else:  # dynamic host, outside the literal, or relative path → destination set at runtime
            out.append(Detection("custom_endpoint", "api_call", m.group("path"), path, line, "unknown"))
    return out


def _waivers(src: str) -> dict[int, str]:
    """Line number → justification for each `borderlint: allow <reason>` comment."""
    out: dict[int, str] = {}
    for i, line in enumerate(src.splitlines(), 1):
        m = _WAIVER.search(line)
        if m:
            out[i] = m.group(1).strip()
    return out


def _apply_waiver(d: Detection, waivers: dict) -> Detection:
    fw = waivers.get(d.file)
    if fw:
        reason = fw.get(d.line) or fw.get(d.line - 1)  # the flagged line or the line above it
        if reason:  # non-empty justification only — a bare waiver is ignored
            return replace(d, waiver=reason)
    return d


def _resolve_sovereignty(detections, kb) -> list[Detection]:
    """Populate the sovereignty bloc on each detection from the provider KB (D3).

    Sovereignty is derived from the provider (its home legal regime), not the endpoint region;
    region-in-endpoint providers inherit the provider sovereignty regardless of resolved residency.
    """
    return [replace(d, sovereignty=kb.resolve_sovereignty(d.provider_id, d.evidence, d.jurisdiction))
            for d in detections]


def _scan_model_refs(src: str, kb) -> list[tuple[int, str, str, str | None]]:
    """(line, identifier, bloc, org) for each string literal matching the model-ID prefix map."""
    out = []
    for m in _STR_LITERAL.finditer(src):
        hit = kb.match_model(m.group(1))
        if hit:
            out.append((src.count("\n", 0, m.start()) + 1, hit[0], hit[1], hit[2]))
    return out


def _attach_models(path: str, src: str, dets: list[Detection], kb) -> list[Detection]:
    """Bind model references to same-file provider detections (D4).

    Refs resolving to exactly one distinct bloc bind to the file's provider detections; otherwise
    (no provider in file, or ambiguous blocs) each ref stands alone as a `model_reference` finding
    with residency `unknown` — it is a weights-origin signal, not a network flow.
    """
    refs = _scan_model_refs(src, kb)
    if not refs:
        return dets
    blocs = {b for _, _, b, _ in refs}
    if dets and len(blocs) == 1:
        # ponytail: first ref represents same-bloc siblings; per-ref pairing needs call-site AST
        return [replace(d, provenance=refs[0][2], model=refs[0][1], model_org=refs[0][3])
                for d in dets]
    return dets + [Detection("model_reference", "model_reference", ref, path, line, "unknown",
                             provenance=bloc, model=ref, model_org=org)
                   for line, ref, bloc, org in refs]


def _resolve_provenance(detections, kb) -> list[Detection]:
    """Tier-2 provenance (D3): unbound flows on first-party-only providers get the org's bloc."""
    return [replace(d, provenance=kb.default_provenance(d.provider_id))
            if d.provenance == "unknown" and d.kind != "model_reference" else d
            for d in detections]


def _walk_files(root: Path) -> list[Path]:
    """Single-pass walk pruning ignored and environment subtrees — never traversed at all.

    Environments are recognised by their markers (PEP 405 `pyvenv.cfg`, conda's `conda-meta/`),
    regardless of directory name; symlinked directories are not followed, matching rglob.
    """
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [n for n in dirnames
                       if n not in IGNORE
                       and not os.path.isfile(os.path.join(dirpath, n, "pyvenv.cfg"))
                       and not os.path.isdir(os.path.join(dirpath, n, "conda-meta"))]
        out.extend(Path(dirpath) / f for f in filenames)
    return out


def scan(root, kb) -> list[Detection]:
    root = Path(root)
    paths = [root] if root.is_file() else _walk_files(root)
    seen, out, waivers = set(), [], {}
    for p in paths:
        if any(part in IGNORE for part in p.parts):
            continue
        suffix = p.suffix
        is_py = suffix == ".py"
        is_js = suffix in JS_EXT
        is_jvm = suffix in JVM_EXT
        is_text = suffix in TEXT_EXT or p.name == ".env"
        if not (is_py or is_js or is_jvm or is_text):
            continue
        try:
            if p.stat().st_size > MAX_FILE_BYTES:  # don't read a huge file into memory (DoS guard)
                continue
            src = p.read_text("utf-8", errors="ignore")
        except OSError:
            continue
        fw = _waivers(src)
        if fw:
            waivers[str(p)] = fw
        cfg = _scan_config_endpoints(str(p), src, kb)  # AI-endpoint keys / base_url kwargs, any file
        if is_py:
            dets = _scan_py(str(p), src, kb) + _scan_api_calls(str(p), src, kb) + cfg
        elif is_js:  # imports + endpoint literals (text scan) + OpenAI-compatible call paths
            dets = _scan_js(str(p), src, kb) + _scan_text(str(p), src, kb) + _scan_api_calls(str(p), src, kb) + cfg
        elif is_jvm:  # same shape as JS: imports + endpoint literals + call paths
            dets = _scan_jvm(str(p), src, kb) + _scan_text(str(p), src, kb) + _scan_api_calls(str(p), src, kb) + cfg
        else:
            dets = _scan_text(str(p), src, kb) + cfg
        # one detection per flow per line: drop an api_call already produced by another scanner on its line
        anchored = {(d.provider_id, d.jurisdiction, d.line) for d in dets if d.kind != "api_call"}
        dets = [d for d in dets if d.kind != "api_call" or (d.provider_id, d.jurisdiction, d.line) not in anchored]
        dets = _attach_models(str(p), src, dets, kb)  # bind model refs → provenance (per file)
        for d in dets:
            key = (d.provider_id, d.kind, d.evidence, d.file, d.line)
            if key not in seen:
                seen.add(key)
                out.append(d)
    return _resolve_provenance(_resolve_sovereignty([_apply_waiver(d, waivers) for d in out], kb), kb)
