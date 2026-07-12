"""Interactive and non-interactive `borderlint init` wizard.

Scaffolds a `residency.json` policy by interviewing the operator for a home base and the data
classes they handle, grounding the proposal in a read-only inventory scan of the target path, then
walking the observed jurisdictions to build per-classification allow-lists.

The CLI layer (`cli.py`) parses arguments and calls `run_init(args)`. All prompts go through an
injectable `input_fn` (default `builtins.input`) so the wizard is unit-testable without a TTY.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass

from .detect import scan
from .kb import load_kb
from .policy import _valid_home

# Supported home-base seats offered by the wizard.
_SUPPORTED_SEATS = ("hk", "mo", "CN-GBA", "jp", "kr", "sg", "au", "uk", "eu", "my")
_DEFAULT_SEAT = "hk"

# Built-in classifications the wizard knows about; user-typed extras are also accepted.
_BUILTIN_CLASSES = ("non-pii", "employee-pii", "customer-pii")

# Default policy blocks emitted alongside the classifications map.
_DEFAULT_ON_UNKNOWN = "warn"
_DEFAULT_FAIL_ON = ["residency", "denied_provider", "sovereignty"]


@dataclass
class _InitArgs:
    """Minimal view of the parsed argparse namespace the wizard needs."""
    path: str = "."
    home: str | None = None
    classes: str | None = None
    output: str = "residency.json"
    force: bool = False


def _ask(input_fn, prompt: str, default: str | None = None) -> str:
    """Prompt once; return the stripped answer (empty -> default)."""
    suffix = f" [{default}]" if default is not None else ""
    return input_fn(f"{prompt}{suffix}: ").strip()


def _ask_home(input_fn) -> str:
    """Interview for the home base, re-prompting on an invalid token."""
    while True:
        ans = _ask(input_fn,
                   f"Home base {', '.join(_SUPPORTED_SEATS)}",
                   _DEFAULT_SEAT)
        seat = ans if ans else _DEFAULT_SEAT
        if _valid_home(seat):
            return seat
        print(f"error: '{seat}' is not a supported seat "
              f"({', '.join(_SUPPORTED_SEATS)})", file=sys.stderr)


def _ask_classes(input_fn) -> list[str]:
    """Interview for handled data classifications; empty -> all built-ins."""
    ans = _ask(input_fn,
               f"Data classes handled (comma-separated; {', '.join(_BUILTIN_CLASSES)})",
               ",".join(_BUILTIN_CLASSES))
    if not ans:
        return list(_BUILTIN_CLASSES)
    seen: list[str] = []
    for raw in ans.split(","):
        cls = raw.strip()
        if cls and cls not in seen:
            seen.append(cls)
    return seen or list(_BUILTIN_CLASSES)


def _observed_jurisdictions(path: str, providers: str | None) -> set[str]:
    """Run an inventory scan and collect the resolved jurisdictions actually present."""
    kb = load_kb(providers)
    detections = scan(path, kb)
    return {d.jurisdiction for d in detections}


def _walk_jurisdictions(input_fn, jurisdictions: set[str], classes: list[str], home: str) -> dict:
    """For each observed jurisdiction x each class, prompt keep/drop.

    The home base is pre-seeded into every class allow-list (a home seat is always acceptable to
    itself). Returns {class: [jurisdictions...]}.
    """
    allow: dict[str, list[str]] = {c: [home] for c in classes}
    for jur in sorted(jurisdictions):
        if jur == home:
            continue  # already seeded
        for cls in classes:
            ans = _ask(input_fn, f"Keep '{jur}' for '{cls}'? (y/N)", "n")
            if ans.lower() in ("y", "yes"):
                if jur not in allow[cls]:
                    allow[cls].append(jur)
    return allow


def _build_policy(home: str, allow: dict[str, list[str]]) -> dict:
    """Assemble the policy dict in the shorthand classifications-map shape."""
    return {
        "home_location": home,
        "on_unknown": _DEFAULT_ON_UNKNOWN,
        "fail_on": _DEFAULT_FAIL_ON,
        "classifications": {c: jur for c, jur in allow.items()},
    }


def _write_policy(policy: dict, out_path: str, force: bool) -> bool:
    """Write the policy, refusing to overwrite without --force.

    Returns True if the file was written, False if an existing file blocked the write
    (caller should surface exit code 2).
    """
    if os.path.exists(out_path) and not force:
        print(f"error: '{out_path}' already exists (use --force to overwrite)",
              file=sys.stderr)
        return False
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(policy, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return True


def run_init(args: object, input_fn=input, providers: str | None = None) -> int:
    """Entry point for `borderlint init`. Returns a process exit code.

    `args` must expose: path, home, classes, output, force (matching the argparse namespace).
    `input_fn` is injectable for tests; `providers` lets tests supply a custom KB path.
    """
    a = args if isinstance(args, _InitArgs) else _InitArgs(
        path=getattr(args, "path", "."),
        home=getattr(args, "home", None),
        classes=getattr(args, "classes", None),
        output=getattr(args, "output", "residency.json"),
        force=getattr(args, "force", False),
    )

    non_interactive = a.home is not None and a.classes is not None

    if non_interactive:
        home = a.home
        if not _valid_home(home):
            print(f"error: --home '{home}' is not a supported seat "
                  f"({', '.join(_SUPPORTED_SEATS)})", file=sys.stderr)
            return 2
        classes = [c.strip() for c in a.classes.split(",") if c.strip()]
        jurisdictions = _observed_jurisdictions(a.path, providers)
        # Scripted users get a permissive starting point: home + every observed jurisdiction.
        allow = {c: [home] + sorted(j for j in jurisdictions if j != home) for c in classes}
    else:
        home = _ask_home(input_fn)
        classes = _ask_classes(input_fn)
        jurisdictions = _observed_jurisdictions(a.path, providers)
        if not jurisdictions:
            print("note: no AI data flows detected; allow-lists seeded with the home base only.",
                  file=sys.stderr)
        allow = _walk_jurisdictions(input_fn, jurisdictions, classes, home)

    policy = _build_policy(home, allow)
    if not _write_policy(policy, a.output, a.force):
        return 2
    print(f"wrote policy to {a.output}")
    return 0
