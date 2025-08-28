#!/usr/bin/env bash
set -euo pipefail

MANIFEST="${1:-packaging/manifests/kernel_bundle_p1.yaml}"
OUT="${2:-dist/potm_kernel_p1_all.md}"

mkdir -p "$(dirname "$OUT")"

# Pull a YAML list by top-level key (e.g., CORE, INTERFACES).
# - Ignores comments/blank lines
# - Stops at the next top-level key "<Word>:" (no leading spaces)
# - Accepts indented "- item" list lines
pull_list () {
  local key="$1"
  awk -v k="$key" '
    # start section when we see "<key>:" (optionally indented)
    $0 ~ ("^[[:space:]]*" k ":[[:space:]]*$") { in=1; next }

    # if we hit another top-level key (non-indented "Word:"), stop section
    in && /^[A-Za-z0-9_]+:[[:space:]]*$/ { in=0 }

    # within section, collect YAML list items "- path"
    in && /^[[:space:]]*-[[:space:]]*/ {
      s=$0
      sub(/^[[:space:]]*-[[:space:]]*/, "", s)     # strip "- "
      # skip if the item itself is commented
      if (s ~ /^[[:space:]]*#/) next
      # trim surrounding spaces
      sub(/^[[:space:]]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      if (length(s) > 0) print s
    }
  ' "$MANIFEST"
}

SECTIONS=(
  CORE
  INTERFACES
  DIAGNOSTICS
  PLAYBOOKS
  DATA
  SCHEMAS
  TESTS
  MISC
)

: > "$OUT"
for sec in "${SECTIONS[@]}"; do
  files="$(pull_list "$sec" || true)"
  [ -z "${files:-}" ] && continue

  {
    echo
    echo "# ===== Section: $sec ====="
    echo
  } >> "$OUT"

  # shellcheck disable=SC2086
  while IFS= read -r f; do
    # skip comments or empties defensively
    [ -z "$f" ] && continue
    case "$f" in \#*) continue ;; esac

    if [ -f "$f" ]; then
      printf '\n---8<--- FILE: %s ---8<---\n' "$f" >> "$OUT"
      cat "$f" >> "$OUT"
      printf '\n---8<--- /END FILE: %s ---8<---\n' "$f" >> "$OUT"
    else
      >&2 echo "[warn] missing file (skipped): $f"
    fi
  done <<< "$files"
done

echo "Built $OUT from $MANIFEST"
