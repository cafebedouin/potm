#!/usr/bin/env bash
# pack_softkernel.sh (v1)
# Packs the PoTM soft-kernel into 10,000-byte (or less) parts.
# No "Recap:" validation. Uses your current microkernels/latest/ layout.

set -euo pipefail

# ---------- Config ----------
MAX_BYTES=${MAX_BYTES:-20800}                         # hard cap per part
OUT_PREFIX=${OUT_PREFIX:-"PoTM_BootPack_minikernel"}  # base filename for parts
TITLE=${TITLE:-"PoTM Boot Pack — Soft Kernel"}
VERSION=${VERSION:-"v1.0"}
DATE_STR=$(date +"%Y-%m-%d")
CACHE_DIR=".pack_cache"
HASHES_FILE="$CACHE_DIR/source_hashes.txt"
DIFF_LOG="diff.log"

# Modes:
#   --core         => kernel only (recommended default)
#   --with-mods    => kernel + key doctrines + protocols + msrl
#   --full         => everything listed below (heavier)
BUILD_MODE="core"

# ---------- File sets (aligned to your tree) ----------
CORE_FILES=(
  "../kernel/00_header.md"
  "../kernel/10_beacons.md"
  "../kernel/20_lenses_p1.md"
  "../kernel/30_quickstart.md"
)

WITH_MODS_FILES=(
  "${CORE_FILES[@]}"
  "doctrines/soft_kernel_doctrine.md"
  "doctrines/soft_kernel_doctrine_addendum_cmg.md"
  "protocols/engagement_flow.md"
  "protocols/cmg_runtime.md"
  "protocols/msrl_runtime.md"
  "modules/ledger/msrl.md"
)

FULL_FILES=(
  "${WITH_MODS_FILES[@]}"
  "annex_h/README.md"
  "annex_a/README.md"
  "protocols/templates/aar_c_worksheet.md"
  "protocols/templates/cmg_manifest.yaml"
  "templates/promotion_packet.md"
  "templates/annex_translation_plan.md"
  "templates/null_day_example.md"
  "templates/when_not_to_use.md"
)

usage() {
  cat <<EOF
Usage: $0 [--core | --with-mods | --full]
  --core       Build kernel-only pack (default).
  --with-mods  Kernel + CMG + engagement + MSRL (balanced).
  --full       Kernel + all listed modules/templates (big).
Environment:
  MAX_BYTES (default: 10000)
  OUT_PREFIX (default: PoTM_BootPack_minikernel)
  TITLE, VERSION
Outputs:
  ${OUT_PREFIX}_part_01.md, _part_02.md, ...
Also writes:
  diff.log (changed/added/removed since last pack)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --core) BUILD_MODE="core"; shift ;;
    --with-mods) BUILD_MODE="with"; shift ;;
    --full) BUILD_MODE="full"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

choose_files() {
  case "$BUILD_MODE" in
    core) printf "%s\n" "${CORE_FILES[@]}" ;;
    with) printf "%s\n" "${WITH_MODS_FILES[@]}" ;;
    full) printf "%s\n" "${FULL_FILES[@]}" ;;
  esac
}

# ---------- Helpers ----------
sha() { shasum -a 256 "$1" | awk '{print $1}'; }

part_header() {
  local part="$1" ; local total="$2"
  cat <<EOF
# ${TITLE} — Part $(printf "%02d" "$part") (of ${total})
Version: ${VERSION} | Generated: ${DATE_STR}

**Operator Contract**
- Don’t assume unstated context; ask if missing.
- Only use content in this part unless I provide another.
- Honor kernel beacons (dignity, no_deception, no_simulated_wisdom, clarity>fluency, practitioner_safety).

EOF
}

collect_and_hash() {
  local tmp
  tmp=$(mktemp)
  while read -r f; do
    if [[ -f "$f" ]]; then
      printf "%s %s\n" "$(sha "$f")" "$f" >> "$tmp"
    else
      printf "%s %s\n" "MISSING" "$f" >> "$tmp"
    fi
  done
  echo "$tmp"
}

log_diff() {
  local prevf="$1"; local curf="$2"
  mkdir -p "$CACHE_DIR"
  : > "$DIFF_LOG"
  echo "Diff since last pack (${DATE_STR}):" >> "$DIFF_LOG"
  awk '{print $2" "$1}' "$prevf" 2>/dev/null | sort > "$CACHE_DIR/_prev.map" || true
  awk '{print $2" "$1}' "$curf"  | sort > "$CACHE_DIR/_curr.map"
  join -a1 -a2 -e "NULL" -o 0,1.2,2.2 -j1 "$CACHE_DIR/_prev.map" "$CACHE_DIR/_curr.map" | while read -r path old new; do
    if [[ "$old" == "NULL" ]]; then
      echo "+ Added: $path" >> "$DIFF_LOG"
    elif [[ "$new" == "NULL" ]]; then
      echo "- Removed: $path" >> "$DIFF_LOG"
    elif [[ "$old" != "$new" ]]; then
      if [[ -f "$path" ]]; then
        sz=$(wc -c < "$path" | tr -d ' ')
        echo "* Updated: $path (now ${sz} bytes)" >> "$DIFF_LOG"
      else
        echo "* Updated: $path" >> "$DIFF_LOG"
      fi
    fi
  done
}

# ---------- Build ----------
FILES_LIST=$(choose_files)
# sanity check presence (warn, don’t fail)
while read -r f; do
  [[ -z "$f" ]] && continue
  if [[ ! -f "$f" ]]; then
    echo "WARN: missing $f (skipping)" >&2
  fi
done <<< "$FILES_LIST"

mkdir -p "$CACHE_DIR"
touch "$HASHES_FILE"
CURR=$(collect_and_hash <<< "$FILES_LIST")
log_diff "$HASHES_FILE" "$CURR"
cp "$CURR" "$HASHES_FILE"
echo "Wrote $DIFF_LOG"

# --- replace the chunk creation loop with this --- #

split_file_into_chunks() {
  local f="$1" ; local base="$(basename "$f")"
  local tmpdir="$2"
  local cap="${3:-$MAX_BYTES}"
  local prefix="$tmpdir/${base%.md}"

  # Make a working copy with trimmed trailing spaces
  local work; work=$(mktemp)
  sed -e 's/[ \t]*$//' "$f" > "$work"

  # If file already fits, emit one chunk and return
  local size; size=$(wc -c < "$work")
  if (( size + 80 <= cap )); then
    local out="${prefix}.chunk"
    {
      echo "---8<--- FILE: $f ---8<---"
      cat "$work"
      echo
      echo "---8<--- /END FILE: $f ---8<---"
      echo
    } > "$out"
    echo "$out"
    rm -f "$work"
    return
  fi

  # Otherwise split on '## ' headings; if none, split on '# '.
  # Keep headings with their sections.
  awk '
    BEGIN{section=0}
    /^## /{section++; fn=sprintf("sec_%03d.md", section); print $0 > fn; next}
    { if(section==0){section=1; fn=sprintf("sec_%03d.md", section)}; print $0 >> fn }
  ' "$work"

  # If we ended up with a single section (no ##), try splitting on top-level '# '
  if [[ $(ls sec_*.md 2>/dev/null | wc -l | tr -d " ") -eq 1 ]]; then
    rm -f sec_*.md
    awk '
      BEGIN{section=0}
      /^# /{section++; fn=sprintf("sec_%03d.md", section); print $0 > fn; next}
      { if(section==0){section=1; fn=sprintf("sec_%03d.md", section)}; print $0 >> fn }
    ' "$work"
  fi

  # If we STILL have one section, hard-split every ~8k to respect cap.
  if [[ $(ls sec_*.md 2>/dev/null | wc -l | tr -d " ") -eq 1 ]]; then
    # 8000 target to leave room for wrappers
    csplit -s -k "$work" 8000 "{*}"
    i=0
    for p in xx*; do
      i=$((i+1))
      mv "$p" "$(printf 'sec_%03d.md' "$i")"
    done
  fi

  # Wrap each section as its own chunk
  local outputs=()
  for s in $(ls sec_*.md | sort); do
    local out="${prefix}.${s%.md}.chunk"
    {
      echo "---8<--- FILE: $f (${s}) ---8<---"
      cat "$s"
      echo
      echo "---8<--- /END FILE: $f (${s}) ---8<---"
      echo
    } > "$out"
    outputs+=("$out")
  done
  rm -f sec_*.md "$work"
  printf "%s\n" "${outputs[@]}"
}

# Build chunks (file-boundary or section-boundary if needed)
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
chunks_dir="$TMPDIR/chunks"; mkdir -p "$chunks_dir"
chunk_list=()

while read -r f; do
  [[ -z "$f" || ! -f "$f" ]] && continue
  # split oversized files into section-chunks
  while IFS= read -r produced; do
    [[ -n "$produced" ]] && chunk_list+=("$produced")
  done < <(split_file_into_chunks "$f" "$chunks_dir" "$MAX_BYTES")
done <<< "$FILES_LIST"

# Assemble parts under MAX_BYTES
parts_dir="$TMPDIR/parts"; mkdir -p "$parts_dir"
current_part=1
current_file="$parts_dir/part_$(printf "%02d" "$current_part").md"
part_header "$current_part" "__TOTAL__" > "$current_file"

for chunk in "${chunk_list[@]}"; do
  pending_size=$(wc -c < "$current_file")
  chunk_size=$(wc -c < "$chunk")
  if (( pending_size + chunk_size > MAX_BYTES )); then
    current_part=$((current_part + 1))
    current_file="$parts_dir/part_$(printf "%02d" "$current_part").md"
    part_header "$current_part" "__TOTAL__" > "$current_file"
  fi
  cat "$chunk" >> "$current_file"
done

TOTAL_PARTS=$(ls "$parts_dir" | wc -l | tr -d ' ')
i=1
for p in $(ls "$parts_dir" | sort); do
  src="$parts_dir/$p"
  dest="${OUT_PREFIX}_part_$(printf "%02d" "$i").md"
  sed "s/(of __TOTAL__)/(of $TOTAL_PARTS)/g" "$src" > "$dest"
  size=$(wc -c < "$dest" | tr -d ' ')
  echo "Wrote $dest ($size bytes)"
  i=$((i + 1))
done

echo "Done."
