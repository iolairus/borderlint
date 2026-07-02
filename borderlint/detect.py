"""Scan a path for AI provider usage (SDK imports + endpoint references)."""

from __future__ import annotations

import ast
import re
import warnings
from dataclasses import dataclass, replace
from pathlib import Path

IGNORE = {".git", "node_modules", "__pycache__", ".venv", "venv", "build", "dist",
          ".mypy_cache", ".pytest_cache", ".tox", ".ruff_cache"}
TEXT_EXT = {".env", ".ts", ".tsx", ".js", ".jsx", ".yaml", ".yml", ".toml", ".json", ".ini", ".cfg", ".sh"}
JS_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
MAX_FILE_BYTES = 5 * 1024 * 1024  # skip files larger than this; no source file is this big

# AI endpoint declared via a config key or a base_url kwarg — anchored on the key, not the URL,
# so arbitrary URLs are not flagged. Works across YAML/JSON/TOML and Python/JS code.
_ENDPOINT_KEY = re.compile(
    r"""(?i)\b(base_?url|api_base|openai_api_base|azure_endpoint|api_endpoint|inference_endpoint)\b['"]?\s*[:=]\s*['"]?\s*([^\s'"#,}\]]+)""")
_LOOPBACK = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}

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


@dataclass(frozen=True)
class Detection:
    provider_id: str
    kind: str  # "sdk_import" | "endpoint_reference" | "config_endpoint" | "api_call"
    evidence: str
    file: str
    line: int
    jurisdiction: str
    waiver: str | None = None  # justification, if an inline `borderlint: allow` waiver applies
    sovereignty: str = "unknown"  # compelled-disclosure bloc; resolved in scan() from the provider KB


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


def _host_of(value: str) -> str | None:
    v = value.strip().strip("'\"")
    if "://" in v:
        v = v.split("://", 1)[1]
    v = v.split("/", 1)[0].rsplit("@", 1)[-1]
    if v.startswith("["):  # ipv6 literal, e.g. [::1]:8080
        return v.split("]", 1)[0].lstrip("[") or None
    return v.split(":", 1)[0] or None


def _scan_config_endpoints(path: str, src: str, kb) -> list[Detection]:
    """Endpoints declared behind an AI-endpoint key (config or base_url kwarg)."""
    out: list[Detection] = []
    for m in _ENDPOINT_KEY.finditer(src):
        host = _host_of(m.group(2))
        if not host:
            continue
        low = host.lower()
        is_loop = low in _LOOPBACK or low.endswith(".localhost")
        if not is_loop and "." not in host:
            continue  # bare non-host value (e.g. an enum), skip
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


def scan(root, kb) -> list[Detection]:
    root = Path(root)
    paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
    seen, out, waivers = set(), [], {}
    for p in paths:
        if any(part in IGNORE for part in p.parts):
            continue
        suffix = p.suffix
        is_py = suffix == ".py"
        is_js = suffix in JS_EXT
        is_text = suffix in TEXT_EXT or p.name == ".env"
        if not (is_py or is_js or is_text):
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
        else:
            dets = _scan_text(str(p), src, kb) + cfg
        # one detection per flow per line: drop an api_call already produced by another scanner on its line
        anchored = {(d.provider_id, d.jurisdiction, d.line) for d in dets if d.kind != "api_call"}
        dets = [d for d in dets if d.kind != "api_call" or (d.provider_id, d.jurisdiction, d.line) not in anchored]
        for d in dets:
            key = (d.provider_id, d.kind, d.evidence, d.file, d.line)
            if key not in seen:
                seen.add(key)
                out.append(d)
    return _resolve_sovereignty([_apply_waiver(d, waivers) for d in out], kb)
