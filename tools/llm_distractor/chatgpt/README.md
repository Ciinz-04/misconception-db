# 用 ChatGPT 網頁版跑會考誘答分析

每個年度開一個新對話（共 5 個），避免前面的回答影響後面。

1. 開新對話，上傳該年度試題本（例如 會考試題本/111P_Math.pdf）。
2. 打開 111_prompt.txt，全部複製貼上，送出。
3. ChatGPT 會輸出 25 行 JSON。全部複製，貼到 results/gpt.jsonl 的最後面（5 個年度都貼在同一個檔案）。
4. 若輸出被截斷，回覆「繼續，從還沒輸出的題目開始」，再把後續的行貼上。
5. 記下使用的模型名稱（對話畫面上方），報告時要寫。

5 個年度都貼完後執行：
uv run --with openpyxl python compare.py results/gemini.jsonl results/claude.jsonl results/gpt.jsonl
