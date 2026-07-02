"""Smallest checks that fail if the core logic breaks (one per key spec scenario)."""

from borderlint.detect import Detection, _scan_config_endpoints, _scan_js, _scan_py, _scan_text, _resolve_sovereignty
from borderlint.kb import load_kb
from borderlint.policy import evaluate

kb = load_kb()


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
