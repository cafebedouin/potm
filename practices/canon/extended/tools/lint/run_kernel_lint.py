#!/usr/bin/env python3
"""
PoTM kernel linter (cross-platform)
- Reads a JSON or YAML config of rules
- Lints Markdown files under kernel/
Usage:
  python extended/lint/run_kernel_lint.py --config extended/lint/kernel_formatting.yaml
"""
import argparse, json, os, re, sys

def load_config(path):
    text = open(path, "r", encoding="utf-8").read()
    if path.endswith((".yaml", ".yml")):
        try:
            from strictyaml import load
            return load(text).data
        except Exception as e:
            print("[lint] Failed to parse YAML config with StrictYAML. "
                  "Check for flow-style lists ([...]) or unquoted patterns.")
            print(e)
            sys.exit(2)
    else:
        import json
        return json.loads(text)

def read_file(path):
    return open(path, "r", encoding="utf-8").read()

def front_matter_ok(md, require_keys):
    # naive YAML front matter: starts with --- then key: lines then ---
    if not md.lstrip().startswith("---"):
        return False
    end = md.find("\n---", 3)
    if end == -1: return False
    fm = md[3:end].strip()
    keys_present = {line.split(":")[0].strip() for line in fm.splitlines() if ":" in line}
    return all(k in keys_present for k in require_keys)

def has_blank_line_around_blocks(md):
    ok = True
    lines = md.splitlines()
    def bad(idx, reason):
        nonlocal ok
        print(f"  - spacing: line {idx+1}: {reason}")
        ok = False
    # check headings/code fences/tables have blank lines before & after
    for i, line in enumerate(lines):
        # headings (## or ###)
        if re.match(r"^#{2,3}\s", line):
            if i>0 and lines[i-1].strip() != "":
                bad(i, "missing blank line before heading")
            if i+1 < len(lines) and lines[i+1].strip() == "":
                pass
            else:
                bad(i, "missing blank line after heading")
        # code fence start
        if re.match(r"^```", line):
            if i>0 and lines[i-1].strip() != "":
                bad(i, "missing blank line before code block")
            # find end fence to check after
            for j in range(i+1, len(lines)):
                if re.match(r"^```", lines[j]):
                    if j+1 < len(lines) and lines[j+1].strip() != "":
                        bad(j, "missing blank line after code block")
                    break
        # table row (starts with | and has another |)
        if re.match(r"^\|.*\|$", line):
            # header sep row ignored (|---|)
            if i>0 and lines[i-1].strip() != "" and not re.match(r"^\|[-: ]+\|$", lines[i].strip()):
                bad(i, "missing blank line before table (header)")
            # after: checked when we hit a non-table line
            if i+1 < len(lines) and lines[i+1].strip() != "" and not lines[i+1].startswith("|"):
                bad(i, "missing blank line after table")
    return ok

def code_fences_labeled(md):
    ok = True
    for i, line in enumerate(md.splitlines()):
        if line.strip() == "```":
            print(f"  - code: line {i+1}: code fence missing language (```yaml, ```json, …)")
            ok = False
    return ok

def forbid_allcaps_ids(md):
    # Headings like "### EDGE" or table cells like "| EDGE |"
    bad = False
    for m in re.finditer(r"(^###\s+[A-Z0-9_]{3,}$)|(^\|\s*[A-Z0-9_]{3,}\s*\|)", md, flags=re.M):
        print(f"  - ids: ALLCAPS tool id found at char {m.start()}")
        bad = True
    return not bad

def require_namespaced_ids(md):
    # ensure at least one valid namespaced id appears if any tool ids appear
    # and flag raw foo.bar emissions that are not allowed
    ok = True
    # Allowed emissions:
    allowed_emissions = re.compile(r"\b(menu\.signal|tool\.call|tool\.result|beacon\.(check|optional)|error\.signal)\b")
    # Allowed namespaced ids:
    allowed_ids = re.compile(r"\b((lens|move|closure|beacon)\.[a-z0-9_]+|recap\.spec)\b")
    # Disallow stray foo.bar tokens that look like emissions but aren’t allowed:
    bad_emission = re.compile(r"\b([a-z]+)\.([a-z0-9_]+)\b")
    for m in bad_emission.finditer(md):
        token = m.group(0)
        if allowed_emissions.search(token) or allowed_ids.search(token):
            continue
        # likely prose "e.g." etc — skip if preceded by backtick? we’ll be conservative
        # If it’s inside backticks, still enforce—kernel inline code should be ids/emissions only.
        print(f"  - tokens: disallowed token `{token}` (use namespaced ids/emissions)")
        ok = False
    return ok

def check_table_headers(md, expect_headers):
    # expect_headers = {"file": ["id","purpose","trigger","output artifact"], ...}
    ok = True
    # find first table header line (starts with | and contains headers)
    for header in expect_headers:
        pattern = r"^\|\s*" + r"\s*\|\s*".join([re.escape(h) for h in header]) + r"\s*\|$"
        if re.search(pattern, md, flags=re.M):
            break
    else:
        print("  - table: required header row not found (check column names/order)")
        ok = False
    return ok

def check_output_word_limit(md, column_name, max_words=12):
    ok = True
    lines = md.splitlines()
    # find the header row
    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("|") and column_name in [c.strip().lower() for c in line.strip("|").split("|")]:
            header_idx = i
            headers = [c.strip().lower() for c in line.strip("|").split("|")]
            break
    if header_idx is None:
        return True
    col = headers.index(column_name)
    # iterate table body until a blank line
    for i in range(header_idx+2, len(lines)):
        row = lines[i]
        if not row.startswith("|"): break
        cells = [c.strip() for c in row.strip("|").split("|")]
        if col >= len(cells): continue
        words = re.findall(r"\b\w+\b", cells[col])
        if len(words) > max_words:
            print(f"  - output limit: line {i+1}: `{cells[col]}` has {len(words)} words (> {max_words})")
            ok = False
    return ok

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = load_config(args.config)
    root = os.getcwd()
    failures = 0

    # Gather files
    md_files = []
    for base, _, files in os.walk(os.path.join(root, "kernel")):
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(base, f))

    for path in sorted(md_files):
        md = read_file(path)
        rel = os.path.relpath(path, root)
        print(f"[lint] {rel}")

        ok = True
        # Front matter
        req_keys = ["id","title","display_title","type","lifecycle","version","status","stability","summary","author","license"]
        if not front_matter_ok(md, req_keys):
            print("  - front matter: missing or incomplete YAML header")
            ok = False

        if not has_blank_line_around_blocks(md): ok = False
        if not code_fences_labeled(md): ok = False
        if not forbid_allcaps_ids(md): ok = False
        if not require_namespaced_ids(md): ok = False

        # Per-file table schemas
        fname = os.path.basename(path)
        if fname == "30_lenses.md":
            if not check_table_headers(md, [["id","purpose","trigger","output artifact"]]): ok = False
            if not check_output_word_limit(md, "output artifact", 12): ok = False
        if fname == "35_micromoves.md":
            if not check_table_headers(md, [["id","purpose","trigger condition"]]): ok = False
        if fname == "20_beacons.md":
            if not check_table_headers(md, [["id","purpose","trigger","action"]]): ok = False

        if not ok:
            failures += 1

    if failures:
        print(f"\n[lint] FAIL: {failures} file(s) have issues.")
        sys.exit(1)
    print("\n[lint] PASS: all checks ok.")

if __name__ == "__main__":
    main()
