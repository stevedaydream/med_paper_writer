# 投稿流程指南
**論文**：A Large Epidermoid Cyst of the Pelvic Floor Mimicking Rectal Submucosal Malignancy: A Case Report  
**目標期刊**：Journal of the Formosan Medical Association (JFMA)  
**最後更新**：2026-06-03

---

## 一、寫作輔助 Skills 使用說明

### 1-1 啟動審稿模擬（academic-paper-reviewer）

在 Claude Code 中輸入：

```
/academic-paper-reviewer
```

**三個階段**：

| 階段 | 指令／動作 | 輸出 |
|---|---|---|
| Phase 0 | 自動執行 | 審稿委員設定卡（5 位）；可回覆調整後繼續 |
| Phase 1 | 輸入 `continue` 或直接等待 | 5 份獨立審稿報告 |
| Phase 2 | 自動執行 | Editorial Decision Letter + Revision Roadmap |

**修改完成後跑驗證審查（re-review）**：

```
/academic-paper-reviewer
```
待 Phase 0 完成後輸入：
```
re-review
```
提供：原始 Revision Roadmap + 修改後稿件 → 輸出 R&R Traceability Matrix + 新決議。

**隨時中止任一階段**：
```
停止
```

---

### 1-2 目前已完成的審查輪次

| 輪次 | 模式 | 結果 |
|---|---|---|
| Round 1 | full（校準至 JFMA） | Major Revision；Revision Roadmap 20 項 |
| Round 2 | re-review | 所有關鍵項目驗證通過；剩餘阻斷項：Figure 1 |

---

## 二、稿件編輯與輸出流程

### 2-1 檔案架構

```
medpaper/
├── Case_Report_Epidermoid_Cyst.md        ← 主稿（唯一編輯來源）
├── Case_Report_Epidermoid_Cyst_raw.docx  ← pandoc 中間產物（勿手動編輯）
├── Case_Report_Epidermoid_Cyst_submission.docx  ← 最終投稿檔
├── format_docx.py                        ← 格式後處理腳本
├── fill_irb_forms.py                     ← IRB 表格填寫腳本
├── paper.md                              ← 進度記錄
├── figures/
│   ├── Figure1_HE_pathology_PENDING.txt  ← ⏳ 待向病理科索取
│   ├── Figure2A_CT_coronal.png
│   ├── Figure2B_CT_axial.png
│   └── Figure3_colonoscopy.png
└── DOC/                                  ← IRB 表格填寫版（共 13 份）
```

### 2-2 稿件修改步驟

1. **只編輯** `Case_Report_Epidermoid_Cyst.md`（Markdown 原始稿）
2. 引用格式：Vancouver 上標，使用 `^1^` 符號（例：`^1,3^`）
3. 字數限制：主文（Introduction → Conclusion）≤ 1,500 字；英文摘要 ≤ 150 字

### 2-3 輸出 Word 投稿檔（兩步驟）

**Step 1 — 用 pandoc 轉換 Markdown → 原始 docx**

```powershell
pandoc --from markdown+superscript `
       "C:\Users\User\Downloads\medpaper\Case_Report_Epidermoid_Cyst.md" `
       -o "C:\Users\User\Downloads\medpaper\Case_Report_Epidermoid_Cyst_raw.docx"
```

> `markdown+superscript` 旗標讓 `^1^` 轉為上標格式。

**Step 2 — 用 format_docx.py 套用 JFMA 格式**

```powershell
cd "C:\Users\User\Downloads\medpaper"
py format_docx.py
```

套用內容：
- Times New Roman 12pt
- 雙倍行距（Double spacing）
- 左對齊正文
- 頁碼（頁底置中）
- 四邊 2.54 cm 邊距
- 表格 11pt

輸出：`Case_Report_Epidermoid_Cyst_submission.docx`

---

## 三、IRB 文件準備流程

### 3-1 來源文件位置

```
C:\Users\User\Downloads\
├── 65_10-1.doc      → 個案報告收件表格
├── 65_10-2.doc      → PI/CoPI 履歷
├── 65_10-4.docx     → 個案報告審查申請表
├── 65_10-5.docx     → 中英文摘要表
├── 65_10-6.docx     → 病人資料提供同意書
├── 65_10-7-1.doc    → 財務利益評估說明表
└── 65_10-7-2.doc    → 財務利益申報表
```

> `.doc` 檔需先用 Word COM 轉為 `.docx` 才能讀取。轉換指令（PowerShell）：
> ```powershell
> $word = New-Object -ComObject Word.Application
> $doc  = $word.Documents.Open("C:\Users\User\Downloads\65_10-1.doc")
> $doc.SaveAs2("C:\Users\User\Downloads\65_10-1_converted.docx", 16)
> $doc.Close(); $word.Quit()
> ```

### 3-2 自動填寫

```powershell
cd "C:\Users\User\Downloads\medpaper"
py fill_irb_forms.py
```

輸出至 `medpaper/DOC/`，共 13 份（見下表）。

### 3-3 輸出檔案清單

| 檔案 | 份數 | 自動填入內容 |
|---|---|---|
| `10-1_收件表格_填.docx` | 1 | 計畫名稱、研究團隊、文件備妥欄 V |
| `10-2_履歷_陳樞鴻_填.docx` | 1 | 現任職務、角色、本次投稿著作 |
| `10-2_履歷_陳紹寬_填.docx` | 1 | 同上（協同主持人） |
| `10-2_履歷_王子建_填.docx` | 1 | 同上（研究人員） |
| `10-2_履歷_吳美智_填.docx` | 1 | 同上（研究人員） |
| `10-4_審查申請表_填.docx` | 1 | 計畫名稱、PI 資訊、研究期間、■無贊助、■病例報告、■病患 |
| `10-5_中英文摘要表_填.docx` | 1 | 目的、設計、完整中英文摘要、關鍵字 |
| `10-6_病人同意書_填.docx` | 1 | 計畫名稱與主持人欄；病人資料留空 |
| `10-7-1_財務評估說明表_填.docx` | 1 | A欄 Q1–Q6 全部填答，B欄聲明無衝突 |
| `10-7-2_財務申報表_陳樞鴻_填.docx` | 1 | A欄無財務利益 + PI 總聲明 |
| `10-7-2_財務申報表_陳紹寬_填.docx` | 1 | A欄無財務利益 |
| `10-7-2_財務申報表_王子建_填.docx` | 1 | A欄無財務利益 |
| `10-7-2_財務申報表_吳美智_填.docx` | 1 | A欄無財務利益 |

### 3-4 需人工補填的欄位

- **所有表格**：各人院內電話分機、非陳樞鴻人員的 email
- **10-2 履歷（×4）**：出生年月日、學歷、曾任經歷
- **10-6 同意書**：病人姓名、出生日期、病歷號（由主持人從病歷填入）
- **IRB 案號**：待秘書處給號後，填入 10-1、10-4、10-7-1
- **所有表格**：親筆簽名 + 日期

### 3-5 送件

完成後以 PDF 掃描或 Word 檔寄至：
```
irb@cgh.org.tw
```

---

## 四、投稿前最終確認清單

### 阻斷項（必須完成才能投稿）

- [ ] **Figure 1**：向病理科索取 H&E 切片照片（≥ 300 dpi，TIFF 或 PNG）
- [ ] **IRB 核准**：送件後取得 CGH-P 案號，填入稿件倫理聲明
- [ ] **重新輸出 docx**：Figure 1 取得後，重跑 pandoc + `format_docx.py`

### 文件完整性

- [ ] `Case_Report_Epidermoid_Cyst_submission.docx`（主稿 + Table 1 + Figure Legends）
- [ ] Figure 1（H&E）、Figure 2A（CT 冠狀面）、Figure 2B（CT 軸狀面）、Figure 3（大腸鏡）
- [ ] Cover Letter（投稿系統填寫，或額外 .docx）
- [ ] Author Contribution Statement（已嵌入稿件 CRediT 聲明）

### JFMA 格式要求確認

| 項目 | 限制 | 狀態 |
|---|---|---|
| 主文字數 | ≤ 1,500 字 | ✅ 1,459 字 |
| 英文摘要 | ≤ 150 字 | ✅ 138 字 |
| 引用格式 | Vancouver 上標編號 | ✅ |
| Figure 數量 | ≤ 4 | ✅ 4 張 |
| Table 數量 | ≤ 2 | ✅ 1 張 |
| CARE 合規 | 13 項清單 | ✅ 主要項目均符合 |

### CARE 重要項目確認

| 項目 | 說明 | 狀態 |
|---|---|---|
| 1 題目 | 含 "case report" | ✅ |
| 3 病人資訊 | 去識別化 | ✅ |
| 5 時間軸 | Table 1 已加入 | ✅ |
| 7 鑑別診斷 | 三聯徵框架 | ✅ |
| 8 診斷評估 | CT、內視鏡、腫瘤標記 | ✅ |
| 12 病人觀點 | Patient Perspective 段落 | ✅ |
| 13 知情同意 | 聲明已填入 | ✅ |

---

## 五、研究團隊聯絡資訊

| 角色 | 姓名 | 科別 | Email |
|---|---|---|---|
| 計畫主持人（通訊作者） | 陳樞鴻 MD | 直腸外科 | cgh07668@cgh.org.tw |
| 協同主持人 | 陳紹寬 MD | 泌尿科 | cgh05315@cgh.org.tw |
| 研究人員（第一作者） | 王子建 NP | 護理科| cgh380131@cgh.org.tw |
| 研究人員 | 吳美智 SA | 護理科 | — |

**機構**：汐止國泰綜合醫院（Xizhi Cathay General Hospital）  
**IRB 信箱**：irb@cgh.org.tw

---

## 六、常用指令速查

```powershell
# 審稿模擬
/academic-paper-reviewer

# Markdown → raw docx
pandoc --from markdown+superscript Case_Report_Epidermoid_Cyst.md -o Case_Report_Epidermoid_Cyst_raw.docx

# 套用 JFMA 格式
py format_docx.py

# 填寫 IRB 表格
py fill_irb_forms.py

# 查看輸出檔案
Get-ChildItem "C:\Users\User\Downloads\medpaper\DOC"
```
