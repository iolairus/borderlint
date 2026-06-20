"""Smallest checks that fail if the core logic breaks (one per key spec scenario)."""

from borderlint.detect import _scan_js, _scan_py, _scan_text
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
