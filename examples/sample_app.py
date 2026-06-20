import openai
from anthropic import Anthropic

# Mainland China endpoint — a violation for customer-pii (allow-list: hk, CN-GBA, sg)
DEEPSEEK = "https://api.deepseek.com/v1"

# Alibaba international endpoint resolves to Singapore — allowed for customer-pii
DASHSCOPE = "dashscope-intl.aliyuncs.com"
