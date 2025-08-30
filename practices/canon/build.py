#!/usr/bin/env python3
import os
from pathlib import Path

# Define repo order
ROOTS = ["kernel", "extended", "runtime", "interpretative", "meta"]

def gather_files(base):
    files = []
    for root, dirs, filenames in os.walk(base):
        dirs.sort()  # ensure lexical order in subdirectories
        md_files = sorted([f for f in filenames if f.endswith(".md")])
        for f in md_files:
            files.append(Path(root) / f)
    return files

def main():
    repo_root = Path(__file__).parent
    out_file = repo_root / "canon_kernel.md"

    with out_file.open("w", encoding="utf-8") as out:
        for section in ROOTS:
            section_dir = repo_root / section
            if not section_dir.exists():
                continue
            files = gather_files(section_dir)
            for f in files:
                rel_path = f.relative_to(repo_root)
                out.write(f"\n\n<!-- {rel_path} -->\n\n")
                out.write(f.read_text(encoding="utf-8"))
                out.write("\n")

    print(f"[✓] Built canon into {out_file}")

if __name__ == "__main__":
    main()
