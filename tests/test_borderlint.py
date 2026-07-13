"""Smallest checks that fail if the core logic breaks (one per key spec scenario)."""

import json
import os
import tempfile

from borderlint.detect import Detection, _scan_config_endpoints, _scan_js, _scan_py, _scan_text, _resolve_sovereignty
from borderlint.init import _InitArgs, run_init
from borderlint.kb import load_kb
from borderlint.policy import evaluate, load_policy

kb = load_kb()

# A tiny fixture path that contains at least one detectable AI flow (OpenAI -> us).
_FIXTURE = os.path.join(tempfile.mkdtemp(), "app.py")
with open(_FIXTURE, "w", encoding="utf-8") as _fh:
    _fh.write('import openai\n')


def _write_input(scripted, walk_default="n"):
    """Build an injectable input_fn over a fixed scripted list, then a default for walk prompts."""
    idx = {"i": 0}
    def _fn(prompt):
        if idx["i"] < len(scripted):
            v = scripted[idx["i"]]; idx["i"] += 1; return v
        return walk_default
    return _fn


def test_init_interactive_writes_policy():
    out = os.path.join(tempfile.mkdtemp(), "residency.json")
    a = _InitArgs(path=_FIXTURE, output=out)
    # home=sg, classes=customer-pii,non-pii; drop the observed 'us' for both classes.
    rc = run_init(a, input_fn=_write_input(["sg", "customer-pii,non-pii"]))
    assert rc == 0
    with open(out, encoding="utf-8") as fh:
        policy = json.load(fh)
    assert policy["home_location"] == "sg"
    assert set(policy["classifications"]) == {"customer-pii", "non-pii"}
    # home base is pre-seeded into every class allow-list.
    assert policy["classifications"]["customer-pii"] == ["sg"]
    assert policy["on_unknown"] == "warn"
    # fail_on is omitted so the policy inherits the engine default.
    assert "fail_on" not in policy
    # the written file must load via the existing policy loader.
    load_policy(out)


def test_init_refuses_overwrite_without_force():
    out = os.path.join(tempfile.mkdtemp(), "residency.json")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write('{"home_location":"hk","classifications":{"non-pii":["hk"]}}')
    a = _InitArgs(path=_FIXTURE, output=out, force=False)
    rc = run_init(a, input_fn=_write_input(["hk", "non-pii"]))
    assert rc == 2  # non-zero, file untouched
    with open(out, encoding="utf-8") as fh:
        assert "home_location" in json.load(fh)


def test_init_overwrites_with_force():
    out = os.path.join(tempfile.mkdtemp(), "residency.json")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write('{"home_location":"hk","classifications":{"non-pii":["hk"]}}')
    a = _InitArgs(path=_FIXTURE, output=out, force=True)
    rc = run_init(a, input_fn=_write_input(["sg", "non-pii"]))
    assert rc == 0
    with open(out, encoding="utf-8") as fh:
        assert json.load(fh)["home_location"] == "sg"


def test_init_non_interactive_no_prompts():
    out = os.path.join(tempfile.mkdtemp(), "residency.json")
    a = _InitArgs(path=_FIXTURE, home="hk", classes="customer-pii,non-pii", output=out)
    # input_fn is never called in non-interactive mode; pass one that would fail if used.
    rc = run_init(a, input_fn=lambda p: (_ for _ in ()).throw(AssertionError("prompted in non-interactive mode")))
    assert rc == 0
    with open(out, encoding="utf-8") as fh:
        policy = json.load(fh)
    # home + every observed jurisdiction (us) seeded into each class.
    assert set(policy["classifications"]["customer-pii"]) == {"hk", "us"}
    load_policy(out)


def test_init_rejects_unsupported_home_seat():
    out = os.path.join(tempfile.mkdtemp(), "residency.json")
    a = _InitArgs(path=_FIXTURE, home="zz", classes="non-pii", output=out)
    # non-interactive path must reject a two-letter code that is not a supported seat.
    rc = run_init(a, input_fn=lambda p: (_ for _ in ()).throw(AssertionError("prompted")))
    assert rc == 2


def test_init_interactive_rejects_unsupported_seat_then_accepts():
    out = os.path.join(tempfile.mkdtemp(), "residency.json")
    a = _InitArgs(path=_FIXTURE, output=out)
    # first answer 'zz' (rejected, re-prompted), then 'sg'; classes default to all three.
    rc = run_init(a, input_fn=_write_input(["zz", "sg"]))
    assert rc == 0
    with open(out, encoding="utf-8") as fh:
        assert json.load(fh)["home_location"] == "sg"


def test_init_single_home_flag_honored_no_reprompt():
    out = os.path.join(tempfile.mkdtemp(), "residency.json")
    a = _InitArgs(path=_FIXTURE, home="hk", output=out)
    # only --home given: home is honoured, classes are prompted (default all three).
    # input_fn is called once for classes; fail if home is re-prompted.
    calls = {"home_prompted": False}
    def _fn(prompt):
        if "Home base" in prompt:
            calls["home_prompted"] = True
        return ""  # empty -> default classes (all three)
    rc = run_init(a, input_fn=_fn)
    assert rc == 0
    assert calls["home_prompted"] is False
    with open(out, encoding="utf-8") as fh:
        assert set(json.load(fh)["classifications"]) == {"non-pii", "employee-pii", "customer-pii"}


def _kb_file(data):
    import json
    import tempfile
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(data, f)
    f.close()
    return f.name


def _scan_file(content, suffix=".py"):
    import os
    import tempfile
    from borderlint.detect import scan
    p = os.path.join(tempfile.mkdtemp(), "f" + suffix)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)
    return scan(p, kb)


def dets(src):
    return _resolve_sovereignty(_scan_py("x.py", src, kb), kb)


def test_detect_import_and_endpoint():
    by = {d.provider_id: d.jurisdiction for d in dets('import openai\nu = "https://api.deepseek.com/v1"\n')}
    assert by["openai"] == "us"
    assert by["deepseek"] == "cn"


def test_dashscope_intl_vs_mainland():
    js = sorted(d.jurisdiction for d in dets('a = "dashscope-intl.aliyuncs.com"\nb = "dashscope.aliyuncs.com"\n'))
    assert js == ["cn", "sg"]


def _pol(allow, **kw):
    return {"classifications": {"customer-pii": allow}, **kw}


def test_deny_by_default_sg_in_my_out():
    f = {x.detection.provider_id: x for x in evaluate(
        dets('import openai\nu = "https://api.deepseek.com"\n'), _pol(["hk", "CN-GBA", "sg"]), "customer-pii", kb)}
    assert f["openai"].severity == "fail"    # us not in allow-list
    assert f["deepseek"].severity == "fail"  # cn not in allow-list
    # sg IS in the allow-list -> a Singapore flow passes
    ok = evaluate(dets('u = "dashscope-intl.aliyuncs.com"\n'), _pol(["hk", "CN-GBA", "sg"]), "customer-pii", kb)
    assert ok[0].severity == "ok"


def test_gba_alias_permits_cn_gba():
    k = load_kb(_kb_file({"endpoints": {"x.local": "CN-GBA"}}))
    f = evaluate(_scan_py("x.py", 'u = "x.local"\n', k), {"classifications": {"c": ["GBA"]}}, "c", k)
    assert f[0].severity == "ok"


def test_unknown_warn_vs_fail():
    d = dets('u = "myresource.openai.azure.com"\n')  # azure -> unknown jurisdiction
    assert evaluate(d, {"classifications": {"c": ["hk"]}, "on_unknown": "warn"}, "c", kb)[0].severity == "warn"
    assert evaluate(d, {"classifications": {"c": ["hk"]}, "on_unknown": "fail"}, "c", kb)[0].severity == "fail"


def test_denied_provider():
    pol = _pol(["us"], providers={"deny": ["openai"]})
    assert evaluate(dets("import openai\n"), pol, "customer-pii", kb)[0].severity == "fail"


def test_bedrock_region_from_host():
    assert dets('u = "https://bedrock-runtime.ap-east-1.amazonaws.com/m"\n')[0].jurisdiction == "hk"
    assert dets('u = "bedrock-runtime.us-east-1.amazonaws.com"\n')[0].jurisdiction == "us"
    assert dets('u = "bedrock-runtime.cn-north-1.amazonaws.com.cn"\n')[0].jurisdiction == "cn"


def test_bedrock_dynamic_region_stays_unknown():
    # region interpolated at runtime -> not in the literal -> unknown
    assert dets('u = "https://bedrock-runtime."\n')[0].jurisdiction == "unknown"


def test_azure_standard_host_stays_unknown():
    assert dets('u = "myresource.openai.azure.com"\n')[0].jurisdiction == "unknown"


def test_azure_regional_host_resolves():
    assert dets('u = "https://eastasia.api.cognitive.microsoft.com/openai"\n')[0].jurisdiction == "hk"
    assert dets('u = "myresource.swedencentral.inference.ai.azure.com"\n')[0].jurisdiction == "se"


def js(src):
    return _resolve_sovereignty(_scan_js("x.ts", src, kb), kb)


def test_ts_import_detection():
    assert js('import OpenAI from "openai";\n')[0].provider_id == "openai"
    assert js('const a = require("@anthropic-ai/sdk");\n')[0].provider_id == "anthropic"
    assert js('const m = await import("openai");\n')[0].provider_id == "openai"


def test_ts_non_us_package():
    d = js('import { Mistral } from "@mistralai/mistralai";\n')[0]
    assert d.provider_id == "mistral" and d.jurisdiction == "eu"


def test_aggregator_unknown():
    assert dets("import litellm\n")[0].jurisdiction == "unknown"
    assert js('import { ChatOpenAI } from "@langchain/openai";\n')[0].jurisdiction == "unknown"


def test_ts_endpoint_literal_still_detected():
    d = _scan_text("x.ts", 'const u = "https://api.openai.com/v1";\n', kb)
    assert d[0].provider_id == "openai"


def test_vercel_ai_sdk():
    assert js('import { openai } from "@ai-sdk/openai";\n')[0].provider_id == "openai"
    assert js('import { generateText } from "ai";\n')[0].jurisdiction == "unknown"


def cfg(src, path="config.yaml"):
    return _resolve_sovereignty(_scan_config_endpoints(path, src, kb), kb)


def test_config_custom_host_unknown():
    assert cfg("base_url: https://llm.acme.cn/v1\n")[0].jurisdiction == "unknown"


def test_config_known_host():
    d = cfg('{"api_base": "https://api.deepseek.com"}', "config.json")
    assert d[0].provider_id == "deepseek" and d[0].jurisdiction == "cn"


def test_code_base_url_override():
    d = cfg('client = OpenAI(base_url="https://llm.acme.cn")\n', "app.py")
    assert d[0].jurisdiction == "unknown"


def test_loopback_is_local():
    assert cfg("base_url: http://localhost:8080\n")[0].jurisdiction == "local"


def test_non_ai_key_not_flagged():
    assert cfg("database_url: https://db.example.com\n") == []


def test_local_passes_strict_policy_and_not_unknown():
    loc = Detection("local", "config_endpoint", "localhost", "x", 1, "local")
    pol = {"classifications": {"c": ["hk"]}, "on_unknown": "fail"}
    assert evaluate([loc], pol, "c", kb)[0].severity == "ok"


def test_user_kb_merges_not_replaces():
    k = load_kb(_kb_file({"providers": [
        {"id": "acme", "name": "Acme", "endpoints": ["llm.acme.io"], "jurisdiction": "us"}]}))
    assert k.match_endpoint("api.deepseek.com")[2] == "cn"   # bundled still resolves
    assert k.match_endpoint("llm.acme.io")[2] == "us"        # user provider resolves


def test_endpoints_map_regions():
    k = load_kb(_kb_file({"endpoints": {"llm-cn.acme.com": "cn", "llm-sg.acme.com": "sg", "llm-hk.acme.com": "hk"}}))
    assert k.match_endpoint("llm-cn.acme.com")[2] == "cn"
    assert k.match_endpoint("llm-sg.acme.com")[2] == "sg"
    assert k.match_endpoint("llm-hk.acme.com")[2] == "hk"


def test_user_overrides_bundled_host():
    k = load_kb(_kb_file({"endpoints": {"api.openai.com": "hk"}}))
    assert k.match_endpoint("api.openai.com")[2] == "hk"


def test_invalid_token_rejected():
    try:
        load_kb(_kb_file({"endpoints": {"x.acme.com": "overseas"}}))
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_wrong_endpoint_is_violation():
    k = load_kb(_kb_file({"endpoints": {"llm-cn.acme.com": "cn"}}))
    dets = _scan_config_endpoints("c.yaml", "base_url: https://llm-cn.acme.com\n", k)
    f = evaluate(dets, {"classifications": {"customer-pii": ["hk", "sg"]}}, "customer-pii", k)
    assert f[0].severity == "fail"


def test_kb_drift_diff():
    import sys
    sys.path.insert(0, "scripts")
    import kb_drift
    known = kb_drift.known_providers({"providers": [{"id": "openai", "name": "OpenAI", "sdks": ["openai"]}]})
    gap = kb_drift.coverage_gap({"openai", "deepseek", "Mistral"}, known)
    assert gap == ["Mistral", "deepseek"]          # openai covered; sorted; names only
    assert all(isinstance(g, str) for g in gap)    # no jurisdiction/endpoint assigned


def _drift():
    import sys
    sys.path.insert(0, "scripts")
    import kb_drift
    return kb_drift


def test_kb_drift_model_coverage():
    kd = _drift()
    k = load_kb()
    ids = [("gpt-4o", "openai"), ("bedrock/anthropic.claude-3-sonnet", "bedrock"),
           ("azure/eu/gpt-4o-2024-08-06", "azure"), ("totally-made-up-model-9x", "unknown_host")]
    gap = kd.model_coverage_gap(ids, k)
    assert gap == ["totally-made-up-model-9x"]     # qualifiers of any depth covered via suffix
    # provider context: ignored providers excluded; speech tiers covered; inference still surfaces
    supp = {"aliases": {"dg": "deepgram"}, "ignore": {"apiserpent": "search"}}
    ctx = [("apiserpent/search", "apiserpent"), ("deepgram/base", "deepgram"),
           ("dg/enhanced", "dg"), ("brand-new-family-1x", "openai")]
    assert kd.model_coverage_gap(ctx, k, supp) == ["brand-new-family-1x"]
    stems = kd.family_stems(["grok-4", "vendor/grok-4-fast", "zzz-solo"])
    assert stems == [("grok", 2, "grok-4"), ("zzz", 1, "zzz-solo")]  # aggregated, count-desc


def test_kb_drift_sovereignty_gaps():
    kd = _drift()
    gaps = kd.sovereignty_gaps(["a", "b", "c"], {"a": "us", "b": "overseas"})
    assert gaps == [("b", "overseas"), ("c", None)]  # invalid + missing; valid not reported
    # the bundled data itself must be complete — the live audit stays empty
    import json
    with open("borderlint/data/providers.json", encoding="utf-8") as fh:
        ids = [p["id"] for p in json.load(fh)["providers"]]
    assert kd.sovereignty_gaps(ids, load_kb().sovereignty_map) == []


def test_kb_drift_suppression():
    kd = _drift()
    known = kd.known_providers({"providers": [{"id": "openai", "name": "OpenAI", "sdks": []}]})
    supp = {"aliases": {"chatgpt": "openai"}, "ignore": {"tavily": "web search"}}
    gap = kd.coverage_gap({"openai", "chatgpt", "tavily", "newvendor"}, known, supp)
    assert gap == ["newvendor"]                    # aliased + ignored excluded; unlisted surfaces
    # loud failures: rotten alias target, reasonless ignore
    for bad in ({"aliases": {"x": "nonexistent"}, "ignore": {}},
                {"aliases": {}, "ignore": {"y": "  "}}):
        try:
            kd.validate_suppression(bad, {"openai"})
            assert False, "expected ValueError"
        except ValueError as e:
            assert "x" in str(e) or "y" in str(e)
    # the shipped suppression file validates against the real KB
    import json
    with open("scripts/kb_drift_aliases.json", encoding="utf-8") as fh:
        shipped = json.load(fh)
    with open("borderlint/data/providers.json", encoding="utf-8") as fh:
        ids = {p["id"] for p in json.load(fh)["providers"]}
    kd.validate_suppression(shipped, ids)
    assert all(r.strip() for r in shipped["ignore"].values())
    # the scanner never reads the suppression list
    import pathlib
    for mod in pathlib.Path("borderlint").glob("*.py"):
        assert "kb_drift_aliases" not in mod.read_text(encoding="utf-8")


def test_kb_drift_residue():
    kd = _drift()
    residue = {"fireworks-ai-": "pricing bucket", "exact-junk-id": "reviewed: not actionable"}
    uncovered = ["fireworks-ai-1b-to-4b", "exact-junk-id", "exact-junk-id-v2", "new-family-1x"]
    actionable, classed = kd.split_residue(uncovered, residue)
    assert actionable == ["exact-junk-id-v2", "new-family-1x"]  # exact key ≠ its variants
    assert dict(classed) == {"pricing bucket": 1, "reviewed: not actionable": 1}
    # empty-reason residue entry fails loudly
    try:
        kd.validate_suppression({"aliases": {}, "ignore": {}, "residue": {"x-": ""}}, set())
        assert False, "expected ValueError"
    except ValueError as e:
        assert "x-" in str(e)
    # summary line + collapsed counts, no raw id lists
    r = kd.render_report(["prov1"], [("fam", 2, "fam-1")], [], [],
                         residue=[("pricing bucket", 7)])
    assert r.startswith("**Actionable:** 1 providers · 1 model families")
    assert "acknowledged residue:** 7 ids" in r and "<details>" in r
    assert "pricing bucket — 7 ids" in r
    zero = kd.render_report([], [], [], [], residue=[("reviewed", 3)])
    assert zero.startswith("**Nothing actionable.**")
    # shipped residue block validates and its reasons are non-empty
    import json
    with open("scripts/kb_drift_aliases.json", encoding="utf-8") as fh:
        shipped = json.load(fh)
    assert shipped["residue"] and all(v.strip() for v in shipped["residue"].values())


def test_kb_drift_staleness():
    import datetime as dt
    kd = _drift()
    today = dt.date(2026, 7, 4)
    stale = kd.stale_kbs({"old.json": "2026-01-01", "fresh.json": "2026-07-01"}, today)
    assert stale == [("old.json", "2026-01-01", 184)]  # stale flagged with age; fresh not


def test_kb_drift_render_report():
    kd = _drift()
    assert kd.render_report([], [], [], []) == ""  # empty report renders nothing
    r = kd.render_report(["deepseek"], [("grok", 2, "grok-4")], [("x", None)],
                         [("old.json", "2026-01-01", 184)])
    assert all(h in r for h in ("### New providers", "### Uncovered model families",
                                "### Sovereignty gaps", "### Stale knowledge bases"))
    assert "- deepseek" in r and "by hand" in r    # gap record carries no assigned bloc
    only = kd.render_report([], [("grok", 2, "grok-4")], [], [])
    assert "### New providers" not in only         # empty sections omitted
    many = [(f"fam{i:03d}", 1, f"fam{i:03d}-1b") for i in range(60)]
    capped = kd.render_report([], many, [], [])
    assert "… and 10 more families" in capped      # cap disclosed


def test_kb_has_iso_date():
    import re
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", load_kb().updated or "")


def test_scanner_has_no_network_imports():
    import inspect
    import borderlint.cli
    import borderlint.detect
    import borderlint.kb
    import borderlint.policy
    import borderlint.report
    for m in (borderlint.kb, borderlint.detect, borderlint.policy, borderlint.cli, borderlint.report):
        src = inspect.getsource(m)
        for bad in ("urllib", "requests", "httpx", "socket"):
            assert bad not in src, f"{m.__name__} references {bad}"


def test_waiver_downgrades_to_waived():
    f = evaluate(_scan_file("import openai  # borderlint: allow reviewed, US ok per SEC-1\n"),
                 _pol(["hk"]), "customer-pii", kb)
    assert any(x.severity == "waived" for x in f)
    assert not any(x.severity == "fail" for x in f)


def test_unjustified_waiver_ignored():
    f = evaluate(_scan_file("import openai  # borderlint: allow\n"), _pol(["hk"]), "customer-pii", kb)
    assert any(x.severity == "fail" for x in f)


def test_waiver_does_not_clear_deny():
    f = evaluate(_scan_file("import openai  # borderlint: allow trust me\n"),
                 _pol(["us"], providers={"deny": ["openai"]}), "customer-pii", kb)
    assert f[0].severity == "fail"


def test_sarif_output():
    import json as _json
    from borderlint.report import sarif
    f = evaluate(_scan_file("import openai\n"), _pol(["hk"]), "customer-pii", kb)
    doc = _json.loads(sarif(f, kb))
    assert doc["version"] == "2.1.0"
    assert doc["runs"][0]["tool"]["driver"]["name"] == "borderlint"
    assert len(doc["runs"][0]["results"]) == len(f)
    assert doc["runs"][0]["results"][0]["locations"][0]["physicalLocation"]["region"]["startLine"] >= 1


def test_sarif_waived_suppressed():
    import json as _json
    from borderlint.report import sarif
    f = evaluate(_scan_file("import openai  # borderlint: allow ok per SEC-9\n"), _pol(["hk"]), "customer-pii", kb)
    doc = _json.loads(sarif(f, kb))
    waived = [r for r in doc["runs"][0]["results"] if r.get("suppressions")]
    assert waived and waived[0]["level"] == "note"


def test_drift26_new_providers_resolve():
    def res(host):
        m = kb.match_endpoint(host)
        return (m[2], kb.category(m[0])) if m else None
    assert res("api.ai21.com") == ("il", "inference")
    assert res("api.stability.ai")[0] == "gb" and res("api.nlpcloud.io")[0] == "fr"
    assert res("api.bfl.ai")[0] == "de"                 # global endpoint -> company seat
    assert res("api.us.bfl.ai")[0] == "us" and res("api.eu.bfl.ai")[0] == "eu"  # regional split
    assert res("api.deepgram.com") == ("us", "speech")  # speech category
    assert res("polly.ap-east-1.amazonaws.com") == ("hk", "speech")  # aws region scheme
    assert res("us.inference.heroku.com")[0] == "us" and res("inference.heroku.com")[0] == "unknown"
    assert res("api.aimlapi.com") == ("unknown", "aggregator")
    assert res("ml.cloud.ibm.com")[0] == "unknown" and res("api.libertai.io")[0] == "unknown"
    assert kb.match_sdk("voyageai") == "voyage" and kb.match_sdk("elevenlabs") == "elevenlabs"


def _ctx(juris, **polkw):
    """A single flagged flow to `juris` -> (findings, parsed JSON report)."""
    import json as _json
    from borderlint.report import as_json
    pol = _pol(["xx"], **polkw)
    f = evaluate([Detection("openai", "sdk_import", "openai", "f.py", 1, juris)], pol, "customer-pii", kb)
    return f, _json.loads(as_json(f, kb, pol))


def test_gba_ref_for_cn_gba_only():
    _, gba = _ctx("CN-GBA", home_regime="pdpo")
    assert any("GBA Standard Contract" in r for r in gba["references"])
    _, cn = _ctx("cn", home_regime="pdpo")  # Beijing is outside the GBA -> PIPL, not the GBA contract
    assert not any("GBA Standard Contract" in r for r in cn["references"])
    assert any("PIPL" in r for r in cn["references"])


def test_gdpr_ref_for_eu_code():
    _, doc = _ctx("de", home_regime="pdpo")
    assert any("GDPR" in r for r in doc["references"])


def test_regime_tags_pdpo_pipl():
    _, doc = _ctx("cn", home_regime="pdpo")
    assert set(doc["regimes"]) == {"PDPO", "PIPL"}


def test_context_does_not_change_verdict():
    import json as _json
    from borderlint.report import sarif
    f = evaluate([Detection("openai", "sdk_import", "openai", "f.py", 1, "cn")],
                 _pol(["xx"], home_regime="pdpo"), "customer-pii", kb)
    assert f[0].severity == "fail"  # tags/refs never alter severity
    doc = _json.loads(sarif(f, kb))
    res = doc["runs"][0]["results"]
    assert len(res) == 1 and res[0]["level"] == "error"
    blob = _json.dumps(doc)
    assert "GBA" not in blob and "PIPL" not in blob and "regimes" not in blob  # SARIF carries no context


def _ctx2(jurs, **polkw):
    """(arrangement refs, regime tags) for flagged flows to `jurs` under a policy."""
    from borderlint.report import _arrangements, _regimes
    dets = [Detection(f"p{i}", "sdk_import", "p", "a.py", i + 1, j) for i, j in enumerate(jurs)]
    pol = _pol(["xx"], **polkw)
    f = evaluate(dets, pol, "customer-pii", kb)
    return _arrangements(f, pol), _regimes(f, pol)


def test_macao_home_gba_contract_and_tags():
    arr, reg = _ctx2(["CN-GBA"], home_location="mo")
    assert any("Mainland, Macao" in a for a in arr)
    assert set(reg) == {"Macao PDPA", "PIPL"}


def test_hk_home_location_contract_and_tags():
    arr, reg = _ctx2(["CN-GBA"], home_location="hk")
    assert any("Mainland, Hong Kong" in a for a in arr)
    assert set(reg) == {"PDPO", "PIPL"}


def test_both_sars_surface_both_contracts():
    arr, _ = _ctx2(["hk", "mo"], home_location="CN-GBA")
    assert any("Mainland, Hong Kong" in a for a in arr) and any("Mainland, Macao" in a for a in arr)


def test_macao_destination_implies_macao_tag():
    _, reg = _ctx2(["mo"], home_location="hk")
    assert set(reg) == {"PDPO", "Macao PDPA"}


def test_plain_cn_surfaces_no_gba_contract():
    arr, _ = _ctx2(["cn"], home_location="hk")
    assert not any("Mainland, Hong Kong" in a or "Mainland, Macao" in a for a in arr)
    assert any("PIPL cross-border" in a for a in arr)


def test_home_regime_pdpo_back_compat():
    arr, reg = _ctx2(["CN-GBA"], home_regime="pdpo")
    assert any("GBA Standard Contract" in a for a in arr) and set(reg) == {"PDPO", "PIPL"}


def test_home_regime_pipl_back_compat():
    arr, reg = _ctx2(["CN-GBA"], home_regime="pipl")
    assert any("GBA Standard Contract" in a for a in arr) and "PIPL" in reg


def test_mo_destination_no_macao_tag_under_home_regime():
    _, reg = _ctx2(["mo"], home_regime="pdpo")  # back-compat: Macao tag is home_location-only
    assert "Macao PDPA" not in reg


def test_uk_allowlist_permits_gb_flow():  # uk is an alias for gb
    f = evaluate([Detection("openai", "sdk_import", "openai", "f.py", 1, "gb")],
                 _pol(["uk", "sg"]), "customer-pii", kb)
    assert f[0].severity == "ok"


def test_uk_home_location_normalises_to_gb():
    import json, os, tempfile
    from borderlint.policy import load_policy
    p = os.path.join(tempfile.mkdtemp(), "pol.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"classifications": {"customer-pii": ["hk"]}, "home_location": "uk"}, fh)
    assert load_policy(p)["home_location"] == "gb"


def test_unmapped_home_location_degrades_gracefully():
    arr, reg = _ctx2(["us"], home_location="br")  # br (Brazil) has no entry in the regime map
    assert arr == [] and reg == []


def test_apac_emea_home_locations():
    arr, reg = _ctx2(["us"], home_location="jp")
    assert reg == ["APPI"] and any("APPI cross-border" in a for a in arr)
    arr, reg = _ctx2(["us"], home_location="uk")  # alias -> gb
    assert reg == ["UK GDPR / DPA 2018"] and any("IDTA" in a for a in arr)
    _, reg = _ctx2(["us"], home_location="kr")
    assert reg == ["PIPA"]
    arr, reg = _ctx2(["us"], home_location="au")
    assert reg == ["Privacy Act / APPs"] and any("Australian Privacy Principle 8" in a for a in arr)
    arr, reg = _ctx2(["sg"], home_location="my")
    assert "PDPA (MY)" in reg and any("s.129" in a for a in arr)


def test_eu_home_surfaces_gdpr_reference_not_tag():
    arr, reg = _ctx2(["us"], home_location="eu")     # GDPR is a reference, never a regime tag
    assert reg == [] and any("GDPR" in a for a in arr)
    arr2, reg2 = _ctx2(["de"], home_location="eu")   # eu home + eu dest: GDPR ref once, still no tag
    assert reg2 == [] and sum("GDPR" in a for a in arr2) == 1


def test_home_location_does_not_change_verdict():
    d = [Detection("openai", "sdk_import", "openai", "f.py", 1, "us")]
    base = evaluate(d, _pol(["hk"]), "customer-pii", kb)
    homed = evaluate(d, _pol(["hk"], home_location="jp"), "customer-pii", kb)
    assert base[0].severity == homed[0].severity == "fail"  # home_location is context only


def test_malformed_home_location_warns_not_fails(capsys):
    import json, os, tempfile
    from borderlint.policy import load_policy
    p = os.path.join(tempfile.mkdtemp(), "pol.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"classifications": {"customer-pii": ["hk"]}, "home_location": "United Kingdom"}, fh)
    data = load_policy(p)  # must not raise
    assert data["home_location"] == "United Kingdom"
    assert "warning" in capsys.readouterr().err.lower()


def test_unmapped_destination_no_regime_tag():
    _, reg = _ctx2(["us"], home_location="hk")  # hk -> PDPO; us maps to no regime -> no tag
    assert reg == ["PDPO"]


def _two_flows():
    return evaluate([Detection("openai", "sdk_import", "openai", "a.py", 3, "us"),
                     Detection("deepseek", "sdk_import", "deepseek", "b.py", 1, "cn")],
                    _pol(["hk"]), "customer-pii", kb)


def test_sbom_envelope_and_flows():
    import json as _json
    from borderlint.report import sbom
    doc = _json.loads(sbom(_two_flows(), kb))
    assert doc["schema"] == "borderlint.ai-dataflow-sbom/1"
    assert doc["kb_updated"] == kb.updated and "borderlint" in doc
    pids = [c["provider"] for c in doc["components"]]
    assert pids == sorted(pids) == ["deepseek", "openai"]
    oa = next(c for c in doc["components"] if c["provider"] == "openai")
    assert oa["jurisdictions"] == ["us"] and oa["sites"][0]["file"] == "a.py"


def test_sbom_is_severity_free():
    from borderlint.report import sbom
    f = evaluate([Detection("openai", "sdk_import", "openai", "a.py", 1, "us")], _pol(["hk"]), "customer-pii", kb)
    assert f[0].severity == "fail"  # would gate under a normal format
    blob = sbom(f, kb)
    assert "severity" not in blob and "level" not in blob and "fail" not in blob


def test_sbom_deterministic_regardless_of_input_order():
    from borderlint.report import sbom
    f = _two_flows()
    assert sbom(f, kb) == sbom(list(reversed(f)), kb)  # input order must not change bytes


def test_sbom_does_not_gate():
    import json as _json
    import os
    import tempfile
    import borderlint.cli as cli
    d = tempfile.mkdtemp()
    with open(os.path.join(d, "app.py"), "w") as fh:
        fh.write("import openai\n")  # us, would fail an hk-only policy
    polf = os.path.join(d, "pol.json")
    with open(polf, "w") as fh:
        fh.write(_json.dumps({"classifications": {"customer-pii": ["hk"]}}))
    assert cli.main(["scan", d, "--policy", polf, "--classification", "customer-pii", "--format", "sbom"]) == 0
    assert cli.main(["scan", d, "--format", "sbom"]) == 0  # inventory, no policy


def _comp(pid, name, jurs):
    return {"provider": pid, "name": name, "jurisdictions": jurs, "sites": []}


def _diff_exit(old_comps, new_comps):
    import json as _json
    import os
    import tempfile
    import borderlint.cli as cli
    d = tempfile.mkdtemp()
    paths = []
    for i, comps in enumerate((old_comps, new_comps)):
        p = os.path.join(d, f"{i}.json")
        with open(p, "w") as fh:
            _json.dump({"schema": "borderlint.ai-dataflow-sbom/1", "components": comps}, fh)
        paths.append(p)
    return cli.main(["diff", paths[0], paths[1]])


def test_diff_flows_added_removed_and_swap():
    from borderlint.report import diff_flows
    old = {"components": [_comp("openai", "OpenAI", ["us"])]}
    new = {"components": [_comp("deepseek", "DeepSeek", ["cn"])]}
    d = diff_flows(old, new)
    assert [(f["provider"], f["jurisdiction"]) for f in d["added"]] == [("deepseek", "cn")]
    assert [(f["provider"], f["jurisdiction"]) for f in d["removed"]] == [("openai", "us")]
    ds = diff_flows(new, old)  # swap inverts added/removed
    assert [(f["provider"], f["jurisdiction"]) for f in ds["added"]] == [("openai", "us")]
    assert [(f["provider"], f["jurisdiction"]) for f in ds["removed"]] == [("deepseek", "cn")]


def test_diff_new_nonlocal_egress_gates():
    assert _diff_exit([], [_comp("openai", "OpenAI", ["us"])]) == 1


def test_diff_new_unknown_gates():
    assert _diff_exit([], [_comp("custom_endpoint", "Custom", ["unknown"])]) == 1


def test_diff_local_only_does_not_gate():
    assert _diff_exit([], [_comp("local", "Local inference", ["local"])]) == 0


def test_diff_removed_only_does_not_gate():
    assert _diff_exit([_comp("openai", "OpenAI", ["us"])], []) == 0


def test_diff_rejects_non_sbom_input():
    import json as _json
    import os
    import tempfile
    import borderlint.cli as cli
    d = tempfile.mkdtemp()
    bad = os.path.join(d, "bad.json")
    with open(bad, "w") as fh:
        _json.dump({"hello": "world"}, fh)
    good = os.path.join(d, "good.json")
    with open(good, "w") as fh:
        _json.dump({"schema": "borderlint.ai-dataflow-sbom/1", "components": []}, fh)
    assert cli.main(["diff", good, bad]) == 2
    assert cli.main(["diff", bad, good]) == 2


def _api(content, suffix=".ts"):
    return [d for d in _scan_file(content, suffix) if d.kind == "api_call"]


def test_openai_compat_runtime_host_unknown():
    d = _api("const u = `${LLAMA_URL}/v1/chat/completions`;\nfetch(u);\n")
    assert len(d) == 1 and d[0].provider_id == "custom_endpoint" and d[0].jurisdiction == "unknown"


def test_openai_compat_host_outside_literal_unknown():
    d = _api('r = base + "/v1/chat/completions"\n', ".py")
    assert len(d) == 1 and d[0].jurisdiction == "unknown"


def test_openai_compat_loopback_local():
    d = _api('fetch("http://localhost:8080/v1/chat/completions")\n')
    assert len(d) == 1 and d[0].provider_id == "local" and d[0].jurisdiction == "local"


def test_openai_compat_known_host_identified_once():
    ds = _scan_file('fetch("https://api.openai.com/v1/chat/completions")\n', ".ts")
    oa = [x for x in ds if x.provider_id == "openai"]
    assert len(oa) == 1 and oa[0].jurisdiction == "us"  # not double-counted by the api_call detector


def test_openai_compat_known_host_cn():
    ds = _scan_file('r = requests.post("https://api.deepseek.com/v1/chat/completions")\n', ".py")
    dk = [x for x in ds if x.provider_id == "deepseek"]
    assert len(dk) == 1 and dk[0].jurisdiction == "cn"


def test_openai_compat_non_ai_v1_not_flagged():
    assert _api('fetch("https://internal.example/v1/users")\nx = "/api/v1/health"\n') == []


def test_mlabel_entity_escape():
    from borderlint.report import _mlabel
    assert _mlabel("a#b") == '"a#35;b"'
    assert _mlabel('a"b') == '"a#quot;b"'
    assert _mlabel('a#"b') == '"a#35;#quot;b"'  # # escaped first; the quote-escape's # is not re-escaped


def test_mermaid_labels_are_quoted():
    from borderlint.report import mermaid
    f = evaluate([Detection("custom_endpoint", "api_call", "/v1/chat/completions", "a.ts", 1, "unknown")],
                 _pol(["hk"]), "customer-pii", kb)
    out = mermaid(f, kb)
    assert 'app(["Your application"])' in out
    assert '["Custom / OpenAI-compatible endpoint (Unknown)"]' in out  # provider label + sovereignty bloc
    assert 'subgraph j_unknown["unknown"]' in out             # zone titled by the jurisdiction code
    assert "custom_endpoint__unknown[" in out                 # node id is per (provider, jurisdiction)


def _tmp_with(files):
    import os
    import tempfile
    d = tempfile.mkdtemp()
    for name, content in files.items():
        with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
            fh.write(content)
    return d


def test_project_label_package_json():
    import json as _json
    from borderlint.report import project_label
    d = _tmp_with({"package.json": _json.dumps({"name": "acme-bot", "version": "1.2.3"})})
    assert project_label(d) == "acme-bot@1.2.3"


def test_project_label_pyproject():
    from borderlint.report import project_label
    d = _tmp_with({"pyproject.toml": '[project]\nname = "acme"\nversion = "0.4.0"\n'})
    assert project_label(d) == "acme@0.4.0"


def test_project_label_name_only():
    from borderlint.report import project_label
    d = _tmp_with({"package.json": '{"name": "nameonly"}'})
    assert project_label(d) == "nameonly"


def test_project_label_dir_fallback():
    import os
    from borderlint.report import project_label
    d = _tmp_with({"README.md": "hi"})  # no manifest, no git
    assert project_label(d) == os.path.basename(d)


def test_project_label_sanitizes_and_escapes():
    import json as _json
    from borderlint.report import project_label, mermaid
    d = _tmp_with({"package.json": _json.dumps({"name": 'a"b#c\nd', "version": "1"})})
    lab = project_label(d)
    assert "\n" not in lab and lab.endswith("@1")  # collapsed to a single line, version kept
    out = mermaid(evaluate([Detection("openai", "sdk_import", "openai", "a.py", 1, "us")],
                           _pol(["hk"]), "customer-pii", kb), kb, None, lab)
    assert "#quot;" in out and "#35;" in out       # the " and # are escaped in the root node


def test_project_label_git_tag_wins():
    import os
    import shutil
    import subprocess
    from borderlint.report import project_label
    if not shutil.which("git"):
        return  # skip when git is unavailable
    d = _tmp_with({"pyproject.toml": '[project]\nname = "gitproj"\nversion = "9.9.9"\n'})
    g = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, check=True)
    g("init", "-q")
    g("-c", "user.name=t", "-c", "user.email=t@t", "commit", "--allow-empty", "-q", "-m", "x")
    g("tag", "v2.0.0")
    assert project_label(d) == "gitproj@v2.0.0"  # git tag preferred over the manifest's 9.9.9


def test_mermaid_multi_jurisdiction_provider():
    from borderlint.report import mermaid
    f = evaluate([Detection("aws_bedrock", "endpoint_reference", "x", "a.py", 1, "us"),
                  Detection("aws_bedrock", "endpoint_reference", "y", "a.py", 2, "de")],
                 _pol(["hk"]), "customer-pii", kb)
    out = mermaid(f, kb)
    assert 'subgraph j_us["us"]' in out and 'subgraph j_de["de"]' in out   # zones titled by code
    assert "aws_bedrock__us[" in out and "aws_bedrock__de[" in out          # distinct node per zone
    assert "app --> aws_bedrock__us" in out and "app --> aws_bedrock__de" in out  # an edge to each


def test_precommit_hook_definition():
    # The hook wraps `borderlint scan` and must NOT pass pre-commit's staged-file list — borderlint
    # resolves/de-dups at directory granularity (ci-integration spec: "scans the path, not the list").
    import os
    txt = open(os.path.join(os.path.dirname(__file__), "..", ".pre-commit-hooks.yaml"), encoding="utf-8").read()
    assert "id: borderlint" in txt
    assert "entry: borderlint scan" in txt
    assert "pass_filenames: false" in txt


def test_vector_store_detection():
    # A managed vector DBaaS import is detected as a data sink: category vector_store, jurisdiction unknown.
    d = {x.provider_id: x for x in dets('import pinecone\nimport qdrant_client\n')}
    assert d["pinecone"].jurisdiction == "unknown" and kb.category("pinecone") == "vector_store"
    assert d["qdrant"].jurisdiction == "unknown" and kb.category("qdrant") == "vector_store"
    assert kb.category("openai") == "inference"  # default for an inference provider


def test_new_inference_providers_resolve():
    by = {d.provider_id: d.jurisdiction for d in dets(
        'import cerebras\nimport baseten\na = "https://api.fireworks.ai/inference/v1"\n')}
    assert by["cerebras"] == "us"
    assert by["baseten"] == "us"
    assert by["fireworks_ai"] == "us"


def test_category_in_output_does_not_change_verdict():
    from borderlint.report import as_json, sbom, text
    import json as _json
    # Same flow scanned with on_unknown warn -> a vector store resolves unknown but must not fail.
    f = evaluate(dets('import pinecone\n'), _pol(["hk"], on_unknown="warn"), "customer-pii", kb)
    assert all(x.severity != "fail" for x in f)              # category doesn't gate; unknown+warn -> warn
    assert "(vector store)" in text(f, kb)                   # text annotates the sink
    assert _json.loads(as_json(f, kb))["findings"][0]["category"] == "vector_store"
    assert _json.loads(sbom(f, kb))["components"][0]["category"] == "vector_store"


def test_oversized_file_is_skipped():
    # A file over the cap is excluded (memory-exhaustion guard); a normal file is still scanned.
    from borderlint.detect import MAX_FILE_BYTES
    big = 'import openai\n' + ('# ' + 'x' * 80 + '\n') * ((MAX_FILE_BYTES // 82) + 1)
    assert len(big.encode()) > MAX_FILE_BYTES
    assert _scan_file(big, ".py") == []                       # skipped: nothing detected
    assert {d.provider_id for d in _scan_file('import openai\n', ".py")} == {"openai"}  # normal still scans


def test_vertex_ai_gcp_region_resolution():
    # Vertex region lives in the host (like Bedrock/Azure); the global endpoint carries none.
    r = {h: kb.match_endpoint(h) for h in [
        "asia-east2-aiplatform.googleapis.com", "europe-west4-aiplatform.googleapis.com",
        "us-central1-aiplatform.googleapis.com", "aiplatform.googleapis.com",
        "aiplatform.eu.rep.googleapis.com"]}
    assert r["asia-east2-aiplatform.googleapis.com"] == ("vertex_ai", "aiplatform.googleapis.com", "hk")
    assert r["europe-west4-aiplatform.googleapis.com"][2] == "nl"
    assert r["us-central1-aiplatform.googleapis.com"][2] == "us"
    assert r["aiplatform.googleapis.com"][2] == "unknown"            # global endpoint -> unknown
    assert r["aiplatform.eu.rep.googleapis.com"][2] == "eu"          # multi-region rep host


def test_drift_providers_resolve():
    assert kb.match_endpoint("gigachat.devices.sberbank.ru")[2] == "ru"
    assert kb.match_endpoint("api.sarvam.ai")[2] == "in"
    assert kb.match_endpoint("api.scaleway.ai")[2] == "fr"
    assert kb.match_endpoint("ark.cn-beijing.volces.com")[0:1] + (kb.match_endpoint("ark.cn-beijing.volces.com")[2],) == ("volcengine", "cn")
    assert kb.match_sdk("ollama") == "ollama" and kb.default_jurisdiction("ollama") == "local"
    assert kb.match_endpoint("https://max.ai/v1") is None            # x.ai host must not false-match


def test_minimax_split_endpoints():
    assert kb.match_endpoint("api.minimaxi.com")[2] == "cn"          # China endpoint
    assert kb.match_endpoint("api.minimax.io")[2] == "unknown"       # intl endpoint, DC undocumented


# --- Sovereignty dimension ---------------------------------------------------

def _det(pid="openai", juris="us", evidence="openai"):
    sov = kb.resolve_sovereignty(pid, evidence, juris)
    return Detection(pid, "sdk_import", evidence, "f.py", 1, juris, sovereignty=sov)


def _sov_pol(allow, **kw):
    """A policy with a sovereignty allow-list for customer-pii."""
    return {"classifications": {"customer-pii": ["hk", "CN-GBA", "sg", "us", "gb", "eu", "uk"]},
            "sovereignty": {"classifications": {"customer-pii": allow}}, **kw}


def test_sovereignty_resolution():
    # Bedrock ap-east-1 -> residency hk, sovereignty us (provider's home sovereign, not the region's)
    d = dets('u = "https://bedrock-runtime.ap-east-1.amazonaws.com/m"\n')[0]
    assert d.jurisdiction == "hk" and d.sovereignty == "us"
    # Provider sovereignty matches residency for home-sovereign providers
    assert dets('a = "https://api.deepseek.com"\n')[0].sovereignty == "cn"
    assert dets('a = "https://api.stability.ai"\n')[0].sovereignty == "uk"
    assert dets('a = "https://gigachat.devices.sberbank.ru"\n')[0].sovereignty == "ru"
    assert dets('a = "https://api.sarvam.ai"\n')[0].sovereignty == "in"
    assert dets('a = "https://api.ai21.com"\n')[0].sovereignty == "il"
    assert dets('import mistralai\n')[0].sovereignty == "eu"
    # Cohere: US endpoint (residency us) but Canadian-headquartered → sovereignty ca (orthogonal)
    c = dets('import cohere\n')[0]
    assert c.jurisdiction == "us" and c.sovereignty == "ca"
    # Loopback / self-hosted -> local sovereignty (no external sovereign)
    assert cfg("base_url: http://localhost:8080\n")[0].sovereignty == "local"
    assert dets('import ollama\n')[0].sovereignty == "local"
    # Aggregators and custom endpoints -> unknown sovereignty
    assert dets('import litellm\n')[0].sovereignty == "unknown"
    assert cfg("base_url: https://llm.acme.cn/v1\n")[0].sovereignty == "unknown"


def test_sovereignty_host_override():
    # AWS China regions (Sinnet/NWCD) override the provider sovereignty us -> cn
    d = dets('u = "https://bedrock-runtime.cn-north-1.amazonaws.com.cn/m"\n')[0]
    assert d.jurisdiction == "cn" and d.sovereignty == "cn"
    d2 = dets('u = "bedrock-runtime.cn-northwest-1.amazonaws.com.cn"\n')[0]
    assert d2.sovereignty == "cn"


def test_sovereignty_unknown_fail():
    # sovereignty.on_unknown: "fail" fails an unknown-sovereignty flow on its own — symmetric with
    # residency on_unknown, and no longer requires "sovereignty" in fail_on as a second gate.
    pol = {"classifications": {"customer-pii": ["hk", "CN-GBA", "sg", "us", "gb", "eu", "uk"]},
           "sovereignty": {"on_unknown": "fail", "classifications": {"customer-pii": ["eu"]}}}
    f = evaluate([_det("litellm", "unknown", "litellm")], pol, "customer-pii", kb)
    assert "sovereignty_unknown" in f[0].reasons and f[0].severity == "fail"


def test_sovereignty_policy_absent():
    # No sovereignty block -> no sovereignty reason, exit behaviour unchanged (regression guard)
    pol = {"classifications": {"customer-pii": ["hk"]}}
    f = evaluate([_det("openai", "us")], pol, "customer-pii", kb)
    assert f[0].severity == "fail"
    assert "sovereignty" not in f[0].reasons and "sovereignty_unknown" not in f[0].reasons


def test_sovereignty_evaluation():
    allow = ["eu", "uk", "local"]
    # us-sovereignty flow -> sovereignty reason (mismatch)
    f = evaluate([_det("openai", "us")], _sov_pol(allow), "customer-pii", kb)
    assert "sovereignty" in f[0].reasons
    # eu-sovereignty flow -> passes sovereignty check
    f = evaluate([_det("mistral", "eu", "mistralai")], _sov_pol(allow), "customer-pii", kb)
    assert "sovereignty" not in f[0].reasons and f[0].severity == "ok"
    # local-sovereignty flow -> exempt regardless of allow-list
    f = evaluate([Detection("ollama", "sdk_import", "ollama", "f.py", 1, "local")],
                 _sov_pol(allow), "customer-pii", kb)
    assert "sovereignty" not in f[0].reasons
    # unknown-sovereignty flow -> warns under on_unknown: warn
    f = evaluate([_det("litellm", "unknown", "litellm")], _sov_pol(allow, **{"on_unknown": "warn"}),
                 "customer-pii", kb)
    assert "sovereignty_unknown" in f[0].reasons and f[0].severity == "warn"


def test_sovereignty_fail_on():
    allow = ["eu", "uk", "local"]
    # With fail_on including sovereignty -> a mismatch fails
    pol_fail = _sov_pol(allow, fail_on=["residency", "denied_provider", "sovereignty"])
    f = evaluate([_det("openai", "us")], pol_fail, "customer-pii", kb)
    assert f[0].severity == "fail"
    # Without sovereignty in fail_on -> the same mismatch only warns
    pol_warn = _sov_pol(allow, fail_on=["residency", "denied_provider"])
    f = evaluate([_det("openai", "us")], pol_warn, "customer-pii", kb)
    assert f[0].severity == "warn"


def test_sovereignty_waiver():
    allow = ["eu", "uk", "local"]
    pol = _sov_pol(allow, fail_on=["residency", "denied_provider", "sovereignty"])
    d = Detection("openai", "sdk_import", "openai", "f.py", 1, "us",
                  waiver="CLOUD Act review done", sovereignty="us")
    f = evaluate([d], pol, "customer-pii", kb)
    assert f[0].severity == "waived"  # justified waiver downgrades the sovereignty failure
    # A provider deny-list entry is NOT waived
    pol_deny = _sov_pol(allow, fail_on=["residency", "denied_provider", "sovereignty"],
                        providers={"deny": ["openai"]})
    f = evaluate([d], pol_deny, "customer-pii", kb)
    assert f[0].severity == "fail"


def test_sovereignty_reporting():
    import json as _json
    from borderlint.report import as_json, text, mermaid
    allow = ["eu", "uk", "local"]
    pol = _sov_pol(allow, fail_on=["sovereignty"])
    f = evaluate([_det("openai", "us")], pol, "customer-pii", kb)
    # Text report: sovereignty column present
    txt = text(f, kb, pol)
    assert "sovereignty:" in txt.lower() and "United States" in txt
    # JSON report: sovereignty field per finding
    doc = _json.loads(as_json(f, kb, pol))
    assert doc["findings"][0]["sovereignty"] == "us"
    # Mermaid: node label includes the sovereignty bloc
    mm = mermaid(f, kb, pol)
    assert "(United States)" in mm


def test_sovereignty_invalid_token():
    # A user-supplied sovereignty map with an unrecognised bloc is rejected
    try:
        load_kb(_kb_file({"sovereignty": {"openai": "overseas"}}))
        assert False, "expected ValueError"
    except ValueError:
        pass
    # And an invalid bloc in a policy sovereignty block is rejected at load time
    import json, os, tempfile
    from borderlint.policy import load_policy
    p = os.path.join(tempfile.mkdtemp(), "pol.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"classifications": {"customer-pii": ["hk"]},
                   "sovereignty": {"classifications": {"customer-pii": ["mars"]}}}, fh)
    try:
        load_policy(p)
        assert False, "expected ValueError"
    except ValueError:
        pass


# --- Provenance dimension ----------------------------------------------------

def _mprov_pol(allow, **kw):
    """A policy with a provenance allow-list for customer-pii."""
    return {"classifications": {"customer-pii": ["hk", "CN-GBA", "sg", "us", "gb", "eu", "uk"]},
            "provenance": {"classifications": {"customer-pii": allow}}, **kw}


def test_provenance_resolution():
    # Tier 1 — one per ID form: managed-platform, bare API name, aggregator-qualified, hub repo
    assert kb.match_model("anthropic.claude-sonnet-4-6")[1] == "us"
    assert kb.match_model("deepseek.r1-v1:0")[1] == "cn"
    assert kb.match_model("claude-sonnet-4-6")[1] == "us"
    assert kb.match_model("qwen2.5-72b-instruct")[1] == "cn"
    assert kb.match_model("mixtral-8x22b")[1] == "eu"
    assert kb.match_model("deepseek/deepseek-r1")[1] == "cn"
    assert kb.match_model("Qwen/Qwen2.5-72B-Instruct")[1] == "cn"  # case-insensitive hub id
    assert kb.match_model("stabilityai/stable-diffusion-3.5")[1] == "uk"
    # Anchoring: prose and non-model strings never match
    assert kb.match_model("gpt-4 is great for this") is None
    assert kb.match_model("unrelated-string") is None
    # Tier 2 — first-party default vs multi-model host
    assert kb.default_provenance("openai") == "us"
    assert kb.default_provenance("deepseek") == "cn"
    assert kb.default_provenance("aws_bedrock") == "unknown"
    assert kb.default_provenance("litellm") == "unknown"
    # Longest prefix wins: a longer user pattern overrides the bundled shorter one
    k = load_kb(_kb_file({"provenance": {"qwen-inhouse-": "eu"}}))
    assert k.match_model("qwen-inhouse-7b")[1] == "eu"   # longer user prefix
    assert k.match_model("qwen2.5-72b")[1] == "cn"       # bundled prefix still applies
    # User precedence beats bundled length: a shorter user prefix wins over a longer bundled one
    k2 = load_kb(_kb_file({"provenance": {"deepseek": "eu"}}))
    assert k2.match_model("deepseek-r1")[1] == "eu"      # user prefix beats bundled "deepseek-"


def test_provenance_binding():
    # Same-file binding: provider flow carries the model reference's provenance + identifier
    ds = _scan_file('import openai\nm = "gpt-4o"\n')
    assert len(ds) == 1 and ds[0].kind == "sdk_import"
    assert ds[0].provenance == "us" and ds[0].model == "gpt-4o"
    # The headline divergence: Bedrock ap-east-1 serving DeepSeek -> hk / us / cn
    ds = _scan_file('u = "https://bedrock-runtime.ap-east-1.amazonaws.com/m"\nm = "deepseek.r1-v1:0"\n')
    d = [x for x in ds if x.kind != "model_reference"][0]
    assert (d.jurisdiction, d.sovereignty, d.provenance) == ("hk", "us", "cn")
    # Self-hosted weights: local flow + qwen model -> local / local / cn
    ds = _scan_file('base_url: "http://localhost:11434"\nmodel: "qwen2.5"\n', suffix=".yaml")
    d = [x for x in ds if x.kind == "config_endpoint"][0]
    assert (d.jurisdiction, d.sovereignty, d.provenance) == ("local", "local", "cn")
    # Standalone: a model reference with no provider in the file stands alone
    ds = _scan_file('MODEL = "deepseek/deepseek-r1"\n')
    assert len(ds) == 1 and ds[0].kind == "model_reference"
    assert ds[0].provider_id == "model_reference" and ds[0].provenance == "cn"
    assert ds[0].jurisdiction == "unknown" and ds[0].model == "deepseek/deepseek-r1"
    # Ambiguous blocs: providers stay unbound (tier-2), refs fall back to standalone rows
    ds = _scan_file('import openai\na = "gpt-4o"\nb = "deepseek-r1"\n')
    prov_det = [x for x in ds if x.kind == "sdk_import"][0]
    assert prov_det.model is None and prov_det.provenance == "us"  # tier-2 first-party default
    assert len([x for x in ds if x.kind == "model_reference"]) == 2
    # No false positive on prose
    assert _scan_file('note = "gpt-4 is great for this"\n') == []


def test_provenance_policy_absent():
    # No provenance block -> no provenance reason, exit behaviour unchanged (regression guard)
    pol = {"classifications": {"customer-pii": ["hk"]}}
    f = evaluate([_det("openai", "us")], pol, "customer-pii", kb)
    assert "provenance" not in f[0].reasons and "provenance_unknown" not in f[0].reasons
    # A standalone model reference is a weights signal, not a flow: no residency reasons either
    d = Detection("model_reference", "model_reference", "deepseek-r1", "f.py", 1, "unknown",
                  provenance="cn", model="deepseek-r1")
    f = evaluate([d], pol, "customer-pii", kb)
    assert f[0].severity == "ok" and f[0].reasons == []


def test_provenance_evaluation():
    allow = ["us", "eu"]
    mk = lambda prov: Detection("openai", "sdk_import", "openai", "f.py", 1, "us",
                                sovereignty="us", provenance=prov)
    # cn-provenance flow -> provenance reason (mismatch)
    f = evaluate([mk("cn")], _mprov_pol(allow), "customer-pii", kb)
    assert "provenance" in f[0].reasons
    # eu-provenance flow -> passes
    f = evaluate([mk("eu")], _mprov_pol(allow), "customer-pii", kb)
    assert "provenance" not in f[0].reasons and f[0].severity == "ok"
    # unknown-provenance flow -> warns under on_unknown: warn (default)
    f = evaluate([mk("unknown")], _mprov_pol(allow), "customer-pii", kb)
    assert "provenance_unknown" in f[0].reasons and f[0].severity == "warn"
    # A standalone model reference IS provenance-evaluated
    d = Detection("model_reference", "model_reference", "deepseek-r1", "f.py", 1, "unknown",
                  provenance="cn", model="deepseek-r1")
    f = evaluate([d], _mprov_pol(allow), "customer-pii", kb)
    assert "provenance" in f[0].reasons and "unknown" not in f[0].reasons


def test_provenance_fail_on():
    allow = ["us", "eu"]
    d = Detection("openai", "sdk_import", "openai", "f.py", 1, "us", sovereignty="us", provenance="cn")
    # With fail_on including provenance -> a mismatch fails
    f = evaluate([d], _mprov_pol(allow, fail_on=["residency", "denied_provider", "provenance"]),
                 "customer-pii", kb)
    assert f[0].severity == "fail"
    # Without provenance in fail_on -> the same mismatch only warns
    f = evaluate([d], _mprov_pol(allow, fail_on=["residency", "denied_provider"]), "customer-pii", kb)
    assert f[0].severity == "warn"
    # Symmetric unknown gate: on_unknown fail gates on its own, no second fail_on gate needed
    du = Detection("litellm", "sdk_import", "litellm", "f.py", 1, "unknown", provenance="unknown")
    pol = {"classifications": {"customer-pii": ["hk", "CN-GBA", "sg", "us", "gb", "eu", "uk"]},
           "provenance": {"on_unknown": "fail", "classifications": {"customer-pii": allow}}}
    f = evaluate([du], pol, "customer-pii", kb)
    assert "provenance_unknown" in f[0].reasons and f[0].severity == "fail"


def test_provenance_waiver():
    allow = ["us", "eu"]
    pol = _mprov_pol(allow, fail_on=["residency", "denied_provider", "provenance"])
    d = Detection("openai", "sdk_import", "openai", "f.py", 1, "us",
                  waiver="weights origin reviewed", sovereignty="us", provenance="cn")
    f = evaluate([d], pol, "customer-pii", kb)
    assert f[0].severity == "waived"  # justified waiver downgrades the provenance failure
    # A provider deny-list entry is NOT waived
    pol_deny = _mprov_pol(allow, fail_on=["residency", "denied_provider", "provenance"],
                          providers={"deny": ["openai"]})
    f = evaluate([d], pol_deny, "customer-pii", kb)
    assert f[0].severity == "fail"


def test_provenance_reporting():
    import json as _json
    from borderlint.report import as_json, text, mermaid, sarif, sbom
    allow = ["us", "eu"]
    pol = _mprov_pol(allow, fail_on=["provenance"])
    d = Detection("aws_bedrock", "endpoint_reference", "bedrock-runtime.ap-east-1.amazonaws.com",
                  "f.py", 1, "hk", sovereignty="us", provenance="cn", model="deepseek.r1-v1:0")
    f = evaluate([d], pol, "customer-pii", kb)
    # Text: weights segment + model on the site line
    txt = text(f, kb, pol)
    assert "weights:" in txt and "Mainland China" in txt and "[model: deepseek.r1-v1:0]" in txt
    # JSON: provenance + model fields
    doc = _json.loads(as_json(f, kb, pol))
    assert doc["findings"][0]["provenance"] == "cn" and doc["findings"][0]["model"] == "deepseek.r1-v1:0"
    # Mermaid: provenance appended only when it diverges from sovereignty
    assert "(United States, weights Mainland China)" in mermaid(f, kb, pol)
    same = evaluate([Detection("openai", "sdk_import", "openai", "f.py", 1, "us",
                               sovereignty="us", provenance="us")], pol, "customer-pii", kb)
    assert "weights" not in mermaid(same, kb, pol)
    # SARIF: provenance in the message
    assert "weights Mainland China" in sarif(f, kb, pol)
    # SBOM: provenances aggregated per component
    bom = _json.loads(sbom(f, kb, pol))
    assert bom["components"][0]["provenances"] == ["cn"]


def test_provenance_invalid_token():
    # A user-supplied provenance map with an unrecognised bloc is rejected
    try:
        load_kb(_kb_file({"provenance": {"gpt-": "overseas"}}))
        assert False, "expected ValueError"
    except ValueError:
        pass
    # `local` is not a provenance bloc (weights always have a developer)
    import json, os, tempfile
    from borderlint.policy import load_policy
    p = os.path.join(tempfile.mkdtemp(), "pol.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"classifications": {"customer-pii": ["hk"]},
                   "provenance": {"classifications": {"customer-pii": ["local"]}}}, fh)
    try:
        load_policy(p)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_provenance_local_models():
    # Redistributor-qualified (GGUF/MLX hubs): org stripped, family name carries provenance
    assert kb.match_model("mlx-community/Qwen2.5-7B-Instruct-4bit")[1] == "cn"
    assert kb.match_model("TheBloke/Llama-2-7B-GGUF")[1] == "us"
    assert kb.match_model("bartowski/Meta-Llama-3.1-8B-Instruct-GGUF")[1] == "us"
    assert kb.match_model("unsloth/DeepSeek-R1-GGUF")[1] == "cn"
    # GGUF file paths match by basename
    assert kb.match_model("models/qwen2.5-7b-instruct-q4_k_m.gguf")[1] == "cn"
    assert kb.match_model("/opt/llm/Meta-Llama-3.1-8B-Q5_K_S.gguf")[1] == "us"
    # Ollama-style bare tags
    assert kb.match_model("llama3.2")[1] == "us"
    assert kb.match_model("phi4")[1] == "us"
    assert kb.match_model("gemma2:9b")[1] == "us"
    assert kb.match_model("qwq:32b")[1] == "cn"
    assert kb.match_model("mistral:7b")[1] == "eu"
    # Tool names that resemble a family prefix are not models
    assert kb.match_model("llama_index") is None
    assert kb.match_model("llama-cpp-python") is None
    assert kb.match_model("llamafile") is None
    # Formerly out-of-vocabulary families resolve since bloc-vocabulary-completion
    assert kb.match_model("falcon-180b")[1] == "ae"
    # e2e: ollama + a bound tag -> residency local, sovereignty local, provenance us
    ds = _scan_file('import ollama\nm = "llama3.2"\n')
    d = [x for x in ds if x.kind == "sdk_import"][0]
    assert (d.jurisdiction, d.sovereignty, d.provenance) == ("local", "local", "us")
    assert d.model == "llama3.2"


def test_bloc_vocabulary_completion():
    k = load_kb()
    # resolution per new bloc; org-anchored and pinned-stem forms
    assert k.match_model("tiiuae/falcon-180B")[1] == "ae"
    assert k.match_model("falcon-40b-instruct")[1] == "ae"
    assert k.match_model("exaone-3.5-7.8b-instruct")[1] == "kr"
    assert k.match_model("upstage/SOLAR-10.7B-v1.0")[1] == "kr"
    assert k.match_model("aisingapore/gemma-sea-lion-v4-27b-it")[1] == "sg"
    assert k.match_model("pfnet/plamo-2-8b")[1] == "jp"
    assert k.match_model("sakana/tinyswallow-1.5b")[1] == "jp"
    # anchoring holds: collision-prone stems stay pinned, bare words don't match
    assert k.match_model("solarwinds-agent") is None
    assert k.match_model("falcon") is None
    # user KB accepts the new tokens
    k2 = load_kb(_kb_file({"provenance": {"acme-model": "sg"}}))
    assert k2.match_model("acme-model-v1")[1] == "sg"
    # policy blocks accept the new tokens for both dimensions
    import json, os, tempfile
    from borderlint.policy import load_policy
    p = os.path.join(tempfile.mkdtemp(), "pol.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"classifications": {"customer-pii": ["hk"]},
                   "sovereignty": {"classifications": {"customer-pii": ["jp", "au"]}},
                   "provenance": {"classifications": {"customer-pii": ["kr", "ae"]}}}, fh)
    pol = load_policy(p)
    # a flow with sovereignty jp passes the check (not just load-time acceptance)
    from borderlint.detect import Detection
    from borderlint.policy import evaluate
    d = Detection("openai", "sdk_import", "import openai", "a.py", 1,
                  jurisdiction="hk", sovereignty="jp")
    f = evaluate([d], pol, "customer-pii", k)[0]
    assert "sovereignty" not in f.reasons
    # user-KB sovereignty override accepts a new token
    k3 = load_kb(_kb_file({"sovereignty": {"openai": "jp"}}))
    assert k3.sovereignty_map["openai"] == "jp"
    # invalid tokens still reject
    try:
        load_kb(_kb_file({"provenance": {"gpt-": "nz"}}))
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_bloc_vocabulary_sources_and_display():
    import json
    from borderlint.kb import _SOVEREIGNTY_BLOCS
    from borderlint.report import SOVEREIGNTY
    with open("borderlint/data/sovereignty.json", encoding="utf-8") as fh:
        sources = json.load(fh)["sources"]
    for bloc in _SOVEREIGNTY_BLOCS:
        assert bloc in sources, f"no source note for {bloc}"
        assert bloc in SOVEREIGNTY, f"no display name for {bloc}"
    # bundled patterns are trusted at load time: guard that every bloc is in-vocabulary
    from borderlint.kb import _PROVENANCE_BLOCS
    with open("borderlint/data/provenance.json", encoding="utf-8") as fh:
        for pat, entry in json.load(fh)["patterns"].items():
            assert entry["bloc"] in _PROVENANCE_BLOCS, f"{pat}: {entry['bloc']}"
    # covered families leave the drift report
    kd = _drift()
    assert kd.model_coverage_gap(
        [("tiiuae/falcon-180B", "x"), ("bedrock/exaone-3.5", "x"), ("made-up-model-7x", "x")],
        load_kb()) == ["made-up-model-7x"]


def test_kb_curation_2026_07():
    k = load_kb()
    # Bedrock cross-region inference profiles strip their region prefix
    assert k.match_model("us.anthropic.claude-3-5-haiku-20241022-v1:0")[1] == "us"
    assert k.match_model("eu.amazon.nova-2-lite-v1:0")[1] == "us"
    assert k.match_model("apac.anthropic.claude-haiku-4-5-20251001-v1:0")[1] == "us"
    # curated families from freshness issue #39
    assert k.match_model("o1-2024-12-17")[1] == "us"
    assert k.match_model("databricks/databricks-bge-large-en")[1] == "us"
    assert k.match_model("flux-pro")[1] == "eu"
    assert k.match_model("rerank-english-v2.0")[1] == "ca"
    assert k.match_model("sd3")[1] == "uk"
    assert k.match_model("kat-coder")[1] == "cn"
    assert k.match_model("ft:babbage-002")[1] == "us"
    # anchoring still holds: lookalike tool/infra names do not match
    assert k.match_model("sonar-scanner") is None
    assert k.match_model("nova-compute") is None
    assert k.match_model("flux-system") is None
    # issue #39 close-out batch (2026-07-05): new-bloc and vendor-prefixed families
    assert k.match_model("jais-30b-chat")[1] == "ae"
    assert k.match_model("GigaChat-2-Lite")[1] == "ru"
    assert k.match_model("j2-light")[1] == "il"
    assert k.match_model("us.twelvelabs.marengo-embed-2-7-v1:0")[1] == "us"
    assert k.match_model("anthropic-claude-3-opus")[1] == "us"
    # new providers resolve: SageMaker region from host, Snowflake host, Lemonade local
    assert k.match_endpoint("runtime.sagemaker.ap-east-1.amazonaws.com")[2] == "hk"
    assert k.match_endpoint("myacct.snowflakecomputing.com")[2] == "unknown"


def test_versioned_model_identifiers():
    k = load_kb()
    # digit-led @-version pins resolve by their base identifier
    m = k.match_model("claude-3-5-haiku@20241022")
    assert m[:2] == ("claude-3-5-haiku@20241022", "us")   # evidence keeps the suffix
    assert k.match_model("anthropic.claude-haiku-4-5@20251001")[1] == "us"
    assert k.match_model("mistral-large@2407")[1] == "eu"
    assert k.match_model("mistral-large@2411-001")[1] == "eu"  # hyphenated version token
    assert k.match_model("jamba-1.5-large@001")[1] == "il"
    assert k.match_model("codestral@2405")[1] == "eu"
    # the version never changes the bloc
    assert k.match_model("mistral-large")[1] == k.match_model("mistral-large@2407")[1]
    # meta-version pins resolve; other letter-led @ segments stay invisible
    assert k.match_model("codestral@latest")[1] == "eu"
    assert k.match_model("mistral-large@latest")[1] == "eu"
    assert k.match_model("claude-fable-5@default")[1] == "us"
    assert k.match_model("gemini-team@google.com") is None
    assert k.match_model("model@stable") is None
    assert k.match_model("a@b@1") is None
    # drift inherits the fix through the same matcher
    kd = _drift()
    assert kd.model_coverage_gap([("vertex_ai/claude-3-5-haiku@20241022", "vertex_ai")], k) == []


def test_ch_bloc_apertus():
    k = load_kb()
    assert k.match_model("swiss-ai/Apertus-70B-Instruct")[1] == "ch"
    assert k.match_model("apertus-70b-instruct")[1] == "ch"
    # ch accepted in a user KB and policy blocks; rejection error names it
    k2 = load_kb(_kb_file({"provenance": {"acme-alpine": "ch"}}))
    assert k2.match_model("acme-alpine-1")[1] == "ch"
    try:
        load_kb(_kb_file({"provenance": {"x-": "zz"}}))
        assert False, "expected ValueError"
    except ValueError as e:
        assert "ch" in str(e)  # the error's vocabulary list includes the new bloc
    import json, os, tempfile
    from borderlint.policy import load_policy
    p = os.path.join(tempfile.mkdtemp(), "pol.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"classifications": {"customer-pii": ["hk"]},
                   "sovereignty": {"classifications": {"customer-pii": ["ch"]}},
                   "provenance": {"classifications": {"customer-pii": ["ch"]}}}, fh)
    load_policy(p)  # must not raise


def test_provenance_model_deny():
    import json as _json, os, tempfile
    from dataclasses import replace
    from borderlint.policy import load_policy
    from borderlint.report import as_json, text
    k = load_kb()

    def pol(**prov):
        p = os.path.join(tempfile.mkdtemp(), "pol.json")
        with open(p, "w", encoding="utf-8") as fh:
            _json.dump({"classifications": {"customer-pii": ["hk", "us", "cn"]},
                        "provenance": {"classifications": {"customer-pii": ["us", "cn"]},
                                       **prov}}, fh)
        return load_policy(p)

    deny = pol(deny_models=["deepseek"])
    d = Detection("aws_bedrock", "endpoint_reference", "bedrock-runtime.us-east-1.amazonaws.com",
                  "a.py", 1, "us", sovereignty="us", provenance="cn", model="deepseek.r1-v1:0")
    f = evaluate([d], deny, "customer-pii", k)[0]
    assert "model_denied" in f.reasons and f.severity == "fail"  # allowed bloc, denied family
    # redistributor path and version pin do not dodge the deny
    for dodge in ("TheBloke/deepseek-llm-7B-GGUF", "deepseek-v3@2412"):
        f = evaluate([replace(d, model=dodge)], deny, "customer-pii", k)[0]
        assert "model_denied" in f.reasons, dodge
    # standalone model reference is denied too
    sa = Detection("model_reference", "model_reference", "deepseek-r1", "b.py", 2, "unknown",
                   provenance="cn", model="deepseek-r1")
    f = evaluate([sa], deny, "customer-pii", k)[0]
    assert "model_denied" in f.reasons and f.severity == "fail"
    # no bound model -> no deny (the bloc allow-list still governs)
    bare = Detection("openai", "sdk_import", "import openai", "c.py", 1, "us",
                     sovereignty="us", provenance="us")
    assert "model_denied" not in evaluate([bare], deny, "customer-pii", k)[0].reasons
    # a waiver cannot override the deny
    f = evaluate([replace(d, waiver="approved")], deny, "customer-pii", k)[0]
    assert f.severity == "fail"
    # lifting is an explicit fail_on edit, mirroring denied_provider
    lifted = dict(deny, fail_on=["residency", "denied_provider"])
    assert evaluate([d], lifted, "customer-pii", k)[0].severity == "warn"
    # load-time rejection of short entries
    try:
        pol(deny_models=["ds"])
        assert False, "expected ValueError"
    except ValueError as e:
        assert "ds" in str(e)
    # org threading: bundled patterns carry the developer org; user patterns do not
    assert k.match_model("exaone-3.5-7.8b")[2] == "LG AI Research"
    k2 = load_kb(_kb_file({"provenance": {"acme-x": "eu"}}))
    assert k2.match_model("acme-x-1")[2] is None
    # reporting: JSON model_org, text names the org, reason description exists
    fs = evaluate([replace(d, model_org="DeepSeek")], deny, "customer-pii", k)
    j = _json.loads(as_json(fs, k))
    assert j["findings"][0]["model_org"] == "DeepSeek"
    assert "deepseek.r1-v1:0 — DeepSeek" in text(fs, k)
    assert "deny list" in text(fs, k)
    # no org -> renders as before, no empty annotation
    fs2 = evaluate([d], deny, "customer-pii", k)
    assert "[model: deepseek.r1-v1:0]" in text(fs2, k)


def test_evidence_pack(tmp_path, monkeypatch, capsys):
    import json as _json, os
    from dataclasses import replace
    from borderlint.policy import Finding
    from borderlint.report import evidence
    k = load_kb()
    d = Detection("aws_bedrock", "endpoint_reference", "bedrock-runtime.ap-east-1.amazonaws.com",
                  "src/app.py", 3, "hk", sovereignty="us", provenance="cn",
                  model="deepseek.r1-v1:0", model_org="DeepSeek")
    pol = {"home_location": "hk", "classifications": {"customer-pii": ["hk"]}}
    fs = [Finding(d, "fail", ["sovereignty"]), Finding(replace(d, waiver="ok'd"), "waived", ["sovereignty"])]
    env = {"version": "x", "kb_providers": "2026-07-05", "timestamp": "T", "path": "p",
           "commit": None, "policy_digest": "abc", "classification": "customer-pii"}
    doc = evidence(fs, k, pol, env)
    # envelope: unresolved fields say so; resolved ones render
    assert "- Git commit: unavailable" in doc and "- Policy SHA-256: abc" in doc
    # inventory row carries the axes, the model, and the org
    assert "| Hong Kong | United States | Mainland China | deepseek.r1-v1:0 (DeepSeek) | fail |" in doc
    # waiver register + summary
    assert "## Waiver register" in doc and "ok'd" in doc and "1 waived" in doc
    # hk home -> PDPO annex: citations, static fill, org blanks, data date
    assert "Regime annex — PDPO" in doc and "PCPD Guidance" in doc
    assert "data classification (as class of personal data): customer-pii" in doc
    assert "- [ ] purpose of each transfer: ________" in doc
    assert "Expectations data last reviewed" in doc
    # cn / mo / sg homes reach their annexes through regime_of
    for loc, marker in (("cn", "PIPL (Mainland China)"), ("CN-GBA", "PIPL (Mainland China)"),
                        ("mo", "Macao PDPA"), ("sg", "PDPA (Singapore)")):
        assert marker in evidence(fs, k, dict(pol, home_location=loc), env), loc
    # uncovered home location: explicit no-annex statement; home_regime-only: no annex section
    assert "No annex is available" in evidence(fs, k, dict(pol, home_location="uk"), env)
    hr = evidence(fs, k, {"home_regime": "pdpo", "classifications": {"c": ["hk"]}}, env)
    assert "Regime annex" not in hr
    # no policy: inventory framing without verdicts, no annex
    inv = evidence([Finding(d, "ok", [])], k, None, env)
    assert "| fail |" not in inv and "Regime annex" not in inv
    # CLI: artifact exit 0 despite failures; SOURCE_DATE_EPOCH determinism
    from borderlint import cli
    src = tmp_path / "app.py"; src.write_text('import openai\nu = "api.deepseek.com"\n')
    polf = tmp_path / "pol.json"
    polf.write_text(_json.dumps({"classifications": {"customer-pii": ["hk"]}}))
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1751900000")
    args = ["scan", str(tmp_path), "--policy", str(polf),
            "--classification", "customer-pii", "--format", "evidence"]
    assert cli.main(args) == 0
    one = capsys.readouterr().out
    assert cli.main(args) == 0
    two = capsys.readouterr().out
    assert one == two and "fail" in one  # byte-identical, records the failing state


def test_jvm_detection(tmp_path):
    from borderlint.detect import scan
    # Java: plain + static imports, dot-boundary negative, endpoint-literal parity
    java = tmp_path / "App.java"
    java.write_text(
        "import com.openai.client.OpenAIClient;\n"
        "import static com.anthropic.client.AnthropicClient.create;\n"
        "import com.openaiutils.Helper;\n"
        'class App { String url = "https://api.deepseek.com/v1"; }\n')
    ds = scan(str(java), kb)
    by = {d.provider_id: d for d in ds}
    assert by["openai"].kind == "sdk_import" and by["openai"].jurisdiction == "us"
    assert by["anthropic"].kind == "sdk_import"  # `import static` form
    assert by["deepseek"].kind == "endpoint_reference"  # _scan_text parity on .java
    # com.openaiutils must NOT resolve to openai (dot-boundary)
    assert {d.evidence for d in ds if d.provider_id == "openai"} == {"com.openai.client.OpenAIClient"}

    # Kotlin: bare import (no semicolon) + JVM aggregator -> unknown
    kt = tmp_path / "Bot.kt"
    kt.write_text(
        "import com.anthropic.client.AnthropicOkHttpClient\n"
        "import dev.langchain4j.model.chat.ChatLanguageModel\n")
    by2 = {d.provider_id: d for d in scan(str(kt), kb)}
    assert by2["anthropic"].jurisdiction == "us"
    assert by2["langchain4j"].jurisdiction == "unknown"
    assert kb.category("langchain4j") == "aggregator" and kb.category("spring_ai") == "aggregator"

    # OpenAI-compatible call path in Kotlin resolves unknown (api_call parity)
    kx = tmp_path / "Client.kt"
    kx.write_text('val path = "/v1/chat/completions"\n')
    assert any(d.kind == "api_call" and d.jurisdiction == "unknown" for d in scan(str(kx), kb))

    # inline waiver on a flagged Java line
    jw = tmp_path / "W.java"
    jw.write_text('String u = "https://api.deepseek.com"; // borderlint: allow reviewed DR flow\n')
    d = [x for x in scan(str(jw), kb) if x.provider_id == "deepseek"][0]
    assert d.waiver and "reviewed" in d.waiver

    # AWS SDK for Kotlin namespace (differs from the Java SDK v2) resolves to Bedrock
    br_kt = tmp_path / "Br.kt"
    br_kt.write_text("import aws.sdk.kotlin.services.bedrockruntime.BedrockRuntimeClient\n")
    assert any(d.provider_id == "aws_bedrock" for d in scan(str(br_kt), kb))

    # model reference binds provenance in a Java file
    jm = tmp_path / "M.java"
    jm.write_text('String host = "bedrock-runtime.ap-east-1.amazonaws.com";\n'
                  'String model = "anthropic.claude-3-5-haiku-20241022-v1:0";\n')
    md = [x for x in scan(str(jm), kb) if x.provider_id == "aws_bedrock"][0]
    assert md.jurisdiction == "hk" and md.provenance == "us" and md.model


def test_kb_site_generator(tmp_path):
    import importlib.util
    import json as _json
    import os
    import re
    root = os.path.join(os.path.dirname(__file__), "..")
    spec = importlib.util.spec_from_file_location("kb_site", os.path.join(root, "scripts", "kb_site.py"))
    kb_site = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kb_site)
    counts = kb_site.build(str(tmp_path))
    # one page per provider + per developer org + index
    with open(os.path.join(root, "borderlint", "data", "providers.json"), encoding="utf-8") as fh:
        n_providers = len(_json.load(fh)["providers"])
    assert counts["providers"] == n_providers
    assert counts["orgs"] >= 1
    assert len(list((tmp_path / "providers").iterdir())) == counts["providers"]
    assert len(list((tmp_path / "models").iterdir())) == counts["orgs"]  # unique slugs
    assert (tmp_path / "index.html").exists()
    # unknown-jurisdiction provider is honest about region-dependence
    vertex = (tmp_path / "providers" / "vertex_ai.html").read_text()
    assert "Region-dependent" in vertex
    # unique title/meta per page, install one-liner everywhere (spot-check two pages)
    a = (tmp_path / "providers" / "openai.html").read_text()
    b = (tmp_path / "providers" / "deepseek.html").read_text()
    for doc in (a, b):
        assert "pip install borderlint" in doc
    t = lambda doc: re.search(r"<title>(.*?)</title>", doc).group(1)
    m = lambda doc: re.search(r'name="description" content="(.*?)"', doc).group(1)
    assert t(a) != t(b) and m(a) != m(b) and "OpenAI" in t(a)
    # cn-destination page names its regime and links the arrangement
    assert 'href="https://' in b and "PIPL" in b
    # site tooling lives outside the shipped package
    assert not os.path.exists(os.path.join(root, "borderlint", "kb_site.py"))


def test_html_report(tmp_path, capsys):
    import json as _json
    from dataclasses import replace
    from borderlint.policy import Finding
    from borderlint.report import html as html_report
    k = load_kb()
    d = Detection("aws_bedrock", "endpoint_reference", "bedrock-runtime.ap-east-1.amazonaws.com",
                  "src/app.py", 3, "hk", sovereignty="us", provenance="cn",
                  model="deepseek.r1-v1:0", model_org="DeepSeek")
    pol = {"home_location": "hk", "classifications": {"customer-pii": ["hk"]}}
    fs = [Finding(d, "fail", ["sovereignty"]),
          Finding(replace(d, waiver="ok'd"), "waived", ["sovereignty"]),
          Finding(replace(d, jurisdiction="CN-GBA"), "fail", ["residency"])]
    env = {"version": "x", "kb_providers": "2026-07-05", "timestamp": "T", "path": "p",
           "commit": None, "policy_digest": "abc", "classification": "customer-pii"}
    doc = html_report(fs, k, pol, env)
    # header: resolved fields render, unresolved say so; policy rows present
    assert "<th>Git commit</th><td>unavailable</td>" in doc
    assert "<th>Policy SHA-256</th><td>abc</td>" in doc and "<td>customer-pii</td>" in doc
    # grouped by jurisdiction, each row carrying all three axes
    assert "<h2>Hong Kong <code>hk</code></h2>" in doc and "<h2>Mainland GBA <code>CN-GBA</code></h2>" in doc
    assert "<td>Hong Kong</td><td>United States</td><td>Mainland China</td>" in doc
    # severity chips + waiver register with escaped justification
    assert 'class="chip fail"' in doc and "<h2>Waiver register</h2>" in doc and "ok&#x27;d" in doc
    # regime tags + arrangement reference as a hyperlink (hk home, CN-GBA destination -> GBA SC)
    assert "Regimes implicated:" in doc and "PDPO" in doc
    assert '<a href="' in doc and "GBA Standard Contract" in doc
    assert "Summary: 2 fail, 0 warn, 1 waived, 0 ok" in doc
    # self-contained: nothing fetched when opened (<a href> reference links are fine)
    for marker in ("<script", "<link ", "<img ", "@import", "url("):
        assert marker not in doc, marker
    # scanned content cannot inject markup
    bad = Detection("openai", "sdk_import", "<script>alert(1)</script>", "a.py", 1, "us")
    doc2 = html_report([Finding(bad, "ok", [])], k, None, env)
    assert "<script" not in doc2 and "&lt;script&gt;" in doc2
    # inventory mode: no verdicts, no severity column, no policy header rows
    inv = html_report([Finding(d, "ok", [])], k, None, env)
    assert 'class="chip' not in inv and "<th>Severity</th>" not in inv and "Policy SHA-256" not in inv
    # CLI: html is an export -> exits 0 despite a violation
    from borderlint import cli
    src = tmp_path / "app.py"
    src.write_text("import openai\n")
    polf = tmp_path / "pol.json"
    polf.write_text(_json.dumps({"classifications": {"customer-pii": ["hk"]}}))
    assert cli.main(["scan", str(tmp_path), "-p", str(polf), "-c", "customer-pii", "-f", "html"]) == 0
    outdoc = capsys.readouterr().out
    assert "<!doctype html>" in outdoc and 'class="chip fail"' in outdoc


def test_config_endpoint_ignores_path_values():
    # tsconfig-style baseUrl values are paths, not endpoints (TellMeWhy false positive)
    assert cfg('{"compilerOptions": {"baseUrl": "."}}', "tsconfig.json") == []
    assert cfg('base_url: ./models\n') == []
    assert cfg('base_url: https://llm-cn.acme.cn/v1\n')[0].provider_id != ""  # real hosts still detected
    assert cfg("base_url: http://localhost:8080\n")[0].jurisdiction == "local"  # loopback unaffected


def test_edge_tts_and_local_whisper():
    # edge-tts: cross-border speech flow to Microsoft; nested import is caught by the AST walk
    ds = _scan_file('def speak():\n    import edge_tts\n')
    d = [x for x in ds if x.provider_id == "edge_tts"][0]
    assert (d.jurisdiction, d.sovereignty, d.provenance) == ("unknown", "us", "us")
    # faster-whisper: local runtime, OpenAI-developed weights
    ds = _scan_file("from faster_whisper import WhisperModel\n")
    d = [x for x in ds if x.provider_id == "whisper_local"][0]
    assert (d.jurisdiction, d.sovereignty, d.provenance) == ("local", "local", "us")


def test_env_style_endpoint_keys():
    # prefixed env keys resolve packaged endpoints (TellMeWhy's .env case)
    assert cfg("TELLMEWHY_LLM_SERVER_URL=http://localhost:8080\n", ".env")[0].jurisdiction == "local"
    hits = cfg("OPENAI_BASE_URL=https://api.openai.com/v1\n", ".env")
    assert any(d.provider_id == "openai" for d in hits)
    assert cfg("llm_server_url: http://llm-cn.acme.cn/v1\n")[0].kind == "config_endpoint"
    # compose list form: scheme-bearing single-label service host -> custom endpoint, unknown
    d = cfg("services:\n  app:\n    environment:\n      - OLLAMA_BASE_URL=http://ollama:11434\n", "docker-compose.yml")
    assert d and d[0].jurisdiction == "unknown"
    # negatives: no AI-stem segment, AI substring, curated-list absences, env getters, path values
    assert cfg("DATABASE_URL=https://db.example.com\n", ".env") == []
    assert cfg("HOMEPAGE_URL=https://example.com\n", ".env") == []
    assert cfg("EMAIL_URL=https://mail.example.com\n", ".env") == []
    assert cfg("MODEL_URL=https://cdn.example.com/x.glb\n", ".env") == []
    assert cfg('LLM_SERVER_URL = os.environ.get("X_LLM_URL", "http://localhost:8080")\n', "settings.py") == []
    assert cfg('{"compilerOptions": {"baseUrl": "."}}', "tsconfig.json") == []


def test_transformers_local_runtime():
    # transformers/sentence-transformers are local runtimes; provenance binds from model refs
    ds = _scan_file('from transformers import AutoModelForCausalLM\nm = "microsoft/Florence-2-large"\n')
    d = [x for x in ds if x.provider_id == "hf_transformers_local"][0]
    assert (d.jurisdiction, d.sovereignty, d.provenance) == ("local", "local", "us")
    assert d.model == "microsoft/Florence-2-large"
    # multi-model runtime: no first-party default — unbound flows stay unknown provenance
    ds = _scan_file("from sentence_transformers import SentenceTransformer\n")
    d = [x for x in ds if x.provider_id == "hf_transformers_local"][0]
    assert (d.jurisdiction, d.sovereignty, d.provenance) == ("local", "local", "unknown")
    # memorybox families resolve
    k = load_kb()
    assert k.match_model("vikhyatk/moondream2")[1] == "us"
    assert k.match_model("moondream2")[1] == "us"
    assert k.match_model("florence-2-base")[1] == "us"
    assert k.match_model("clip-ViT-B-32")[1] == "us"


def test_model_file_basenames():
    k = load_kb()
    assert k.match_model("models/clip-vit-b-32.onnx")[1] == "us"
    assert k.match_model("weights/qwen2.5-vl-3b.safetensors")[1] == "cn"
    assert k.match_model("models/qwen2.5-7b-instruct-q4_k_m.gguf")[1] == "cn"  # unchanged
    assert k.match_model("dir/qwen2.5.zip") is None  # unlisted extension: whole-path anchoring


def test_env_directories_excluded_by_marker(tmp_path):
    import os
    from borderlint.detect import scan
    # nonstandard-named venv with a PEP 405 marker: excluded as a subtree
    venv = tmp_path / ".venv-cuda"
    (venv / "lib" / "site-packages").mkdir(parents=True)
    (venv / "pyvenv.cfg").write_text("home = /usr/bin\n")
    (venv / "lib" / "site-packages" / "hub.py").write_text("import openai\n")
    # conda env: excluded by its conda-meta dir
    conda = tmp_path / "env-gpu"
    (conda / "conda-meta").mkdir(parents=True)
    (conda / "runtime.py").write_text("import anthropic\n")
    # bare site-packages with no marker: excluded by name
    sp = tmp_path / "embedded" / "site-packages"
    sp.mkdir(parents=True)
    (sp / "vendored.py").write_text("import cohere\n")
    # application code beside them: scanned as usual
    (tmp_path / "app.py").write_text("import openai\n")
    ds = scan(tmp_path, kb)
    files = {d.file for d in ds}
    assert files == {str(tmp_path / "app.py")}
