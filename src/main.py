"""
Auto Paper Writer — CLI entry point
Pipeline: draft.txt + cite_map.json → LLM rewrite → processed_draft.md → Final_Paper.docx

Citation format (NotebookLM output):
  In-text : {{1}}  {{1, 2}}  {{1, 2, 3}}
  Footnote: 文獻對應表 {{1}}: Title A  {{2}}: Title B

Provider selection (set LLM_PROVIDER env var):
  openai  → OPENAI_API_KEY,    OPENAI_MODEL   (default: gpt-4o)
  claude  → ANTHROPIC_API_KEY, CLAUDE_MODEL   (default: claude-sonnet-4-6)
  gemini  → GEMINI_API_KEY,    GEMINI_MODEL   (default: gemini-2.5-flash)
"""

import difflib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE          = Path(__file__).parent.parent
DRAFT_PATH    = BASE / "data" / "draft.txt"
CITE_MAP_PATH = BASE / "data" / "cite_map.json"
BIB_PATH      = BASE / "data" / "epidermal_cyst.bib"
CSL_PATH      = BASE / "styles" / "journal-of-the-formosan-medical-association.csl"
OUTPUT_DIR    = BASE / "output"
PROCESSED_MD  = OUTPUT_DIR / "processed_draft.md"
FINAL_DOCX    = OUTPUT_DIR / "Final_Paper.docx"

# ── LLM config ─────────────────────────────────────────────────────────────────
DEFAULT_MODELS = {
    "openai": "gpt-4o",
    "claude": "claude-sonnet-4-6",
    "gemini": "gemini-2.5-flash",
}

_KEY_ENVS = {
    "openai": "OPENAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
}

SYSTEM_PROMPT = """\
You are a medical academic writing assistant. Perform the following tasks on the text provided:

1. Translate the Chinese text into formal academic English.
2. Use a professional, third-person, passive-voice style suitable for a medical journal \
(JFMA / Vancouver format).
3. CRITICAL: Preserve ALL citation markers of the form [@citekey] and [@ck1; @ck2] EXACTLY \
as they appear — do NOT remove, reorder, or alter them in any way.
4. Output ONLY the rewritten English text. No preamble, no explanations.\
"""


# ── Citation helpers ───────────────────────────────────────────────────────────

def replace_citation_tags(draft: str, cite_map: dict) -> str:
    """
    Replace {{1}}, {{1, 2, 3}} → [@ck1], [@ck1; @ck2; @ck3]
    cite_map format: {"1": "@citekey", "2": "@citekey2", ...}
    """
    def _replace(m: re.Match) -> str:
        nums = [n.strip() for n in m.group(1).split(",")]
        keys = [cite_map[n] for n in nums if n in cite_map]
        return "[" + "; ".join(keys) + "]" if keys else m.group(0)
    return re.sub(r"\{\{([^}]+)\}\}", _replace, draft)


def strip_reference_table(draft: str) -> str:
    """Remove the dashed separator + 文獻對應表 section from the end of the draft."""
    # Try with separator line first
    cleaned = re.sub(r"\n*-{10,}\n+文獻對應表.*$", "", draft, flags=re.DOTALL)
    if cleaned == draft:
        # Fallback: no separator
        cleaned = re.sub(r"\n*文獻對應表.*$", "", draft, flags=re.DOTALL)
    return cleaned.strip()


def parse_reference_table(text: str) -> dict[str, str]:
    """
    Extract {num: title} from the 文獻對應表 section.
    Input:  '文獻對應表 {{1}}: Title A {{2}}: Title B'
    Output: {'1': 'Title A', '2': 'Title B'}
    """
    m = re.search(r"文獻對應表\s*(.*?)$", text, re.DOTALL)
    if not m:
        return {}
    parts = re.split(r"\{\{(\d+)\}\}\s*:", m.group(1).strip())
    # parts: ['', '1', ' Title A ', '2', ' Title B', ...]
    result = {}
    for i in range(1, len(parts) - 1, 2):
        result[parts[i].strip()] = parts[i + 1].strip()
    return result


def _parse_bib_entries(bib_path: Path) -> list[tuple[str, str, str]]:
    """Return [(citekey, title, doi), ...] from a .bib file."""
    text = bib_path.read_text(encoding="utf-8")
    entries = []
    for entry_m in re.finditer(r"@\w+\{\s*(\w+)\s*,([^@]+)", text, re.DOTALL):
        citekey = entry_m.group(1)
        body    = entry_m.group(2)
        title_m = re.search(r"\btitle\s*=\s*[{\"](.*?)[}\"]", body, re.IGNORECASE | re.DOTALL)
        doi_m   = re.search(r"\bdoi\s*=\s*[{\"](.*?)[}\"]",   body, re.IGNORECASE)
        if title_m:
            title = re.sub(r"[{}\\]|\s+", " ", title_m.group(1)).strip()
            doi   = doi_m.group(1).strip().lower() if doi_m else ""
            entries.append((citekey, title, doi))
    return entries


def _semantic_scholar_lookup(title: str) -> tuple[str | None, str | None]:
    """
    Query Semantic Scholar API by title.
    Returns (doi, matched_title) when confidence ≥ 0.70, else (None, None).
    """
    params = urllib.parse.urlencode({
        "query": title,
        "fields": "title,externalIds",
        "limit": 3,
    })
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "med-paper-writer/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        for candidate in data.get("data", []):
            s2_title = candidate.get("title", "")
            ratio = difflib.SequenceMatcher(
                None, title.lower(), s2_title.lower()
            ).ratio()
            if ratio >= 0.70:
                doi = candidate.get("externalIds", {}).get("DOI")
                return doi, s2_title
    except Exception:
        pass
    return None, None


def auto_generate_cite_map(draft: str, bib_path: Path) -> dict[str, dict]:
    """
    Parse 文獻對應表 from draft, match each title to the .bib file via:
      Tier 0 — Semantic Scholar API + DOI exact match
      Tier 1 — difflib fuzzy title match (fallback)

    Returns:
      {"1": {"citekey": "@key", "source": "S2 API" | "模糊比對" | "未比對"}, ...}
    """
    ref_table = parse_reference_table(draft)
    if not ref_table:
        return {}

    bib        = _parse_bib_entries(bib_path)
    bib_titles = [t.lower() for _, t, _ in bib]
    bib_dois   = {doi: ck for ck, _, doi in bib if doi}

    result: dict[str, dict] = {}
    for num, search_title in ref_table.items():
        citekey = None
        source  = "未比對"

        # Tier 0: Semantic Scholar API → DOI → bib DOI lookup
        doi, _ = _semantic_scholar_lookup(search_title)
        if doi:
            citekey = bib_dois.get(doi.lower())
            if citekey:
                source = "S2 API"

        # Tier 1: difflib fuzzy title match
        if not citekey:
            matches = difflib.get_close_matches(
                search_title.lower(), bib_titles, n=1, cutoff=0.25
            )
            if matches:
                idx     = bib_titles.index(matches[0])
                citekey = bib[idx][0]
                source  = "模糊比對"

        result[num] = {
            "citekey": f"@{citekey}" if citekey else f"@UNMATCHED_{num}",
            "source":  source,
        }
    return result


# ── LLM provider implementations ───────────────────────────────────────────────

def _call_openai(text: str, api_key: str, model: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": text},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()


def _call_claude(text: str, api_key: str, model: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )
    return resp.content[0].text.strip()


def _call_gemini(text: str, api_key: str, model: str) -> str:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=model,
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
        ),
    )
    return resp.text.strip()


_PROVIDERS = {
    "openai": _call_openai,
    "claude": _call_claude,
    "gemini": _call_gemini,
}


# ── Core pipeline (shared by CLI and GUI) ──────────────────────────────────────

def run_pipeline(config: dict):
    """
    config keys:
      provider, api_key, model,
      draft_path, cite_map_path, bib_path, csl_path, output_dir
    """
    provider      = config["provider"]
    api_key       = config["api_key"]
    model         = config["model"]
    draft_path    = Path(config["draft_path"])
    cite_map_path = Path(config["cite_map_path"])
    bib_path      = Path(config["bib_path"])
    csl_path      = Path(config["csl_path"])
    output_dir    = Path(config["output_dir"])
    processed_md  = output_dir / "processed_draft.md"
    final_docx    = output_dir / "Final_Paper.docx"

    if provider not in _PROVIDERS:
        sys.exit(f"[ERROR] Unknown provider '{provider}'. Choose: {', '.join(_PROVIDERS)}")

    print("[1/5] Loading draft and cite map...")
    draft    = draft_path.read_text(encoding="utf-8")
    cite_map = json.loads(cite_map_path.read_text(encoding="utf-8"))
    print(f"      {len(cite_map)} citation mapping(s) found.")

    print("[2/5] Replacing citation tags and stripping reference table...")
    body = strip_reference_table(draft)
    body = replace_citation_tags(body, cite_map)

    print(f"[3/5] Rewriting with LLM ({provider} / {model})...")
    rewritten = _PROVIDERS[provider](body, api_key, model)
    print(f"      Preview: {rewritten[:100]}...")

    print("[4/5] Saving processed Markdown draft...")
    output_dir.mkdir(exist_ok=True)
    yaml_header = "---\ntitle: Auto-generated Paper\n---\n\n"
    processed_md.write_text(yaml_header + rewritten, encoding="utf-8")
    print(f"      Saved → {processed_md}")

    print("[5/5] Running Pandoc...")
    pandoc = _pandoc_exe()
    cmd = [pandoc, str(processed_md), "--citeproc",
           f"--bibliography={bib_path}", f"--csl={csl_path}", "-o", str(final_docx)]
    ref_doc = output_dir.parent / "styles" / "reference.docx"
    if ref_doc.exists():
        cmd += ["--reference-doc", str(ref_doc)]
    print(f"      {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"[ERROR] Pandoc failed:\n{result.stderr}")
    print(f"      Saved → {final_docx}")


# ── Pandoc helper ──────────────────────────────────────────────────────────────

_PANDOC_FALLBACKS = [
    r"C:\Program Files\Pandoc\pandoc.exe",
    r"C:\Program Files (x86)\Pandoc\pandoc.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Pandoc\pandoc.exe"),
]

def _pandoc_exe() -> str:
    try:
        result = subprocess.run(["pandoc", "--version"], capture_output=True)
        if result.returncode == 0:
            return "pandoc"
    except FileNotFoundError:
        pass
    for path in _PANDOC_FALLBACKS:
        if os.path.isfile(path):
            return path
    sys.exit("[ERROR] Pandoc not found. Install from https://pandoc.org/installing.html")


# ── CLI entry point ────────────────────────────────────────────────────────────

def main():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    api_key  = os.getenv(_KEY_ENVS.get(provider, ""), "")
    if not api_key:
        sys.exit(f"[ERROR] {_KEY_ENVS.get(provider, 'API key')} environment variable is not set.")
    model = os.getenv(provider.upper() + "_MODEL", DEFAULT_MODELS.get(provider, ""))

    print("=== Auto Paper Writer ===\n")
    run_pipeline({
        "provider":      provider,
        "api_key":       api_key,
        "model":         model,
        "draft_path":    DRAFT_PATH,
        "cite_map_path": CITE_MAP_PATH,
        "bib_path":      BIB_PATH,
        "csl_path":      CSL_PATH,
        "output_dir":    OUTPUT_DIR,
    })
    print("\n=== Done! ===")
    print(f"Output: {OUTPUT_DIR / 'Final_Paper.docx'}")


if __name__ == "__main__":
    main()
