"""Smallest checks that fail if the core logic breaks (one per key spec scenario)."""

from borderlint.detect import Detection, _scan_config_endpoints, _scan_js, _scan_py, _scan_text
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
    return _scan_py("x.py", src, kb)


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
    return _scan_js("x.ts", src, kb)


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
    return _scan_config_endpoints(path, src, kb)


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
