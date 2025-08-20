import sys, json, yaml
from jsonschema import validate, Draft202012Validator

spec_path = sys.argv[1] if len(sys.argv) > 1 else "../kernel/30_lenses_p1lean.yaml"
schema_path = sys.argv[2] if len(sys.argv) > 2 else "../kernel/30_lenses_p1.min.json"

with open(spec_path, "r", encoding="utf-8") as f:
    spec = yaml.safe_load(f)
with open(schema_path, "r", encoding="utf-8") as f:
    schema = json.load(f)

validator = Draft202012Validator(schema)
errors = sorted(validator.iter_errors(spec), key=lambda e: e.path)
if errors:
    for e in errors:
        loc = " → ".join(str(p) for p in e.path)
        print(f"[FAIL] {loc}: {e.message}")
    sys.exit(1)
else:
    validate(spec, schema)
    # light chain target sanity
    ids = {l["id"] for l in spec["lenses"]}
    for l in spec["lenses"]:
        for tgt in l["chains"]["next"]:
            if tgt not in ids:
                print(f"[WARN] {l['id']} chains to undefined lens '{tgt}'")
    print("[OK] lenses_p1lean passes schema (and chain sanity).")
