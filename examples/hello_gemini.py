"""P0.4 驗收：呼叫 Gemini，並依 Langfuse 最佳實務記錄 trace。

trace 結構：
  explain-misconception（span，根節點：input = 學生寫的行，output = 模型的說明）
    └─ Gemini 呼叫（generation，由 Google GenAI 整合自動產生：模型名稱、token 用量、成本）
"""
import os

from dotenv import load_dotenv

load_dotenv()  # 一定要在 import langfuse 之前載入 .env

# 新版 SDK 讀 LANGFUSE_BASE_URL；.env 只有舊的 LANGFUSE_HOST 時自動沿用
if os.getenv("LANGFUSE_HOST") and not os.getenv("LANGFUSE_BASE_URL"):
    os.environ["LANGFUSE_BASE_URL"] = os.environ["LANGFUSE_HOST"]
# 測試用的 trace 標成 development，之後不會混進正式資料
os.environ.setdefault("LANGFUSE_TRACING_ENVIRONMENT", "development")

from google import genai  # noqa: E402
from langfuse import get_client, propagate_attributes  # noqa: E402
from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor  # noqa: E402

for key in ("GEMINI_API_KEY", "GEMINI_MODEL", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_BASE_URL"):
    if not os.getenv(key):
        raise SystemExit(f"請先在 .env 填入 {key}")

langfuse = get_client()
if not langfuse.auth_check():
    raise SystemExit("Langfuse 驗證失敗：請檢查金鑰與 LANGFUSE_BASE_URL（日本地區是 https://jp.cloud.langfuse.com）")

# 在任何 Gemini 呼叫之前啟用整合：每次呼叫會自動記成 generation，含模型名稱與 token 用量
GoogleGenAIInstrumentor().instrument()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL"]
PROMPT_VERSION = "explain-mc-v1"  # 改提示詞時一併改版本號，方便在 Langfuse 比較


def explain_misconception(prev_line: str, student_line: str, mc_id: str) -> str:
    """請 LLM 用一句話說明學生這一步反映了什麼迷思概念。"""
    prompt = (
        f"國中生把 {prev_line} 寫成 {student_line}。"
        "請用一句話說明這反映了哪一種迷思概念。"
    )
    with langfuse.start_as_current_observation(as_type="span", name="explain-misconception") as root:
        # 根節點的 input/output 就是整個 trace 在列表上顯示的內容，只放審閱時需要的資訊
        root.update(input={"prev_line": prev_line, "student_line": student_line, "mc_id": mc_id})
        with propagate_attributes(
            trace_name="explain-misconception",
            tags=["p0-smoke-test"],
            metadata={"mc_id": mc_id, "prompt_version": PROMPT_VERSION, "app_version": "0.1.0"},
        ):
            response = client.models.generate_content(model=MODEL, contents=prompt)
        root.update(output=response.text)
    return response.text


if __name__ == "__main__":
    print(explain_misconception("-(x-2)", "-x-2", "MC-ALG-003"))
    langfuse.flush()  # 短程式結束前一定要 flush，否則 trace 可能還沒送出
    print("\n已送到 Langfuse：Tracing → Traces，找名稱 explain-misconception 的紀錄。")
