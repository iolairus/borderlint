import OpenAI from 'openai';                       // Western escalation tier (US)

// Region-pinned internal endpoint (Shenzhen, CN-GBA) for customer-PII inference.
const GBA_LLM = process.env.GBA_LLM_URL ?? 'https://llm-sz.acme.cn';

export async function infer(prompt: string): Promise<string> {
  const res = await fetch(`${GBA_LLM}/v1/chat/completions`, {
    method: 'POST',
    body: JSON.stringify({ model: 'qwen3', messages: [{ role: 'user', content: prompt }] }),
  });
  return (await res.json()).choices[0].message.content;
}

export const escalate = new OpenAI();
