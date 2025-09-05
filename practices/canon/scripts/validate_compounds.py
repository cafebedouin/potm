#!/usr/bin/env python3
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "extended" / "lenses" / "catalog.v1.json"
COMPOUND_DIR = ROOT / "extended" / "lenses" / "compounds"

def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to read JSON {path}: {e}")

def main():
    errors = []

    # 1. Load catalog and collect compounds[]
    try:
        catalog = load_json(CATALOG)
    except Exception as e:
        sys.exit(f"[ERROR] Cannot load catalog: {e}")

    compounds = catalog.get("compounds", [])
    if not compounds:
        sys.exit("[ERROR] No compounds[] found in catalog.v1.json")

    # 2. Validate each compound entry
    for entry in compounds:
        cid = entry.get("id")
        manifest_path = ROOT / entry.get("manifest", "")
        if not manifest_path.exists():
            errors.append(f"{cid}: manifest missing at {manifest_path}")
            continue

        try:
            manifest = load_json(manifest_path)
        except Exception as e:
            errors.append(f"{cid}: cannot parse manifest {manifest_path} → {e}")
            continue

        # check id consistency
        mid = manifest.get("$id") or manifest.get("id")
        if not mid:
            errors.append(f"{cid}: manifest has no $id/id field")
        elif cid not in mid:
            errors.append(f"{cid}: catalog id does not match manifest id ($id={mid})")

        # check version presence
        if "version" not in manifest:
            errors.append(f"{cid}: manifest missing version")

        # optional: sanity check schemas section if present
        if "schemas" in manifest and not isinstance(manifest["schemas"], list):
            errors.append(f"{cid}: manifest.schemas must be a list")

    # 3. Report
    if errors:
        print("[FAIL] Compound validation errors:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print(f"[OK] {len(compounds)} compounds validated successfully.")

if __name__ == "__main__":
    main()
