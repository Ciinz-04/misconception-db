# 資料規格的 JSON Schema（P2.2）

依 `docs/data_spec.md` 寫成，放到 repo 的 `schemas/`。

| 檔案 | 內容 |
|---|---|
| schemas/misconception.schema.json | 全域迷思 |
| schemas/mc_instance.schema.json | 知識點實例 |
| schemas/item_template.schema.json | 題目範本 |
| examples/*.example.json | 三種各 1 筆範例 |
| tools/validate.py | 驗證程式 |

自動檢查的規則：
- mc_id 格式為 MC-領域-三位數，領域只能是 8 種代碼
- name 不超過 15 字
- T2 必填 old_rule 與 trigger，origin 要含 overgeneralization
- evidence_tier 為 verified 時，至少要有一筆 E1 或 E2
- 知識點實例為 T1、T2、T6、T8 時，必填 trigger_conditions、buggy_rule、item_template、diagnostic_items
- 題目範本固定 4 個選項，每個選項標出產生它的迷思（正答填 null）

執行：
```bash
uv pip install jsonschema
python tools/validate.py
```
