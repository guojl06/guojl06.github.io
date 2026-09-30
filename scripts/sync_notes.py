#!/usr/bin/env python3
"""sync_notes.py — 把 sTBook 笔记库同步进网站（wiki 模块数据源）

用法:
  python3 scripts/sync_notes.py [--book PATH] [--site ROOT] [--no-pull]

生成:
  assets/notes/            课程文件镜像 + typst 编译的 PDF + manifest.json + search.json
  _notes/                  Jekyll 页面（/notes/ 总览 + 每门课一页）
"""
import argparse, json, os, shutil, subprocess, sys, urllib.parse

BOOK_URL = "https://github.com/smartThise/sTBook.git"
IGNORE_DIRS = {".git", ".github", ".reasonix", ".vscode", ".claude", "node_modules", "__pycache__", "psyst-lab", "pi-release-exp", "Unable-to-Forget-paper"}
IGNORE_FILES = {".DS_Store", "desktop.ini", "Thumbs.db"}
IGNORE_EXT = {".log", ".out", ".o", ".class"}
PREFIX_JUNK = ("._", "~$", ".~")

TEXT_EXTS = {".md", ".typ", ".txt", ".py", ".cpp", ".c", ".h", ".hpp", ".java", ".js", ".ts",
             ".json", ".yml", ".yaml", ".css", ".html", ".sh", ".bib", ".csv", ".toml", ".xml"}
IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico"}
PREVIEW_PDF = {".pdf"}
CODE_LANG = {".py": "python", ".cpp": "cpp", ".c": "c", ".h": "cpp", ".hpp": "cpp", ".java": "java",
             ".js": "javascript", ".ts": "typescript", ".json": "json", ".yml": "yaml", ".yaml": "yaml",
             ".css": "css", ".html": "html", ".sh": "bash", ".bib": "bib", ".csv": "csv", ".typ": "typst"}


def is_junk(name):
    return name in IGNORE_FILES or name.startswith(PREFIX_JUNK)


def load_wiki(book):
    """解析 wiki.yml（优先 PyYAML，失败则用内置简化解析器）"""
    path = os.path.join(book, "wiki.yml")
    try:
        import yaml
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        return parse_wiki_minimal(path)


def parse_wiki_minimal(path):
    cfg = {"courses": [], "shared_dirs": []}
    cur = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            s = line.split("#", 1)[0].strip()
            if s.startswith("- {") and s.endswith("}"):
                parts = [p.strip() for p in s[3:-1].split(",")]
                item = {}
                for p in parts:
                    k, _, v = p.partition(":")
                    item[k.strip()] = v.strip().strip("'\"")
                cfg["courses"].append(item)
                cur = item
            elif s.startswith("shared_dirs:"):
                cfg["shared_dirs"] = [x.strip() for x in s.split(":", 1)[1].strip("[]").split(",") if x.strip()]
                cur = None
            elif cur is not None and ":" in s and not line.startswith(" ") is False:
                pass
    return cfg


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r


def ensure_book(book, no_pull):
    if os.path.isdir(os.path.join(book, ".git")):
        if not no_pull:
            print("pull sTBook ...")
            sh(["git", "-C", book, "pull", "--ff-only"])
    else:
        print("clone sTBook ...")
        sh(["git", "clone", "--depth", "1", BOOK_URL, book])


def walk_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(PREFIX_JUNK))
        for name in sorted(filenames):
            if is_junk(name) or os.path.splitext(name)[1].lower() in IGNORE_EXT:
                continue
            if os.path.splitext(name)[1].lower() == ".typ" and name.endswith(".typ.pdf"):
                continue
            yield os.path.join(dirpath, name), os.path.relpath(os.path.join(dirpath, name), root)


def build_tree(files):
    """files: [(relpath, size, kind)] -> nested dict"""
    tree = {}
    for rel, size, kind in files:
        node = tree
        parts = rel.split(os.sep)
        for p in parts[:-1]:
            node = node.setdefault("dirs", {}).setdefault(p, {})
        node.setdefault("files", []).append({"n": parts[-1], "s": size, "k": kind})
    return tree


def compile_typst(book, typ_rels, out_base):
    """typst -> pdf（root 固定为仓库根，保证 ../module 等相对引用可用）"""
    fonts = []
    for cand in ("/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/Library/Fonts"),
                 "/Library/Fonts", "/System/Library/Fonts", os.path.join(book, "Assets", "fonts")):
        if os.path.isdir(cand):
            fonts.append(cand)
    ok, fail = 0, 0
    for rel in typ_rels:
        src = os.path.join(book, rel)
        out = os.path.join(out_base, rel + ".pdf")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        cmd = ["typst", "compile", "--root", book]
        for fdir in fonts:
            cmd += ["--font-path", fdir]
        cmd += [src, out]
        try:
            sh(cmd)
            ok += 1
        except RuntimeError as e:
            fail += 1
            print(f"  [typst fail] {rel}: {str(e).splitlines()[-1][:120]}")
    return ok, fail


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.0f}{u}" if u == "B" else f"{n/1:.1f}{u}"
        n /= 1024


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=None, help="sTBook 本地路径（默认 <site>/_notes_src）")
    ap.add_argument("--site", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--no-pull", action="store_true")
    args = ap.parse_args()

    site = args.site
    book = args.book or os.path.join(site, "_notes_src")
    ensure_book(book, args.no_pull)

    cfg = load_wiki(book)
    courses = [c for c in cfg.get("courses", []) if os.path.isdir(os.path.join(book, c["slug"]))]
    shared = [s for s in cfg.get("shared_dirs", []) if os.path.isdir(os.path.join(book, s))]
    missing = [c["slug"] for c in cfg.get("courses", []) if c["slug"] not in {x["slug"] for x in courses}]
    if missing:
        print(f"[warn] wiki.yml 中目录不存在: {missing}")

    out_base = os.path.join(site, "assets", "notes")
    pages_base = os.path.join(site, "_notes")
    for d in (out_base, pages_base):
        shutil.rmtree(d, ignore_errors=True)
    os.makedirs(out_base, exist_ok=True)
    os.makedirs(pages_base, exist_ok=True)

    manifest = {"title": cfg.get("title", "sTBook"), "subtitle": cfg.get("subtitle", ""),
                "courses": [], "shared": []}
    all_typ, all_text = [], []

    def sync_section(slug):
        src_root = os.path.join(book, slug)
        dst_root = os.path.join(out_base, slug)
        files = []
        for absf, rel in walk_files(src_root):
            ext = os.path.splitext(rel)[1].lower()
            rel_norm = rel.replace(os.sep, "/")
            if ext == ".typ":
                kind = "typst"
                all_typ.append(os.path.join(slug, rel))
            elif ext == ".pdf":
                kind = "pdf"
            elif ext in IMG_EXTS:
                kind = "img"
            elif ext == ".html":
                kind = "html"
            elif ext == ".md":
                kind = "md"
            elif ext in TEXT_EXTS:
                kind = "code"
            else:
                kind = "file"
            files.append((rel_norm, os.path.getsize(absf), kind))
            dst = os.path.join(dst_root, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(absf, dst)
            if kind in ("md", "code") and os.path.getsize(absf) < 300_000:
                try:
                    text = open(absf, encoding="utf-8", errors="replace").read()
                    all_text.append({"c": slug, "p": rel_norm, "x": text})
                except OSError:
                    pass
        return files

    for c in courses:
        slug = c["slug"]
        print(f"sync {slug} ...")
        files = sync_section(slug)
        typ_rels = [f[0] for f in files if f[2] == "typst"]
        manifest["courses"].append({
            "slug": slug, "name": c.get("name", slug), "group": c.get("group", ""),
            "desc": c.get("desc", ""), "n": len(files),
            "tree": build_tree((f[0], f[1], f[2]) for f in files),
        })
    for s in shared:
        print(f"sync (shared) {s} ...")
        files = sync_section(s)
        manifest["shared"].append({"slug": s, "name": s, "n": len(files),
                                   "tree": build_tree((f[0], f[1], f[2]) for f in files)})

    print(f"typst 编译 {len(all_typ)} 个文件 ...")
    ok, fail = compile_typst(book, all_typ, out_base)
    print(f"  typst ok={ok} fail={fail}")

    with open(os.path.join(out_base, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(out_base, "search.json"), "w", encoding="utf-8") as f:
        json.dump(all_text, f, ensure_ascii=False, separators=(",", ":"))

    # Jekyll 页面
    fm = "---\nlayout: notes\ntitle: 学习笔记\npermalink: /notes/\nnav: true\nnav_order: 3\ncourse: null\n---\n"
    with open(os.path.join(pages_base, "index.md"), "w", encoding="utf-8") as f:
        f.write(fm)
    for c in courses:
        p = os.path.join(pages_base, c["slug"])
        os.makedirs(p, exist_ok=True)
        with open(os.path.join(p, "index.md"), "w", encoding="utf-8") as f:
            f.write(f"---\nlayout: notes\ntitle: {c.get('name', c['slug'])}\n"
                    f"permalink: /notes/{c['slug']}/\nnav: false\ncourse: {c['slug']}\n---\n")

    nfiles = sum(c["n"] for c in manifest["courses"]) + sum(s["n"] for s in manifest["shared"])
    print(f"done: {len(courses)} 门课程, {nfiles} 个文件, 搜索索引 {len(all_text)} 条")


if __name__ == "__main__":
    sys.exit(main())
