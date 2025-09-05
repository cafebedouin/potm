#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()

    #!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse, hashlib, re, textwrap, sys, os, json, yaml
from pathlib import Path

# ---------------- Helpers ---------------- #

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def extract_id(text: str, suffix: str):
    """Extract id from Markdown front-matter, JSON, or YAML files."""
    if suffix == ".md":
        m = FRONTMATTER_RE.match(text)
        if not m:
            return None
        block = m.group(1)
        id_m = ID_LINE_RE.search(block)
        return id_m.group(1).strip() if id_m else None

    if suffix == ".json":
        try:
            data = json.loads(text)
            return data.get("id")
        except Exception:
            return None

    if suffix in (".yaml", ".yml"):
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data.get("id")
        except Exception:
            return None

    return None

def ensure_id_header(md_text: str, doc_id: str):
    """Inject anchor and H1 header if not present."""
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        return f'<a id="{doc_id}"></a>\n' + md_text
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

def gather_files(base: Path):
    exts = (".md", ".json", ".yaml", ".yml")
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(exts):
                yield Path(root) / name

def process_content(path: Path, doc_id):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        return ensure_id_header(text, doc_id) if doc_id else text
    if path.suffix == ".json":
        return f'<a id="{doc_id}"></a>\n```json\n{text}\n```\n'
    if path.suffix in (".yaml", ".yml"):
        return f'<a id="{doc_id}"></a>\n```yaml\n{text}\n```\n'
    return f'<a id="{doc_id}"></a>\n{text}\n'

# ---------------- Runtime Collectors ---------------- #

def collect_runtime_dir(repo_root: Path, rel_dir: str, prefix: str, category: str):
    runtime_dir = repo_root / rel_dir
    if not runtime_dir.exists():
        return []
    records = []
    for f in gather_files(runtime_dir):
        text = f.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, f.suffix)
        if not file_id:
            stem = f.stem.replace(".", "_").replace("-", "_")
            file_id = f"{prefix}.{stem}.v1"
        content = process_content(f, file_id)
        records.append({
            "category": category,
            "id": file_id,
            "title": None,
            "path": f.relative_to(repo_root).as_posix(),
            "hash": h,
            "content": content
        })
    return records

# ---------------- Manifest ---------------- #

def parse_manifest(manifest_path: Path):
    rows = []
    with manifest_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("| order"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.strip("| \n").split("|")]
                if len(parts) < 4:
                    continue
                order, category, path, doc_id = parts[:4]
                notes = parts[4] if len(parts) > 4 else ""
                rows.append({
                    "order": int(order),
                    "category": category,
                    "path": path,
                    "id": doc_id if doc_id else None,
                    "notes": notes
                })
    return sorted(rows, key=lambda r: r["order"])

# ---------------- Build ---------------- #

def build_text(records, mode, repo_root: Path, runtime_records, runtime_ext_records):
    buf = []
    buf.append(textwrap.dedent(f"""\
    ---
    id: potm.build.{mode}
    title: build_{mode}
    display_title: "PoTM Build ({mode})"
    type: build
    version: 1.0
    status: active
    stability: draft
    author: practitioner
    license: CC0-1.0
    ---\n
    """))

    all_records = records + runtime_records + runtime_ext_records
    buf.append("# PACKAGE_INDEX\n\n")
    buf.append("| id | category | path | hash |\n|----|----------|------|------|\n")
    for r in all_records:
        buf.append(f"| {r['id'] or ''} | {r['category']} | `{r['path']}` | {r['hash']} |\n")
    buf.append("\n---\n")

    def section(title, recs):
        if recs:
            buf.append(f"\n\n## {title}\n")
            for r in recs:
                buf.append(f"\n<!-- {r['path']} -->\n")
                if r["id"]:
                    buf.append(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n")
                buf.append(r["content"] + "\n")

    section("Kernel", [r for r in records if r["category"] == "kernel"])
    section("Runtime", runtime_records)
    section("Extended", [r for r in records if r["category"] == "extended"])
    section("Extended Runtime", runtime_ext_records)
    section("Interpretative", [r for r in records if r["category"] == "interpretative"])
    return "".join(buf)

# ---------------- Split ---------------- #

def split_into_parts(text, out_prefix, max_bytes, mode, counts):
    paras = text.split("\n\n")
    parts, current = [], ""
    for p in paras:
        if len((current+p).encode("utf-8")) > max_bytes and current:
            parts.append(current)
            current = ""
        current += p + "\n\n"
    if current.strip():
        parts.append(current)

    total = len(parts)
    total_bytes = 0
    for idx, body in enumerate(parts, 1):
        header = f"# PoTM Build ({mode}) — Part {idx} of {total}\n\n"
        out_file = f"{out_prefix}_part{idx:02d}.md"
        Path(out_file).write_text(header + body, encoding="utf-8")
        size = len((header+body).encode("utf-8"))
        total_bytes += size
        print(f"[✓] Wrote {out_file} ({size} bytes)")

    print("\n--- Build Summary ---")
    print(f"Mode: {mode}")
    print("Files included:")
    for cat, num in counts.items():
        print(f"  {cat.capitalize()}: {num}")
    print(f"Total files: {sum(counts.values())}")
    print(f"Total parts: {total}")
    print(f"Total size: {total_bytes:,} bytes")

# ---------------- Main ---------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", action="store_true")
    ap.add_argument("--extended", action="store_true")
    ap.add_argument("--interpretative", action="store_true")
    ap.add_argument("--docs", action="store_true")
    ap.add_argument("-o", "--output", default="docs/canon_build")
    ap.add_argument("--max-bytes", type=int, default=1000000)
    ap.add_argument("--manifest", default="docs/build_manifest.md")
    args = ap.parse_args()

    repo_root = Path(__file__).parent
    manifest = parse_manifest(repo_root / args.manifest)

    if args.kernel:
        cats, mode = ["kernel"], "kernel"
    elif args.extended:
        cats, mode = ["kernel","extended"], "extended"
    elif args.interpretative:
        cats, mode = ["kernel","extended","interpretative"], "interpretative"
    elif args.docs:
        cats, mode = ["interpretative"], "docs"
    else:
        ap.error("Pick one of --kernel / --extended / --interpretative / --docs")

    records = []
    for r in manifest:
        if r["category"] not in cats:
            continue
        fpath = repo_root / r["path"]
        if not fpath.exists():
            sys.exit(f"[ERROR] Manifest file not found: {r['path']}")
        text = fpath.read_text(encoding="utf-8")
        h = short_hash(text)
        file_id = extract_id(text, fpath.suffix)

        if r["id"]:
            if not file_id:
                sys.exit(f"[ERROR] Manifest expects id '{r['id']}' but {r['path']} has none")
            if file_id != r["id"]:
                sys.exit(f"[ERROR] ID mismatch for {r['path']}: manifest '{r['id']}' vs file '{file_id}'")
        elif file_id:
            sys.exit(f"[ERROR] File {r['path']} declares id '{file_id}' but manifest leaves it blank")

        content = process_content(fpath, r["id"] or file_id)
        records.append({
            "category": r["category"],
            "id": r["id"] or file_id,
            "title": None,
            "path": r["path"],
            "hash": h,
            "content": content
        })

    runtime_records = collect_runtime_dir(repo_root, "runtime", "potm.runtime", "runtime")
    runtime_ext_records = []
    if mode in ("extended", "interpretative"):
        runtime_ext_records = collect_runtime_dir(repo_root, "extended/runtime", "potm.runtime_ext", "runtime_ext")

    text = build_text(records, mode, repo_root, runtime_records, runtime_ext_records)

    counts = {
        "kernel": sum(1 for r in records if r["category"] == "kernel"),
        "runtime": len(runtime_records),
        "extended": sum(1 for r in records if r["category"] == "extended"),
        "runtime_ext": len(runtime_ext_records),
        "interpretative": sum(1 for r in records if r["category"] == "interpretative"),
    }

    split_into_parts(text, args.output, args.max_bytes, mode, counts)

if __name__ == "__main__":
    main()
