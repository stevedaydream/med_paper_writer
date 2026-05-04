"""
Auto Paper Writer — GUI
Run: python src/gui.py

Tabs:
  設定與執行  — LLM settings, file paths, run pipeline, log
  草稿        — edit draft.txt inline
  引用表      — CRUD editor for cite_map.json
"""

import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

load_dotenv(Path(__file__).parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))
from main import (BASE, BIB_PATH, CITE_MAP_PATH, CSL_PATH, DRAFT_PATH, OUTPUT_DIR,
                  DEFAULT_MODELS, run_pipeline, auto_generate_cite_map)

# ── Provider metadata ──────────────────────────────────────────────────────────
PROVIDERS = {
    "OpenAI (GPT)":       {"id": "openai", "key_label": "OPENAI_API_KEY"},
    "Claude (Anthropic)": {"id": "claude", "key_label": "ANTHROPIC_API_KEY"},
    "Gemini (Google)":    {"id": "gemini", "key_label": "GEMINI_API_KEY"},
}

FILETYPES = {
    "draft":    [("Text files", "*.txt"), ("All files", "*.*")],
    "cite_map": [("JSON files", "*.json"), ("All files", "*.*")],
    "bib":      [("BibTeX files", "*.bib"), ("All files", "*.*")],
    "csl":      [("CSL files", "*.csl"), ("All files", "*.*")],
}


# ── Stdout redirector (thread-safe) ────────────────────────────────────────────
class _QueueWriter:
    def __init__(self, q: queue.Queue):
        self._q = q
    def write(self, text: str):
        if text:
            self._q.put(text)
    def flush(self):
        pass


# ── Main window ────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Auto Paper Writer")
        self.resizable(True, True)
        self.minsize(660, 640)
        self._log_queue: queue.Queue = queue.Queue()
        self._build_ui()
        self._poll_log()

    # ── Top-level layout ──────────────────────────────────────────────────────

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._nb = ttk.Notebook(self)
        self._nb.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self._nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

        # Tab 1 — 設定與執行
        t1 = ttk.Frame(self._nb)
        t1.columnconfigure(0, weight=1)
        t1.rowconfigure(3, weight=1)
        self._nb.add(t1, text="  設定與執行  ")
        self._build_llm_section(t1, row=0)
        self._build_file_section(t1, row=1)
        self._build_run_button(t1, row=2)
        self._build_log_section(t1, row=3)

        # Tab 2 — 草稿編輯
        t2 = ttk.Frame(self._nb)
        t2.columnconfigure(0, weight=1)
        t2.rowconfigure(0, weight=1)
        self._nb.add(t2, text="  草稿  ")
        self._build_draft_tab(t2)

        # Tab 3 — 引用表
        t3 = ttk.Frame(self._nb)
        t3.columnconfigure(0, weight=1)
        t3.rowconfigure(0, weight=1)
        self._nb.add(t3, text="  引用表  ")
        self._build_cite_tab(t3)

    # ── Tab 1 — 設定與執行 ────────────────────────────────────────────────────

    def _build_llm_section(self, parent, row):
        frame = ttk.LabelFrame(parent, text=" LLM 設定 ", padding=(12, 8))
        frame.grid(row=row, column=0, sticky="ew", padx=12, pady=(12, 4))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Provider").grid(row=0, column=0, sticky="w", pady=4)
        self._provider_var = tk.StringVar(value="Gemini (Google)")
        cb = ttk.Combobox(frame, textvariable=self._provider_var,
                          values=list(PROVIDERS.keys()), state="readonly", width=26)
        cb.grid(row=0, column=1, columnspan=2, sticky="w", padx=(8, 0), pady=4)
        cb.bind("<<ComboboxSelected>>", self._on_provider_change)

        self._key_label_var = tk.StringVar()
        ttk.Label(frame, textvariable=self._key_label_var).grid(row=1, column=0, sticky="w", pady=4)
        self._api_key_var = tk.StringVar()
        self._key_entry = ttk.Entry(frame, textvariable=self._api_key_var, show="•", width=42)
        self._key_entry.grid(row=1, column=1, sticky="ew", padx=(8, 4), pady=4)
        self._show_key_btn = ttk.Button(frame, text="顯示", width=5, command=self._toggle_key)
        self._show_key_btn.grid(row=1, column=2, pady=4)

        ttk.Label(frame, text="Model").grid(row=2, column=0, sticky="w", pady=4)
        self._model_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self._model_var, width=30).grid(
            row=2, column=1, sticky="w", padx=(8, 0), pady=4)

        self._on_provider_change()

    def _build_file_section(self, parent, row):
        frame = ttk.LabelFrame(parent, text=" 檔案路徑 ", padding=(12, 8))
        frame.grid(row=row, column=0, sticky="ew", padx=12, pady=4)
        frame.columnconfigure(1, weight=1)

        rows = [
            ("草稿  (.txt)",   DRAFT_PATH,    "draft"),
            ("引用表 (.json)", CITE_MAP_PATH, "cite_map"),
            ("文獻庫 (.bib)",  BIB_PATH,      "bib"),
            ("格式  (.csl)",   CSL_PATH,      "csl"),
        ]
        self._file_vars: list[tk.StringVar] = []
        for i, (label, default, key) in enumerate(rows):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=3)
            var = tk.StringVar(value=str(default))
            self._file_vars.append(var)
            ttk.Entry(frame, textvariable=var).grid(
                row=i, column=1, sticky="ew", padx=(8, 4), pady=3)
            ttk.Button(frame, text="瀏覽", width=5,
                       command=lambda v=var, k=key: self._browse(v, FILETYPES[k])
                       ).grid(row=i, column=2, pady=3)

    def _build_run_button(self, parent, row):
        frame = ttk.Frame(parent, padding=(12, 4))
        frame.grid(row=row, column=0, sticky="ew")
        frame.columnconfigure(0, weight=1)
        self._run_btn = ttk.Button(frame, text="▶   執行 Pipeline", command=self._on_run)
        self._run_btn.grid(row=0, column=0, sticky="ew", ipady=6)

    def _build_log_section(self, parent, row):
        frame = ttk.LabelFrame(parent, text=" 執行紀錄 ", padding=(12, 8))
        frame.grid(row=row, column=0, sticky="nsew", padx=12, pady=(4, 12))
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self._log = scrolledtext.ScrolledText(
            frame, state="disabled", wrap="word",
            bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
            font=("Consolas", 9), relief="flat", height=12,
        )
        self._log.grid(row=0, column=0, sticky="nsew")

        btn_bar = ttk.Frame(frame)
        btn_bar.grid(row=1, column=0, sticky="e", pady=(6, 0))
        self._open_btn = ttk.Button(btn_bar, text="開啟輸出資料夾",
                                    command=self._open_output, state="disabled")
        self._open_btn.grid(row=0, column=0, padx=(0, 6))
        ttk.Button(btn_bar, text="清除紀錄", command=self._clear_log).grid(row=0, column=1)

    # ── Tab 2 — 草稿編輯 ──────────────────────────────────────────────────────

    def _build_draft_tab(self, parent):
        frame = ttk.Frame(parent, padding=(12, 8))
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Path indicator
        top = ttk.Frame(frame)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        top.columnconfigure(1, weight=1)
        ttk.Label(top, text="檔案：").grid(row=0, column=0, sticky="w")
        self._draft_path_lbl = ttk.Label(top, foreground="#888")
        self._draft_path_lbl.grid(row=0, column=1, sticky="w", padx=(4, 0))

        # Text editor
        self._draft_editor = tk.Text(
            frame, wrap="word", undo=True,
            font=("Consolas", 10), relief="flat",
            bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="white", selectbackground="#264f78",
        )
        vsb = ttk.Scrollbar(frame, command=self._draft_editor.yview)
        self._draft_editor.configure(yscrollcommand=vsb.set)
        self._draft_editor.grid(row=1, column=0, sticky="nsew")
        vsb.grid(row=1, column=1, sticky="ns")

        # Buttons
        btn_bar = ttk.Frame(frame)
        btn_bar.grid(row=2, column=0, columnspan=2, sticky="e", pady=(8, 0))
        ttk.Button(btn_bar, text="重新載入", command=self._load_draft).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(btn_bar, text="儲存草稿", command=self._save_draft).grid(row=0, column=1)

    # ── Tab 3 — 引用表編輯 ────────────────────────────────────────────────────

    def _build_cite_tab(self, parent):
        frame = ttk.Frame(parent, padding=(12, 8))
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Path indicator
        top = ttk.Frame(frame)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        top.columnconfigure(1, weight=1)
        ttk.Label(top, text="檔案：").grid(row=0, column=0, sticky="w")
        self._cite_path_lbl = ttk.Label(top, foreground="#888")
        self._cite_path_lbl.grid(row=0, column=1, sticky="w", padx=(4, 0))

        # Treeview
        tree_frame = ttk.Frame(frame)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self._cite_tree = ttk.Treeview(tree_frame, columns=("tag", "citekey", "source"),
                                        show="headings", selectmode="extended")
        self._cite_tree.heading("tag",     text="編號 ({{n}})")
        self._cite_tree.heading("citekey", text="Citekey  (如 @authorYear)")
        self._cite_tree.heading("source",  text="來源")
        self._cite_tree.column("tag",     width=100, minwidth=60,  stretch=False)
        self._cite_tree.column("citekey", width=370, minwidth=200, stretch=True)
        self._cite_tree.column("source",  width=100, minwidth=80,  stretch=False)
        self._cite_tree.tag_configure("s2",        background="#e8f5e9")
        self._cite_tree.tag_configure("fuzzy",     background="#fff9c4")
        self._cite_tree.tag_configure("unmatched", background="#ffebee")
        self._cite_tree.tag_configure("saved",     background="#ffffff")
        self._cite_tree.bind("<Double-1>", self._cite_double_click)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self._cite_tree.yview)
        self._cite_tree.configure(yscrollcommand=vsb.set)
        self._cite_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Hint label
        ttk.Label(frame, text="雙擊儲存格可編輯", foreground="#888", font=("", 8)
                  ).grid(row=2, column=0, sticky="w", pady=(4, 0))

        # Buttons
        btn_bar = ttk.Frame(frame)
        btn_bar.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        ttk.Button(btn_bar, text="＋ 新增列",      command=self._cite_add).pack(side="left", padx=(0, 4))
        ttk.Button(btn_bar, text="－ 刪除列",      command=self._cite_delete).pack(side="left", padx=(0, 4))
        ttk.Button(btn_bar, text="重新載入",        command=self._load_cite_map).pack(side="left", padx=(0, 12))
        ttk.Button(btn_bar, text="⚡ 從草稿自動產生", command=self._auto_generate).pack(side="left")
        ttk.Button(btn_bar, text="儲存引用表",      command=self._save_cite_map).pack(side="right")

    # ── Tab-change: auto-load editors ────────────────────────────────────────

    def _on_tab_change(self, _event=None):
        tab = self._nb.index(self._nb.select())
        if tab == 1:
            self._load_draft()
        elif tab == 2:
            self._load_cite_map()

    # ── Draft editor actions ──────────────────────────────────────────────────

    def _draft_path(self) -> Path:
        return Path(self._file_vars[0].get())

    def _load_draft(self):
        path = self._draft_path()
        self._draft_path_lbl.config(text=str(path))
        try:
            content = path.read_text(encoding="utf-8")
            self._draft_editor.delete("1.0", "end")
            self._draft_editor.insert("1.0", content)
        except FileNotFoundError:
            messagebox.showerror("找不到檔案", f"{path}")

    def _save_draft(self):
        path = self._draft_path()
        path.write_text(self._draft_editor.get("1.0", "end-1c"), encoding="utf-8")
        messagebox.showinfo("已儲存", f"草稿已儲存：\n{path}")

    # ── Cite map editor actions ───────────────────────────────────────────────

    def _cite_map_path(self) -> Path:
        return Path(self._file_vars[1].get())

    def _load_cite_map(self):
        path = self._cite_map_path()
        self._cite_path_lbl.config(text=str(path))
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self._cite_tree.delete(*self._cite_tree.get_children())
            for num, citekey in data.items():
                self._cite_tree.insert("", "end",
                                       values=(num, citekey, "已存檔"),
                                       tags=("saved",))
        except FileNotFoundError:
            messagebox.showerror("找不到檔案", f"{path}")
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON 格式錯誤", str(e))

    def _save_cite_map(self):
        path = self._cite_map_path()
        data = {
            str(self._cite_tree.item(r)["values"][0]): str(self._cite_tree.item(r)["values"][1])
            for r in self._cite_tree.get_children()
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
        for r in self._cite_tree.get_children():
            vals = list(self._cite_tree.item(r)["values"])
            vals[2] = "已存檔"
            self._cite_tree.item(r, values=vals, tags=("saved",))
        messagebox.showinfo("已儲存", f"引用表已儲存：\n{path}")

    def _auto_generate(self):
        """Parse 文獻對應表 from draft, fuzzy-match to .bib, populate table."""
        draft_path = Path(self._file_vars[0].get())
        bib_path   = Path(self._file_vars[2].get())
        try:
            draft = draft_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            messagebox.showerror("找不到草稿", str(draft_path))
            return

        cite_map = auto_generate_cite_map(draft, bib_path)
        if not cite_map:
            messagebox.showwarning("找不到文獻對應表",
                                   "草稿末尾需有「文獻對應表」區段。\n"
                                   "請確認 NotebookLM 輸出包含：\n"
                                   "文獻對應表 {{1}}: 標題 {{2}}: 標題")
            return

        # Populate tree with colour-coded source
        self._cite_tree.delete(*self._cite_tree.get_children())
        unmatched, s2_count, fuzzy_count = [], 0, 0
        _tag_map = {"S2 API": "s2", "模糊比對": "fuzzy", "未比對": "unmatched"}
        for num, info in sorted(cite_map.items(), key=lambda x: int(x[0])):
            citekey = info["citekey"]
            source  = info["source"]
            row_tag = _tag_map.get(source, "saved")
            self._cite_tree.insert("", "end",
                                   values=(num, citekey, source),
                                   tags=(row_tag,))
            if citekey.startswith("@UNMATCHED"):
                unmatched.append(num)
            elif source == "S2 API":
                s2_count += 1
            else:
                fuzzy_count += 1

        # Summary dialog
        total = len(cite_map)
        ok    = total - len(unmatched)
        msg   = (f"比對完成：{total} 筆\n"
                 f"  ✓ Semantic Scholar API：{s2_count} 筆\n"
                 f"  ~ 模糊比對（需確認）：{fuzzy_count} 筆\n"
                 f"  ✗ 未比對：{len(unmatched)} 筆")
        if unmatched:
            msg += f"\n\n請雙擊 @UNMATCHED_n 的列，手動輸入正確 citekey。"
            messagebox.showwarning("部分未比對", msg)
        else:
            messagebox.showinfo("自動產生完成", msg + "\n\n確認無誤後請點「儲存引用表」。")

    def _cite_add(self):
        iid = self._cite_tree.insert("", "end",
                                     values=("?", "@citekey", "手動"),
                                     tags=("saved",))
        self._cite_tree.selection_set(iid)
        self._cite_tree.see(iid)
        self._open_inline_editor(iid, col_index=0)

    def _cite_delete(self):
        selected = self._cite_tree.selection()
        if not selected:
            messagebox.showinfo("未選取", "請先選取要刪除的列。")
            return
        if messagebox.askyesno("確認刪除", f"刪除選取的 {len(selected)} 筆？"):
            for item in selected:
                self._cite_tree.delete(item)

    def _cite_double_click(self, event):
        iid = self._cite_tree.identify_row(event.y)
        col = self._cite_tree.identify_column(event.x)
        if iid and col:
            col_index = int(col.replace("#", "")) - 1
            if col_index < 2:   # 只允許編輯編號和 citekey，不編輯來源欄
                self._open_inline_editor(iid, col_index)

    def _open_inline_editor(self, iid: str, col_index: int):
        """Floating Entry widget for in-place cell editing."""
        bbox = self._cite_tree.bbox(iid, column=f"#{col_index + 1}")
        if not bbox:
            return
        x, y, w, h = bbox
        current = str(self._cite_tree.item(iid)["values"][col_index])
        var = tk.StringVar(value=current)
        entry = ttk.Entry(self._cite_tree, textvariable=var)
        entry.place(x=x, y=y, width=w, height=h)
        entry.focus()
        entry.select_range(0, "end")

        def _commit(_e=None):
            vals = list(self._cite_tree.item(iid)["values"])
            vals[col_index] = var.get()
            self._cite_tree.item(iid, values=vals)
            entry.destroy()

        entry.bind("<Return>",   _commit)
        entry.bind("<Tab>",      _commit)
        entry.bind("<Escape>",   lambda _e: entry.destroy())
        entry.bind("<FocusOut>", _commit)

    # ── Pipeline (Tab 1) ──────────────────────────────────────────────────────

    def _on_run(self):
        api_key = self._api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("未填 API Key",
                                   f"請輸入 {PROVIDERS[self._provider_var.get()]['key_label']} 後再執行。")
            return
        info = PROVIDERS[self._provider_var.get()]
        config = {
            "provider":      info["id"],
            "api_key":       api_key,
            "model":         self._model_var.get().strip(),
            "draft_path":    self._file_vars[0].get(),
            "cite_map_path": self._file_vars[1].get(),
            "bib_path":      self._file_vars[2].get(),
            "csl_path":      self._file_vars[3].get(),
            "output_dir":    str(OUTPUT_DIR),
        }
        self._run_btn.config(state="disabled")
        self._open_btn.config(state="disabled")
        self._log_append("=== Auto Paper Writer ===\n")
        threading.Thread(target=self._pipeline_thread, args=(config,), daemon=True).start()

    def _pipeline_thread(self, config: dict):
        old_stdout = sys.stdout
        sys.stdout = _QueueWriter(self._log_queue)
        success = False
        try:
            run_pipeline(config)
            success = True
        except SystemExit as e:
            print(str(e))
        except Exception as e:
            print(f"[ERROR] {type(e).__name__}: {e}")
        finally:
            sys.stdout = old_stdout
        self.after(0, self._on_done, success)

    def _on_done(self, success: bool):
        try:
            while True:
                self._log_append(self._log_queue.get_nowait())
        except queue.Empty:
            pass
        self._run_btn.config(state="normal")
        if success:
            self._log_append("\n=== 完成！輸出已儲存至 output/ ===\n")
            self._open_btn.config(state="normal")
        else:
            self._log_append("\n=== 執行失敗，請查看上方錯誤訊息 ===\n")

    # ── Shared helpers ────────────────────────────────────────────────────────

    def _on_provider_change(self, _event=None):
        info = PROVIDERS[self._provider_var.get()]
        self._key_label_var.set(info["key_label"])
        self._model_var.set(DEFAULT_MODELS[info["id"]])
        self._api_key_var.set(os.getenv(info["key_label"], ""))
        self._key_entry.config(show="•")
        self._show_key_btn.config(text="顯示")
        self._show_key = False

    def _toggle_key(self):
        self._show_key = not getattr(self, "_show_key", False)
        self._key_entry.config(show="" if self._show_key else "•")
        self._show_key_btn.config(text="隱藏" if self._show_key else "顯示")

    def _browse(self, var: tk.StringVar, filetypes: list):
        path = filedialog.askopenfilename(filetypes=filetypes, initialdir=str(BASE))
        if path:
            var.set(path)

    def _poll_log(self):
        try:
            while True:
                self._log_append(self._log_queue.get_nowait())
        except queue.Empty:
            pass
        self.after(100, self._poll_log)

    def _log_append(self, text: str):
        self._log.config(state="normal")
        self._log.insert("end", text)
        self._log.see("end")
        self._log.config(state="disabled")

    def _clear_log(self):
        self._log.config(state="normal")
        self._log.delete("1.0", "end")
        self._log.config(state="disabled")

    def _open_output(self):
        subprocess.Popen(f'explorer "{OUTPUT_DIR}"')


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
