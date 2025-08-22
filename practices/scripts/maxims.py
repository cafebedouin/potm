#!/usr/bin/env python3

#chmod +x scripts/maxims.py
#
# Instructons:
# add a new maxim
# ./scripts/maxims.py add "Hold the slot; don’t fill it." --tags edge,attention --origin "Practice log 2025-08-08"
#
# pick a random
# ./scripts/maxims.py sample
# ./scripts/maxims.py sample --tag permission -n 3
#
# regenerate the Markdown view
# ./scripts/maxims.py export-md


import argparse, json, os, random, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSONL = ROOT / "ledger" / "data" / "maxims.jsonl"
MDOUT = ROOT / "core" / "docs" / "living_maxims.md"

def load_jsonl():
    items=[]
    if JSONL.exists():
        with JSONL.open("r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line: continue
                try: items.append(json.loads(line))
                except json.JSONDecodeError: pass
    return items

def write_jsonl(items):
    JSONL.parent.mkdir(parents=True, exist_ok=True)
    with JSONL.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

def gen_id():
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    rand = f"{random.randint(0,9999):04d}"
    return f"potm.maxim.{ts}-{rand}"

def add_maxim(args):
    items = load_jsonl()
    entry = {
        "id": gen_id(),
        "text": args.text.strip(),
        "tags": [t.strip() for t in (args.tags or "").split(",") if t.strip()],
        "origin": args.origin or "",
        "source": args.source or "practitioner",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "status": "active",
        "weight": int(args.weight or 1),
        "notes": args.notes or ""
    }
    items.append(entry)
    write_jsonl(items)
    print(entry["id"])

def sample(args):
    items = [it for it in load_jsonl() if it.get("status","active")=="active"]
    if args.tag:
        tag=args.tag.strip()
        items=[it for it in items if tag in it.get("tags",[])]
    if not items:
        print("No items match.", file=sys.stderr); sys.exit(1)
    # Weight-aware sampling
    weights=[max(int(it.get("weight",1)),1) for it in items]
    choice=random.choices(items, weights=weights, k=args.n)
    for it in choice:
        print(f"{it['text']}  — #{','.join(it.get('tags',[]))}  [{it['id']}]")

def export_md(args):
    items = [it for it in load_jsonl() if it.get("status","active")=="active"]
    items.sort(key=lambda x: x.get("created",""))
    header = """---
id: potm.guide.general.living_maxims.v1
title: living_maxims
type: guideline
status: experimental
version: 0.1
stability: core
relations:
  relation_to_agent_protocol: none
  supersedes: []
  superseded_by: []
interfaces: []
applicability: [P0]
intensity: gentle
preconditions: []
outputs: [maxim.random]
cadence: []
entry_cues: []
safety_notes: []
tags: [repository, aphorisms, stance_shifting, glitch_gift_inclusive]
author: practitioner + models
license: CC0-1.0
created: 2025-08-02
maintainer: Pal
generated_from: ledger/data/maxims.jsonl
---
# Living Maxims

> This file is auto-generated from `ledger/data/maxims.jsonl`. Edit that file or use `scripts/maxims.py add` to add entries.

"""
    MDOUT.parent.mkdir(parents=True, exist_ok=True)
    with MDOUT.open("w", encoding="utf-8") as f:
        f.write(header)
        for it in items:
            tags = " ".join(f"#{t}" for t in it.get("tags",[]))
            f.write(f"\n## “{it['text']}”\n")
            if tags: f.write(f"- **Tags:** {tags}\n")
            if it.get("origin"): f.write(f"- **Origin:** {it['origin']}\n")
            f.write(f"- **ID:** `{it['id']}`  \n")
    print(f"Wrote {MDOUT}")

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd", required=True)

    ap_add=sub.add_parser("add", help="Add a new maxim")
    ap_add.add_argument("text")
    ap_add.add_argument("--tags")
    ap_add.add_argument("--origin")
    ap_add.add_argument("--source", default="practitioner")
    ap_add.add_argument("--weight", type=int, default=1)
    ap_add.add_argument("--notes")
    ap_add.set_defaults(func=add_maxim)

    ap_s=sub.add_parser("sample", help="Sample maxims")
    ap_s.add_argument("-n", type=int, default=1)
    ap_s.add_argument("--tag")
    ap_s.set_defaults(func=sample)

    ap_x=sub.add_parser("export-md", help="Render Markdown view")
    ap_x.set_defaults(func=export_md)

    args=ap.parse_args()
    args.func(args)

if __name__=="__main__":
    main()
