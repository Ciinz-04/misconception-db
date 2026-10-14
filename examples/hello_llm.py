"""驗收 2：能呼叫 LLM API；有設定 Langfuse 的話，這次呼叫會出現在 Langfuse 後台。"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

for key in ("ANTHROPIC_API_KEY", "ANTHROPIC_MODEL"):
    if not os.getenv(key):
        raise SystemExit(f"請先在 .env 填入 {key}")

# Langfuse 是選用的：有填金鑰就記錄，沒填也能跑
use_langfuse = bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
observe = lambda *a, **k: (lambda f: f)
if use_langfuse:
    try:
        from langfuse import observe  # Langfuse v3
    except ImportError:
        from langfuse.decorators import observe  # Langfuse v2

client = anthropic.Anthropic()


@observe()
def ask(prompt: str) -> str:
    msg = client.messages.create(
        model=os.environ["ANTHROPIC_MODEL"],
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


answer = ask("請用一句話說明：國中生把 -(x-2) 寫成 -x-2，是哪一種迷思概念？")
print(answer)

if use_langfuse:
    try:
        from langfuse import get_client
        get_client().flush()
    except ImportError:
        from langfuse.decorators import langfuse_context
        langfuse_context.flush()
    print("\n已送到 Langfuse，請到後台的 Traces 頁面查看。")
