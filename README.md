# misconception-db

K7–K9 數學迷思概念資料庫（500 個知識點）。

## 目錄結構

| 路徑 | 內容 |
|---|---|
| `schemas/` | JSON Schema：misconception、instance、diagnostic_item、qmatrix、checks |
| `sources/literature/` | 文獻摘要與 BibTeX |
| `sources/cap_exam/` | 會考誘答選項紀錄（CSV） |
| `sources/unit_notes/` | 各單元來源摘要 |
| `sources/inventory/` | 思考鏈家教系統的知識點盤點表（含版本） |
| `catalog/misconceptions.json` | 全域迷思概念目錄 |
| `instances/{kp_id}.json` | 知識點實例 |
| `items/{kp_id}.json` | 選擇式診斷題 |
| `qmatrix/{kp_id}.csv` | 題目 × 迷思概念矩陣 |
| `buggy_rules/` | 可執行錯誤規則（以 mc_id 分檔，含 tests/） |
| `review/` | 各單元審定表與重審紀錄 |
| `tools/` | draft.py、review_sheet.py、itemgen.py、qmatrix.py、checks.py、dedup.py |
| `prompts/` | 提示詞（檔名含版本號） |
| `checks/` | 檢查結果與 summary.csv |
| `examples/` | 環境測試範例 |

## 環境設定

```bash
uv sync                 # 安裝 Python 3.12 與所有套件
cp .env.example .env    # 再把金鑰填進 .env
uv run examples/hello_sympy.py
uv run examples/hello_llm.py
```
