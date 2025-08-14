#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

ONBOARD_BUILD="$DIST_DIR/kernel_onboard.md"
SIZE_LIMIT=10240
LENSES_FILE="$ROOT_DIR/kernel/30_lenses.md"
LENSES_LITE="$ROOT_DIR/kernel/30_lenses_mini.md"
TRIM_LOG="$DIST_DIR/kernel_onboard_trim.log"
TRIM_DIR="$DIST_DIR/trimmed_content"

trim_stage=0

log() {
    echo "$@" | tee -a "$TRIM_LOG"
}

rebuild_onboard() {
    "$ROOT_DIR/scripts/pack_agent.sh" --profile onboard
}

measure_size() {
    wc -c < "$ONBOARD_BUILD"
}

capture_removed() {
    local before="$1"
    local after="$2"
    local stage="$3"
    local out_file="$TRIM_DIR/${stage}_$(basename "$before").diff"
    mkdir -p "$TRIM_DIR"
    diff -U0 "$before" "$after" | grep -E "^\-" > "$out_file" || true
    local removed_count
    removed_count=$(grep -E "^\-" "$out_file" | wc -l || true)
    log "   Captured $removed_count removed lines to $out_file"
}

echo "=== Onboard Trim Log: $(date) ===" > "$TRIM_LOG"

if [ -f "$ONBOARD_BUILD" ]; then
    FILE_SIZE=$(measure_size)
    log "Onboard build size: $FILE_SIZE chars (limit: $SIZE_LIMIT)"

    while [ "$FILE_SIZE" -gt "$SIZE_LIMIT" ] && [ $trim_stage -lt 3 ]; do
        trim_stage=$((trim_stage + 1))
        log "⚠ Stage $trim_stage trim — over by $((FILE_SIZE - SIZE_LIMIT)) chars."

        case $trim_stage in
            1)
                log "🔧 Stage 1: Removing ## Examples sections from lenses..."
                cp "$LENSES_FILE" "${LENSES_FILE}.bak"
                awk '
                  BEGIN {in_examples=0}
                  /^## Examples/ {in_examples=1; next}
                  /^## / && in_examples {in_examples=0}
                  !in_examples {print}
                ' "$LENSES_FILE" > "$LENSES_LITE"
                capture_removed "${LENSES_FILE}.bak" "$LENSES_LITE" "stage1"
                sed -i.bak "s|$LENSES_FILE|$LENSES_LITE|" "$ROOT_DIR/build_manifest.yaml"
                rm -f "${LENSES_FILE}.bak"
                ;;
            2)
                log "🔧 Stage 2: Removing long descriptions (keep heading + gist) from lenses..."
                cp "$LENSES_LITE" "${LENSES_LITE}.bak"
                awk '
                  /^## / {print; getline; if ($0 ~ /^gist:/) {print} next}
                  /^gist:/ {print}
                ' "$LENSES_LITE" > "${LENSES_LITE}.tmp" && mv "${LENSES_LITE}.tmp" "$LENSES_LITE"
                capture_removed "${LENSES_LITE}.bak" "$LENSES_LITE" "stage2"
                rm -f "${LENSES_LITE}.bak"
                ;;
            3)
                log "🔧 Stage 3: Stripping inline notes/comments from all onboard files..."
                yq -r '.profiles.onboard.include[]' "$ROOT_DIR/build_manifest.yaml" \
                  | while read -r f; do
                        FULL="$ROOT_DIR/$f"
                        if [[ -f "$FULL" ]]; then
                            cp "$FULL" "${FULL}.bak"
                            sed -i '/^\s*#/d;/^> /d' "$FULL"
                            capture_removed "${FULL}.bak" "$FULL" "stage3"
                            rm -f "${FULL}.bak"
                        fi
                    done
                ;;
        esac

        log "♻ Rebuilding onboard profile..."
        rebuild_onboard
        FILE_SIZE=$(measure_size)
        log "📏 New size after stage $trim_stage: $FILE_SIZE chars (limit: $SIZE_LIMIT)"
    done

    if [ "$FILE_SIZE" -le "$SIZE_LIMIT" ]; then
        log "✅ Onboard build is now under limit."
    else
        log "❌ Could not get under limit after 3 stages."
    fi

    [ -f "$ROOT_DIR/build_manifest.yaml.bak" ] && mv "$ROOT_DIR/build_manifest.yaml.bak" "$ROOT_DIR/build_manifest.yaml"
    rm -f "$LENSES_LITE"
else
    log "❌ Onboard build file not found: $ONBOARD_BUILD"
fi
