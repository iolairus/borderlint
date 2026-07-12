#!/usr/bin/env python3
"""Generate the browsable KB site (static HTML) from borderlint/data/*.json.

Dev-side tooling — the shipped package is untouched. Every page is a pure
projection of the KB: corrections go to the KB via CONTRIBUTING.md, never to
the site. Page content comes from the JSON; only display-name constants are
imported from the package so labels can't drift.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "borderlint", "data")
sys.path.insert(0, ROOT)
from borderlint.report import _EU, JURIS, SOVEREIGNTY  # noqa: E402 — display labels, single source

REPO = "https://github.com/iolairus/borderlint"
INSTALL = "pip install borderlint"
SITE_NAME = "borderlint KB"

# Destination-side cross-border arrangement ids per jurisdiction (ids in arrangements.json).
# A provider page has no home-location context, so it lists the mechanisms that govern
# transfers *toward* the provider's jurisdiction(s) — reference links, never adjudicated.
_ARR_BY_DEST = {"cn": ["pipl"], "CN-GBA": ["gba", "gba_mo"], "hk": ["gba"],
                "jp": ["appi_xborder"], "kr": ["pipa_xborder"], "sg": ["sg_pdpa_transfer"],
                "au": ["au_app8"], "gb": ["uk_idta"], "my": ["my_pdpa_xborder"]}

_STYLE = """\
body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;margin:2rem auto;max-width:52rem;padding:0 1rem;color:#1a1a1a;line-height:1.5}
h1{font-size:1.5rem}h2{font-size:1.1rem;margin-top:1.6rem}
table{border-collapse:collapse;width:100%;font-size:.92rem;margin:.4rem 0}
th,td{border:1px solid #ccc;padding:.35rem .5rem;text-align:left;vertical-align:top}
th{background:#f5f5f5;white-space:nowrap}
code{font-family:ui-monospace,monospace;font-size:.9em;background:#f5f5f5;padding:0 .2rem}
nav{font-size:.9rem;margin-bottom:1rem}
footer{margin-top:2.5rem;padding-top:1rem;border-top:1px solid #ccc;font-size:.85rem;color:#555}
ul.cols{columns:3;list-style:none;padding:0}ul.cols li{margin:.15rem 0}
.axis{color:#555;font-size:.95rem}"""


def _load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def _slug(name: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]", "-", name.lower())).strip("-")


def _page(title: str, desc: str, body: str, depth: int) -> str:
    home = "../" * depth
    return "\n".join([
        "<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{escape(title)}</title>",
        f'<meta name="description" content="{escape(desc, quote=True)}">',
        "<style>", _STYLE, "</style>", "</head>", "<body>",
        f'<nav><a href="{home}index.html">{escape(SITE_NAME)}</a></nav>',
        body,
        "<footer>", FOOTER, "</footer>", "</body>", "</html>"])


def _juris_label(j: str) -> str:
    return JURIS.get(j, j)


def _regime_names(jset, regimes) -> list[str]:
    names = {regimes[j]["regime"] for j in jset if j in regimes}
    return sorted(names)


def _arrangement_ids_for(jset) -> list[str]:
    out = []
    for j in sorted(jset):
        for aid in _ARR_BY_DEST.get(j, []):
            if aid not in out:
                out.append(aid)
    if jset & _EU and "gdpr" not in out:
        out.append("gdpr")
    return out


def _provider_body(p, sov_map, regimes, arr_map) -> str:
    e = lambda v: escape(str(v), quote=True)
    name = p["name"]
    j = p["jurisdiction"]
    ej = p.get("endpoint_jurisdictions", {})
    jset = {j} | set(ej.values())
    bloc = sov_map.get(p["id"], "unknown")
    rows = []
    if p.get("category"):
        rows.append(("Category", e(p["category"])))
    if j == "unknown":
        res = "Region-dependent — unresolved until an endpoint region is pinned"
        if p.get("region_scheme"):
            res += f" (region scheme: {e(p['region_scheme'])})"
    else:
        res = e(_juris_label(j)) + f" <code>{e(j)}</code>"
    rows.append(("Residency", res))
    srow = e(SOVEREIGNTY.get(bloc, bloc)) + f" <code>{e(bloc)}</code>"
    if p.get("sovereignty_overrides"):
        ov = ", ".join(f"{e(_juris_label(k))} → <code>{e(v)}</code>"
                       for k, v in sorted(p["sovereignty_overrides"].items()))
        srow += f" — region-level overrides: {ov}"
    rows.append(("Sovereignty", srow))
    if p.get("endpoints"):
        rows.append(("Endpoints", ", ".join(f"<code>{e(h)}</code>" for h in p["endpoints"])))
    pkgs = [f"<code>{e(s)}</code> (Python)" for s in p.get("sdks", [])]
    pkgs += [f"<code>{e(n)}</code> (npm)" for n in p.get("npm", [])]
    if pkgs:
        rows.append(("Packages", ", ".join(pkgs)))
    if ej:
        rows.append(("Endpoint regions", ", ".join(
            f"<code>{e(h)}</code> → {e(_juris_label(v))}" for h, v in sorted(ej.items()))))
    regs = _regime_names(jset, regimes)
    if regs:
        rows.append(("Regimes", ", ".join(e(r) for r in regs)))
    aids = _arrangement_ids_for(jset)
    if aids:
        rows.append(("Cross-border references", "<br>".join(
            f'<a href="{e(arr_map[a]["url"])}">{e(arr_map[a]["name"])}</a> — {e(arr_map[a]["summary"])}'
            for a in aids)))
    if p.get("note"):
        rows.append(("KB note", e(p["note"])))
    body = [f"<h1>{e(name)}</h1>",
            '<p class="axis">Where does this provider put your AI data — and who can compel its disclosure?</p>',
            "<table>"]
    body += [f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows]
    body.append("</table>")
    return "\n".join(body)


def _org_body(org, entries, blocs) -> str:
    e = lambda v: escape(str(v), quote=True)
    body = [f"<h1>{e(org)} — model provenance</h1>",
            '<p class="axis">Whose model weights are these? Model-id patterns the KB resolves to this developer.</p>',
            f"<p>Provenance bloc: {', '.join(e(SOVEREIGNTY.get(b, b)) + f' <code>{e(b)}</code>' for b in sorted(blocs))}</p>",
            "<table>", "<tr><th>Model-id pattern</th><th>Bloc</th></tr>"]
    body += [f"<tr><td><code>{e(pat)}</code></td><td><code>{e(v['bloc'])}</code></td></tr>"
             for pat, v in sorted(entries)]
    body.append("</table>")
    return "\n".join(body)


def build(out_dir: str) -> dict:
    providers = _load("providers.json")
    sov = _load("sovereignty.json")
    prov = _load("provenance.json")
    regimes = _load("regimes.json")["regimes"]
    arrangements = {a["id"]: a for a in _load("arrangements.json")["arrangements"]}
    global FOOTER
    e = lambda v: escape(str(v), quote=True)
    FOOTER = (f"<p>Generated from the <a href=\"{REPO}\">borderlint</a> knowledge base — "
              f"providers reviewed {e(providers['updated'])}, sovereignty {e(sov['updated'])}, "
              f"provenance {e(prov['updated'])}. Corrections welcome via the repo.</p>"
              f"<p>Check your own repo: <code>{INSTALL}</code></p>")

    os.makedirs(os.path.join(out_dir, "providers"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "models"), exist_ok=True)
    sov_map = sov["providers"]

    plinks = []
    for p in sorted(providers["providers"], key=lambda x: x["name"].lower()):
        jlabel = "region-dependent" if p["jurisdiction"] == "unknown" else _juris_label(p["jurisdiction"])
        title = f"{p['name']} data residency & sovereignty — {SITE_NAME}"
        desc = (f"AI data residency and sovereignty for {p['name']}: residency {jlabel}, "
                f"sovereignty bloc {sov_map.get(p['id'], 'unknown')}. From the borderlint knowledge base.")
        doc = _page(title, desc, _provider_body(p, sov_map, regimes, arrangements), depth=1)
        with open(os.path.join(out_dir, "providers", f"{p['id']}.html"), "w", encoding="utf-8") as fh:
            fh.write(doc)
        plinks.append((p["name"], f"providers/{p['id']}.html"))

    orgs = {}
    for pat, v in prov["patterns"].items():
        orgs.setdefault(v["org"], []).append((pat, v))
    slugs, olinks = {}, []
    for org in sorted(orgs, key=str.lower):
        s = _slug(org) or "org"
        if s in slugs:
            slugs[s] += 1
            s = f"{s}-{slugs[s]}"
        else:
            slugs[s] = 1
        blocs = {v["bloc"] for _, v in orgs[org]}
        title = f"{org} model provenance — {SITE_NAME}"
        desc = (f"Model provenance for {org}: {len(orgs[org])} model-id pattern(s), "
                f"provenance bloc {', '.join(sorted(blocs))}. Whose weights does your AI run?")
        doc = _page(title, desc, _org_body(org, orgs[org], blocs), depth=1)
        with open(os.path.join(out_dir, "models", f"{s}.html"), "w", encoding="utf-8") as fh:
            fh.write(doc)
        olinks.append((org, f"models/{s}.html"))

    body = [f"<h1>{escape(SITE_NAME)} — AI data residency, sovereignty & model provenance</h1>",
            "<p>The hand-curated knowledge base behind "
            f'<a href="{REPO}">borderlint</a>: {len(plinks)} AI providers and '
            f"{len(olinks)} model developers, each resolved to the three questions that govern an "
            "AI flow — <strong>where do the bytes rest</strong> (residency), "
            "<strong>who can compel disclosure</strong> (sovereignty), and "
            "<strong>whose model weights run</strong> (provenance).</p>",
            "<h2>The three axes in one example</h2>",
            "<p>AWS Bedrock <code>ap-east-1</code> serving DeepSeek-R1 is residency "
            "<strong>Hong Kong</strong>, sovereignty <strong>United States</strong> (CLOUD Act "
            "reaches a US provider in any region), provenance <strong>Mainland China</strong> "
            "(DeepSeek weights) — three different answers to “where is our AI?”, all correct.</p>",
            "<h2>Providers</h2>", '<ul class="cols">']
    body += [f'<li><a href="{escape(h, quote=True)}">{escape(n)}</a></li>' for n, h in plinks]
    body += ["</ul>", "<h2>Model developers</h2>", '<ul class="cols">']
    body += [f'<li><a href="{escape(h, quote=True)}">{escape(n)}</a></li>' for n, h in olinks]
    body += ["</ul>"]
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(_page(f"{SITE_NAME} — AI data residency, sovereignty & model provenance by provider",
                       "Browsable knowledge base: AI providers and model families resolved to "
                       "data residency, sovereignty, and model provenance. Generated from borderlint.",
                       "\n".join(body), depth=0))
    return {"providers": len(plinks), "orgs": len(olinks)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the borderlint KB site.")
    ap.add_argument("--out", default=os.path.join(ROOT, "site"))
    a = ap.parse_args(argv)
    counts = build(a.out)
    print(f"kb-site: {counts['providers']} provider pages, {counts['orgs']} model-developer pages -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
