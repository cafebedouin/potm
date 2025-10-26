#!/usr/bin/env python3
# WSL-safe front-matter upgrader to PoTM schema v0.1
import argparse, pathlib, re, sys, uuid
from datetime import date
try:
    import yaml
except ImportError:
    print("This script requires PyYAML. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

SCHEMA_VERSION = "0.1"
TODAY = date.today().isoformat()

# Infer fields from path
def infer_fields(path: pathlib.Path):
    p = str(path).replace("\\", "/")
    # type
    if "/core/practices/protocols/" in p:
        ftype = "agent_protocol"
    elif "/core/diagnostics/" in p:
        ftype = "diagnostic"
    elif "/docs/protocols/" in p:
        ftype = "practitioner_protocol"
    else:
        ftype = "guideline"
    # stability mirrors channel
    stability = "core" if p.startswith("core/") else "experimental" if p.startswith("experimental/") else "core"
    # title/id defaults
    title = path.stem
    # namespace
    fam = title.lower().replace("-", "_")
    ns_type = {
        "agent_protocol":"proto",
        "practitioner_protocol":"pract",
        "diagnostic":"diag",
        "guideline":"guide",
    }[ftype]
    # crude family bucket
    if "kernel" in p or "microkernel" in p:
        family = "kernel"
    elif "mirror" in p:
        family = "mirror"
    elif "guardian" in p:
        family = "guardian"
    else:
        family = "general"
    id_ = f"potm.{ns_type}.{family}.{fam}.v1"
    return {
        "type": ftype,
        "stability": stability,
        "title": title,
        "id": id_,
    }

# Default scaffold per schema v0.1
def default_schema(path: pathlib.Path):
    inf = infer_fields(path)
    return {
        "id": inf["id"],
        "title": inf["title"],
        # humans can add display_title later; we don't force it
        "type": inf["type"],
        "status": "stable",
        "version": "1.0",
        "stability": inf["stability"],
        "relations": {
            "relation_to_agent_protocol": "none",
            # optional pointers; leave absent if unknown
            # "agent_protocol": "",
            # "practitioner_doc": "",
            "supersedes": [],
            "superseded_by": [],
        },
        "interfaces": [],
        "applicability": ["P0"],
        "intensity": "gentle",
        "preconditions": [],
        "outputs": [],
        "cadence": [],
        "entry_cues": [],
        "safety_notes": [],
        "tags": [],
        "author": "Sean + models",
        "license": "CC0-1.0",
    }

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)

def load_front_matter(text):
    m = FM_RE.match(text)
    if not m:
        return None, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        print(f"[WARN] YAML parse error: {e}")
        fm = {}
    body = text[m.end():]
    return fm, body

def dump_front_matter(fm):
    return "---\n" + yaml.safe_dump(fm, sort_keys=False).strip() + "\n---\n"

def merge_schema(existing: dict, path: pathlib.Path):
    base = default_schema(path)
    # Shallow merge; nested 'relations' needs care
    merged = {**base, **(existing or {})}
    rel = base["relations"].copy()
    rel.update((existing or {}).get("relations", {}))
    merged["relations"] = rel
    # Normalize some fields to lists
    for k in ("interfaces","applicability","preconditions","outputs","cadence","entry_cues","safety_notes","tags",
              "relations","relations.supersedes","relations.superseded_by"):
        pass  # minimal normalization; avoid being too opinionated
    return merged

def process_file(path: pathlib.Path, write: bool, verbose: bool):
    text = path.read_text(encoding="utf-8")
    fm, body = load_front_matter(text)
    merged = merge_schema(fm or {}, path)
    # Respect existing keys over defaults
    for k, v in (fm or {}).items():
        if k == "relations" and isinstance(v, dict):
            merged["relations"].update(v)
        else:
            merged[k] = v
    # Small niceties
    if "display_title" not in merged and merged["type"] == "practitioner_protocol":
        merged["display_title"] = merged["title"].replace("_"," ").title()
    new_text = dump_front_matter(merged) + body
    changed = (text != new_text)
    if verbose:
        print(f"{'CHANGED' if changed else 'OK     '}: {path}")
    if write and changed:
        path.write_text(new_text, encoding="utf-8")
    return changed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("globs", nargs="+", help="File globs, e.g., core/**/*.md docs/**/*.md")
    ap.add_argument("--write", action="store_true", help="Write changes (default is dry-run)")
    ap.add_argument("--verbose", action="store_true", help="Verbose output")
    args = ap.parse_args()

    files = []
    for g in args.globs:
        files.extend(pathlib.Path().glob(g))
    files = [p for p in files if p.is_file() and p.suffix.lower()==".md"]

    if not files:
        print("No files matched.")
        return

    changed = 0
    for p in files:
        changed += 1 if process_file(p, write=args.write, verbose=args.verbose) else 0

    print(f"Total files: {len(files)} | Changed: {changed} | Mode: {'WRITE' if args.write else 'DRY-RUN'}")

if __name__ == "__main__":
    main()
