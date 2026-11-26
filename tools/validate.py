"""檢查 JSON 檔是否符合 schemas/ 裡的規格（P2.4 Q-1 檢查的雛形）。

用法：python tools/validate.py            # 檢查 examples/ 的三個範例
      python tools/validate.py 檔案.json 規格名稱   # 例：python tools/validate.py catalog/MC-ALG-003.json misconception
"""
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

root = Path(__file__).resolve().parent.parent
def check(path, kind):
    schema = json.load(open(root / "schemas" / f"{kind}.schema.json", encoding="utf-8"))
    data = json.load(open(path, encoding="utf-8"))
    errs = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    for e in errs:
        print(f"  ✗ {path}：{'/'.join(map(str, e.path)) or '(根)'}：{e.message}")
    print(("✓ " if not errs else "✗ ") + f"{path}（{kind}）")
    return not errs

if len(sys.argv) == 3:
    ok = check(sys.argv[1], sys.argv[2])
else:
    ok = all(check(root / "examples" / f"{k}.example.json", k) for k in ["misconception", "mc_instance", "item_template"])
sys.exit(0 if ok else 1)
