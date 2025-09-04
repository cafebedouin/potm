#!/usr/bin/env python3
import re
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KERNEL_DIR = ROOT / "kernel"
RUNTIME_DIR = ROOT / "runtime"
SCHEMA_DIR = RUNTIME_DIR / "schema"
SPEC_DIR = RUNTIME_DIR / "spec"
EXAMPLES_DIR = RUNTIME_DIR / "examples"
INDEX_OUT = ROOT / "runtime" / "index" / "wiring.index.json"

ID_PATTERN = re.compile(r"^potm\.[a-z0-9_.]+\.v[0-9]+$")
ID_INLINE_PATTERN = re.compile(r"potm\.[a-z0-9_.]+\.v[0-9]+")

def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to read JSON {path}: {e}")

def read_text(path: Path):
    return path.read_text(encoding="utf-8")

def parse_frontmatter_id(text: str):
    # Very simple YAML-ish frontmatter: between lines starting with --- and ---
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    for i in range(1, min(len(lines), 50)):
        line = lines[i]
        if line.strip() == '---':
            break
        m = re.match(r"\s*(\$?id):\s*(.+?)\s*$", line)
        if m:
            return m.group(2).strip()
    return None

def collect_kernel_refs():
    refs = {}
    for path in sorted(KERNEL_DIR.glob('*.md')):
        # ignore editor backups and composite doc
        if path.name.startswith('#') or path.name.startswith('.#') or path.name.startswith('.') or path.name == 'kernel.md':
            continue
        text = read_text(path)
        kid = parse_frontmatter_id(text)
        inline_ids = set(ID_INLINE_PATTERN.findall(text))
        schema_paths = set(re.findall(r"runtime/schema/[a-zA-Z0-9_./-]+\\.json", text))
        spec_paths = set(re.findall(r"runtime/spec/[a-zA-Z0-9_./-]+\\.json", text))
        example_paths = set(re.findall(r"runtime/examples/[a-zA-Z0-9_./-]+\\.json", text))
        # Exclude the file's own id from referenced ids to avoid false missing links
        if kid in inline_ids:
            inline_ids.discard(kid)
        refs[str(path)] = {
            "kernel_id": kid,
            "referenced_ids": sorted(inline_ids),
            "referenced_schema_paths": sorted(schema_paths),
            "referenced_spec_paths": sorted(spec_paths),
            "referenced_example_paths": sorted(example_paths),
        }
    return refs

def index_repo_ids():
    files_by_id = {}
    errors = []
    all_files = list(SCHEMA_DIR.glob('*.json')) + list(SPEC_DIR.glob('*.json')) + list((SPEC_DIR/"min").glob('*.json'))
    for path in all_files:
        try:
            data = load_json(path)
        except RuntimeError as e:
            errors.append(str(e))
            continue
        # Only index files that declare $id; skip data payloads without $id
        sid = data.get("$id")
        if not sid:
            # If it isn't a schema (no $schema), just skip
            if "$schema" not in data:
                continue
            else:
                errors.append(f"Missing $id in {path}")
                continue
        if not sid.islower():
            errors.append(f"$id must be lowercase: {sid} in {path}")
        if not ID_PATTERN.match(sid):
            errors.append(f"$id does not match pattern potm.<ns>.<name>.v#: {sid} in {path}")
        if sid in files_by_id:
            errors.append(f"Duplicate $id {sid} in {path} and {files_by_id[sid]}")
        else:
            files_by_id[sid] = str(path.relative_to(ROOT))
    return files_by_id, errors

def validate_examples(files_by_id):
    results = []
    errors = []
    try:
        import jsonschema  # type: ignore
    except Exception:
        return results, [
            "jsonschema not installed; skipping example validation. Install with: pip install jsonschema"
        ]

    # Heuristic mapping of example files to schemas by $id
    example_map = {
        'runtime/examples/beacon_event.json': 'potm.kernel.beacon.event.v1',
        'runtime/examples/router_error.example.json': 'potm.kernel.router.error.v1',
        'runtime/examples/latency_breach_ledger.json': 'potm.kernel.ledger.latency_breach.v1',
    }
    for ex_rel, sid in example_map.items():
        ex_path = ROOT / ex_rel
        if not ex_path.exists():
            errors.append(f"Missing example file {ex_rel}")
            continue
        schema_path_rel = files_by_id.get(sid)
        if not schema_path_rel:
            errors.append(f"No schema/spec found for $id {sid} needed by example {ex_rel}")
            continue
        schema_path = ROOT / schema_path_rel
        schema = load_json(schema_path)
        example = load_json(ex_path)
        try:
            jsonschema.validate(instance=example, schema=schema)
            results.append({"example": ex_rel, "schema_id": sid, "schema_path": schema_path_rel, "valid": True})
        except jsonschema.ValidationError as ve:
            errors.append(f"Example {ex_rel} invalid against {sid}: {ve.message}")
        except Exception as e:
            errors.append(f"Failed validating {ex_rel} against {sid}: {e}")
    return results, errors

def main():
    kernel_refs = collect_kernel_refs()
    kernel_ids = {info.get("kernel_id") for info in kernel_refs.values() if info.get("kernel_id")}
    files_by_id, id_errors = index_repo_ids()

    # Cross-reference: ensure kernel referenced ids resolve
    cross_errors = []
    for kfile, info in kernel_refs.items():
        kid = info.get("kernel_id")
        if kid and (not kid.islower() or not ID_PATTERN.match(kid)):
            cross_errors.append(f"Kernel $id invalid in {kfile}: {kid}")
        for sid in info.get("referenced_ids", []):
            if sid in kernel_ids:
                continue
            if sid not in files_by_id:
                cross_errors.append(f"Kernel reference not found: {sid} (from {kfile})")
        for spath in info.get("referenced_schema_paths", []):
            if not (ROOT / spath).exists():
                cross_errors.append(f"Kernel schema path missing: {spath} (from {kfile})")
        for spath in info.get("referenced_spec_paths", []):
            if not (ROOT / spath).exists():
                cross_errors.append(f"Kernel spec path missing: {spath} (from {kfile})")
        for epath in info.get("referenced_example_paths", []):
            if not (ROOT / epath).exists():
                cross_errors.append(f"Kernel example path missing: {epath} (from {kfile})")

    # Validate examples if possible
    example_results, example_errors = validate_examples(files_by_id)

    # Build index
    index = {
        "kernel": kernel_refs,
        "ids": files_by_id,
        "example_validation": example_results,
    }

    # Write index
    INDEX_OUT.parent.mkdir(parents=True, exist_ok=True)
    INDEX_OUT.write_text(json.dumps(index, indent=2, sort_keys=True), encoding="utf-8")

    # Aggregate errors
    errors = id_errors + cross_errors + example_errors
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        sys.exit(1)
    print("Validation OK. Index written to", INDEX_OUT)

if __name__ == "__main__":
    main()
