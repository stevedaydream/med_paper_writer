# Auto Paper Writer

將 NotebookLM 產出的中文草稿，透過 LLM 翻譯改寫為學術英文，並整合 Zotero 文獻庫與 Pandoc，一鍵輸出符合 JFMA / Vancouver 格式且帶有正確 Citation 的 Word 文件。

---

## 目錄結構

```
med_paper_writer/
├── data/
│   ├── draft.txt               # NotebookLM 產出的中文草稿（含 [1]、[2] 標記）
│   ├── cite_map.json           # 引用標籤對應表，例：{"[1]": "[@citekey]"}
│   └── epidermal_cyst.bib      # Zotero Better BibTeX 匯出的文獻庫
├── styles/
│   ├── journal-of-the-formosan-medical-association.csl  # JFMA 格式（預設）
│   ├── nlm-citation-sequence-superscript.csl            # Vancouver 上標格式（備用）
│   └── reference.docx          # （選用）Word 樣式模板，存在時 Pandoc 自動套用
├── src/
│   ├── main.py                 # Pipeline 核心邏輯 + CLI 入口
│   └── gui.py                  # tkinter GUI 入口
├── output/                     # 自動建立
│   ├── processed_draft.md      # LLM 改寫後的 Markdown（含 citekey）
│   └── Final_Paper.docx        # Pandoc 渲染的最終 Word 文件
├── .env                        # API 金鑰（不納入版控）
├── .env.example                # 金鑰格式範本
└── requirements.txt
```

---

## 執行流程

```
draft.txt + cite_map.json
        │
        ▼
[1] 讀取草稿與引用表
        │
        ▼
[2] 將 [1][2] 替換為 [@citekey]
        │
        ▼
[3] LLM 翻譯改寫（保留 citekey）
        │
        ▼
[4] 儲存 processed_draft.md（含 YAML front matter）
        │
        ▼
[5] Pandoc --citeproc → Final_Paper.docx
         （結合 .bib 與 .csl 渲染 Reference List）
```

---

## 環境設定

### 安裝依賴

```powershell
py -m pip install -r requirements.txt
```

`requirements.txt` 內容：

| 套件 | 用途 |
|------|------|
| `openai` | OpenAI GPT API |
| `anthropic` | Claude API |
| `google-genai` | Gemini API |
| `python-dotenv` | 自動載入 `.env` |

### API 金鑰（`.env`）

複製 `.env.example` 為 `.env`，填入對應金鑰：

```ini
GEMINI_API_KEY=AIza...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

啟動時自動載入，GUI 會依選取的 Provider 自動帶入對應欄位。

---

## 啟動方式

### GUI（建議）

```powershell
py src/gui.py
```

| 欄位 | 說明 |
|------|------|
| Provider | OpenAI / Claude / Gemini 三選一 |
| API Key | 自動從 `.env` 帶入，可手動覆蓋 |
| Model | 預設值可手動修改（例如換成 gemini-2.5-flash）|
| 草稿 / 引用表 / 文獻庫 / 格式 | 預設指向 `data/` 與 `styles/`，可點「瀏覽」換檔 |

執行完成後點「開啟輸出資料夾」直接跳到 `output/`。

### CLI

```powershell
# 設定 Provider（預設 openai）
$env:LLM_PROVIDER = "gemini"   # openai | claude | gemini

py src/main.py
```

---

## LLM Provider 對照

| Provider | 環境變數 | 預設 Model | 自訂 Model 變數 |
|----------|----------|------------|-----------------|
| `openai` | `OPENAI_API_KEY` | `gpt-4o` | `OPENAI_MODEL` |
| `claude` | `ANTHROPIC_API_KEY` | `claude-sonnet-4-6` | `CLAUDE_MODEL` |
| `gemini` | `GEMINI_API_KEY` | `gemini-2.0-flash` | `GEMINI_MODEL` |

---

## 換稿件 / 換文獻庫的標準流程

1. 將新草稿存為 `data/draft.txt`，確認引用標記格式為 `[1]`、`[2]` 等
2. 更新 `data/cite_map.json`，將每個標記對應到 Zotero citekey
3. 從 Zotero 匯出 Better BibTeX `.bib` 覆蓋 `data/epidermal_cyst.bib`（或在 GUI 點「瀏覽」選新檔）
4. 執行 Pipeline

### cite_map.json 格式

```json
{
    "[1]": "[@smithEpidermalCyst2023]",
    "[2]": "[@leeWoundHealing2021]"
}
```

citekey 來自 Zotero Better BibTeX 的 Citation Key 欄位。

---

## Pandoc 安裝位置

本機安裝於 `C:\Program Files\Pandoc\pandoc.exe`（v3.9.0.2）。
程式會在 PATH 找不到 `pandoc` 時自動 fallback 到此路徑，無需手動設定環境變數。

---

## ARS 整合（前段研究工具）

本專案後段（翻譯 → Word）整合 **Academic Research Skills (ARS)** 作為前段（問題收斂 → 文獻蒐集）。

### 安裝 ARS

```powershell
mkdir -p .claude/skills
git clone https://github.com/Imbad0202/academic-research-skills.git .claude/skills/academic-research-skills
```

### 整合後完整工作流

```
Step 1  ARS deep-research（蘇格拉底模式）
        輸入模糊想法 → AI 引導收斂 research question → 輸出文獻清單 + 研究架構

Step 2  將文獻加入 Zotero → 匯出更新 data/epidermal_cyst.bib

Step 3  上傳同一批文獻到 NotebookLM 作為 source
        → 生成中文草稿（含 {{n}} 標記）+ 文末「文獻對應表」

Step 4  med_paper_writer GUI
        ├─ 草稿分頁：貼入草稿並儲存
        ├─ 引用表分頁：⚡ 從草稿自動產生（S2 API + 模糊比對）
        └─ 設定與執行：▶ 執行 Pipeline → Final_Paper.docx

Step 5  ARS academic-paper-reviewer（選用）
        把英文稿貼入 → 5 位 AI 審稿人模擬同儕審查 → 修訂後重跑 Pipeline
```

### 引用表自動比對邏輯（三層）

| 層級 | 方法 | 說明 |
|------|------|------|
| Tier 0 | Semantic Scholar API | 標題搜尋 → DOI → .bib DOI 精確比對（綠色） |
| Tier 1 | difflib 模糊比對 | 標題相似度 ≥ 0.25 → .bib 標題比對（黃色） |
| 未比對 | — | 顯示 @UNMATCHED_n，需手動輸入 citekey（紅色） |

---

## System Prompt 設計原則

LLM 收到的 system prompt 要求：

1. 中文 → 正式學術英文
2. 第三人稱、被動語態，符合 JFMA / Vancouver 風格
3. **強制保留** `[@citekey]` 標記，不得移除或改動
4. 只輸出改寫後的正文，不加任何說明文字
