"""Scan a path for AI provider usage (SDK imports + endpoint references)."""

from __future__ import annotations

import ast
import warnings
from dataclasses import dataclass
from pathlib import Path

IGNORE = {".git", "node_modules", "__pycache__", ".venv", "venv", "build", "dist",
          ".mypy_cache", ".pytest_cache", ".tox", ".ruff_cache"}
TEXT_EXT = {".env", ".ts", ".tsx", ".js", ".jsx", ".yaml", ".yml", ".toml", ".json", ".ini", ".cfg", ".sh"}


@dataclass(frozen=True)
class Detection:
    provider_id: str
    kind: str  # "sdk_import" | "endpoint_reference"
    evidence: str
    file: str
    line: int
    jurisdiction: str


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


def scan(root, kb) -> list[Detection]:
    root = Path(root)
    paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
    seen, out = set(), []
    for p in paths:
        if any(part in IGNORE for part in p.parts):
            continue
        if p.suffix != ".py" and p.suffix not in TEXT_EXT and p.name != ".env":
            continue
        try:
            src = p.read_text("utf-8", errors="ignore")
        except OSError:
            continue
        dets = _scan_py(str(p), src, kb) if p.suffix == ".py" else _scan_text(str(p), src, kb)
        for d in dets:
            key = (d.provider_id, d.kind, d.evidence, d.file, d.line)
            if key not in seen:
                seen.add(key)
                out.append(d)
    return out
