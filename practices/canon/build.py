#!/usr/bin/env python3
import os, re, hashlib
from pathlib import Path

# Repo order
ROOTS = ["kernel", "extended", "runtime", "interpretative", "meta"]

# --- Helpers --------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)
ID_LINE_RE     = re.compile(r"^\s*id\s*:\s*(.+?)\s*$", re.MULTILINE)
TITLE_LINE_RE  = re.compile(r"^\s*title\s*:\s*(.+?)\s*$", re.MULTILINE)

def gather_files(base: Path):
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for name in sorted(f for f in files if f.endswith(".md")):
            yield Path(root) / name

def extract_id_and_title(md_text: str):
    """
    Very lightweight front-matter read (no deps).
    Returns (id_value_or_None, title_or_None)
    """
    m = FRONTMATTER_RE.match(md_text)
    if not m:
        return (None, None)
    block = m.group(1)
    id_m = ID_LINE_RE.search(block)
    title_m = TITLE_LINE_RE.search(block)
    doc_id = id_m.group(1).strip() if id_m else None
    title  = title_m.group(1).strip() if title_m else None
    # strip surrounding quotes if present
    if doc_id and ((doc_id[0] == doc_id[-1]) and doc_id[0] in ("'", '"')):
        doc_id = doc_id[1:-1]
    if title and ((title[0] == title[-1]) and title[0] in ("'", '"')):
        title = title[1:-1]
    return (doc_id, title)

def short_hash(text: str, n=8):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]

def ensure_id_header(md_text: str, doc_id: str):
    """
    If the file doesn't already start with a header '# <doc_id>' (or a heading that exactly equals the id),
    prepend a visible H1 header and a hidden anchor.
    We only look at the first ~300 chars to decide.
    """
    head = md_text[:300]
    already = re.search(rf"^#\s*{re.escape(doc_id)}\s*$", head, re.MULTILINE)
    if already:
        # still inject an anchor just above the existing heading for robust linking
        return f'<a id="{doc_id}"></a>\n' + md_text
    # Prepend anchor + H1 id header
    return f'<a id="{doc_id}"></a>\n# {doc_id}\n\n' + md_text

# --- Build ---------------------------------------------------------------

def main():
    repo_root = Path(__file__).parent
    out_file = repo_root / "canon_kernel.md"

    records = []  # [{id, title, path, hash, content}]
    for section in ROOTS:
        section_dir = repo_root / section
        if not section_dir.exists():
            continue
        for f in gather_files(section_dir):
            rel_path = f.relative_to(repo_root).as_posix()
            text = f.read_text(encoding="utf-8")
            doc_id, title = extract_id_and_title(text)
            h = short_hash(text)
            records.append({
                "id": doc_id,
                "title": title,
                "path": rel_path,
                "hash": h,
                "content": text,
            })

    with out_file.open("w", encoding="utf-8") as out:
        # PACKAGE INDEX (top of file)
        out.write("# PACKAGE_INDEX (merged_single_file)\n\n")
        out.write("- resolver_order: by_id_then_anchor_then_path\n")
        out.write("- includes:\n")
        for r in records:
            if r["id"]:
                title = f'  title: "{r["title"]}"' if r["title"] else ""
                out.write(f"  - id: {r['id']}  # {r['hash']}  [{r['path']}] {title}\n")
            else:
                out.write(f"  - path_only: [{r['path']}]  # {r['hash']}\n")
        out.write("\n---\n")

        # Optional: one-time resolver rules (models will see this early)
        out.write("### RESOLVER_RULES\n")
        out.write("1. Resolve by **ID** if present in this file (anchor `<a id=\"ID\">`).\n")
        out.write("2. If ID anchor not found, resolve by heading `# ID`.\n")
        out.write("3. Else, resolve by repository path noted in PACKAGE_INDEX.\n")
        out.write("4. If all fail, **fail-closed** to Minimal Menu Fallback.\n\n")
        out.write("---\n")

        # Body: concatenate files in repo order with anchors/headers
        for r in records:
            out.write(f"\n\n<!-- {r['path']} -->\n\n")
            content = r["content"]
            if r["id"]:
                content = ensure_id_header(content, r["id"])
                # Also echo a machine-readable comment for audits
                out.write(f"<!-- PKG_ID: {r['id']} HASH: {r['hash']} -->\n\n")
            out.write(content)
            out.write("\n")

    print(f"[✓] Built canon into {out_file}")

if __name__ == "__main__":
    main()
