# 論文進度記錄

**標題**: A Large Epidermoid Cyst of the Pelvic Floor Mimicking Rectal Submucosal Malignancy: A Case Report

**目標期刊**: Fu-Jen Journal of Medicine (FJJM)（原以 JFMA 格式準備，2026-07-20 改投 FJJM，詳見下方「FJJM 投稿轉換」章節；JFMA 版本保留於 `Final/paper/`）

**作者**:
- 第一作者：王子建 (Wang Tzu-Chien), NP — 汐止國泰綜合醫院 直腸外科
- 通訊作者：陳樞鴻 (Chen Shu-Hung), MD — 汐止國泰綜合醫院 直腸外科

---

## 字數狀態

| 部分 | 字數 | JFMA 上限 | 狀態 |
|---|---|---|---|
| 主文（Introduction–Conclusion） | 1,459 | 1,500 | ✅ |
| Abstract (EN) | 138 | 150 | ✅ |

---

## 檔案清單

| 檔案 | 說明 | 狀態 |
|---|---|---|
| `Case_Report_Epidermoid_Cyst.md` | 主稿（Markdown 原始檔） | ✅ 完成 |
| `Case_Report_Epidermoid_Cyst_submission.docx` | 投稿用 Word 檔（Times New Roman 12pt、雙倍行距、左對齊、2.54 cm 邊距） | ✅ 完成 |
| `figures/Figure2A_CT_coronal.png` | CT 冠狀面 | ✅ 去識別化完成 |
| `figures/Figure2B_CT_axial.png` | CT 軸狀面（含 PACS 量測線，已於 legend 說明） | ✅ 去識別化完成 |
| `figures/Figure3_colonoscopy.png` | 大腸鏡直腸外壓影像 | ✅ 去識別化完成 |
| `figures/Figure1_HE_pathology_PENDING.txt` | H&E 病理切片 | ⏳ 待向病理科索取 |

---

## 待辦事項（投稿前必須完成）

- [ ] **Figure 1**：H&E 病理切片照片（向病理科索取，需 300 dpi 以上）
- [x] **通訊作者 Email**：cgh07668@cgh.org.tw（已填入論文署名列）
- [ ] **重新輸出 Word 檔**：補完上述項目後重跑 `format_docx.py`

## 待回醫院確認的臨床細節

- [x] **DRE**：已確認有做（3/2），左側 2 點鐘方向 >5cm 硬塊，距肛門約 4 cm。已更正稿件中「deferred」錯誤描述。
- [x] **雙J管拔除時間**：目前仍在（DBJ尚未取出）。已於術後段落補入「retained in situ at discharge, outpatient removal planned」。
- [x] **術後腎功能**：Cr 0.85 mg/dL、eGFR 99（術後 day 9）；無水腎（沒有水腎）。已補入 Case Presentation 及已從 Limitations 移除「unavailable」說明。

---

## 已完成修改記錄

### Revision Roadmap（來自 academic-paper-reviewer 審查）

| 項目 | 狀態 |
|---|---|
| Diagnostic triad 重新框架（改為指向良性外壓性囊腫，非特指 epidermoid cyst） | ✅ |
| 病理描述矛盾解決（補入術中抽吸減壓步驟） | ✅ |
| DRE 未做說明（臨床判斷充分） | ✅ |
| MRI 未做說明（CT + 其他檢查已足夠） | ✅ |
| L2 骨折交代（骨質疏鬆性偶發發現） | ✅ |
| 血尿術後消失記錄 | ✅ |
| 淋巴結歸因限制聲明 | ✅ |
| Limitations 段落新增 | ✅ |
| Figure 2B PACS 量測線說明加入 legend | ✅ |
| 「fewer than 20 cases」補充說明 | ✅ |
| CRediT 作者姓名填入 | ✅ |
| AI 工具名稱填入（Claude, Anthropic） | ✅ |
| 作者署名列新增（含機構、通訊作者） | ✅ |
| Figure 2（CT 兩張）、Figure 3（大腸鏡）Legend 更新 | ✅ |
| 全文精簡至 JFMA 字數上限 | ✅ |
| 水腎分級補入（SFU Grade 3，術中確認） | ✅ |
| Limitations 移除水腎未分級聲明 | ✅ |
| CARE 合規：Patient Perspective 段落補入 | ✅ |
| CARE 合規：Table 1 臨床時間軸新增 | ✅ |

---

## 備註

- 手術日期：2026-03-10
- 病人病歷號已去識別化（圖片已處理）
- 倫理聲明、病人同意書、利益衝突聲明均已填入

---

## FJJM 投稿轉換（2026-07-20）

來源：https://cme.fju.edu.tw/networkServices.jsp?labelID=15（及其子頁 labelID=16–19, 27）

### JFMA → FJJM 格式差異與已完成調整

| 項目 | FJJM 規定 | 調整內容 | 狀態 |
|---|---|---|---|
| 引用格式 | 方括號數字，標點後（如 `[1-3].`），非上標 | 全文 `^n^` 改為 `[n]` | ✅ |
| Running title | < 40 字元 | 新增 "Epidermoid Cyst Mimicking Rectal Cancer"（39 字元） | ✅ |
| 章節順序 | Main Text → References → Figures+Legends → Tables | Table 1 移至 Figure Legends 之後 | ✅ |
| IRB 核准號 | 須寫在 Materials and Methods（本文對應 Case Presentation）段落內 | 於 Case Presentation 開頭補入 IRB 核准聲明（CGH-P115074） | ✅ |
| 中文摘要 | 需作為**獨立文件**提交（含中文作者姓名） | 新增 `FJJM/Chinese_Abstract_FJJM.docx` | ✅ |
| Authorship and Transfer of Copyright Form | 全體作者需簽署 | 下載官方表格 + 預填姓名/Email 草稿：`FJJM/FJJM_Authorship_Copyright_Transfer_Form_filled.docx` | ⏳ 待各作者簽名 |
| 摘要字數 | ≤ 200 字（case report 為 unstructured） | 現況 141 字 | ✅ |
| 標題頁中文資訊 | 需含中文標題、中文短標題、作者中文全名、中文服務單位、通訊作者電話 | 補齊：中文標題「骨盆底巨大硬皮囊腫擬似直腸惡性腫瘤：病例報告」、中文短標題「盆底硬皮囊腫擬似直腸腫瘤」（12字）、作者中文全名與中文單位、電話 0983701132／傳真 (02)2648-2690 | ✅ 2026-07-24 |
| 通訊作者科別更正 | 陳樞鴻實際為一般外科，非大腸直腸外科 | 新增附註³「Department of General Surgery／一般外科」，僅套用於陳樞鴻 | ✅ 2026-07-24 |
| 王子建／吳美智科別更正 | 兩人實際為護理部（NP），非大腸直腸外科 | 附註¹改為「Department of Nursing／護理部」 | ✅ 2026-07-24 |
| 中文摘要字數 | 個案報告 ≤ 200 字 | 原 390 字 → 精簡至 186 字 | ✅ 2026-07-24 |
| 主文字數 | ≤ 1,500 字 | 修正後 1,496 字（含章節標題） | ✅ 2026-07-24 |
| 參考文獻期數 | 期刊論文不需刊出期數 | 移除 Ref 5, 8, 9 的 `(issue)` 標示 | ✅ 2026-07-24 |
| 邊界 margin | 英文版規定 ≥3 cm | `format_docx_fjjm.py` 由 2.54cm 改為 3cm | ✅ 2026-07-24 |
| 投稿信件（Cover Letter） | 投稿檢查表第一項 | 新增 `FJJM/Cover_Letter_FJJM.md` / `.docx` | ✅ 2026-07-24 |
| 圖片未內嵌於投稿 Word 檔 | Google Form「Upload manuscript」欄位要求含 Figures 本體，非僅圖說 | 在 `.md` 對應圖說前以 `![](FJJM/figures/xxx.png){width=...}` 插入 4 張圖（Figure1 病理、Figure2A/2B CT、Figure3 大腸鏡），重新產出 docx（5.8MB，遠低於 100MB 上限） | ✅ 2026-07-24 |
| 版權讓渡書格式 | Google Form 該欄位僅收 PDF/JPG，不收 docx | 用 Word COM 將 `FJJM_Authorship_Copyright_Transfer_Form_filled.docx` 轉出同名 `.pdf` | ✅ 2026-07-24 |
| 主文字數 | ≤ 1,500 字 | 現況 1,486 字（含新增 IRB 聲明句） | ✅ |
| 作者人數 | ≤ 5 人 | 現況 4 人 | ✅ |
| 參考文獻 | ≤ 25 筆 | 現況 9 筆 | ✅ |
| 關鍵字 | ≤ 6 個 | 現況 5 個 | ✅ |

### FJJM 投稿檔案清單（`FJJM/` 資料夾）

- `Case_Report_Epidermoid_Cyst_FJJM.md` — 主稿原始檔（唯一編輯來源，改稿只改這份；已含中英文標題頁）
- `Case_Report_Epidermoid_Cyst_FJJM_submission.docx` — 投稿用 Word 檔（3cm 邊界、雙倍行距）
- `Chinese_Abstract_FJJM.docx` — 獨立中文摘要文件（含中文標題頁資訊，摘要已精簡至 186 字）
- `Cover_Letter_FJJM.md` / `.docx` — 投稿信件（新增）
- `FJJM_Authorship_Copyright_Transfer_Form.pdf` — 官方空白表格（存查）
- `FJJM_Authorship_Copyright_Transfer_Form_filled.docx` — 預填姓名/Email 草稿，待列印簽名
- 圖片沿用 `figures/Final/`（Figure1_HE_pathology.png、Figure2A/B、Figure3）

### 重新產出 Word 檔的指令

```powershell
cd "C:\Users\User\Downloads\medpaper"
pandoc "Case_Report_Epidermoid_Cyst_FJJM.md" -o "Case_Report_Epidermoid_Cyst_FJJM_raw.docx"
py format_docx_fjjm.py
```

### 待辦（投稿前）

- [x] 吳美智 email：chih900818@hotmail.com（已填入 Copyright Form）
- [x] 通訊作者（陳樞鴻）電話與傳真：0983701132（院內手機）／傳真 (02)2648-2690（教學研究室）
- [x] 標題頁補齊中文標題／短標題／作者中文名／中文單位／通訊作者電話（2026-07-24）
- [x] 中文摘要精簡至 200 字以內（2026-07-24）
- [x] Cover Letter 草稿完成，待陳樞鴻確認內容與簽名（2026-07-24）
- [x] 推薦審稿人欄位：填寫「由編輯部指派」（2026-07-24，使用者決定）
- [x] Google Form 文字欄位已由 Claude 透過瀏覽器自動化填寫完成（2026-07-24，草稿已自動儲存）；檔案上傳（English/Chinese abstract、Cover Letter、manuscript 含圖、copyright form PDF）由使用者手動完成
- [x] 第二頁「Checklist for Submission」勾選完成並送出（2026-07-24）
- [x] 透過 Google Form 提交：https://forms.gle/6YCNaR2B4vaSE5ws5（2026-07-24，已完成送出）
- [x] 提交後確認信已寄至 fjjm@mail.fju.edu.tw（2026-07-24，已完成寄出）
- [x] 確認信附件 manuscript 為含 4 張圖片的最新版（5.8MB），非舊版（使用者已核實，2026-07-24）
- [ ] 全體 4 位作者親筆簽署 Copyright Transfer Form — 依須知第七項可於接受後再補簽，不須卡在投稿前（見下方說明）
- [ ] 等待期刊編輯部回覆（分派審稿人／進入審稿流程）

**投稿狀態：已於 2026-07-24 完成送出。** 後續只剩全體作者補簽 Copyright Transfer Form（可待接受後再辦），其餘等待編輯部回覆即可。
- [ ] 建議：投稿前以 fjjm@mail.fju.edu.tw 或 (02)2905-3477 確認截稿/收費資訊（官網頁面未列明）

> **簽名時機說明**：官方投稿須知檢查表第七項明載「作者簽名之投稿聲明書與版權讓渡書，亦可於本刊接受您的稿件後，再行簽署」，因此不需要在今天送出 Google Form 時就備妥簽名版——可先寄未簽名的草稿版本，待期刊來信確認方向後，全體作者再親簽補交。

### Google Form 填寫內容（截至最新更新，供送出時核對）

| 欄位 | 內容 |
|---|---|
| Types of Articles | Case Report |
| IRB/IACUC NO. | CGH-P115074 |
| Article title | A Large Epidermoid Cyst of the Pelvic Floor Mimicking Rectal Malignancy: A Case Report |
| Running title | Epidermoid Cyst Mimicking Rectal Cancer |
| 作者（英文） | Wang Tzu-Chien, Chen Shao-Kuan, Wu Mei-Chih, Chen Shu-Hung |
| 作者（中文） | 王子建、陳紹寬、吳美智、陳樞鴻 |
| 服務機構 | Department of Nursing / Department of Urology / Department of General Surgery, Xizhi Cathay General Hospital, New Taipei City, Taiwan |
| 通訊作者（英文） | Chen Shu-Hung |
| 通訊作者 Email | cgh07668@cgh.org.tw |
| 通訊作者電話/傳真 | 0983701132（院內手機）／(02)2648-2690（傳真） |
| 通訊作者服務機構 | Department of General Surgery, Xizhi Cathay General Hospital, New Taipei City, Taiwan |
| 推薦審稿人 | 由編輯部指派 |
| Upload abstract | FJJM/English_Abstract_FJJM.docx |
| Upload chinese abstract | FJJM/Chinese_Abstract_FJJM.docx |
