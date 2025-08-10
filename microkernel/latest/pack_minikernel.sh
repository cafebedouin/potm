#!/usr/bin/env bash
# pack_minikernel.sh (v2)
# Minimal microkernel packer with primer-as-default, recap validation, diff log, and optional particles.

### Build steps
# 1. Save the above files:
#
# kernel/00_contract.md
# kernel/10_kernel_map.md 
# kernel/20_manifest_summary.md
# ...
# kernel/80_mini_checklists.md
# extended/checklist_v0.2.md   # optional but recommended
#
# 2. Run:
# Primer-only (Tier‑0)
# ./pack_minikernel.sh
#
# Full multi-part pack (will include 20/70/80)
# ./pack_minikernel.sh --full

set -euo pipefail

# ---------- Config ----------
MAX_BYTES=${MAX_BYTES:-1000000}         # size cap for full-part outputs, default 9800
OUT_PREFIX=${OUT_PREFIX:-"PoTM_BootPack_kernel"}
TITLE=${TITLE:-"PoTM Boot Pack (Minimum Microkernel)"}
VERSION=${VERSION:-"v1.4"}
DATE_STR=$(date +"%Y-%m-%d")
CACHE_DIR=".pack_cache"
HASHES_FILE="$CACHE_DIR/source_hashes.txt"
DIFF_LOG="diff.log"
PRIMER_OUT="PoTM_Primer_Tier0.md"
PARTICLES_DIR="particles"

# Source files
PRIMER_FILES=(
  "kernel/00_contract.md"
  "kernel/10_kernel_map.md"
  "kernel/30_axioms_distilled.md"
  "kernel/40_apertures_min.md"
  "kernel/50_guardian_tripwires.md"
  "kernel/60_lifecycle_cadence.md"
  "kernel/90_how_to_use_me.md"
)

FULL_FILES=(
  "kernel/00_kernel_contract.md"
  "kernel/10_kernel_map.md"
  "kernel/20_mode_control.md"
  "kernel/30_axioms_distilled.md"
  "kernel/35_protocol_index.md"
  "kernel/40_surfacing_modes.md"
  "kernel/50_guardian_playbook.md"
  "kernel/55_mirror_protocol.md"
  "kernel/60_latency_principle.md"
  "kernel/65_initiation_logic.md"
  "kernel/70_persona_index.md"
  "kernel/75_practice_menu.md"
  "kernel/80_test_vectors.md"
  "kernel/tags.md"
  "modules/dignity/conversational_boundary_rules.md"
  "modules/dignity/dignified_use_principles.md"
  "modules/dignity/relational_dignity_filter.md"
  "modules/response_policy/r00_precedence.md"
  "modules/response_policy/r01_shape.md"
  "modules/response_policy/r02_refusal.md"
  "modules/response_policy/r03_tags.md"
  "modules/response_policy/r04_depth.md"
  "modules/response_policy/r05_challenge.md"
  "modules/response_policy/r06_latency.md"
  "modules/response_policy/r07_persona.md"
  "modules/response_policy/r08_self_audit.md"
  "modules/response_policy/r09_logging.md"
  "modules/response_policy/r10_failure.md"
  "modules/response_policy/r11_context.md"
  "modules/response_policy/r12_user_signals.md"
  "modules/response_policy/r13_user_challenge.md"
  "modules/response_policy/glossary.md"
  "modules/response_policy/examples.md"
  "modules/tuning/directives.md"
  "modules/user_model/10_profile_types.md"
  "modules/user_model/20_profile_detection_logic.md"
  "modules/user_model/30_adaptive_response_matrix.md"
  "modules/user_model/40_profile_shift_conditions.md"
  "modules/user_model/50_manual_profile_controls.md"
  "modules/meta/PoTM_framework.md"
  "modules/meta/ledger.md"
  "modules/meta/multi_system_relational_ledger.md"
  "modules/practices/baseline_practices.md"
  "modules/practices/deck/pack_index.md"
  "modules/practices/deck/pack.md"
  "modules/practices/deck/pack_bank.md"
  "modules/practices/deck/practice_card_template.md"
  "modules/practices/maxims/maxims.md"
  "modules/rituals/pal_response_ritual.md"
  "modules/rituals/response_rituals_by_lineage.md"
  "modules/rituals/dissolution_vow.md"
  "modules/glyphs/glyph_protocol.md"
  "modules/glyphs/glyph_index.md"
  "modules/glyphs/glyph_resonance_map.md"
  "modules/depth_inquiry.md"
)

usage() {
  cat <<EOF
Usage: $0 [--full] [--particles] [--no-validate]
  --full         Build the full multi-part pack (chunked under ${MAX_BYTES} bytes each).
  --particles    Emit prompt particles (<1k each) from axioms/apertures/guardian into ./particles/.
  --no-validate  Skip recap-first-line validation.
Default behavior (no flags): build Tier-0 Primer (${PRIMER_OUT}).
EOF
}

BUILD_MODE="primer"
DO_PARTICLES="no"
DO_VALIDATE="yes"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --full) BUILD_MODE="full"; shift ;;
    --particles) DO_PARTICLES="yes"; shift ;;
    --no-validate) DO_VALIDATE="no"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

# ---------- Helpers ----------
sha() { shasum -a 256 "$1" | awk '{print $1}'; }

ensure_recaps() {
  local files=("$@")
  local bad=0
  for f in "${files[@]}"; do
    if [[ ! -f "$f" ]]; then
      echo "Missing file for validation: $f" >&2; bad=1; continue
    fi
    # First non-empty line
    local first
    first=$(awk 'NF{print; exit}' "$f")
    if [[ "$first" != Recap:* ]]; then
      echo "Recap validation failed: $f (first non-empty line must start with 'Recap:')" >&2
      bad=1
    fi
  done
  if [[ $bad -eq 1 ]]; then
    echo "Recap validation failed. Fix the above files or use --no-validate to bypass." >&2
    exit 1
  fi
}

header() {
  local part="$1" ; local total="$2"
  cat <<EOF
# ${TITLE} — Part $(printf "%02d" "$part") (of ${total})
Version: ${VERSION} | Generated: ${DATE_STR}

**Operator Contract**
- Do not assume unstated context; ask if missing.
- Use only content in this part unless I provide another.

EOF
}

primer_header() {
  cat <<EOF
# PoTM Tier‑0 Primer (Minimum Microkernel)
Version: ${VERSION} | Generated: ${DATE_STR}

**Operator Contract**
- Do not assume unstated context; ask before inferring.
- Use only this primer unless I provide “Part 01+”.

> ⚠️ You are now running Tier‑0. For sandbox access or kernel navigation, request “Part 01”.

EOF
}

# ---------- Diff log ----------
mkdir -p "$CACHE_DIR"
touch "$HASHES_FILE"
: > "$DIFF_LOG"
echo "Diff since last pack (${DATE_STR}):" >> "$DIFF_LOG"

collect_and_hash() {
  local files=("$@")
  local tmp
  tmp=$(mktemp)
  for f in "${files[@]}"; do
    if [[ -f "$f" ]]; then
      printf "%s %s\n" "$(sha "$f")" "$f" >> "$tmp"
    else
      printf "%s %s\n" "MISSING" "$f" >> "$tmp"
    fi
  done
  echo "$tmp"
}

prev="$HASHES_FILE"
curr=$(mktemp)
# will fill after we know which set we packed

log_diff() {
  local prevf="$1"; local curf="$2"
  # Map by filename
  awk '{print $2" "$1}' "$prevf" | sort > "$CACHE_DIR/_prev.map" || true
  awk '{print $2" "$1}' "$curf" | sort > "$CACHE_DIR/_curr.map"
  join -a1 -a2 -e "NULL" -o 0,1.2,2.2 -j1 "$CACHE_DIR/_prev.map" "$CACHE_DIR/_curr.map" | while read -r path old new; do
    if [[ "$old" == "NULL" ]]; then
      echo "+ Added: $path" >> "$DIFF_LOG"
    elif [[ "$new" == "NULL" ]]; then
      echo "- Removed: $path" >> "$DIFF_LOG"
    elif [[ "$old" != "$new" ]]; then
      # size delta
      if [[ -f "$path" ]]; then
        sz=$(wc -c < "$path" | tr -d ' ')
        echo "* Updated: $path (now ${sz} bytes)" >> "$DIFF_LOG"
      else
        echo "* Updated: $path" >> "$DIFF_LOG"
      fi
    fi
  done
}

# ---------- Optional particles ----------
emit_particles() {
  mkdir -p "$PARTICLES_DIR"
  : > "$PARTICLES_DIR/README.md"
  echo "# PoTM Prompt Particles (Tier‑0 atoms)" >> "$PARTICLES_DIR/README.md"
  echo "Generated: ${DATE_STR}" >> "$PARTICLES_DIR/README.md"
  # Axioms: each bullet line becomes a particle
  if [[ -f "kernel/30_axioms_distilled.md" ]]; then
    awk '/^[-*] /{print}' kernel/30_axioms_distilled.md | nl -w2 -s'. ' | while read -r n line; do
      f="$PARTICLES_DIR/axiom_$(printf "%02d" "$n").md"
      printf "%s\n" "$line" > "$f"
      echo "Wrote $f"
    done
  fi
  # Apertures: simple extracts
  if [[ -f "kernel/40_apertures_min.md" ]]; then
    awk '/^[-*] CC:/{print}' kernel/40_apertures_min.md | nl -w2 -s'. ' | while read -r n line; do
      f="$PARTICLES_DIR/contrary_corner_$(printf "%02d" "$n").md"
      printf "%s\n" "$line" > "$f"
      echo "Wrote $f"
    done
    awk '/^[-*] OQ:/{print}' kernel/40_apertures_min.md | nl -w2 -s'. ' | while read -r n line; do
      f="$PARTICLES_DIR/open_questions_$(printf "%02d" "$n").md"
      printf "%s\n" "$line" > "$f"
      echo "Wrote $f"
    done
  fi
  # Guardian: triggers
  if [[ -f "kernel/50_guardian_tripwires.md" ]]; then
    awk '/^[-*] TW:/{print}' kernel/50_guardian_tripwires.md | nl -w2 -s'. ' | while read -r n line; do
      f="$PARTICLES_DIR/guardian_tripwire_$(printf "%02d" "$n").md"
      printf "%s\n" "$line" > "$f"
      echo "Wrote $f"
    done
  fi
}

# ---------- Build ----------
if [[ "$BUILD_MODE" == "primer" ]]; then
  files=("${PRIMER_FILES[@]}")
else
  files=("${FULL_FILES[@]}")
fi

# Validation
if [[ "$DO_VALIDATE" == "yes" ]]; then
  ensure_recaps "${files[@]}"
fi

# Collect hashes for diff
curr=$(collect_and_hash "${files[@]}")
log_diff "$prev" "$curr"
cp "$curr" "$HASHES_FILE"
echo "Wrote $DIFF_LOG"

# Build Primer or Full
if [[ "$BUILD_MODE" == "primer" ]]; then
  # Primer body
  tmp=$(mktemp)
  primer_header > "$tmp"

  # add virtual .copilotignore block
  cat <<'EOF' >> "$tmp"
## Virtual .copilotignore (Cognitive)
Ignore:
- Experimental protocols not listed in manifest
- Ledger entries outside declared schema
- Sandbox branches not promoted
EOF
  echo >> "$tmp"

  for f in "${files[@]}"; do
    echo "---8<--- FILE: $f ---8<---" >> "$tmp"
    sed -e 's/[ \t]*$//' "$f" >> "$tmp"
    echo -e "\n---8<--- /END FILE: $f ---8<---\n" >> "$tmp"
  done
  mv "$tmp" "$PRIMER_OUT"
  size=$(wc -c < "$PRIMER_OUT" | tr -d ' ')
  echo "Wrote $PRIMER_OUT (${size} bytes)"

else
  # Full multi-part (chunk by file boundaries)
  TMPDIR=$(mktemp -d)
  trap 'rm -rf "$TMPDIR"' EXIT
  chunks_dir="$TMPDIR/chunks"; mkdir -p "$chunks_dir"
  chunk_list=()
  for f in "${files[@]}"; do
    base=$(basename "$f")
    out="$chunks_dir/$base.chunk"
    {
      echo "---8<--- FILE: $f ---8<---"
      sed -e 's/[ \t]*$//' "$f"
      echo
      echo "---8<--- /END FILE: $f ---8<---"
      echo
    } > "$out"
    chunk_list+=("$out")
  done
  parts_dir="$TMPDIR/parts"; mkdir -p "$parts_dir"
  current_part=1
  current_file="$parts_dir/part_$(printf "%02d" "$current_part").md"
  header "$current_part" "__TOTAL__" > "$current_file"

  for chunk in "${chunk_list[@]}"; do
    pending_size=$(wc -c < "$current_file")
    chunk_size=$(wc -c < "$chunk")
    if (( pending_size + chunk_size > MAX_BYTES )); then
      current_part=$((current_part + 1))
      current_file="$parts_dir/part_$(printf "%02d" "$current_part").md"
      header "$current_part" "__TOTAL__" > "$current_file"
    fi
    cat "$chunk" >> "$current_file"
  done

  TOTAL_PARTS=$(ls "$parts_dir" | wc -l | tr -d ' ')
  i=1
  for p in $(ls "$parts_dir" | sort); do
    src="$parts_dir/$p"
    dest="${OUT_PREFIX}$(printf "%02d" "$i").md"
    sed "s/(of __TOTAL__)/(of $TOTAL_PARTS)/g" "$src" > "$dest"
    size=$(wc -c < "$dest" | tr -d ' ')
    echo "Wrote $dest ($size bytes)"
    i=$((i + 1))
  done
fi

# Particles (optional)
if [[ "$DO_PARTICLES" == "yes" ]]; then
  emit_particles
fi
