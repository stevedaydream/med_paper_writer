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
| 主文字數 | ≤ 1,500 字 | 現況 1,486 字（含新增 IRB 聲明句） | ✅ |
| 作者人數 | ≤ 5 人 | 現況 4 人 | ✅ |
| 參考文獻 | ≤ 25 筆 | 現況 9 筆 | ✅ |
| 關鍵字 | ≤ 6 個 | 現況 5 個 | ✅ |

### FJJM 投稿檔案清單（`FJJM/` 資料夾）

- `Case_Report_Epidermoid_Cyst_FJJM.md` — 主稿原始檔（唯一編輯來源，改稿只改這份）
- `Case_Report_Epidermoid_Cyst_FJJM_submission.docx` — 投稿用 Word 檔
- `Chinese_Abstract_FJJM.docx` — 獨立中文摘要文件
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
- [ ] 至少 3 位推薦審稿人（姓名／機構／Email，副教授以上，無利益衝突）— Google Form 必填，尚缺
- [ ] 全體 4 位作者親筆簽署 Copyright Transfer Form
- [ ] 透過 Google Form 提交：https://forms.gle/6YCNaR2B4vaSE5ws5
- [ ] 提交後寄信確認至 fjjm@mail.fju.edu.tw（三項附件：manuscript + Chinese abstract + copyright form）
- [ ] 建議：投稿前以 fjjm@mail.fju.edu.tw 或 (02)2905-3477 確認截稿/收費資訊（官網頁面未列明）

### Google Form 填寫內容（截至最新更新，供送出時核對）

| 欄位 | 內容 |
|---|---|
| Types of Articles | Case Report |
| IRB/IACUC NO. | CGH-P115074 |
| Article title | A Large Epidermoid Cyst of the Pelvic Floor Mimicking Rectal Malignancy: A Case Report |
| Running title | Epidermoid Cyst Mimicking Rectal Cancer |
| 作者（英文） | Wang Tzu-Chien, Chen Shao-Kuan, Wu Mei-Chih, Chen Shu-Hung |
| 作者（中文） | 王子建、陳紹寬、吳美智、陳樞鴻 |
| 服務機構 | Department of Colorectal Surgery / Department of Urology, Xizhi Cathay General Hospital, New Taipei City, Taiwan |
| 通訊作者（英文） | Chen Shu-Hung |
| 通訊作者 Email | cgh07668@cgh.org.tw |
| 通訊作者電話/傳真 | 0983701132（院內手機）／(02)2648-2690（傳真） |
| 通訊作者服務機構 | Department of Colorectal Surgery, Xizhi Cathay General Hospital, New Taipei City, Taiwan |
| 推薦審稿人 | ⏳ 尚缺（需至少 3 位） |
| Upload abstract | FJJM/English_Abstract_FJJM.docx |
| Upload chinese abstract | FJJM/Chinese_Abstract_FJJM.docx |
