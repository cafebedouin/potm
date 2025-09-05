#!/usr/bin/env python3
"""
check_lens_wiring.py
Guardrail script for PoTM lenses:
1. Ensure every lens in kernel/30_lenses.md has schema, examples, and catalog entry.
2. Validate each *_invoke.json example against its schema.
"""

import re
import sys
import json
from pathlib import Path

try:
    import jsonschema
except ImportError:
    sys.exit("❌ Missing dependency: install with `pip install jsonschema`")

ROOT = Path(__file__).resolve().parents[1]
KERNEL_FILE = ROOT / "kernel" / "lenses_min.md"
SCHEMA_DIR = ROOT / "extended" / "runtime" / "schema"
EXAMPLES_DIR = ROOT / "extended" / "runtime" / "examples"
CATALOG_FILE = ROOT / "extended" / "runtime" / "spec" / "lens.catalog.v1.json"

LENS_PATTERN = re.compile(r"\b(lens_[a-z0-9_]+)\b")

def load_kernel_lenses():
    text = KERNEL_FILE.read_text(encoding="utf-8")
    ids = set(LENS_PATTERN.findall(text))

    for line in text.splitlines():
        if line.strip().startswith("#"):  # heading
            name = line.strip("# ").lower()
            if any(x in name for x in ["catalog", "contract", "schema", "notes", "tool", "versioning"]):
                continue  # skip meta sections
            if len(name.split()) > 2:
                continue  # too long to be a lens name
            norm = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
            if norm and not norm.startswith("lens_"):
                ids.add(f"lens_{norm}")
    return sorted(ids)

def load_catalog_ids():
    """Load lens IDs from the catalog JSON"""
    data = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    return sorted(set(x.get("id") for x in data.get("lenses", [])))


def check_runtime_files(lens_id):
    """Check schema and example files for a given lens"""
    schema = SCHEMA_DIR / f"{lens_id}.json"
    invoke = EXAMPLES_DIR / f"{lens_id}_invoke.json"
    result = EXAMPLES_DIR / f"{lens_id}_result.json"
    missing = []
    for f in (schema, invoke, result):
        if not f.exists():
            missing.append(str(f.relative_to(ROOT)))
    return schema, invoke, missing


def validate_invoke_against_schema(schema_path: Path, invoke_path: Path):
    """Validate an invoke example against its schema (if both exist)"""
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        data = json.loads(invoke_path.read_text(encoding="utf-8"))
        jsonschema.validate(instance=data, schema=schema)
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    kernel_ids = load_kernel_lenses()
    catalog_ids = load_catalog_ids()

    print(f"🔎 Found {len(kernel_ids)} lens IDs in kernel.")
    missing_any = False
    invalid_any = False

    for lid in kernel_ids:
        schema, invoke, missing_files = check_runtime_files(lid)
        in_catalog = lid in catalog_ids

        if missing_files or not in_catalog:
            missing_any = True
            print(f"\n⚠️  {lid}")
            if missing_files:
                for f in missing_files:
                    print(f"   - Missing file: {f}")
            if not in_catalog:
                print("   - Missing catalog entry")

        # Schema validation only if both files exist
        if schema.exists() and invoke.exists():
            valid, error = validate_invoke_against_schema(schema, invoke)
            if not valid:
                invalid_any = True
                print(f"\n❌ Schema validation failed for {lid}")
                print(f"   Schema: {schema.relative_to(ROOT)}")
                print(f"   Invoke: {invoke.relative_to(ROOT)}")
                print(f"   Error : {error}")

    if not missing_any and not invalid_any:
        print("\n✅ All kernel lenses are fully wired and schema-valid.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

    
