"""用 Gemini 分析會考選擇題的誘答選項。

用法：
  uv pip install google-genai python-dotenv
  python run_llm.py --model gemini-2.5-flash --pdf-dir 會考試題本 --out results/gemini.jsonl
金鑰放在 .env：GEMINI_API_KEY=...（不要上傳 .env）
--pdf-dir 資料夾裡放各年度試題本，檔名為 111P_Math.pdf、112P_Math.pdf…（不要上傳）
已完成的題目會自動跳過，中斷後重跑即可接續。
"""
import argparse, json, os, time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()
ap = argparse.ArgumentParser()
ap.add_argument("--model", default=os.getenv("GEMINI_MODEL") or "gemini-2.5-flash")
ap.add_argument("--out", default="results/gemini.jsonl")
ap.add_argument("--items", default="items.json")
ap.add_argument("--catalog", default="catalog.json")
ap.add_argument("--only", default="", help="只跑部分題目，例如 114-02,115-10")
ap.add_argument("--pdf-dir", default="", help="試題本 PDF 資料夾；沒給就只用文字")
a = ap.parse_args()

here = Path(__file__).parent
items = json.load(open(here / a.items, encoding="utf-8"))
catalog = json.load(open(here / a.catalog, encoding="utf-8"))
template = open(here / "prompt.md", encoding="utf-8").read()
cat_text = "\n".join(f'{c["id"]}｜{c["type"]}｜{c["belief"]}' for c in catalog)

out = here / a.out
out.parent.mkdir(parents=True, exist_ok=True)
done = set()
if out.exists():
    for line in open(out, encoding="utf-8"):
        try: done.add(json.loads(line)["item_id"])
        except Exception: pass
only = set(x for x in a.only.split(",") if x)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
pdfs = {}
def pdf_for(year):
    if not a.pdf_dir: return None
    if year not in pdfs:
        path = Path(a.pdf_dir) / f"{year}P_Math.pdf"
        pdfs[year] = client.files.upload(file=str(path)) if path.exists() else None
    return pdfs[year]
for it in items:
    if it["item_id"] in done or (only and it["item_id"] not in only):
        continue
    item_text = json.dumps({k: it[k] for k in ["item_id", "content_code", "goal", "stem_text", "answer", "pct_all", "pct_low"]}, ensure_ascii=False, indent=1)
    prompt = template.replace("{ITEM}", item_text).replace("{CATALOG}", cat_text).replace("{Q}", str(it["q"]))
    f = pdf_for(it["year"])
    contents = [f, prompt] if f else prompt
    for attempt in range(3):
        try:
            r = client.models.generate_content(model=a.model, contents=contents,
                                               config={"response_mime_type": "application/json", "temperature": 0})
            res = json.loads(r.text)
            res["item_id"] = it["item_id"]; res["model"] = a.model
            with open(out, "a", encoding="utf-8") as f:
                f.write(json.dumps(res, ensure_ascii=False) + "\n")
            print("ok", it["item_id"])
            break
        except Exception as e:
            print("retry", it["item_id"], e); time.sleep(10)
    time.sleep(2)
