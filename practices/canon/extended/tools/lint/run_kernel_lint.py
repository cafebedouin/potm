#!/usr/bin/env python3
"""
PoTM kernel linter (cross-platform)
- Reads a JSON or YAML config of rules
- Lints Markdown files under kernel/
Usage:
  python extended/lint/run_kernel_lint.py --config extended/lint/kernel_formatting.yaml
"""
#!/usr/bin/env python3
"""
PoTM kernel linter (cross-platform)
- Reads a JSON or YAML config of rules
- Lints Markdown files under kernel/
Usage:
  python extended/lint/run_kernel_lint.py --config extended/lint/potm.kernel.formatting.yaml
"""
import argparse
import os
import re
import sys
from fnmatch import fnmatch

def load_config(path):
    text = open(path, "r", encoding="utf-8").read()
    if path.endswith((".yaml", ".yml")):
        try:
            from strictyaml import load
            return load(text).data
        except Exception as e:
            print("[lint] Failed to parse YAML config with StrictYAML.")
            print(e)
            sys.exit(2)
    else:
        import json
        return json.loads(text)

def read_file(path):
    return open(path, "r", encoding="utf-8").read()

# -- Handlers for each rule type -------------------------------------------

def handle_required_front_matter(md, rule):
    keys = rule.get("require_keys", [])
    if not md.lstrip().startswith("---"):
        print("  - front matter: missing leading '---'")
        return False
    end = md.find("\n---", 3)
    if end == -1:
        print("  - front matter: missing trailing '---'")
        return False
    fm = md[3:end].strip().splitlines()
    present = {line.split(":",1)[0].strip() for line in fm if ":" in line}
    missing = [k for k in keys if k not in present]
    if missing:
        print(f"  - front matter: missing keys {missing}")
        return False
    return True

def handle_no_duplicate_headings(md, rule):
    pattern = re.compile(rule.get("pattern"))
    seen = set()
    ok = True
    for i, line in enumerate(md.splitlines()):
        m = pattern.match(line)
        if m:
            heading = m.group(1).strip()
            if heading in seen:
                print(f"  - headings: duplicate '{heading}' at line {i+1}")
                ok = False
            else:
                seen.add(heading)
    return ok

def handle_blank_lines_around_blocks(md, rule):
    checks = rule.get("checks", {})
    ok = True
    lines = md.splitlines()

    def report(i, what):
        nonlocal ok
        print(f"  - spacing: line {i+1}: {what}")
        ok = False

    for i, line in enumerate(lines):
        # Heading
        if checks.get("before_heading") and re.match(r"^#{2,}\s", line):
            if i > 0 and lines[i-1].strip():
                report(i, "missing blank line before heading")
        if checks.get("after_heading") and re.match(r"^#{2,}\s", line):
            if i+1 < len(lines) and lines[i+1].strip():
                report(i, "missing blank line after heading")

        # Code fences
        if re.match(r"^```", line):
            if checks.get("before_code_block") and i>0 and lines[i-1].strip():
                report(i, "missing blank line before code block")
            # find end
            for j in range(i+1, len(lines)):
                if re.match(r"^```", lines[j]):
                    if checks.get("after_code_block") and j+1<len(lines) and lines[j+1].strip():
                        report(j, "missing blank line after code block")
                    break

        # Tables
        if re.match(r"^\|.*\|$", line) and not re.match(r"^\|[-: ]+\|$", line):
            # before
            if checks.get("before_table") and i>0 and lines[i-1].strip() and not lines[i-1].startswith("|"):
                report(i, "missing blank line before table")
            # after
            if checks.get("after_table") and i+1<len(lines) and lines[i+1].strip() and not lines[i+1].startswith("|"):
                report(i, "missing blank line after table")

    return ok

def handle_code_block_language_required(md, rule):
    unlabeled = re.compile(rule.get("pattern_unlabeled_fence", r"^```\s*$"))
    ok = True
    for i, line in enumerate(md.splitlines()):
        if unlabeled.match(line):
            print(f"  - code: line {i+1}: {rule.get('message')}")
            ok = False
    return ok

def handle_forbid_allcaps_tool_ids(md, rule):
    pat = re.compile(rule.get("pattern"))
    ok = True
    for m in pat.finditer(md):
        print(f"  - ids: {rule.get('message')} at char {m.start()}")
        ok = False
    return ok

def handle_namespaced_ids_snake_case(md, rule):
    allow = re.compile(rule.get("allow_pattern"))
    pat = re.compile(r"\b([a-z0-9_]+\.[a-z0-9_]+)\b")
    ok = True
    for m in pat.finditer(md):
        token = m.group(1)
        if not allow.search(token):
            print(f"  - tokens: {rule.get('message')} `{token}`")
            ok = False
    return ok

def handle_emissions_allowlist(md, rule):
    dis = re.compile(rule.get("disallow_pattern"))
    ok = True
    for m in dis.finditer(md):
        token = m.group(0)
        print(f"  - emissions: {rule.get('message')} `{token}`")
        ok = False
    return ok

def handle_catalog_columns(md, rule):
    expect = rule.get("header_columns_exact", [])
    # build a tight regex for the header row
    cols = r"\|\s*" + r"\s*\|\s*".join(re.escape(c) for c in expect) + r"\s*\|"
    if not re.search(f"^{cols}$", md, flags=re.M):
        print("  - table: required header row not found or wrong order")
        return False
    return True

def handle_output_artifact_word_limit(md, rule):
    colname = rule.get("column").lower()
    maxw = rule.get("max_words")
    lines = md.splitlines()
    header_idx = None
    headers = []
    for i, l in enumerate(lines):
        if l.startswith("|"):
            cells = [c.strip().lower() for c in l.strip("|").split("|")]
            if colname in cells:
                header_idx, headers = i, cells
                break
    if header_idx is None:
        return True
    col = headers.index(colname)
    ok = True
    for i in range(header_idx+2, len(lines)):
        row = lines[i]
        if not row.startswith("|"):
            break
        cells = [c.strip() for c in row.strip("|").split("|")]
        if col < len(cells):
            words = re.findall(r"\b\w+\b", cells[col])
            if len(words) > maxw:
                print(f"  - output limit: line {i+1}: ... has {len(words)} words (> {maxw})")
                ok = False
    return ok

def handle_entry_tokens_literal(md, rule):
    ok = True
    for pat in rule.get("require_patterns", []):
        if pat not in md:
            print(f"  - entry/exit tokens: missing `{pat}`")
            ok = False
    return ok

# Mapping from rule name to handler function
HANDLERS = {
    "required_front_matter":       handle_required_front_matter,
    "no_duplicate_headings":       handle_no_duplicate_headings,
    "blank_lines_around_blocks":   handle_blank_lines_around_blocks,
    "code_block_language_required":handle_code_block_language_required,
    "forbid_allcaps_tool_ids":     handle_forbid_allcaps_tool_ids,
    "namespaced_ids_snake_case":   handle_namespaced_ids_snake_case,
    "emissions_allowlist":         handle_emissions_allowlist,
    "lenses_catalog_columns":      handle_catalog_columns,
    "micromoves_catalog_columns":  handle_catalog_columns,
    "beacons_catalog_columns":     handle_catalog_columns,
    "output_artifact_word_limit":  handle_output_artifact_word_limit,
    "entry_tokens_literal":        handle_entry_tokens_literal,
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_config(args.config)
    root = os.getcwd()
    failures = 0

    # Collect all .md under kernel/
    md_files = []
    for base, _, files in os.walk(os.path.join(root, "kernel")):
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(base, f))

    for path in sorted(md_files):
        rel = os.path.relpath(path, root)
        md = read_file(path)
        print(f"[lint] {rel}")
        file_ok = True

        # Apply each rule whose patterns match this file
        for rule in cfg.get("lint", []):
            for pat in rule.get("files", []):
                if fnmatch(rel, pat):
                    handler = HANDLERS.get(rule["rule"])
                    if handler:
                        ok = handler(md, rule)
                        if not ok:
                            file_ok = False
                    else:
                        # unknown rule → skip or warn
                        print(f"  - warning: no handler for rule '{rule['rule']}'")
                    break  # only run once per rule

        if not file_ok:
            failures += 1

    if failures:
        print(f"\n[lint] FAIL: {failures} file(s) have issues.")
        sys.exit(1)
    else:
        print("\n[lint] PASS: all checks ok.")

if __name__ == "__main__":
    main()

