# 會考誘答的多模型分析

- items.json：111–115 年會考數學 125 題選擇題（擷取文字、正答、各選項選答百分比、學習內容代碼）。擷取文字的分數、次方會亂碼，所以分析時要附上試題本 PDF。題目文字來自心測中心，repo 公開時不要上傳此檔。
- catalog.json：目前的迷思目錄（118 條）。
- prompt.md：所有模型共用的提示詞。
- run_llm.py：用 Gemini API 跑全部題目，結果存在 results/gemini.jsonl。
- compare.py：比較各模型的判斷，輸出 compare.xlsx（逐選項比較與一致率）。

流程：
1. Gemini：python run_llm.py --pdf-dir 會考試題本（資料夾放 111P_Math.pdf～115P_Math.pdf，模型會直接看 PDF 裡的題目與圖）
2. Claude：用同一份 prompt.md 分析，結果存成 results/claude.jsonl
3. （選用）ChatGPT 網頁版：挑部分題目貼 prompt，結果整理成 results/gpt.jsonl
4. python compare.py results/gemini.jsonl results/claude.jsonl
5. 研究生只需人工檢查「不一致」的選項
