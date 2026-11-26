"""比較不同模型對誘答選項的判斷，輸出 compare.xlsx。

用法：python compare.py results/gemini.jsonl results/claude.jsonl [results/gpt.jsonl ...]
"""
import json, sys
from pathlib import Path
from openpyxl import Workbook

files = sys.argv[1:]
items = {i["item_id"]: i for i in json.load(open(Path(__file__).parent / "items.json", encoding="utf-8"))}
res = {}
names = []
for f in files:
    name = Path(f).stem; names.append(name)
    for line in open(f, encoding="utf-8"):
        r = json.loads(line)
        for d in r.get("distractors", []):
            res.setdefault((r["item_id"], d["option"]), {})[name] = d

wb = Workbook(); ws = wb.active; ws.title = "比較"
head = ["題目", "選項", "全體%", "待加強%"]
for n in names:
    head += [f"{n} 是迷思", f"{n} 編號", f"{n} 類型", f"{n} 推測算法"]
head += ["是否迷思一致", "編號一致", "類型一致"]
ws.append(head)
agree = {"m": 0, "id": 0, "t": 0, "n": 0}
for (iid, opt), v in sorted(res.items()):
    it = items.get(iid, {})
    row = [iid, opt, it.get("pct_all", {}).get(opt), it.get("pct_low", {}).get(opt)]
    ms, ids, ts = [], [], []
    for n in names:
        d = v.get(n, {})
        m = d.get("is_misconception"); i = d.get("mc_id") or d.get("new_belief") or ""; t = d.get("type", "")
        ms.append(m); ids.append(i); ts.append(t)
        row += ["是" if m else ("否" if m is False else ""), i, t, d.get("student_work", "")]
    full = len(v) == len(names)
    a1 = full and len(set(ms)) == 1; a2 = full and len(set(ids)) == 1; a3 = full and len(set(ts)) == 1
    row += ["是" if a1 else "否", "是" if a2 else "否", "是" if a3 else "否"]
    ws.append(row)
    if full:
        agree["n"] += 1; agree["m"] += a1; agree["id"] += a2; agree["t"] += a3
ws2 = wb.create_sheet("一致率")
ws2.append(["項目", "一致數", "總數", "一致率"])
for k, lab in [("m", "是否迷思"), ("id", "迷思編號"), ("t", "性質類型")]:
    ws2.append([lab, agree[k], agree["n"], round(agree[k] / agree["n"], 3) if agree["n"] else None])
wb.save("compare.xlsx")
print(agree)
