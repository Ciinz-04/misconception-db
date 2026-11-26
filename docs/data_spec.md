# 資料規格（初稿 v0.1）

- 依據：`classification_rules.md`
- 狀態：草案
- 更新日期：2026/11/18

## 1. 資料的兩層結構

| 層級 | 內容 | 數量（目標） | 本期何時建立 |
|---|---|---|---|
| 第一層：全域迷思 `misconception` | 學生心中的錯誤想法本身，跨知識點共用 | 200–250 條 | W1–W12（現在） |
| 第二層：知識點實例 `mc_instance` | 這個想法在某個知識點、某個步驟上如何出現與偵測 | 2,000–2,500 個 | W13 起（需要知識點盤點表） |

一條全域迷思平均對應 8–10 個知識點實例。

另外有兩個附屬資料：

- `buggy_rule`：錯誤規則程式（T1、T2、T6、T8），掛在全域迷思上。
- `diagnostic_item`、`item_template`：診斷題與題目範本，掛在知識點實例上。

## 2. 第一層：全域迷思欄位

| 欄位 | 型別 | 必填 | 說明 | 例子 |
|---|---|---|---|---|
| `mc_id` | 字串 | 是 | `MC-領域-三位數序號`，領域代碼見第 4 節 | `MC-ALG-003` |
| `name` | 字串 | 是 | 簡短名稱，15 字以內 | 負號只屬於第一項 |
| `belief` | 字串 | 是 | 學生口吻的一句話錯誤想法 | 括號前是負號，只要改第一項的符號。 |
| `correct_conception` | 字串 | 是 | 對應的正確概念，3 句以內 | 括號前是負號時，去括號後括號內每一項都要變號。 |
| `nature_type` | `T1`–`T8` | 是 | 主要性質類型，依分類規則第 3 節判斷 | `T1` |
| `secondary_type` | `T1`–`T8` 或 null | 否 | 備註類型（分類規則第 5 節） | null |
| `old_rule` | 字串或 null | T2 必填 | 在舊範圍成立的規則 | 正整數乘法會讓數變大 |
| `trigger` | 字串或 null | T2 必填 | 舊規則失效的新範圍；其他類型可填 | 乘數介於 0 和 1 之間 |
| `origin` | 列舉，可多選 | 是 | 可能成因：`overgeneralization`（舊經驗類化）、`representation`（表徵誤讀）、`instruction`（教學用語、口訣）、`intuition`（直覺）、`visual`（圖形外觀）、`unknown`（來源沒有說明）。T2 一律含 `overgeneralization`；其他類型只在來源有寫成因時填，否則填 `unknown` | `["instruction"]` |
| `evidence` | 陣列 | 是，至少 1 筆 | 來源清單，格式見第 2.1 節 | |
| `evidence_tier` | `verified`／`unverified` | 是 | 有 E1 或 E2 → verified；只有 E4 → unverified | `verified` |
| `units` | 陣列 | 是 | 可能出現的單元代碼；盤點表到位前先填單元名稱 | `["正負數（整數運算）", "一元一次方程式"]` |
| `related_mc` | 陣列 | 否 | 相關的其他迷思 `mc_id` | `["MC-ALG-002"]` |
| `status` | 列舉 | 是 | 審定狀態：`draft`（已草擬，研究生還沒逐條檢查）／`reviewed`（研究生已審定） | `draft` |

### 2.1 `evidence` 的格式

每筆來源一個物件：

| 欄位 | 必填 | 說明 | 例子 |
|---|---|---|---|
| `level` | 是 | `E1` 文獻／`E2` 會考、TIMSS、PISA／`E4` 推測 | `E1` |
| `source` | 是 | 作者（年）或測驗名稱與年份 | 張郁苓（2015） |
| `source_ref` | 是 | P1.2 論文編號或會考題號 | `TH25`；`114 會考 第 22 題` |
| `page` | 否 | 頁碼 | `p.70` |
| `grade` | 否 | 研究對象年級 | `G8` |
| `rate` | 否 | 錯誤率或選擇比例（原文數字） | `57.5%` |
| `example` | 否 | 原文中的學生錯誤例子 | `(2a−16)−(18+9a)=2a−16−18+9a` |

## 3. 第二層：知識點實例欄位（W13 起使用，先列出）

| 欄位 | 必填 | 說明 |
|---|---|---|
| `instance_id` | 是 | `kp_id#mc_id`，例：`A-7-03-03#MC-ALG-003` |
| `kp_id` | 是 | 盤點表的知識點 ID |
| `mc_id` | 是 | 對應的全域迷思 |
| `anchor.type` | 是 | `step`（解題步驟）／`concept`（概念層）／`formulation`（列式層） |
| `anchor.step_desc` | 是 | 錯點步驟的文字描述，例如「去括號」「移項」 |
| `anchor.step_id` | 否 | 思考鏈步驟 ID；思考鏈還沒做好時可空 |
| `error_patterns` | 是 | 錯誤樣態，每個附 2–3 個具體錯誤作答例子 |
| `trigger_conditions` | T1、T2、T6、T8 必填 | 迷思會暴露的題目條件；不在此條件下，迷思的答案與正確答案相同 |
| `buggy_rule` | T1、T2、T6、T8 必填 | 錯誤規則名稱與參數 |
| `item_template` | T1、T2、T6、T8 必填 | 題幹範本、參數範圍（須在 `trigger_conditions` 內）、答案公式 |
| `diagnostic_items` | T1、T2、T6、T8 必填 | 選擇題 ID；T3、T4、T5、T7 本期為空 |
| `remediation` | 是 | 正確概念說明（3 句以內），以及回流到的步驟或先備知識點 |
| `evidence_tier` | 是 | 繼承全域層級，可個別升級（例如此知識點有會考誘答證據） |
| `checks` | 自動產生 | 品質檢查結果（可區辨性、模擬學生一致性） |
| `provenance` | 自動產生 | LLM 草擬版本、審定批次與分鐘數、修改類型、是否被抽樣重審 |

## 4. 領域代碼

| 代碼 | 領域 | 對應的單元 |
|---|---|---|
| `NUM` | 數與量 | 正負數、分數、因數與倍數、指數與科學記號、平方根 |
| `ALG` | 代數 | 一元一次方程式、二元一次聯立方程式、乘法公式與多項式、因式分解、一元二次方程式 |
| `FUN` | 函數 | 線型函數、二次函數 |
| `COO` | 坐標 | 直角坐標、方程式的圖形 |
| `GEO` | 幾何 | 三角形、四邊形、相似形、圓、三心、幾何證明 |
| `STA` | 統計 | 統計圖表、統計量 |
| `PRB` | 機率 | 機率 |
| `TRN` | 情境轉譯 | 跨單元的 T8 迷思 |

一條迷思出現在多個領域時，以最早出現的單元決定領域，其他單元填在 `units`。T8 一律用 `TRN`。

## 5. 範例

```json
{
  "mc_id": "MC-ALG-003",
  "name": "負號只屬於第一項",
  "belief": "括號前是負號，只要改第一項的符號。",
  "correct_conception": "括號前是負號時，去括號後括號內每一項都要變號。",
  "nature_type": "T1",
  "secondary_type": null,
  "old_rule": null,
  "trigger": "括號內有兩項以上",
  "origin": ["instruction"],
  "evidence": [
    {"level": "E1", "source": "楊淑如（2016）", "source_ref": "TH01", "page": "p.45", "grade": "G7"},
    {"level": "E1", "source": "（TH02 作者待補）", "source_ref": "TH02", "page": "表 4-19", "grade": "G7", "rate": "57.5%"},
    {"level": "E1", "source": "張郁苓（2015）", "source_ref": "TH25", "page": "p.70", "grade": "G8"}
  ],
  "evidence_tier": "verified",
  "units": ["正負數（整數運算）", "一元一次方程式", "乘法公式與多項式", "因式分解"],
  "related_mc": [],
  "status": "draft"
}
```

T2 的範例（必填 `old_rule` 與 `trigger`）：

```json
{
  "mc_id": "MC-NUM-001",
  "name": "乘法一定變大",
  "belief": "乘一個數，結果一定比原來的數大。",
  "correct_conception": "乘以大於 1 的數才變大；乘以 0 到 1 之間的數會變小；乘以負數會改變正負號。",
  "nature_type": "T2",
  "secondary_type": null,
  "old_rule": "正整數乘法會讓數變大",
  "trigger": "乘數介於 0 和 1 之間",
  "origin": ["overgeneralization"],
  "evidence": [
    {"level": "E1", "source": "Fischbein et al. (1985)", "source_ref": "seed-03"},
    {"level": "E1", "source": "（P1.2 對應論文）", "source_ref": "TH03"}
  ],
  "evidence_tier": "verified",
  "units": ["分數", "正負數（整數運算）"],
  "related_mc": [],
  "status": "draft"
}
```

## 6. 待確認
1. `secondary_type`、`old_rule`、`status` 是計劃書 2.2 節之外新增的欄位。
2. `origin` 是計劃書 2.2 節的欄位，但多數來源沒有說明學生的想法成因；本規格允許填 `unknown`，請老師確認是否可以。

