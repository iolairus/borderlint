"""Smallest checks that fail if the core logic breaks (one per key spec scenario)."""

from borderlint.detect import _scan_py
from borderlint.kb import load_kb
from borderlint.policy import evaluate

kb = load_kb()


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
    k = load_kb()
    k.by_id["x"] = {"id": "x", "name": "X", "jurisdiction": "CN-GBA"}
    k._eps.insert(0, ("x.local", "x", "CN-GBA"))
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
