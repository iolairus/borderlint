"""Scan a path for AI provider usage (SDK imports + endpoint references)."""

from __future__ import annotations

import ast
import re
import warnings
from dataclasses import dataclass
from pathlib import Path

IGNORE = {".git", "node_modules", "__pycache__", ".venv", "venv", "build", "dist",
          ".mypy_cache", ".pytest_cache", ".tox", ".ruff_cache"}
TEXT_EXT = {".env", ".ts", ".tsx", ".js", ".jsx", ".yaml", ".yml", ".toml", ".json", ".ini", ".cfg", ".sh"}
JS_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}

# Capture the module specifier from: `import X from "pkg"`, `import "pkg"`, `export ... from "pkg"`,
# `require("pkg")`, dynamic `import("pkg")`. Regex over tree-sitter keeps borderlint zero-dependency.
_JS_IMPORT = re.compile(
    r'''(?:^[ \t]*import\b[^'"\n]*?\bfrom[ \t]*|^[ \t]*import[ \t]*|^[ \t]*export\b[^'"\n]*?\bfrom[ \t]*|\brequire[ \t]*\([ \t]*|\bimport[ \t]*\([ \t]*)['"]([^'"]+)['"]''',
    re.M)


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


def _scan_js(path: str, src: str, kb) -> list[Detection]:
    out: list[Detection] = []
    for m in _JS_IMPORT.finditer(src):
        pid = kb.match_npm(m.group(1))
        if pid:
            line = src.count("\n", 0, m.start()) + 1
            out.append(Detection(pid, "sdk_import", m.group(1), path, line, kb.default_jurisdiction(pid)))
    return out


def scan(root, kb) -> list[Detection]:
    root = Path(root)
    paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
    seen, out = set(), []
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
            src = p.read_text("utf-8", errors="ignore")
        except OSError:
            continue
        if is_py:
            dets = _scan_py(str(p), src, kb)
        elif is_js:  # imports (new) + endpoint literals (existing text scan)
            dets = _scan_js(str(p), src, kb) + _scan_text(str(p), src, kb)
        else:
            dets = _scan_text(str(p), src, kb)
        for d in dets:
            key = (d.provider_id, d.kind, d.evidence, d.file, d.line)
            if key not in seen:
                seen.add(key)
                out.append(d)
    return out
