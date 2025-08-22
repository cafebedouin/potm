#!/usr/bin/env python3
import os, sys, re, json, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Please `pip install pyyaml`.\n"); sys.exit(1)

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
INCLUDE = ("*.md",)
EXCLUDE_DIRS = {"validation", "deprecated", ".git", ".venv", "node_modules"}

def read_front_matter(p: Path):
    txt = p.read_text(encoding="utf-8", errors="ignore")
    if not txt.startswith("---"): return None
    m = re.match(r"^---\n(.*?)\n---\n", txt, flags=re.S)
    if not m: return None
    try:
        return yaml.safe_load(m.group(1))
    except Exception:
        return None

def wants(path: Path):
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS: return False
    return path.suffix == ".md"

def get(d, key, default=""):
    return d.get(key, default) if isinstance(d, dict) else default

items = []
for p in ROOT.rglob("*.md"):
    if not wants(p): continue
    fm = read_front_matter(p)
    if not fm: continue
    tags = get(fm, "tags", [])
    # Normalize tags to key:value map if given as flat list
    tag_map = {}
    if isinstance(tags, dict):
        tag_map = tags
    elif isinstance(tags, list):
        for t in tags:
            if isinstance(t, str) and ":" in t:
                k,v = t.split(":",1)
                tag_map[k.strip()] = v.strip()

    items.append({
        "path": str(p),
        "id": get(fm, "id"),
        "title": get(fm, "display_title", get(fm, "title")),
        "type": get(fm, "type"),
        "status": get(fm, "status"),
        "version": get(fm, "version"),
        "tags": {
            "forge_origin": tag_map.get("forge_origin",""),
            "spiral_eval": tag_map.get("spiral_eval",""),
        }
    })

doc = {
  "version": "0.1",
  "generated_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
  "scope": {"root": str(ROOT), "include": ["**/*.md"], "exclude": ["validation/**","deprecated/**"]},
  "fields": {"required": ["path","id","title","type","status","version","tags"],
             "tag_keys": {"forge_origin": True, "spiral_eval": True}},
  "items": sorted(items, key=lambda x: x["path"])
}

out = ROOT / "meta" / "lineage_index.yaml"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
print(f"Wrote {out}")
